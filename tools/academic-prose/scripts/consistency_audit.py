#!/usr/bin/env python3
"""Cross-artifact consistency audit for bilingual academic manuscripts.

Variant-pair counting (the terminology audit) sees one direction of drift: many
names for one concept. Three other directions are invisible to it and to every
prose scanner, and each one has produced a defect that survived a clean build,
a clean citation check, and an independent peer review:

  REFERENT_COLLISION  one name, several referents (the same label used for two
                      different populations or artifacts)
  FORMAT_ZONE         one quantity, two surface conventions across language
                      zones (decimal comma in one language, decimal point in the
                      other, applied to the wrong zone)
  SELF_COUNT          a claim about the manuscript's own contents that the
                      artifact contradicts ("seven checks" above a six-row table)

Plus four mechanical checks that the same rounds also needed: hardcoded
cross-references, abbreviation-before-definition, bilingual keyword parity, and
caption terminal punctuation.

A finding is a candidate for human adjudication, never an automatic rewrite:
`REFERENT_COLLISION` reports co-occurring quantities so a reader can decide
whether the label really names two things, and `SELF_COUNT` compares a number
word against the nearest table's row count, which the author may legitimately
have phrased loosely.

Report only. Exit: 0 no candidate, 2 candidates present, 3 input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Language zones
# --------------------------------------------------------------------------

VI_CHARS = set(
    "ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ"
    "ĂÂĐÊÔƠƯÀẢÃÁẠẰẲẴẮẶẦẨẪẤẬÈẺẼÉẸỀỂỄẾỆÌỈĨÍỊÒỎÕÓỌỒỔỖỐỘỜỞỠỚỢÙỦŨÚỤỪỬỮỨỰỲỶỸÝỴ"
)


def language_of(text: str) -> str:
    """Classify a zone by Vietnamese diacritic density, not by declaration."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "unknown"
    vi = sum(1 for c in letters if c in VI_CHARS)
    return "vi" if vi / len(letters) > 0.02 else "en"


ABSTRACT_RE = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.S)
TEXTTT_RE = re.compile(r"\\texttt\{[^}]*\}")
CITE_RE = re.compile(r"\\cite\{[^}]*\}")
URL_RE = re.compile(r"\\url\{[^}]*\}")
LABEL_RE = re.compile(r"\\label\{[^}]*\}")
REF_RE = re.compile(r"\\ref\{[^}]*\}")

THOUSANDS = re.compile(r"(?<![\d.,])\d{1,3}([.,])\d{3}(?!\d)")
DECIMAL = re.compile(r"(?<![\d.,])\d+([.,])\d+(?!\d)")


def _strip_markup(text: str) -> str:
    text = TEXTTT_RE.sub(" ", text)
    text = CITE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = LABEL_RE.sub(" ", text)
    text = REF_RE.sub(" ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", text)
    return text.replace("{", " ").replace("}", " ")


def decimal_separators(text: str) -> list[str]:
    """Separator characters actually used as decimal marks (thousands excluded)."""
    masked = THOUSANDS.sub(" ", text)
    return [m.group(1) for m in DECIMAL.finditer(masked)]


# --------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------


def finding(cls: str, where: str, detail: str, span: str = "") -> dict:
    return {"class": cls, "where": where, "detail": detail, "span": span.strip()}


def check_format_zones(source: str) -> list[dict]:
    """A decimal convention that belongs to the other language zone."""
    out: list[dict] = []
    blocks = ABSTRACT_RE.findall(source)
    for i, block in enumerate(blocks, 1):
        plain = _strip_markup(block)
        zone = language_of(plain)
        seps = decimal_separators(plain)
        if not seps:
            continue
        if zone == "vi" and "." in seps:
            out.append(
                finding(
                    "FORMAT_ZONE",
                    f"abstract block {i} (vi)",
                    "Vietnamese zone uses a decimal point; Vietnamese convention is the comma",
                    " ".join(sorted({s for s in seps if s == "."})) + " -> " + str(len(seps)) + " decimals",
                )
            )
        if zone == "en" and "," in seps:
            out.append(
                finding(
                    "FORMAT_ZONE",
                    f"abstract block {i} (en)",
                    "English zone uses a decimal comma; English convention is the point",
                    str(len([s for s in seps if s == ","])) + " comma decimals",
                )
            )
    return out


