"""Monitor/triage benchmark: current-style LLM batch scoring vs Jev per-item Score.

Mirrors Hermes' cron/scripts/classify_items.py: given N candidate items and a
plain-language importance criterion, score each 0-10 and surface those >= threshold.

  baseline  = ONE LLM call scoring the whole batch, JSON parsed back (the current
              approach; goes through 9router / NINEROUTER_API_KEY).
  jev       = one Jev Score per item on a 0-10 danger/importance rubric.

Metrics vs gold labels:
  - MAE               mean absolute error of the 0-10 score
  - surface_f1        F1 of "surfaced (>=threshold)" decision vs gold-surfaced
  - parse_failures    baseline only: items the LLM JSON step lost
  - latency, tokens

Run:
  python3 monitor/run_monitor_bench.py --baseline   # LLM via 9router
  python3 monitor/run_monitor_bench.py --jev         # Jev
  python3 monitor/run_monitor_bench.py --both        # both + comparison
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

DATA = Path(__file__).resolve().parent / "items.jsonl"
CRITERIA = (
    "Importance for an ops/on-call operator. High (8-10): production outages, "
    "security incidents, payment/billing failures, expiring certs, contracts due "
    "today. Medium (4-7): CI red, disk filling, cost spikes, review requests, "
    "schedule changes. Low (0-3): newsletters, social notifications, shipping "
    "updates, spam, far-future reminders."
)
THRESHOLD = 7

# 0-10 importance rubric as 4 ordered Score levels; code maps score*3.33 back.
_JEV_LEVELS = [
    "Low importance: newsletters, social notifications, shipping updates, spam, "
    "far-future reminders. Safe to ignore now.",
    "Medium-low: informational, review requests, schedule changes, minor FYI.",
    "Medium-high: CI failing, disk filling, cost spikes, password reset, things "
    "needing attention soon.",
    "Critical: production outage, security incident, payment/billing failure, "
    "cert expiring, contract due today. Surface immediately.",
]


def load_items():
    rows = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


# ── baseline: one LLM batch call via 9router (OpenAI-compatible) ─────────────

def _nine_base_url() -> str:
    return os.environ.get("NINEROUTER_BASE_URL", "http://localhost:8080/v1").rstrip("/")


def baseline_scores(items, model="qwen/qwen3.7-flash"):
    key = os.environ.get("NINE" + "ROUTER_API_" + "KEY", "")
    if not key:
        raise RuntimeError("NINEROUTER_API_KEY not set")
    view_keys = ("title", "text")
    lines = [f"IMPORTANCE CRITERIA:\n{CRITERIA}\n", "ITEMS:"]
    for i, it in enumerate(items):
        view = {k: it[k] for k in view_keys if k in it}
        lines.append(f"[{i}] {json.dumps(view, ensure_ascii=False)[:600]}")
    lines.append(
        "\nScore each item 0-10 for importance. Return ONLY a JSON array, one "
        'object per item: {"index": <int>, "score": <int 0-10>}. Same order.'
    )
    prompt = "\n".join(lines)
    body = json.dumps({
        "model": model, "temperature": 0, "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        _nine_base_url() + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    latency_ms = (time.monotonic() - t0) * 1000.0
    content = data["choices"][0]["message"]["content"] or ""
    usage = data.get("usage", {})
    tokens = usage.get("total_tokens", 0)

    # Parse — tolerate fences and stray text, like classify_items.py.
    text = content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if "\n" in text:
            text = text.split("\n", 1)[1]
    parsed = {}
    try:
        arr = json.loads(text)
    except json.JSONDecodeError:
        s, e = text.find("["), text.rfind("]")
        arr = json.loads(text[s:e + 1]) if (s >= 0 and e > s) else []
    for o in arr if isinstance(arr, list) else []:
        if isinstance(o, dict) and isinstance(o.get("index"), int):
            try:
                parsed[o["index"]] = float(o["score"])
            except (TypeError, ValueError, KeyError):
                pass
    scores = [parsed.get(i) for i in range(len(items))]
    parse_failures = sum(1 for s in scores if s is None)
    return scores, latency_ms, tokens, parse_failures


# ── jev: one Score per item ─────────────────────────────────────────────────

def jev_scores(items):
    from jev_client import JevClient
    c = JevClient()
    instr = (
        "Rate the importance of this item for an ops/on-call operator, using the "
        "levels. Judge only `title` and `text`."
    )
    scores, total_ms, total_tok = [], 0.0, 0
    for it in items:
        state = {"title": it.get("title", ""), "text": it.get("text", "")}
        ans = c.ask_score(state, instr, _JEV_LEVELS)
        scores.append(round(ans.score * (10.0 / 3.0), 2))  # 0..3 -> 0..10
        total_ms += ans.latency_ms
        total_tok += ans.input_tokens + ans.output_tokens
    return scores, total_ms, total_tok, 0


# ── scoring ─────────────────────────────────────────────────────────────────

def evaluate(items, scores):
    golds = [it["gold"] for it in items]
    paired = [(g, s) for g, s in zip(golds, scores) if s is not None]
    mae = sum(abs(g - s) for g, s in paired) / len(paired) if paired else float("nan")
    tp = fp = fn = 0
    for it, s in zip(items, scores):
        gold_surf = it["gold"] >= THRESHOLD
        pred_surf = (s is not None) and (s >= THRESHOLD)
        if pred_surf and gold_surf:
            tp += 1
        elif pred_surf and not gold_surf:
            fp += 1
        elif not pred_surf and gold_surf:
            fn += 1
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {"mae": round(mae, 2), "surface_f1": round(f1, 3),
            "precision": round(prec, 3), "recall": round(rec, 3),
            "tp": tp, "fp": fp, "fn": fn}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--jev", action="store_true")
    ap.add_argument("--both", action="store_true")
    args = ap.parse_args()
    if not (args.baseline or args.jev or args.both):
        args.both = True

    items = load_items()
    results = {}

    if args.baseline or args.both:
        try:
            sc, ms, tok, pf = baseline_scores(items)
            results["baseline"] = (evaluate(items, sc), ms, tok, pf, sc)
        except Exception as e:
            print(f"baseline FAILED: {type(e).__name__}: {e}", file=sys.stderr)

    if args.jev or args.both:
        try:
            sc, ms, tok, pf = jev_scores(items)
            results["jev"] = (evaluate(items, sc), ms, tok, pf, sc)
        except Exception as e:
            print(f"jev FAILED: {type(e).__name__}: {e}", file=sys.stderr)

    print("\n" + "=" * 72)
    print(f"  MONITOR/TRIAGE BENCHMARK  ({len(items)} items, threshold>={THRESHOLD})")
    print("=" * 72)
    hdr = f"{'metric':<16}" + "".join(f"{k:>16}" for k in results)
    print(hdr)
    print("-" * 72)
    for m in ("mae", "surface_f1", "precision", "recall", "parse_failures",
              "latency_ms", "total_tokens"):
        row = f"{m:<16}"
        for k in results:
            ev, ms, tok, pf, _ = results[k]
            val = {"parse_failures": pf, "latency_ms": round(ms, 0),
                   "total_tokens": tok}.get(m, ev.get(m))
            row += f"{str(val):>16}"
        print(row)
    print("-" * 72)
    print("Note: lower MAE = closer to human labels; higher surface_f1 = better")
    print("triage decisions. Baseline parse_failures>0 means the LLM JSON step")
    print("silently dropped items — the exact fragility Jev's typed output removes.")


if __name__ == "__main__":
    main()
