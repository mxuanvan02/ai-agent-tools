#!/usr/bin/env python3
"""Print or re-probe the source registry in assets/verified_terms.json.

WHY THIS EXISTS

Several domains that reference lists in this field habitually cite are unreachable,
and several catalogues that matter most block plain HTTP clients. The two look
identical from a failed `curl`, but they have opposite consequences: a bot-walled
catalogue is still a source, a DNS-dead domain must not appear in a deliverable.
Guessing which is which costs hours. Measuring takes thirty seconds.

DEFAULT IS OFFLINE. It prints the registry as recorded, so the skill is usable
with no network. Add --live to re-measure with curl + getent.

USAGE

  python3 scripts/probe_sources.py                  # print registry, grouped by layer
  python3 scripts/probe_sources.py --layer 1        # only layer 1 (primary/manuscript)
  python3 scripts/probe_sources.py --reach curl-ok   # only scriptable sources
  python3 scripts/probe_sources.py --live            # re-measure everything
  python3 scripts/probe_sources.py --live --json out.json
  python3 scripts/probe_sources.py --check-dead      # exit 1 if any recorded URL now resolves

Exit code: 0 normal, 1 with --check-dead when a dns-dead URL now resolves or a
recorded live URL is now dead (registry is stale), 2 on I/O error.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1]
ASSETS = TOOL / "assets" / "verified_terms.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

LAYER_TITLE = {
    1: "Layer 1 — Primary / manuscript",
    2: "Layer 2 — Peer-reviewed scholarship",
    3: "Layer 3 — Reference works",
    4: "Layer 4 — Open corpora (verify spelling, do not cite as scholarship)",
}
REACH_LABEL = {
    "curl-ok":      "curl-ok",
    "browser-only": "browser-only",
    "dns-dead":     "DNS-DEAD",
}


def host_of(url: str) -> str:
    u = url.split("://", 1)[-1]
    return u.split("/", 1)[0]


def dns_ok(host: str) -> bool:
    return subprocess.run(["getent", "hosts", host],
                          capture_output=True).returncode == 0


def http_code(url: str, timeout: int) -> str:
    """curl HTTP status, or '000' when curl could not complete the request."""
    r = subprocess.run([
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "--max-time", str(timeout), "--connect-timeout", str(max(5, timeout // 2)),
        "-A", UA, "-L", url], capture_output=True, text=True)
    return (r.stdout or "000").strip() or "000"


def classify(url: str, timeout: int) -> tuple[str, bool, str]:
    """Return (reach_class, dns_ok, http_code).

    The classification rule matters more than the numbers: a host that RESOLVES
    but refuses non-browser clients is bot-walled, not dead. Only a DNS failure
    means the domain cannot be cited at all.
    """
    ok = dns_ok(host_of(url))
    if not ok:
        return "dns-dead", False, "000"
    code = http_code(url, timeout)
    if code == "000":
        return "browser-only", True, code
    try:
        n = int(code)
    except ValueError:
        return "browser-only", True, code
    if n in (403, 401, 451):
        return "browser-only", True, code
    if 200 <= n < 400:
        return "curl-ok", True, code
    if n == 404:
        # Host is alive but this exact path is gone. Not dead, not fetchable.
        return "browser-only", True, code
    return "browser-only", True, code


def main() -> int:
    ap = argparse.ArgumentParser(description="Print or re-probe the verified source registry.")
    ap.add_argument("--layer", type=int, choices=[1, 2, 3, 4], help="filter by layer")
    ap.add_argument("--reach", help="filter by reachability class")
    ap.add_argument("--live", action="store_true",
                    help="re-measure with curl + getent (network required)")
    ap.add_argument("--timeout", type=int, default=25, help="per-URL curl timeout")
    ap.add_argument("--delay", type=float, default=0.5, help="delay between probes")
    ap.add_argument("--check-dead", action="store_true",
                    help="exit 1 if the registry disagrees with a live measurement")
    ap.add_argument("--json", help="write results to this path")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    try:
        data = json.loads(ASSETS.read_text(encoding="utf-8"))
    except OSError as e:
        print("cannot read %s: %s" % (ASSETS, e), file=sys.stderr)
        return 2
    srcs = data.get("sources", [])
    if not srcs:
        print("registry empty", file=sys.stderr)
        return 2

    rows = []
    for s in srcs:
        r = dict(s)
        if a.live:
            cls, dns, code = classify(s["url"], a.timeout)
            r["live_reach"], r["live_dns"], r["live_http"] = cls, dns, code
            r["stale"] = cls != s.get("reach")
            time.sleep(a.delay)
        rows.append(r)

    if a.layer is not None:
        rows = [r for r in rows if r["layer"] == a.layer]
    if a.reach:
        key = "live_reach" if a.live else "reach"
        rows = [r for r in rows if r.get(key) == a.reach]

    if not a.quiet:
        mode = "LIVE probe" if a.live else "recorded (offline; add --live to re-measure)"
        print("source registry — %s — %d source(s)\n" % (mode, len(rows)))
        by_layer: dict[int, list[dict]] = {}
        for r in rows:
            by_layer.setdefault(r["layer"], []).append(r)
        for layer in sorted(by_layer):
            print("== %s ==" % LAYER_TITLE.get(layer, "Layer %d" % layer))
            for r in by_layer[layer]:
                # Field to display depends on the mode: with --live the measured
                # class wins, otherwise the recorded one. Resolving the FIELD NAME
                # first and then looking it up once avoids the bug this line had
                # (keying REACH_LABEL by a *value*), and keeps one source of truth
                # for the tag.
                field = "live_reach" if a.live else "reach"
                cls = r.get(field) or "unknown"
                tag = REACH_LABEL.get(cls, cls)
                extra = ""
                if a.live:
                    extra = "  [http %s, dns %s]" % (r["live_http"], "ok" if r["live_dns"] else "FAIL")
                    if r["stale"]:
                        extra += "  <-- STALE (recorded: %s)" % r["reach"]
                print("  %-14s %s%s" % (tag, r["url"], extra))
                print("       %s" % r["name"])
            print()

        from collections import Counter
        key = "live_reach" if a.live else "reach"
        print("reach classes:", dict(Counter(r[key] for r in rows)))

    if a.json:
        Path(a.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1),
                                encoding="utf-8")
        print("wrote %s" % a.json)

    if a.check_dead:
        if not a.live:
            print("--check-dead requires --live", file=sys.stderr)
            return 2
        stale = [r for r in rows if r.get("stale")]
        if stale:
            print("\nSTALE registry entries (%d):" % len(stale))
            for r in stale:
                print("  %s: recorded=%s live=%s (http %s)"
                      % (r["url"], r["reach"], r["live_reach"], r["live_http"]))
            print("Update assets/verified_terms.json, then re-run scripts/build_glossary.py")
            return 1
        print("\nregistry agrees with live measurement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