# Vietnamese number words, including the ones that open a count claim.
NUMBER_WORDS = {
    "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6,
    "bảy": 7, "tám": 8, "chín": 9, "mười": 10,
}
# Only classifiers whose count can plausibly equal a table's data-row count.
# Deliberately excluded: mô hình, lượt, điều kiện, tập, giai đoạn — a sentence
# saying "four models" is not a claim about how many rows a nearby table has,
# and including them made the check fire 23 times on a clean manuscript.
CLASSIFIERS = ("phép", "bước", "mục", "tiêu chí", "hàng", "dòng")
COUNT_CLAIM = re.compile(
    r"\b(" + "|".join(NUMBER_WORDS) + r")\s+(" + "|".join(CLASSIFIERS) + r")\b",
    re.I,
)

# A count claim belongs to a table only when the counted noun appears in that
# table's own caption or header row. Proximity alone is not evidence: a sentence
# saying "five steps" sitting above a six-row results table is not a defect.
# Tolerance is therefore zero — an off-by-one IS the defect this check exists for.
MAX_CLAIM_TABLE_DISTANCE = 1200
MAX_ROW_DELTA = 0

TABULAR_RE = re.compile(r"\\begin\{tabular[x]?\}(.*?)\\end\{tabular[x]?\}", re.S)
CAPTION_BEFORE = re.compile(r"\\caption\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")


def tabular_rows(body: str) -> int:
    """Data rows: '&' rows after the rule that closes the header."""
    cut = max(body.rfind("\\midrule"), body.rfind("\\toprule"))
    region = body[cut:] if cut != -1 else body
    region = region.split("\\bottomrule")[0]
    # Drop the leading rule tokens before splitting: the first chunk otherwise
    # still contains `\midrule`, which the row filter would discard, silently
    # losing row 1 and making every count one short.
    region = re.sub(r"\\(?:toprule|midrule|bottomrule|hline)", " ", region)
    rows = 0
    for chunk in region.split("\\\\"):
        if "&" in chunk and _strip_markup(chunk).strip():
            rows += 1
    return rows


def table_context(source: str, start: int, body: str) -> str:
    """Caption plus header row — what the table says it is counting."""
    header = body.split("\\midrule")[0] if "\\midrule" in body else ""
    caps = CAPTION_BEFORE.findall(source[max(0, start - 800): start])
    return _strip_markup((caps[-1] if caps else "") + " " + header).lower()


def check_self_count(source: str) -> list[dict]:
    """A number word followed by a classifier, checked against the next table.

    Two guards keep this from firing on every sentence. The claim must sit near
    its table, and the counted noun must appear in that table's caption or header
    row — otherwise the table was never describing the counted object, and "five
    steps" above a six-row results table is not a defect.
    """
    out: list[dict] = []
    tables = [
        (m.start(), tabular_rows(m.group(1)), table_context(source, m.start(), m.group(1)))
        for m in TABULAR_RE.finditer(source)
    ]
    if not tables:
        return out
    for m in COUNT_CLAIM.finditer(source):
        claimed = NUMBER_WORDS[m.group(1).lower()]
        noun = m.group(2).lower()
        after = [(pos, rows, ctx) for pos, rows, ctx in tables if pos > m.end()]
        if not after:
            continue
        pos, rows, ctx = after[0]
        if pos - m.end() > MAX_CLAIM_TABLE_DISTANCE:
            continue
        if noun not in ctx:
            continue
        if rows and abs(rows - claimed) <= MAX_ROW_DELTA:
            continue
        if rows and rows != claimed:
            line = source[: m.start()].count("\n") + 1
            out.append(
                finding(
                    "SELF_COUNT",
                    f"line {line}",
                    f"prose says {m.group(1)} {m.group(2)} ({claimed}); "
                    f"the table it introduces has {rows} data rows",
                    " ".join(m.group(0).split()),
                )
            )
    return out


CROSSREF_HARDCODE = re.compile(
    r"(?<!\\ref\{)(?<!\\eqref\{)\b(Mục|Bảng|Hình|Chương|Phần|Section|Table|Figure|Eq\.)\s*~?\s*(\d+)\b"
)


def check_crossrefs(source: str) -> list[dict]:
    out: list[dict] = []
    for m in CROSSREF_HARDCODE.finditer(source):
        line = source[: m.start()].count("\n") + 1
        out.append(
            finding(
                "CROSSREF_HARDCODE",
                f"line {line}",
                "typed number instead of a generated reference; renumbering will desynchronise it",
                " ".join(m.group(0).split()),
            )
        )
    return out


