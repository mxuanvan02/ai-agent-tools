#!/usr/bin/env python3
"""Public-hygiene gate for one tool directory in this repository.

Ships byte-identically in every tool that CI validates; TOOL_DIR is derived from __file__, so the
same text works wherever it is copied. Keep the copies identical -- a tool whose gate drifted is a
tool whose PASS means something different from its neighbour's.

Scans every text file in the tool directory for tokens that must never appear
in the public repo: personal identifiers, internal host paths, codenames of
UNPUBLISHED papers, institution names, secret-shaped strings, leftover
sanitizer placeholders.

Forbidden patterns are assembled by concatenation so this script does not
flag itself.

Matching runs on whitespace-normalised text, so a forbidden token split across a line break is
still caught; offsets are mapped back to the original file for the reported context and for the
allowlist's same-line check.

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


# Narrow allowlist for scholarly citations. A public institution named as the AUTHORITY for a
# measured convention is evidence a reader can go and check, not identity leakage -- the same
# distinction that lets a rights notice name its copyright holder. Each entry pins the file, the
# exact matched literal, and a context substring that must appear on the same line, so the
# allowance dies the moment the citation framing is removed or the name is reused anywhere else.
# Literals are assembled by concatenation for the same reason FORBIDDEN patterns are: this file
# sits inside a scanned tool directory in every copy and must not flag itself.
ALLOWED_CITATIONS: list[tuple[str, str, str, str]] = [
    # Decision 1418/QD-DHSP is the authority for the decimal-point convention documented here;
    # the surrounding lines argue FROM it, they do not name an employer.
    ("references/academic-vietnamese-standard.md", "institution-1", "ĐH" + "SP", "Decision 1418"),
    # Same sentence, second institution pattern: the English name wraps across the line break,
    # which is exactly the case normalised matching was added to see.
    ("references/academic-vietnamese-standard.md", "institution-3",
     "Hue " + "University", "Decision 1418"),
    # The journal and its faculty are the source of the word-limit rule quoted verbatim below it.
    ("references/word-budget-and-rendered-artifact-compliance.md", "institution-2",
     "Đại học " + "Huế", "Tạp chí"),
]


def normalise(text: str) -> tuple[str, list[int]]:
    """Collapse each whitespace run to one space; return it plus norm-index -> original-index.

    Collapsing to a single space cannot invent a match for the secret-shaped patterns, because a
    space breaks every character class they use. It can only reveal matches that a line break was
    hiding, which is the point.
    """
    out: list[str] = []
    mp: list[int] = []
    i, n = 0, len(text)
    while i < n:
        if text[i].isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            out.append(" ")
            mp.append(j - 1)
            i = j
        else:
            out.append(text[i])
            mp.append(i)
            i += 1
    return "".join(out), mp


def allowed(label: str, rel: str, text: str, mp: list[int], m: "re.Match[str]") -> bool:
    """True only when file, matched literal AND same-line citation context all agree.

    The context line is taken from the ORIGINAL text, not the normalised copy: after normalisation
    a whole file is one line, so a "same line" test there silently degrades into a "same file"
    test and the allowlist becomes far wider than the three citations it was written for.
    """
    a = mp[m.start()]
    b = mp[m.end() - 1] + 1
    line_start = text.rfind("\n", 0, a) + 1
    line_end = text.find("\n", b)
    line = text[line_start:line_end if line_end > 0 else len(text)]
    for a_rel, a_label, a_literal, a_ctx in ALLOWED_CITATIONS:
        if a_rel == rel and a_label == label and m.group(0) == a_literal and a_ctx in line:
            return True
    return False


def main() -> int:
    findings: list[str] = []
    n_files = 0
    for path in sorted(TOOL_DIR.rglob("*")):
        if not path.is_file() or path.resolve() == SELF:
            continue
        # Byte-code caches are gitignored, so they can never be a committed binary -- but they are
        # undecodable, and the validation block in README.md runs test suites before this gate, so
        # a second run used to fail on litter the first run created. Skipping them cannot hide a
        # real binary; that check still applies to every other file.
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"binary-file\t{path.relative_to(TOOL_DIR)}")
            continue
        n_files += 1
        rel = path.relative_to(TOOL_DIR).as_posix()
        norm, mp = normalise(text)
        for label, pat in FORBIDDEN:
            for m in pat.finditer(norm):
                if allowed(label, rel, text, mp, m):
                    continue
                a = mp[m.start()]
                b = mp[m.end() - 1] + 1
                ctx = text[max(0, a - 40):b + 40].replace("\n", " ")
                findings.append(f"{label}\t{rel}\t…{ctx}…")

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
