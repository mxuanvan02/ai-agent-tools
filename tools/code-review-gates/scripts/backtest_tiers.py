#!/usr/bin/env python3
"""Backtest the risk tier against real, already-merged pull requests.

The question this answers is the only one that matters before trusting a tier policy: on the
changes this team actually ships, does the classifier put them where a human would? A policy
that calls everything `high` is safe and useless; one that calls a payment adapter `low` is
worse than no policy.

Reads PR file lists straight from the GitHub API (additions/deletions/filename), so the verdict
is on what the PR contained, not on the local checkout.

Usage:
    python3 scripts/backtest_tiers.py --repo mxuanvan02/ai-agent-tools --limit 40
    python3 scripts/backtest_tiers.py --repo mxuanvan02/easyhome --limit 30 --json out.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import risk_tier  # noqa: E402


def gh(*args: str) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=180)
    if proc.returncode != 0:
        raise SystemExit("gh failed: %s\n%s" % (" ".join(args), (proc.stderr or proc.stdout)[:400]))
    return proc.stdout


def list_prs(repo: str, limit: int, state: str) -> list[dict]:
    out = gh("pr", "list", "--repo", repo, "--state", state, "--limit", str(limit),
             "--json", "number,title,state,additions,deletions,changedFiles")
    return json.loads(out)


def pr_files(repo: str, number: int) -> list[tuple[int, int, str]]:
    out = gh("api", "repos/%s/pulls/%d/files" % (repo, number), "--paginate",
             "--jq", ".[] | \"\\(.additions)\\t\\(.deletions)\\t\\(.filename)\"")
    files: list[tuple[int, int, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        a, d, name = line.split("\t", 2)
        files.append((int(a), int(d), name))
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="owner/name")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--state", default="merged", choices=["merged", "open", "closed", "all"])
    ap.add_argument("--config", type=Path)
    ap.add_argument("--json", type=Path, help="write the per-PR table here")
    args = ap.parse_args()

    cfg = risk_tier.DEFAULT_CONFIG
    if args.config:
        cfg = {**risk_tier.DEFAULT_CONFIG, **json.loads(args.config.read_text(encoding="utf-8"))}

    prs = list_prs(args.repo, args.limit, args.state)
    rows = []
    for pr in prs:
        try:
            files = pr_files(args.repo, pr["number"])
        except SystemExit as exc:
            print("skip #%s: %s" % (pr["number"], exc), file=sys.stderr)
            continue
        if not files:
            continue
        verdict = risk_tier.decide(files, cfg)
        top = [f for f in verdict["files"] if f["tier"] == verdict["tier"]][:2]
        rows.append({
            "number": pr["number"],
            "title": pr["title"][:80],
            "tier": verdict["tier"],
            "approvals": verdict["approvals_required"],
            "lines": verdict["total_lines"],
            "files": len(files),
            "size_note": verdict["size_note"],
            "top_paths": [f["path"] for f in top],
            "why": top[0]["reasons"][0] if top and top[0]["reasons"] else "",
        })

    counts = Counter(r["tier"] for r in rows)
    total = len(rows) or 1
    print("repo: %s   PRs measured: %d" % (args.repo, len(rows)))
    print("tier distribution: " + "  ".join(
        "%s=%d (%.0f%%)" % (t, counts.get(t, 0), 100.0 * counts.get(t, 0) / total)
        for t in ("low", "medium", "high")))
    print("mean approvals required: %.2f" % (sum(r["approvals"] for r in rows) / total))
    print()
    for r in rows:
        print("#%-4s %-6s appr=%d  %5dL %2df  %s" % (
            r["number"], r["tier"], r["approvals"], r["lines"], r["files"], r["title"]))
        print("        why: %s | %s" % (r["why"], ", ".join(r["top_paths"])[:100]))

    if args.json:
        args.json.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print("\nwrote %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