BIBLIO_RE = re.compile(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.S)
ABBREV_RE = re.compile(r"(?<![\w-])([A-ZĐ]{2,6})(?![\w-])")
# The only reliable evidence that a token is an abbreviation rather than a name
# or a unit is that the document itself supplies the full form, in the
# conventional `full form (ACR)` shape. Guessing the expansion from initials
# produced two failures in measurement: it missed the real case and it invented
# one for `GB` out of an accidental two-word match. Require the definition.
DEFINITION_RE = re.compile(r"\(\s*([A-ZĐ]{2,6})\s*\)")


def check_abbrev(source: str) -> list[dict]:
    """An abbreviation used before the document supplies its full form.

    Only reports when the document does define the token, so the finding is
    `use-before-definition` — a defect with an obvious fix — and never
    `name used without expansion`, which is not a defect at all. Units and
    proper names have no `(...)` definition and are therefore out of scope.
    """
    out: list[dict] = []
    masked = BIBLIO_RE.sub(lambda m: " " * len(m.group(0)), source)
    plain = _strip_markup(masked)
    for token in sorted({m.group(1) for m in DEFINITION_RE.finditer(plain)}):
        definition_sites = [m.start() for m in DEFINITION_RE.finditer(plain) if m.group(1) == token]
        uses = [m.start() for m in re.finditer(rf"(?<![\w-]){re.escape(token)}(?![\w-])", plain)]
        if len(uses) < 2:
            continue
        first_definition = min(definition_sites)
        earlier = [u for u in uses if u < first_definition]
        if not earlier:
            continue
        line = source[: earlier[0]].count("\n") + 1
        out.append(
            finding(
                "ABBREV_LATE",
                f"line {line}",
                f"`{token}` appears at {len(earlier)} site(s) before the document defines it; "
                "move the definition to first use",
                token,
            )
        )
    return out


KEYWORD_BLOCK = re.compile(r"\\textbf\{(Từ khóa|Keywords)\s*:\}\s*(.+?)\n", re.S)


def check_keywords(source: str) -> list[dict]:
    blocks = KEYWORD_BLOCK.findall(source)
    if len(blocks) < 2:
        return []
    lists = []
    for name, body in blocks:
        items = [x.strip().rstrip(".") for x in re.split(r";", _strip_markup(body)) if x.strip()]
        lists.append((name, items))
    out: list[dict] = []
    counts = {name: len(items) for name, items in lists}
    if len(set(counts.values())) > 1:
        out.append(
            finding(
                "KEYWORD_PARITY",
                "keyword blocks",
                "bilingual lists differ in length: "
                + ", ".join(f"{k}={v}" for k, v in counts.items()),
                " | ".join(items[0] for _, items in lists),
            )
        )
    return out


CAPTION_RE = re.compile(r"\\caption\{")
MATH_SPLIT = re.compile(r"\$[^$]*\$")


def check_captions(source: str) -> list[dict]:
    out: list[dict] = []
    for m in CAPTION_RE.finditer(source):
        depth, i = 1, m.end()
        while i < len(source) and depth:
            if source[i] == "{":
                depth += 1
            elif source[i] == "}":
                depth -= 1
            i += 1
        cap = source[m.end(): i - 1].rstrip()
        if not cap:
            continue
        # A caption ending in a formula or an abbreviation dot is legitimate.
        tail = MATH_SPLIT.sub("X", cap).rstrip()
        if tail and tail[-1] not in ".!?":
            line = source[: m.start()].count("\n") + 1
            out.append(
                finding(
                    "CAPTION_TERMINAL",
                    f"line {line}",
                    "caption does not end a sentence; uniform captions read as one edited artifact",
                    tail[-60:],
                )
            )
    return out


CLAUSE_BREAK = re.compile(r"\n|&|\\\\|(?<!\d)\.\s|;\s|:\s")


