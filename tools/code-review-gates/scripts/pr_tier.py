#!/usr/bin/env python3
"""Quick risk tier check for a pull request.

Usage:
    python3 scripts/pr_tier.py --pr 68
    python3 scripts/pr_tier.py --pr 68 --repo mxuanvan02/ai-agent-tools
    python3 scripts/pr_tier.py --pr 68 --json /tmp/tier.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import risk_tier  # noqa: E402


def gh(*args: str) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise SystemExit("gh failed: %s\n%s" % (" ".join(args), (proc.stderr or proc.stdout)[:400]))
    return proc.stdout


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
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    cfg = risk_tier.DEFAULT_CONFIG
    if args.config:
        cfg = {**risk_tier.DEFAULT_CONFIG, **json.loads(args.config.read_text(encoding="utf-8"))}

    files = pr_files(args.repo, args.pr)
    if not files:
        print("PR has no files", file=sys.stderr)
        return 1

    verdict = risk_tier.decide(files, cfg)

    print("PR #%d: tier=%s, approvals=%d, lines=%d, files=%d" % (
        args.pr, verdict["tier"], verdict["approvals_required"],
        verdict["total_lines"], len(files)))
    print()
    for f in verdict["files"]:
        print("  %-6s %5dL  %s" % (f["tier"], f["lines"], f["path"]))
        print("           %s" % (f["reasons"][0] if f["reasons"] else ""))

    if args.json:
        args.json.write_text(json.dumps(verdict, indent=2, ensure_ascii=False), encoding="utf-8")
        print("\nwrote %s" % args.json)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
