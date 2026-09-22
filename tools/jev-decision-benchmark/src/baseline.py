"""Baseline: a pure pattern matcher, standing in for the deny/escalate decision
made WITHOUT a smart guardian. This is the 'manual mode' floor — a flagged
command that isn't obviously fatal just escalates to a human.

It is intentionally simple: a small deny list of clearly-fatal patterns, else
escalate. It has no semantic understanding, so it cannot tell `rm -rf ./build`
(safe) from `rm -rf /` (fatal) beyond the literal patterns — which is exactly
the gap a guardian is meant to close.
"""
from __future__ import annotations

import re

_FATAL = [
    re.compile(r"\brm\s+-rf\s+(/|~|\$HOME)(\s|/|\*|$)"),
    re.compile(r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:"),  # fork bomb
    re.compile(r"\bdd\s+.*of=/dev/"),
    re.compile(r"\bmkfs\."),
    re.compile(r"DROP\s+DATABASE", re.IGNORECASE),
    re.compile(r"\bchmod\s+-R\s+777\s+/"),
    re.compile(r"\|\s*bash\b|\|\s*sh\b"),  # pipe to shell
]


def baseline_verdict(command: str, flagged_as: str) -> str:
    """Return 'deny' for literal-fatal matches, else 'escalate'. Never auto-approves."""
    for pat in _FATAL:
        if pat.search(command):
            return "deny"
    return "escalate"