def check_referent_collision(source: str, terms: list[str], window: int = 60) -> list[dict]:
    """One label, several quantities it governs in its own clause -> candidate.

    Semantics cannot be automated, but the *shape* of a referent collision can:
    a label and its quantity sit adjacent in one clause, and the collision
    appears as the same label taking different quantities across sites.

    Two guards, both measured on a clean manuscript that the earlier versions
    flagged:

    - **Direction.** A label governs the quantity that follows it. Collecting
      every number within ±200 characters reported 12 quantities for one label,
      because neighbouring sentences and table cells have numbers of their own.
    - **Clause boundary.** The quantity must be in the same clause. Without this,
      `bản phát hành cuối. Từ 5.975 ngữ cảnh ...` attributed 5.975 to the release
      and a table row on the next line attributed 16.158 to it as well — two
      false quantities around the one true value.
    """
    out: list[dict] = []
    plain = _strip_markup(source)
    # Whole quantities only: the lookarounds stop `0,025` from yielding `025`
    # and stop a decimal from being read as a thousands group.
    qty_re = re.compile(r"(?<![\d.,])(?:\d{1,3}(?:\.\d{3})+|\d{3,})(?![\d.,])")
    for term in terms:
        # Case-insensitive: a Vietnamese term opens a sentence with a capital and
        # appears mid-sentence in lower case, and matching case-sensitively
        # silently drops the sentence-initial occurrence — often the only one
        # that carries the first quantity.
        hits = [m.start() for m in re.finditer(re.escape(term), plain, re.I)]
        if len(hits) < 2:
            continue
        seen: dict[str, str] = {}
        for pos in hits:
            tail = plain[pos + len(term): pos + len(term) + window]
            clause = CLAUSE_BREAK.split(tail)[0]
            m = qty_re.search(clause)
            if not m:
                continue
            seen.setdefault(m.group(0), clause.strip()[:110])
        if len(seen) < 2:
            continue
        out.append(
            finding(
                "REFERENT_COLLISION",
                f"term `{term}`",
                "same label governs "
                + str(len(seen))
                + " different quantities: "
                + ", ".join(sorted(seen)[:6])
                + " -- confirm they name one referent",
                " || ".join(seen[k] for k in sorted(seen)[:2]),
            )
        )
    return out


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------


def scan(source: str, terms: list[str] | None = None) -> dict:
    findings: list[dict] = []
    findings += check_format_zones(source)
    findings += check_self_count(source)
    findings += check_crossrefs(source)
    findings += check_abbrev(source)
    findings += check_keywords(source)
    findings += check_captions(source)
    if terms:
        findings += check_referent_collision(source, terms)
    order = [
        "REFERENT_COLLISION", "FORMAT_ZONE", "SELF_COUNT", "CROSSREF_HARDCODE",
        "ABBREV_LATE", "KEYWORD_PARITY", "CAPTION_TERMINAL",
    ]
    findings.sort(key=lambda f: (order.index(f["class"]), f["where"]))
    return {
        "findings": findings,
        "counts": {c: sum(1 for f in findings if f["class"] == c) for c in order},
        "note": (
            "Candidates only. FORMAT_ZONE and CAPTION_TERMINAL are near-deterministic; "
            "SELF_COUNT, CROSSREF_HARDCODE and ABBREV_LATE need the artifact in front of you; "
            "REFERENT_COLLISION is a prompt to compare referents, not a verdict. "
            "A clean report is a partial verification: the plain-reader pass still governs."
        ),
        "exit_code": 2 if findings else 0,
    }


def render_report(result: dict, path: str) -> str:
    lines = [f"# Consistency audit — {path}", ""]
    lines.append(f"- findings: {len(result['findings'])}")
    for cls, n in result["counts"].items():
        if n:
            lines.append(f"- {cls}: {n}")
    lines.append("")
    if not result["findings"]:
        lines.append("No mechanical candidate. The manual referent and plain-reader passes are still required.")
    for f in result["findings"]:
        lines.append(f"- **{f['class']}** {f['where']} — {f['detail']}")
        if f["span"]:
            lines.append(f"  > {f['span']}")
    lines += ["", f"> {result['note']}"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--terms", default="", help="comma-separated labels to test for referent collision")
    ap.add_argument("--json", dest="json_path", type=Path)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    try:
        source = args.input.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 3
    terms = [t.strip() for t in args.terms.split(",") if t.strip()]
    result = scan(source, terms)
    if args.json_path:
        args.json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.report:
        args.report.write_text(render_report(result, str(args.input)), encoding="utf-8")
    if not args.quiet:
        print(render_report(result, str(args.input)))
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
