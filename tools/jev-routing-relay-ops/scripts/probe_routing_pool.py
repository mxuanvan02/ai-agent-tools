#!/usr/bin/env python3
"""Probe a Jev routing pool that sits behind a local relay.

Two modes:

  --self-check   offline, no network, no key. Verifies the parts that depend only on
                 routing internals: catalog presence of the pool refs, `_pick` behaviour
                 (including the vision pool going inert for catalog-unknown refs), the
                 large-context guard, and the decision-cache boundary. This is the mode
                 to run first, and the mode CI can run.

  live probe     requires --base-url and --models. Proves the wire: does the relay
                 forward `reasoning_effort`, can each model call a tool, does it accept
                 each effort level, can it read a drawn digit back.

Credentials are read at runtime (never printed, never stored in this file):
`--auth-from-env NAME` or `--auth-file PATH` holding the raw header value.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

DEFAULT_PLUGIN = Path.home() / ".hermes/plugins/hermes-jev"


# ── offline: routing internals ────────────────────────────────────────────────

def load_routing(plugin_dir: Path) -> Any:
    if str(plugin_dir) not in sys.path:
        sys.path.insert(0, str(plugin_dir))
    from jevkit import route  # noqa: E402  (import after sys.path edit)
    return route


def collect_pool_refs(config: Dict[str, Any], prefix: str) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for tier, pools in (config.get("tiers") or {}).items():
        for spec, refs in (pools or {}).items():
            matched = [r for r in (refs or []) if str(r).startswith(f"{prefix}:")]
            if matched:
                out.setdefault(tier, []).extend(matched)
    return {k: sorted(set(v)) for k, v in out.items()}


def self_check(plugin_dir: Path, prefix: str, exempt_caps: Sequence[str] = ()) -> int:
    route = load_routing(plugin_dir)
    config = route.load_config()
    failures: List[str] = []
    warnings: List[str] = []
    checks = 0

    print(f"=== self-check (offline) plugin={plugin_dir} prefix={prefix!r} ===")

    rows = route._by_ref(None) or {}
    print(f"catalog rows: {len(rows)}")
    known_prefixes = sorted({k.split(":", 1)[0] for k in rows})
    print(f"catalog providers: {known_prefixes[:12]}")
    prefix_known = prefix in known_prefixes
    print(f"pool prefix in catalog: {prefix_known}")
    if prefix_known:
        print("  note: catalog knows this prefix; the inert-pool findings below may not apply")

    refs = collect_pool_refs(config, prefix)
    if not refs:
        print(f"no {prefix}:* refs in any pool — nothing to check")
        return 0
    print("pool refs per tier:", json.dumps(refs, ensure_ascii=False))

    # 1. _pick resolves a non-vision turn
    checks += 1
    first_tier = next(iter(("simple", "medium", "hard")))
    got = route._pick(config, rows, first_tier, "general", False, 500, prefix)
    ok = bool(got) and str(got).startswith(f"{prefix}:")
    print(f"[{'PASS' if ok else 'FAIL'}] _pick({first_tier}/general, ctx=500) -> {got}")
    if not ok:
        failures.append("_pick returned no relay ref for a small non-vision turn")

    # 2. vision pool is inert for catalog-unknown refs
    checks += 1
    vision = route._pick(config, rows, first_tier, "general", True, 500, prefix)
    if prefix_known:
        print(f"[INFO] vision pick with a catalog-known prefix: {vision}")
    elif vision is None:
        # Safe (the turn keeps the current model) but the pool does nothing, so an
        # operator who edited it would see no effect. That is a warning, not a pass.
        warnings.append("vision pool is inert for this prefix: image turns keep the current model")
        print("[WARN] vision pool resolves to None (inert; image turns keep the current model)")
    else:
        failures.append(f"vision pool resolved to {vision!r} although the prefix is "
                        "catalog-unknown; re-verify capability probing before trusting it")
        print(f"[FAIL] vision pool resolved unexpectedly -> {vision}")

    # 3. context guard: no switch above the threshold when prices are unknown
    checks += 1
    threshold = config.get("sticky_context_tokens")
    print(f"sticky_context_tokens: {threshold}")
    if isinstance(threshold, int) and threshold > 0:
        small = route.decide("hello there", current=f"{prefix}:current-model",
                             only_provider=prefix, context_tokens=500, config=config)
        large = route.decide("hello there", current=f"{prefix}:current-model",
                             only_provider=prefix, context_tokens=threshold * 4, config=config)
        ok = bool(large.get("routed")) is False or large.get("model") == f"{prefix}:current-model"
        print(f"[{'PASS' if ok else 'FAIL'}] large context keeps the model "
              f"(reason={large.get('reason')!r})")
        if not ok:
            failures.append("large-context turn still switches models (guard inert for this prefix)")
        print(f"        small context -> routed={small.get('routed')} model={small.get('model')}")
    else:
        print("[SKIP] sticky_context_tokens not a positive int")

    # 4. cache-key boundary matches the guard's strict comparison
    checks += 1
    if hasattr(route, "_sticky_side") and isinstance(threshold, int):
        below = route._sticky_side(threshold - 1, config)
        at = route._sticky_side(threshold, config)
        above = route._sticky_side(threshold + 1, config)
        ok = (below, at, above) == (False, False, True)
        print(f"[{'PASS' if ok else 'FAIL'}] _sticky_side boundary "
              f"(t-1={below} t={at} t+1={above}) matches strict `>`")
        if not ok:
            failures.append("_sticky_side disagrees with decide()'s strict comparison")
        key_below = route._cache_key("hi", "p", prefix, False, False, threshold - 1, config)
        key_above = route._cache_key("hi", "p", prefix, False, False, threshold + 1, config)
        same_bucket = route._context_bucket(threshold - 1) == route._context_bucket(threshold + 1)
        ok2 = key_below != key_above
        print(f"[{'PASS' if ok2 else 'FAIL'}] cache key separates the two sides "
              f"(same context bucket={same_bucket})")
        if not ok2:
            failures.append("cache key does not separate the guard boundary")
    else:
        print("[SKIP] route._sticky_side not present (patch not applied)")

    # 5. effort caps cover every pool model, and no rejected level is declared
    checks += 1
    caps = ((config.get("effort") or {}).get("models")) or {}
    models = sorted({r.split(":", 1)[1] for group in refs.values() for r in group})
    declared = []
    undeclared = []
    for m in models:
        if caps.get(f"{prefix}:{m}") or caps.get(f"custom:{m}"):
            declared.append(m)
        else:
            undeclared.append(m)
    print(f"effort caps declared for: {declared}")
    print(f"effort caps absent for:   {undeclared} (field is never sent for these)")
    from jevkit import effort  # noqa: E402
    levels = effort.levels_from_config(config)
    effort_cfg = config.get("effort") or {}
    print(f"effort.levels: {levels}")

    # An enabled table that does not parse resolves to None, and every effort branch below
    # is then skipped — a green report while effort routing is entirely dead. That is the
    # "0 findings is not evidence the check ran" trap, so it gets its own area.
    checks += 1
    if levels is None:
        if effort_cfg.get("enabled"):
            failures.append(
                "effort.enabled is true but effort.levels did not parse (None), so effort "
                "routing is silently dead: levels_from_config wants either a 4-entry list "
                "(one level per difficulty bucket) or a dict keyed by bucket name")
            print("[FAIL] effort enabled but the level table is invalid")
        else:
            print("[SKIP] effort routing not enabled; the caps areas do not apply")
    else:
        print("[PASS] effort.levels parsed")

    # A pool model with NO caps entry is not "effort off": the middleware leaves the
    # request alone, so it keeps whatever effort the host already resolved (often the
    # maximum). The turn is then billed and paced as if effort routing did not exist.
    # That is a real defect unless the operator says the model rejects every level.
    checks += 1
    if levels:
        exempt = set(exempt_caps)
        silent = sorted(m for m in undeclared if m not in exempt)
        if silent:
            failures.append(
                f"pool models with no effort caps keep the host default effort "
                f"(routing silently inert): {silent}; declare measured levels, or pass "
                f"--exempt-caps for models that reject every level")
        print(f"[{'FAIL' if silent else 'PASS'}] every pool model has caps or an explicit exemption")
        if sorted(exempt & set(declared)):
            warnings.append(f"exempted but caps declared anyway: {sorted(exempt & set(declared))}")

        # A declared level that is not in the global table can never be applied: the
        # middleware requires `candidate in supported` AND `candidate in KNOWN_LEVELS`,
        # and the pick only ever returns table entries — so the extra level is dead weight
        # that hides a typo.
        dead = {m: sorted(set(caps.get(f"{prefix}:{m}") or caps.get(f"custom:{m}") or []) - set(levels))
                for m in declared}
        dead = {m: v for m, v in dead.items() if v}
        if dead:
            warnings.append(f"caps declare levels outside effort.levels (never applied): {dead}")
        print(f"[{'WARN' if dead else 'PASS'}] declared levels all appear in effort.levels")

        # The cheap tier must not declare only expensive levels, or the pool's whole
        # purpose (latency/cost on trivial turns) is defeated.
        cheap = sorted({r.split(":", 1)[1] for r in refs.get("simple", [])})
        if cheap:
            weakest = levels[0]
            missing_low = [m for m in cheap
                           if (caps.get(f"{prefix}:{m}") or caps.get(f"custom:{m}"))
                           and weakest not in (caps.get(f"{prefix}:{m}") or caps.get(f"custom:{m}"))]
            if missing_low:
                warnings.append(f"simple-tier models cannot use the cheapest level {weakest!r}: {missing_low}")
            print(f"[{'WARN' if missing_low else 'PASS'}] simple tier can reach level {weakest!r}")

    print(f"\n=== self-check: {checks} areas, {len(failures)} failure(s), {len(warnings)} warning(s) ===")
    for f in failures:
        print("  FAIL:", f)
    for w in warnings:
        print("  WARN:", w)
    return 1 if failures else 0


# ── live: prove the wire ──────────────────────────────────────────────────────

def auth_header(args: argparse.Namespace) -> Optional[str]:
    if args.auth_from_env:
        value = os.environ.get(args.auth_from_env, "")
        if value:
            return value if value.lower().startswith("bearer ") else "Bearer " + value
    if args.auth_file:
        value = Path(args.auth_file).read_text(encoding="utf-8").strip()
        if value:
            return value if value.lower().startswith("bearer ") else "Bearer " + value
    return None


def post_json(url: str, body: Dict[str, Any], auth: str, timeout: int = 120) -> Dict[str, Any]:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": auth})
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read(8_000_000))
        return {"ok": True, "secs": round(time.time() - started, 1), "payload": payload}
    except urllib.error.HTTPError as exc:
        raw = exc.read(400).decode("utf-8", "replace")
        kind = ("quota" if any(t in raw for t in ("insufficient", "402", "429"))
                else ("no-accounts" if "No available accounts" in raw else f"http{exc.code}"))
        return {"ok": False, "kind": kind, "secs": round(time.time() - started, 1), "body": raw[:180]}
    except Exception as exc:  # noqa: BLE001 — probe must report, not raise
        return {"ok": False, "kind": type(exc).__name__, "secs": round(time.time() - started, 1)}


def probe_tool_call(base_url: str, model: str, auth: str) -> Dict[str, Any]:
    tool = {"type": "function", "function": {
        "name": "get_current_time",
        "description": "Get the current time in a timezone",
        "parameters": {"type": "object",
                       "properties": {"timezone": {"type": "string"}},
                       "required": ["timezone"]}}}
    res = post_json(base_url.rstrip("/") + "/chat/completions", {
        "model": model, "max_tokens": 512, "tools": [tool], "tool_choice": "auto",
        "messages": [{"role": "user", "content": "What time is it? Use the tool."}],
    }, auth)
    if not res["ok"]:
        return {"tool_ok": False, "err": res.get("kind") or res.get("body")}
    msg = (res["payload"].get("choices") or [{}])[0].get("message") or {}
    calls = msg.get("tool_calls") or []
    finish = (res["payload"].get("choices") or [{}])[0].get("finish_reason")
    return {"tool_ok": bool(calls), "finish": finish, "names": [c["function"]["name"] for c in calls],
            "secs": res["secs"]}


def probe_effort(base_url: str, model: str, auth: str, levels: Sequence[str],
                 prompt: str) -> Dict[str, Any]:
    """Per-level acceptance. Equal completion counts across levels means the relay
    dropped the field — that is a finding, not a pass."""
    out: Dict[str, Any] = {"accepted": [], "rejected": {}, "ctok": {}}
    for level in levels:
        res = post_json(base_url.rstrip("/") + "/chat/completions", {
            "model": model, "max_tokens": 4000, "temperature": 0.2,
            "reasoning_effort": level,
            "messages": [{"role": "user", "content": prompt}],
        }, auth)
        if res["ok"]:
            usage = res["payload"].get("usage") or {}
            out["accepted"].append(level)
            out["ctok"][level] = usage.get("completion_tokens")
        else:
            out["rejected"][level] = res.get("kind") or "error"
    counts = [v for v in out["ctok"].values() if isinstance(v, int)]
    out["forwarding_evidence"] = (len(set(counts)) > 1) if len(counts) >= 2 else None
    return out


def _digit_png(digit: str) -> Optional[bytes]:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None
    img = Image.new("RGB", (140, 140), "white")
    ImageDraw.Draw(img).text((52, 48), digit, fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def probe_vision(base_url: str, model: str, auth: str, digit: str = "7") -> Dict[str, Any]:
    png = _digit_png(digit)
    if png is None:
        return {"vision_ok": None, "note": "Pillow missing; install it to probe vision"}
    data_url = "data:image/png;base64," + base64.b64encode(png).decode()
    res = post_json(base_url.rstrip("/") + "/chat/completions", {
        "model": model, "max_tokens": 40,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": "The image contains one digit. Reply with only that digit."},
            {"type": "image_url", "image_url": {"url": data_url}}]}],
    }, auth)
    if not res["ok"]:
        return {"vision_ok": False, "err": res.get("kind") or res.get("body")}
    msg = (res["payload"].get("choices") or [{}])[0].get("message") or {}
    text = msg.get("content") or ""
    return {"vision_ok": digit in text, "text": text[:30], "secs": res["secs"]}


def live_probe(args: argparse.Namespace) -> int:
    auth = auth_header(args)
    if not auth:
        print("live probe needs --auth-from-env NAME or --auth-file PATH", file=sys.stderr)
        return 2
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    levels = [x.strip() for x in args.efforts.split(",") if x.strip()]
    report: Dict[str, Any] = {}
    for model in models:
        entry: Dict[str, Any] = {}
        entry["tool"] = probe_tool_call(args.base_url, model, auth)
        entry["effort"] = probe_effort(args.base_url, model, auth, levels, args.prompt)
        if args.vision:
            entry["vision"] = probe_vision(args.base_url, model, auth)
        report[model] = entry
        print(f"\n--- {model} ---")
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        time.sleep(args.pause)

    print("\n=== summary ===")
    for model, entry in report.items():
        acc = entry["effort"]["accepted"]
        rej = entry["effort"]["rejected"]
        print(f"{model:26s} tool={entry['tool'].get('tool_ok')} "
              f"effort_accepted={acc} rejected={list(rej)} "
              f"forwarding={entry['effort']['forwarding_evidence']} "
              f"vision={entry.get('vision', {}).get('vision_ok')}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"\nwrote {args.json_out}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--plugin-dir", type=Path, default=DEFAULT_PLUGIN,
                   help="hermes-jev plugin directory (default: %(default)s)")
    p.add_argument("--prefix", default="omniproxy",
                   help="pool ref prefix the relay uses (default: %(default)s)")
    p.add_argument("--self-check", action="store_true",
                   help="offline checks only: no network, no key")
    p.add_argument("--exempt-caps", default="",
                   help="comma-separated pool models that reject every reasoning-effort "
                        "level, so having no caps entry is deliberate rather than a defect")
    p.add_argument("--base-url", help="relay base URL, e.g. http://localhost:20131/v1")
    p.add_argument("--models", default="", help="comma-separated model ids to probe")
    p.add_argument("--efforts", default="low,medium,high,max",
                   help="reasoning-effort levels to test (default: %(default)s)")
    p.add_argument("--vision", action="store_true", help="also probe image reading")
    p.add_argument("--prompt", default="Count the primes below 100. Reply with only the number.",
                   help="probe prompt; must need some thinking so levels can differ")
    p.add_argument("--pause", type=float, default=2.0, help="seconds between models")
    p.add_argument("--auth-from-env", help="env var holding the Authorization value")
    p.add_argument("--auth-file", help="file holding the Authorization value (mode 600)")
    p.add_argument("--json-out", help="write the raw probe report here")
    args = p.parse_args()

    if args.self_check or not (args.base_url and args.models):
        return self_check(args.plugin_dir, args.prefix,
                          exempt_caps=tuple(x.strip() for x in args.exempt_caps.split(",") if x.strip()))
    return live_probe(args)


if __name__ == "__main__":
    sys.exit(main())
