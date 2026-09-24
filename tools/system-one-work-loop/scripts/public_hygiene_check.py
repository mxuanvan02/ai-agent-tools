#!/usr/bin/env python3
"""Public-hygiene gate for the evidence-first-research tool.

Scans every text file in the tool directory for tokens that must never appear
in the public repo: personal identifiers, internal host paths, codenames of
UNPUBLISHED papers, institution names, secret-shaped strings, leftover
sanitizer placeholders.

Forbidden patterns are assembled by concatenation so this script does not
flag itself.

Exit 0 = clean, exit 1 = findings printed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

FORBIDDEN: list[tuple[str, re.Pattern[str]]] = [
    # personal identifiers
    ("personal-name", re.compile(r"anh\s+văn|người dùng Van\b|\bVan's\b", re.I)),
    ("host-username", re.compile("hito" + "kiri")),
    ("old-skill-name", re.compile("anh-van-" + r"research-workflow")),
    # internal paths / storage
    ("internal-path", re.compile(r"/media/" + "SAS|/home/van\b|/Users/van\b")),
    # UNPUBLISHED project/paper codenames (must stay genericized)
    ("codename-1", re.compile("CAW-" + "VoU")),
    ("codename-2", re.compile(r"\bRA" + "BS\b")),
    ("codename-3", re.compile("Probe" + "Transmit")),
    ("codename-4", re.compile("ECM-" + "TQAG")),
    ("codename-5", re.compile(r"\bST" + "AIS\b")),
    ("codename-6", re.compile("Mekong-" + "Trace")),
    ("codename-7", re.compile("HOEIT-" + "LegalQA|VDTM-" + "LegalQA")),
    # institution identifiers
    ("institution-1", re.compile(r"ĐH" + "SP|ĐHSP")),
    ("institution-2", re.compile("ĐH " + "Huế|Đại học " + "Huế")),
    ("institution-3", re.compile("Hue " + "University")),
    ("institution-4", re.compile(r"\bDH" + "H\b|\bDHH\b")),
    ("institution-5", re.compile(r"\bHO" + "EIT\b")),
    ("institution-6", re.compile("Thu " + "Dau Mot")),
    # secret shapes
    ("secret-token", re.compile(r"gh[oprsu]_[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}")),
    ("secret-key", re.compile("BEGIN [A-Z ]*PRIVATE KEY")),
    # sanitizer leftovers
    ("placeholder", re.compile(r"\x00")),
]


def main() -> int:
    findings: list[str] = []
    n_files = 0
    for path in sorted(TOOL_DIR.rglob("*")):
        if not path.is_file() or path.resolve() == SELF:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"binary-file\t{path.relative_to(TOOL_DIR)}")
            continue
        n_files += 1
        for label, pat in FORBIDDEN:
            for m in pat.finditer(text):
                start = max(0, m.start() - 40)
                ctx = text[start:m.end() + 40].replace("\n", " ")
                findings.append(f"{label}\t{path.relative_to(TOOL_DIR)}\t…{ctx}…")

    print(f"scanned {n_files} files under {TOOL_DIR}")
    if findings:
        print(f"FAIL: {len(findings)} finding(s)")
        for f in findings[:40]:
            print(" ", f[:180])
        if len(findings) > 40:
            print(f"  … and {len(findings) - 40} more")
        return 1
    print("PASS: no forbidden tokens found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
