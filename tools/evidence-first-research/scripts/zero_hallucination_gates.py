#!/usr/bin/env python3
"""Executable zero-hallucination gates for hard-to-reach evidence.

Prose rules decay; a command does not. Each gate here returns a verdict a reviewer can
re-run, so an absence finding ("the document does not mention X") is a measurement
rather than an impression.

Gates
-----
1  source_integrity   A zero keyword count is meaningless until the source is real text.
                      Undecompressed gzip and image-only PDF scans both read near-zero.
2  positive_control   Before reporting any zero, prove the checker can find one item
                      that is definitely present. A checker that finds nothing cannot
                      tell "absent" from "looked in the wrong place".
3  version_marker     Flag a citation whose article number may come from a draft rather
                      than the enacted text (drafts renumber silently).
4  context_window     Print +-N chars around every hit a number will be quoted from.
5  identifier_forms   Decide "missing citation" only on full identifier forms, never on
                      a bare number that collides with unrelated data.
6  file_is_filetype   A file is what its bytes say, not what its extension says. HTML
                      error pages and landing pages routinely land on disk as .pdf.

Usage
-----
    python3 zero_hallucination_gates.py --self-test     # prove every gate can FAIL
    python3 zero_hallucination_gates.py FILE [FILE...]  # gate 1 + 6 over evidence files

Library use: import the functions; every one returns a dict with an explicit "pass" key
and the measurements behind it, so a caller can assert rather than eyeball.

Self-test discipline: a gate that has never been observed failing is not a gate. Each
fixture below is a real failure shape taken from a session where the gate was needed.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# Thresholds chosen from measured Vietnamese legal and journal text: full texts ran
# 0.227-0.243 diacritic ratio and 26k-75k characters, while a gzip payload measured
# 0.007 and an image-only PDF scan 164 characters over 24 pages.
MIN_CHARS = 5000
MIN_DIACRITIC_RATIO = 0.03
MIN_DIACRITIC_LENIENT = 0.015  # for non-Vietnamese or lightly diacritised sources

SUMMARY_LINE = "Executable zero-hallucination gates for hard-to-reach evidence."

PDF_MAGIC = b"%PDF"
HTML_MARKERS = (b"<!DOCTYPE html", b"<html", b"403 Forbidden", b"<head>")
MIN_PLAUSIBLE_PAPER_BYTES = 40_000  # a 1-4 KB ".pdf" is a page, never an article


def _combine(text: str) -> int:
    """Count combining marks (Vietnamese tone/accent marks) via NFD decomposition."""
    return sum(1 for ch in unicodedata.normalize("NFD", text) if unicodedata.combining(ch))


def diacritic_ratio(text: str) -> float:
    return _combine(text) / max(len(text), 1)


# --------------------------------------------------------------------------- gate 1
def source_integrity(
    path: str | Path,
    text: str | None = None,
    *,
    min_chars: int = MIN_CHARS,
    min_diacritic: float = MIN_DIACRITIC_RATIO,
    markers: tuple[str, ...] = (),
) -> dict:
    """Decide whether a source is readable text at all, BEFORE any keyword is counted.

    `text` lets a caller pass already-extracted content (e.g. from a PDF); otherwise the
    file is read as UTF-8. Failures here mean "do not report counts", not "topic absent".
    """
    p = Path(path)
    if text is None:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:  # unreadable is a verdict, not an exception
            return {"gate": 1, "pass": False, "reason": f"unreadable: {exc}", "chars": 0}

    chars = len(text)
    ratio = diacritic_ratio(text)
    missing = [m for m in markers if text.count(m) == 0]
    reasons = []
    if chars < min_chars:
        reasons.append(f"only {chars:,} chars (< {min_chars:,}): not full text, or a scan "
                       "with no text layer, or an HTML shell")
    if ratio < min_diacritic:
        reasons.append(f"diacritic ratio {ratio:.3f} < {min_diacritic}: compressed bytes, "
                       "wrong encoding, or a language this threshold does not fit")
    if missing:
        reasons.append(f"structural markers absent: {missing}")
    return {
        "gate": 1, "pass": not reasons, "file": p.name, "chars": chars,
        "diacritic_ratio": round(ratio, 4), "reasons": reasons,
    }


# --------------------------------------------------------------------------- gate 2
def positive_control(text: str, must_contain: list[str], *, case_sensitive: bool = False) -> dict:
    """Prove the checker can see something known-present before trusting any zero.

    `case_sensitive=False` by default because a measured failure probed for a personal
    name in mixed case while the document printed it in capitals on the masthead.
    """
    hay = text if case_sensitive else unicodedata.normalize("NFC", text).lower()
    found, absent = {}, []
    for probe in must_contain:
        needle = probe if case_sensitive else probe.lower()
        n = hay.count(needle)
        found[probe] = n
        if n == 0:
            absent.append(probe)
    return {
        "gate": 2, "pass": not absent, "found": found, "absent": absent,
        "reason": ("checker sees every control item" if not absent else
                   f"controls NOT found {absent} -> the checker is broken, not the corpus; "
                   "fix it before counting anything else"),
    }


# --------------------------------------------------------------------------- gate 3
def version_marker(citation: str, enacted_evidence: str | None) -> dict:
    """Require an article/clause number to come from the promulgated text.

    A draft's article 13 can become the enacted text's article 12 with the rule itself
    changed. If `enacted_evidence` is None, the citation may only be used without a
    clause number.
    """
    has_clause = bool(re.search(r"(?:Điều|Article|khoản|clause|§)\s*\d", citation))
    if not has_clause:
        return {"gate": 3, "pass": True, "reason": "no clause number cited", "clause": False}
    if enacted_evidence:
        return {"gate": 3, "pass": True, "reason": "clause number backed by enacted text",
                "clause": True}
    return {"gate": 3, "pass": False, "clause": True,
            "reason": "clause number cited with no enacted-version evidence; drafts renumber. "
                      "Cite the clause only from the signed/promulgated text."}


# --------------------------------------------------------------------------- gate 4
def context_window(text: str, keyword: str, span: int = 150, limit: int = 8) -> dict:
    """Print the context of every hit a number will be quoted from.

    A count is a candidate. Substring traps are common: a two-word term can appear inside
    a longer phrase with a different meaning, so the count alone misrepresents the source.
    """
    hits = [m for m in re.finditer(re.escape(keyword), text, re.I)]
    out = []
    for m in hits[:limit]:
        a, b = max(0, m.start() - span), min(len(text), m.end() + span)
        out.append(re.sub(r"\s+", " ", text[a:b]).strip())
    return {"gate": 4, "pass": True, "keyword": keyword, "total": len(hits),
            "shown": len(out), "contexts": out}


# --------------------------------------------------------------------------- gate 5
def identifier_forms(manuscript: str, forms: list[str]) -> dict:
    """Decide "citation missing" only on full identifier forms.

    Searching a bare number collides with unrelated data: a split identifier matched a
    word-count datum in the body and reported the document as already cited.
    """
    if not forms:
        return {"gate": 5, "pass": False, "matched": [], "reason": "no identifier forms given"}
    matched = [f for f in forms if f in manuscript]
    return {
        "gate": 5, "pass": bool(matched), "matched": matched, "tried": forms,
        "reason": ("already cited" if matched else
                   "NOT cited on any full form -> a real gap claim, safe to report"),
    }


# --------------------------------------------------------------------------- gate 6
def file_is_filetype(path: str | Path) -> dict:
    """A file is what its bytes say, not what its extension says.

    Measured: three .pdf files of 1.2-4.0 KB were HTML - one a 403 page, two article
    landing pages. They survived several review rounds as "downloaded sources".
    """
    p = Path(path)
    if not p.exists():
        return {"gate": 6, "pass": False, "file": p.name, "reason": "missing"}
    head = p.open("rb").read(512)
    size = p.stat().st_size
    ext = p.suffix.lower()
    is_html = any(m.lower() in head.lower() for m in HTML_MARKERS)
    problems = []
    if ext == ".pdf":
        if not head.startswith(PDF_MAGIC):
            problems.append("extension .pdf but bytes are not PDF"
                            + (" (HTML error/landing page)" if is_html else ""))
        elif size < MIN_PLAUSIBLE_PAPER_BYTES:
            problems.append(f"only {size:,} bytes - too small for an article")
    elif is_html and ext not in (".html", ".htm"):
        problems.append(f"HTML content saved as {ext}")
    return {"gate": 6, "pass": not problems, "file": p.name, "bytes": size,
            "reasons": problems}


# ---------------------------------------------------------- scan detection (gate 1 aid)
def scan_without_text_layer(page_count: int, extracted_chars: int) -> dict:
    """Distinguish "empty document" from "image-only scan".

    A genuine 11 MB signed PDF yielded 164 characters over 24 pages. The fix is to render
    pages to images and OCR them, not to conclude the document says nothing.
    """
    per_page = extracted_chars / max(page_count, 1)
    is_scan = page_count > 0 and per_page < 200
    return {
        "gate": "1a", "pass": not is_scan, "pages": page_count,
        "chars_per_page": round(per_page, 1), "scan": is_scan,
        "action": ("render pages to PNG (dpi>=170) and OCR them; locate the target page "
                   "first by mapping clause offsets from a readable secondary copy"
                   if is_scan else "text layer present"),
    }


# ------------------------------------------------------------------------- read status
READ_STATUSES = ("READ-IN-FULL", "METADATA-ONLY", "ABSTRACT-ONLY", "UNREADABLE")


def read_status(status: str, carries_number: bool, carries_quote: bool) -> dict:
    """Only READ-IN-FULL may carry a statistic or a quotation."""
    s = status.strip().upper()
    if s not in READ_STATUSES:
        return {"gate": 7, "pass": False, "reason": f"unknown read-status {status!r}"}
    if s != "READ-IN-FULL" and (carries_number or carries_quote):
        return {"gate": 7, "pass": False, "status": s,
                "reason": f"{s} citation carries a number/quote; drop the specific hook and "
                          "let the sentence stand as a general statement, or obtain full text"}
    return {"gate": 7, "pass": True, "status": s}


# -------------------------------------------------------------------------- self-test
def _self_test() -> int:
    """Every gate must be observed FAILING on a real failure shape. Mutation discipline:
    a gate that cannot go red is decoration."""
    failures: list[str] = []
    checks = 0

    def expect(cond: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(label)

    # gate 1 -- gzip-looking payload: short + no diacritics
    gz = "\x1f\x8b\x08\x00" * 400
    r = source_integrity("fake.bin", gz)
    expect(r["pass"] is False, "gate1 must FAIL on compressed bytes")
    expect(r["diacritic_ratio"] < MIN_DIACRITIC_RATIO, "gate1 ratio must be near zero")
    # gate 1 -- real Vietnamese full text passes
    real = ("Điều 12. Đánh giá và tính điểm học phần. " * 400) + "ăâêôơưđ" * 300
    expect(source_integrity("ok.txt", real)["pass"] is True, "gate1 must PASS on full text")

    # gate 2 -- control absent means broken checker (name printed in capitals)
    doc = "PHAN TRUNG HIỀN và NGUYỄN DƯƠNG ANH THẮNG, đào tạo luật đa ngành."
    expect(positive_control(doc, ["Hiền"])["pass"] is True,
           "gate2 must PASS case-insensitively")
    expect(positive_control(doc, ["Hiền"], case_sensitive=True)["pass"] is False,
           "gate2 must FAIL when the probe misses the printed surface form")

    # gate 3 -- clause number without enacted evidence
    expect(version_marker("(Bộ, 2026, Điều 12 khoản 6)", None)["pass"] is False,
           "gate3 must FAIL on a clause number with no enacted text")
    expect(version_marker("(Bộ, 2026, Điều 12 khoản 6)", "signed PDF p11")["pass"] is True,
           "gate3 must PASS when backed by the promulgated text")
    expect(version_marker("(Bộ, 2026)", None)["pass"] is True,
           "gate3 must PASS when no clause is cited")

    # gate 4 -- substring trap is visible only with context
    trap = "chuyển đổi số lượng chứng chỉ" + " x" * 400
    cw = context_window(trap, "chuyển đổi số")
    expect(cw["total"] == 1 and "lượng chứng chỉ" in cw["contexts"][0],
           "gate4 must expose the substring trap in context")

    # gate 5 -- bare number collides, full forms do not
    ms = "dài nhất 56 từ. Không có văn bản nào khác."
    expect(identifier_forms(ms, ["56"])["pass"] is True,
           "bare-number search produces a FALSE 'already cited'")
    expect(identifier_forms(ms, ["56/2026", "Thông tư 56", "Thông tư số 56"])["pass"] is False,
           "gate5 must report a real gap on full forms")

    # gate 6 -- HTML saved as .pdf
    html = Path("/tmp/_zhg_fixture.html_as_pdf.pdf")
    html.write_bytes(b"<!DOCTYPE html>\n<html><title>403 Forbidden</title>")
    expect(file_is_filetype(html)["pass"] is False, "gate6 must FAIL on HTML-as-PDF")
    tiny = Path("/tmp/_zhg_fixture_tiny.pdf")
    tiny.write_bytes(PDF_MAGIC + b"-1.5\n" + b"0" * 100)
    expect(file_is_filetype(tiny)["pass"] is False, "gate6 must FAIL on an undersized PDF")
    ok = Path("/tmp/_zhg_fixture_ok.pdf")
    ok.write_bytes(PDF_MAGIC + b"-1.5\n" + b"0" * (MIN_PLAUSIBLE_PAPER_BYTES + 10))
    expect(file_is_filetype(ok)["pass"] is True, "gate6 must PASS on a plausible PDF")
    for f in (html, tiny, ok):
        f.unlink(missing_ok=True)

    # gate 1a -- image-only scan
    sc = scan_without_text_layer(24, 164)
    expect(sc["scan"] is True and sc["pass"] is False, "gate1a must flag an image-only scan")
    expect("OCR" in sc["action"], "gate1a must say what to do instead of concluding 'empty'")
    expect(scan_without_text_layer(24, 60_000)["scan"] is False,
           "gate1a must PASS on a real text layer")

    # gate 7 -- metadata-only citation carrying a number
    expect(read_status("METADATA-ONLY", True, False)["pass"] is False,
           "gate7 must FAIL when a metadata-only citation carries a number")
    expect(read_status("READ-IN-FULL", True, True)["pass"] is True,
           "gate7 must PASS for a fully read source")
    expect(read_status("GUESS", False, False)["pass"] is False,
           "gate7 must reject an unknown status")

    print(f"zero-hallucination gates self-test: {checks - len(failures)}/{checks} assertions passed")
    for f in failures:
        print(f"  FAIL {f}")
    return 1 if failures else 0


def _verdict(res: dict) -> str:
    """One-line PASS/FAIL for a gate result, whatever shape its failure field has."""
    if res.get("pass"):
        return "PASS"
    parts = res.get("reasons") or []
    if not parts and res.get("reason"):
        parts = [str(res["reason"])]
    return "FAIL " + "; ".join(str(x) for x in parts)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=SUMMARY_LINE)
    ap.add_argument("files", nargs="*", help="evidence files to run gates 1 and 6 over")
    ap.add_argument("--self-test", action="store_true", help="prove every gate can fail")
    ap.add_argument("--min-chars", type=int, default=MIN_CHARS)
    ap.add_argument("--min-diacritic", type=float, default=MIN_DIACRITIC_RATIO)
    ap.add_argument("--markers", default="", help="comma-separated structural markers")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()
    if not args.files:
        ap.error("pass evidence files, or --self-test")

    markers = tuple(m for m in (x.strip() for x in args.markers.split(",")) if m)
    bad = 0
    for f in args.files:
        g6 = file_is_filetype(f)
        p = Path(f)
        text = None
        if p.suffix.lower() == ".pdf":
            try:
                import fitz  # type: ignore

                d = fitz.open(str(p))
                text = "\n".join(pg.get_text() for pg in d)
                sc = scan_without_text_layer(d.page_count, len(text))
                print(f"[{sc['gate']}] {p.name}: {sc['pages']} pages, "
                      f"{sc['chars_per_page']} chars/page -> "
                      f"{'SCAN, needs OCR' if sc['scan'] else 'text layer OK'}")
                if sc["scan"]:
                    bad += 1
                    continue
            except ImportError:
                print(f"[--] {p.name}: PyMuPDF not installed; PDF text not extracted")
        g1 = source_integrity(f, text, min_chars=args.min_chars,
                              min_diacritic=args.min_diacritic, markers=markers)
        print(f"[6] {p.name}: {_verdict(g6)}")
        print(f"[1] {p.name}: {_verdict(g1)} "
              f"({g1['chars']:,} chars, diacritic {float(g1.get('diacritic_ratio', 0.0)):.3f})")
        if not (g6["pass"] and g1["pass"]):
            bad += 1
    print(f"\n{len(args.files) - bad}/{len(args.files)} files usable as evidence")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
