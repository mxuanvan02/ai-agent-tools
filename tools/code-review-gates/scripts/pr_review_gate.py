#!/usr/bin/env python3
"""One command a PR workflow calls before merging: is THIS pull request mergeable?

It combines the three things that decide the answer and refuses to guess any of them:

  1. tier + required PEOPLE       from the diff (risk_tier.py), not from the author
  2. approvals that actually count distinct humans whose LATEST review on the CURRENT head
                                  sha is APPROVED. An approval on an older commit is stale;
                                  approve-then-request-changes is not an approval; a bot's
                                  approval never fills a human slot.
  3. unanswered findings           from the review ledger (review_ledger.py)

Exit codes matter and are not interchangeable:

  0  mergeable
  1  blocked, and every reason is in the JSON
  2  could not evaluate (gh failed, PR unreadable, ledger unparsable) -- FAIL CLOSED

A caller that treats 2 as 0 merges anything whose check crashed. That is the one mistake this
tool exists to make impossible, so 2 is reserved for "I do not know" and never printed as a
blocked/allowed verdict.

Usage:
    python3 scripts/pr_review_gate.py --pr 68
    python3 scripts/pr_review_gate.py --pr 68 --repo mxuanvan02/ai-agent-tools
    python3 scripts/pr_review_gate.py --pr-json fixture.json --pr-files fixture.tsv \
        --ledger review-ledger.jsonl --offline     # no network; used by the tests
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import risk_tier  # noqa: E402
import review_ledger  # noqa: E402

BOT_SUFFIX = "[bot]"


class CannotEvaluate(Exception):
    """Raised when the inputs needed for a verdict are missing. Always maps to exit 2."""


def run_gh(args: list[str]) -> str:
    if shutil.which("gh") is None:
        raise CannotEvaluate("gh is not installed; cannot read PR state (refusing to guess)")
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise CannotEvaluate("gh %s failed: %s" % (" ".join(args), (proc.stderr or proc.stdout).strip()[:400]))
    return proc.stdout


def fetch_pr(pr: int, repo: str | None) -> dict:
    fields = "number,state,isDraft,mergeable,headRefOid,headRefName,baseRefName,author,reviews,files"
    cmd = ["pr", "view", str(pr), "--json", fields]
    if repo:
        cmd += ["--repo", repo]
    try:
        return json.loads(run_gh(cmd))
    except json.JSONDecodeError as exc:
        raise CannotEvaluate("gh returned unparsable JSON: %s" % exc)


def fetch_files(pr: int, repo: str | None) -> list[tuple[int, int, str]]:
    """Per-file additions/deletions from the PR itself, so the tier is computed on what the
    pull request actually contains rather than on whatever the local checkout happens to be."""
    cmd = ["api", "repos/{owner}/{repo}/pulls/%d/files" % pr, "--paginate",
           "--jq", ".[] | \"\\(.additions)\\t\\(.deletions)\\t\\(.filename)\""]
    if repo:
        # gh substitutes {owner}/{repo} only when --repo is given on api calls via -R
        cmd += ["-R", repo]
    out = run_gh(cmd)
    files: list[tuple[int, int, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            raise CannotEvaluate("unexpected file line from gh: %r" % line)
        files.append((int(parts[0]), int(parts[1]), parts[2]))
    if not files:
        raise CannotEvaluate("PR reports no changed files; refusing to classify an empty diff")
    return files


def is_bot(login: str | None, user_type: str | None) -> bool:
    if user_type == "Bot":
        return True
    return bool(login) and login.endswith(BOT_SUFFIX)


def human_approvals(reviews: list[dict], head_sha: str) -> dict[str, str]:
    """Logins whose LATEST review on the current head sha is APPROVED, bot-free.

    Two traps this closes, both real:

      * an approval on an older commit is stale -- the rule is "an approval covers one specific
        commit", so ``commit_id`` must equal the current head;
      * a reviewer who approved and later requested changes has not approved -- only the latest
        review per login counts, which is why the whole list is replayed in order.
    """
    latest: dict[str, dict] = {}
    for rev in reviews:
        user = rev.get("author") or rev.get("user") or {}
        login = user.get("login")
        if not login:
            continue
        latest[login] = rev  # later reviews overwrite earlier ones for the same person
    approved: dict[str, str] = {}
    for login, rev in latest.items():
        if rev.get("state") != "APPROVED":
            continue
        commit = rev.get("commit", {}).get("oid") if isinstance(rev.get("commit"), dict) else rev.get("commit_id")
        if commit and commit != head_sha:
            continue  # stale approval: the code moved after it was given
        user = rev.get("author") or rev.get("user") or {}
        if is_bot(login, user.get("type")):
            continue  # a bot's approval never fills a human slot
        approved[login] = commit or head_sha
    return approved


def evaluate(pr: dict, files: list[tuple[int, int, str]], ledger: Path,
             max_rounds: int, cfg: dict) -> dict:
    head_sha = pr.get("headRefOid") or ""
    if not head_sha:
        raise CannotEvaluate("PR has no head sha; cannot bind approvals to a commit")

    tier = risk_tier.decide(files, cfg)
    reviews = pr.get("reviews") or []
    approvals = human_approvals(reviews, head_sha)

    reasons: list[str] = []

    if pr.get("isDraft"):
        reasons.append("PR is a draft")
    if str(pr.get("state", "")).upper() != "OPEN":
        reasons.append("PR state is %s, not OPEN" % pr.get("state"))
    if str(pr.get("mergeable", "")).upper() == "CONFLICTING":
        reasons.append("PR has merge conflicts")

    required = tier["approvals_required"]
    if len(approvals) < required:
        reasons.append("%d human approval(s) required by tier %s; %d counted on head %s"
                       % (required, tier["tier"], len(approvals), head_sha[:12]))

    rows = review_ledger.read_ledger(ledger)
    state = review_ledger.current_state(rows)
    open_findings = [f for f in state.values() if f.status == "open" and not f.id.startswith("__round__")]
    rounds_used = max((f.round for f in state.values() if not f.id.startswith("__round__")), default=0)
    if open_findings:
        reasons.append("%d review finding(s) still open: %s"
                       % (len(open_findings), ", ".join(sorted(f.id for f in open_findings))))
    if rounds_used > max_rounds:
        reasons.append("round %d exceeds cap of %d; the reviewer must ask the author to "
                       "reconsider the approach instead of producing another round"
                       % (rounds_used, max_rounds))

    return {
        "mergeable": not reasons,
        "pr": pr.get("number"),
        "head_sha": head_sha,
        "tier": tier["tier"],
        "approvals_required": required,
        "approvals_counted": sorted(approvals),
        "approvals_needed_more": max(0, required - len(approvals)),
        "open_findings": len(open_findings),
        "rounds_used": rounds_used,
        "max_rounds": max_rounds,
        "total_lines": tier["total_lines"],
        "size_note": tier["size_note"],
        "files": tier["files"],
        "reasons": reasons,
        "note": "approvals count PEOPLE whose latest review on this head is APPROVED; "
                "bot approvals and approvals on an older commit do not count",
    }


def load_fixture_files(path: Path) -> list[tuple[int, int, str]]:
    files = risk_tier.parse_numstat(path.read_text(encoding="utf-8"))
    if not files:
        raise CannotEvaluate("fixture has no files")
    return files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pr", type=int, help="pull request number")
    ap.add_argument("--repo", help="owner/name; defaults to the current repo")
    ap.add_argument("--config", type=Path, help="risk-tier policy JSON")
    ap.add_argument("--ledger", type=Path, default=review_ledger.DEFAULT_LEDGER)
    ap.add_argument("--max-rounds", type=int, default=review_ledger.DEFAULT_MAX_ROUNDS)
    ap.add_argument("--pr-json", type=Path, help="offline: fixture of `gh pr view --json`")
    ap.add_argument("--pr-files", type=Path, help="offline: fixture of additions/deletions/filename TSV")
    ap.add_argument("--offline", action="store_true", help="require fixtures; never call gh")
    args = ap.parse_args(argv)

    cfg = risk_tier.DEFAULT_CONFIG
    if args.config:
        try:
            cfg = {**risk_tier.DEFAULT_CONFIG, **json.loads(args.config.read_text(encoding="utf-8"))}
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"error": "cannot read config: %s" % exc}), file=sys.stderr)
            return 2

    try:
        if args.offline or args.pr_json:
            if not args.pr_json or not args.pr_files:
                raise CannotEvaluate("offline mode needs both --pr-json and --pr-files")
            try:
                pr = json.loads(args.pr_json.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise CannotEvaluate("cannot read PR fixture: %s" % exc)
            files = load_fixture_files(args.pr_files)
        else:
            if not args.pr:
                raise CannotEvaluate("either --pr or --offline fixtures are required")
            pr = fetch_pr(args.pr, args.repo)
            files = fetch_files(args.pr, args.repo)

        verdict = evaluate(pr, files, args.ledger, args.max_rounds, cfg)
    except CannotEvaluate as exc:
        print(json.dumps({"mergeable": None, "error": str(exc),
                          "note": "cannot evaluate is NOT mergeable; fix the input"},
                         indent=2, ensure_ascii=False))
        return 2

    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    return 0 if verdict["mergeable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
