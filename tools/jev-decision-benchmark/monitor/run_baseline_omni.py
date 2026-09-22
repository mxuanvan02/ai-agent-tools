"""Baseline monitor scoring via omniproxy chat/completions, using the WORKING
providers.omniproxy.api_key (chat path). Model chosen on CLI. Prints scorecard
comparable to the Jev run.

Usage: python3 monitor/run_baseline_omni.py --model qwen3.8-max
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_monitor_bench as b  # noqa: E402


def omni_key() -> str:
    cfg_path = os.environ.get("HERMES_CONFIG", os.path.expanduser("~/.hermes/config.yaml"))
    cfg = yaml.safe_load(open(cfg_path))
    return cfg.get("providers", {}).get("omniproxy", {}).get("api_key", "") or ""


def baseline(items, model, key):
    view_keys = ("title", "text")
    lines = [f"IMPORTANCE CRITERIA:\n{b.CRITERIA}\n", "ITEMS:"]
    for i, it in enumerate(items):
        view = {k: it[k] for k in view_keys if k in it}
        lines.append(f"[{i}] {json.dumps(view, ensure_ascii=False)[:600]}")
    lines.append('\nScore each item 0-10 for importance. Return ONLY a JSON array, '
                 'one object per item: {"index": <int>, "score": <int 0-10>}. Same order.')
    body = json.dumps({"model": model, "temperature": 0, "max_tokens": 1024,
                       "messages": [{"role": "user", "content": "\n".join(lines)}]}).encode()
    req = urllib.request.Request(
        "http://localhost:8080/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST")
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode())
    latency_ms = (time.monotonic() - t0) * 1000.0
    content = d["choices"][0]["message"]["content"] or ""
    tok = d.get("usage", {}).get("total_tokens", 0)
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
            except Exception:
                pass
    scores = [parsed.get(i) for i in range(len(items))]
    pf = sum(1 for s in scores if s is None)
    return scores, latency_ms, tok, pf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3.8-max")
    args = ap.parse_args()
    items = b.load_items()
    key = omni_key()
    sc, ms, tok, pf = baseline(items, args.model, key)
    ev = b.evaluate(items, sc)
    print(f"model={args.model}")
    print("BASELINE:", ev, f"latency_ms={ms:.0f} tokens={tok} parse_failures={pf}")
    print("scores:", sc)


if __name__ == "__main__":
    main()
