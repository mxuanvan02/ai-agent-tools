#!/usr/bin/env python3
"""Decide the risk tier of a change and how many humans must approve it.

The tier comes from the CHANGE, never from the author: the same rule file produces the same
answer for a staff engineer and for an agent. Unknown paths fail closed to the highest tier,
because the failure mode of a wrong ``low`` is a silent merge and the failure mode of a wrong
``high`` is one extra read.

Input is `git diff --numstat` (or --name-only) on stdin or from a file. Output is JSON on
stdout; exit 0 means a tier was assigned, exit 2 means the input could not be read at all --
never exit 0 with an empty verdict, because a caller that pipes this into CI would then treat
an unparsed diff as a clean one.

Usage:
    git diff --numstat origin/main...HEAD | python3 scripts/risk_tier.py --config risks.json
    python3 scripts/risk_tier.py --config risks.json --numstat /tmp/changes.tsv
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

TIER_ORDER = {"low": 0, "medium": 1, "high": 2}
APPROVALS = {"low": 0, "medium": 1, "high": 2}

# Default policy. Chosen so that the rules a reader would NOT think to write (CI workflows, auth,
# migrations) are already covered, and so that anything unmatched lands on the strict side.
DEFAULT_CONFIG = {
    "default_tier": "high",
    "always_human": [
        "**/.github/workflows/**",
        "**/.gitlab-ci.yml",
        "**/Dockerfile",
        "**/docker-compose*.yml",
        "**/requirements*.txt",
        "**/pyproject.toml",
        "**/package.json",
        "**/*lock*.json",
        "**/migrations/**",
        "**/alembic/**",
        "**/auth/**",
        "**/*auth*",
        "**/billing/**",
        "**/*payment*",
        "**/install.sh",
        "**/*.pem",
        "**/*.key",
    ],
    "rules": [
        {"glob": "docs/**", "tier": "low", "reason": "documentation only"},
        {"glob": "**/*.md", "tier": "low", "reason": "prose change"},
        {"glob": "**/tests/**", "tier": "medium", "reason": "test code: wrong tests hide bugs"},
        {"glob": "**/*.tex", "tier": "medium", "reason": "typeset source: renders, does not execute"},
        {"glob": "**/references/**", "tier": "low", "reason": "reference material, not executed"},
    ],
    # A change this large is not reviewed line by line by anyone. Treat size as its own risk
    # signal: the measured finding rate on changes over 1k lines is high enough that the tier
    # floor is raised rather than trusting the path rules alone.
    "large_change": {"lines": 1000, "tier_floor": "medium"},
}


@dataclass
class FileVerdict:
    path: str
    added: int
    deleted: int
    tier: str
    reasons: list[str] = field(default_factory=list)

    @property
    def lines(self) -> int:
        return self.added + self.deleted


def glob_match(pattern: str, path: str) -> bool:
    """Segment-aware glob: ``*`` and ``?`` stay inside one path segment, ``**`` crosses them.

    fnmatch is deliberately NOT used: its ``*`` matches ``/``, so ``docs/*`` would match
    ``docs/a/b/c.py`` and a broad-but-shallow rule would silently grant the low tier to a
    deeply nested file. For a gate whose whole job is bounding blast radius that is the wrong
    direction to be loose in.
    """
    pat_segs = [s for s in pattern.split("/") if s not in ("", ".")]
    path_segs = [s for s in path.split("/") if s not in ("", ".")]
    if pattern.endswith("/**") and pat_segs:
        pat_segs = pat_segs + ["**"]
    return _match_segs(pat_segs, path_segs)


def _match_segs(pat: list[str], segs: list[str]) -> bool:
    if not pat:
        return not segs
    head, rest = pat[0], pat[1:]
    if head == "**":
        # ** matches zero or more segments; try every split, shortest first so a pattern like
        # ``**/tests/**`` still matches ``tests/x.py`` with zero leading segments.
        for i in range(len(segs) + 1):
            if _match_segs(rest, segs[i:]):
                return True
        return False
    if not segs:
        return False
    if fnmatch.fnmatchcase(segs[0], head):
        return _match_segs(rest, segs[1:])
    return False


def parse_numstat(text: str) -> list[tuple[int, int, str]]:
    """Parse `git diff --numstat`. Binary entries show '-' and are counted as 0 lines but kept,
    because a binary change is exactly the kind that must not be silently dropped."""
    out: list[tuple[int, int, str]] = []
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            raise ValueError("not a --numstat line: %r" % line)
        a, d, path = parts[0], parts[1], "\t".join(parts[2:])
        # rename syntax: 12\t3\told => new  -- keep the destination, it is what will exist
        if " => " in path:
            path = path.split(" => ")[-1].strip("{} ")
        out.append((int(a) if a.isdigit() else 0, int(d) if d.isdigit() else 0, path))
    return out


def parse_name_only(text: str) -> list[tuple[int, int, str]]:
    return [(0, 0, ln.strip()) for ln in text.splitlines() if ln.strip()]


def classify(path: str, cfg: dict) -> tuple[str, list[str]]:
    """Tier for one path: always-human wins, else the STRICTEST matching rule, else the default.

    The default is a floor under UNMATCHED paths only. A common way to get this wrong is to start
    the running maximum at the default: then no rule can ever lower a tier, every change becomes
    high, and the gate is quietly useless while still printing a verdict. So matching rules are
    combined among themselves first, and the default is consulted only when nothing matched.
    """
    for pat in cfg.get("always_human", []):
        if glob_match(pat, path):
            return "high", ["always-human path: %s" % pat]
    matched: list[tuple[str, str]] = []
    for rule in cfg.get("rules", []):
        if rule.get("tier") not in TIER_ORDER:
            raise ValueError("rule tier must be one of %s: %r" % (sorted(TIER_ORDER), rule))
        if glob_match(rule["glob"], path):
            matched.append((rule["tier"], "%s (%s)" % (rule.get("reason", rule["glob"]), rule["tier"])))
    if not matched:
        return cfg.get("default_tier", "high"), ["no rule matched; default tier %s applied"
                                                % cfg.get("default_tier", "high")]
    best = max((t for t, _ in matched), key=lambda t: TIER_ORDER[t])
    return best, [r for t, r in matched if t == best]


def decide(files: list[tuple[int, int, str]], cfg: dict) -> dict:
    verdicts: list[FileVerdict] = []
    for added, deleted, path in files:
        tier, reasons = classify(path, cfg)
        verdicts.append(FileVerdict(path, added, deleted, tier, reasons))

    total_lines = sum(v.lines for v in verdicts)
    tier = "low"
    if verdicts:
        tier = max((v.tier for v in verdicts), key=lambda t: TIER_ORDER[t])
    else:
        tier = "medium"  # an empty diff is not a change we can vouch for
        verdicts.append(FileVerdict("<empty>", 0, 0, "medium", ["no files parsed; refusing to call this low"]))

    large = cfg.get("large_change", {}) or {}
    size_reason = None
    # One threshold, one effect: raise the floor to `medium` when the change is too big for
    # anyone to read line by line. Kept as a floor rather than a tier so an always-human path
    # inside a big change still wins.
    threshold = int(large.get("lines") or 10**9)
    if total_lines >= threshold:
        floor = large.get("tier_floor", "medium")
        if floor not in TIER_ORDER:
            raise ValueError("large_change.tier_floor must be one of %s" % sorted(TIER_ORDER))
        if TIER_ORDER[tier] < TIER_ORDER[floor]:
            tier = floor
        size_reason = "%d changed lines is over the %d-line threshold; tier floor raised to %s" % (
            total_lines, threshold, floor)

    return {
        "tier": tier,
        "approvals_required": APPROVALS[tier],
        "total_lines": total_lines,
        "files": [
            {"path": v.path, "tier": v.tier, "lines": v.lines, "reasons": v.reasons}
            for v in sorted(verdicts, key=lambda v: (-TIER_ORDER[v.tier], v.path))
        ],
        "size_note": size_reason,
        "note": "approvals_required counts PEOPLE; an automated review never fills one",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, help="JSON policy file (see templates/risk-tiers.json)")
    ap.add_argument("--numstat", type=Path, help="file containing `git diff --numstat` output")
    ap.add_argument("--name-only", action="store_true", help="input is `git diff --name-only` (no line counts)")
    ap.add_argument("--json", action="store_true", help="accepted for symmetry; output is always JSON")
    args = ap.parse_args(argv)

    cfg = DEFAULT_CONFIG
    if args.config:
        try:
            loaded = json.loads(args.config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"error": "cannot read config: %s" % exc}), file=sys.stderr)
            return 2
        cfg = {**DEFAULT_CONFIG, **loaded}

    try:
        raw = args.numstat.read_text(encoding="utf-8") if args.numstat else sys.stdin.read()
    except OSError as exc:
        print(json.dumps({"error": "cannot read diff input: %s" % exc}), file=sys.stderr)
        return 2

    try:
        files = parse_name_only(raw) if args.name_only else parse_numstat(raw)
    except ValueError as exc:
        print(json.dumps({"error": str(exc), "hint": "pipe `git diff --numstat`, not a patch"}), file=sys.stderr)
        return 2

    print(json.dumps(decide(files, cfg), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
