#!/usr/bin/env python3
"""Measure prose style dimensions as RATES against registry thresholds.

The candidate scanners (vi_ai_pattern_scan, academic_discourse_scan,
process_logic_scan, veracity_protestation_scan, internal_register_scan,
consistency_audit) match lexical patterns and report per-occurrence findings.
A tell used at a high *rate* is invisible to all of them: measured on a 10-page
bilingual manuscript, six gates returned 5 findings while 34 explanatory colons
sat in 6,326 words -- 5.4x the registry ceiling. No gate was wrong; none of them
divides.

This script divides. It measures, it does not adjudicate: a value above a
threshold is a candidate for the manual pass, and a clean value is a partial
verification only.

Every threshold is quoted from the registries in this skill
(references/ai-pattern-vietnamese.md, the two language standards); none is
invented here. The rate metrics are language-neutral; the lexical metrics
(`d\u01b0\u1ee3c`, `s\u1ef1`, `vi\u1ec7c`, Vietnamese connectives) apply to Vietnamese prose.

Usage:
    python3 scripts/tex_prose_extract.py manuscript.tex > prose.txt
    python3 scripts/style_metrics.py prose.txt
    python3 scripts/style_metrics.py prose.txt --strict   # exit 1 on any FAIL

Input is extracted prose (see tex_prose_extract.py), not raw .tex: markup,
tabular rows and preamble inflate every rate here.
"""

import argparse
import re
import statistics
import sys
from collections import Counter

# ---------------------------------------------------------------- thresholds
COLON_PER_WORDS = 1000      # ai-pattern-vietnamese.md section 2b: <= 1 per 1000 words
DUOC_PER_WORDS = 19.2       # ai-pattern-vietnamese.md section 7: measured defect level
CV_MACHINE_RHYTHM = 0.35    # below this, sentence lengths are too uniform
LONG_SENTENCE = 40          # words; clause overload review threshold
VERY_LONG_SENTENCE = 60
REPEATED_OPENING_MIN = 3

LABEL_BEFORE_COLON = re.compile(
    r"(T\u1eeb kh\u00f3a|Keywords|T\u00f3m t\u1eaft|Abstract|B\u1ea3ng|H\u00ecnh|Figure|Table|"
    r"B\u01b0\u1edbc|Giai \u0111o\u1ea1n|Step)\s*$"
)


def words(text):
    return re.findall(r"\S+", text)


def split_captions(raw):
    """Separate float captions from body prose.

    The registry sets different limits for each (explanatory colons: <=1/1000 in
    body, zero in captions), so they cannot share one denominator.
    """
    body, caps = [], []
    for line in raw.split("\n"):
        (caps if line.startswith("[caption]") else body).append(line)
    return "\n".join(body), "\n".join(caps)


def count_explanatory_colons(text):
    """Colons that introduce an explanation, excluding labels, ratios and URLs."""
    n = 0
    for m in re.finditer(r":", text):
        pre = text[max(0, m.start() - 24):m.start()]
        post = text[m.end():m.end() + 20]
        if LABEL_BEFORE_COLON.search(pre):
            continue
        if re.search(r"\d\s*$", pre) and re.search(r"^\s*\d", post):
            continue          # 10:1, 3:2 -- ratio, not prose punctuation
        if re.search(r"https?$|/$|www\.\S*$", pre):
            continue
        n += 1
    return n


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in parts if len(words(s)) >= 4]


def paragraphs(text):
    parts = re.split(r"\n\s*\n", text)
    return [p.strip() for p in parts if len(words(p)) >= 15]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="extracted prose file")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when a hard threshold fails")
    args = ap.parse_args()

    raw = open(args.input, encoding="utf8").read()
    body, caps = split_captions(raw)
    W = words(body)
    n = len(W)
    if n < 200:
        print(f"REFUSING: only {n} words. Extract prose first "
              f"(scripts/tex_prose_extract.py), do not scan raw .tex.", file=sys.stderr)
        return 2

    fails = []

    def line(label, value, verdict):
        print(f"  {label:<34} {value:<22} {verdict}")

    print("=" * 78)
    print(f"BODY {n} words | CAPTIONS {len(words(caps))} words")
    print("=" * 78)

    # 1. explanatory colons -- the strongest machine tell the gates cannot see
    cb = count_explanatory_colons(body)
    cc = count_explanatory_colons(caps)
    per = n / max(cb, 1)
    ok = per >= COLON_PER_WORDS
    print("\n[1] EXPLANATORY COLONS (<=1 per 1000 words body, 0 in captions)")
    line("body", f"{cb} (1 per {per:.0f} words)", "PASS" if ok else f"FAIL {COLON_PER_WORDS / per:.1f}x")
    line("captions", str(cc), "PASS" if cc == 0 else "FAIL")
    if not ok:
        fails.append("colons")
    if cc:
        fails.append("colons_caption")

    # 2. reasonless duoc -- report the rate, compare to the measured defect level
    duoc = len(re.findall(r"\b\u0111\u01b0\u1ee3c\b", body, re.I))
    rate = duoc / n * 1000
    print(f"\n[2] 'duoc' WITHOUT REASON (defect level {DUOC_PER_WORDS}/1000)")
    line("count / rate", f"{duoc} / {rate:.1f} per 1000", "PASS" if rate < DUOC_PER_WORDS else "REVIEW")

    # 3. nominalisation
    su = len(re.findall(r"\bs\u1ef1\s+\w+", body, re.I))
    viec = len(re.findall(r"\bvi\u1ec7c\s+\w+", body, re.I))
    print("\n[3] NOMINALISATION (report only)")
    line("'su + V'", f"{su} ({su / n * 1000:.1f}/1000)", "")
    line("'viec + V'", f"{viec} ({viec / n * 1000:.1f}/1000)", "")

    # 4. em dash in prose -- forbidden; en dash in ranges is notation, not prose
    em = body.count("\u2014")
    en = body.count("\u2013")
    print("\n[4] DASHES")
    line("em dash in prose", str(em), "PASS" if em == 0 else "FAIL")
    line("en dash (ranges)", str(en), "notation, keep")
    if em:
        fails.append("em_dash")

    # 5. sentence length distribution -- uniformity is the machine tell, not length
    ss = sentences(body)
    sl = [len(words(s)) for s in ss]
    mean, sd = statistics.mean(sl), statistics.pstdev(sl)
    cv = sd / mean
    over40 = sum(1 for x in sl if x > LONG_SENTENCE)
    over60 = sum(1 for x in sl if x > VERY_LONG_SENTENCE)
    print(f"\n[5] SENTENCE LENGTH ({len(ss)} sentences)")
    line("mean / median", f"{mean:.1f} / {statistics.median(sl):.0f}", f"max {max(sl)}")
    line("CV (machine rhythm < 0.35)", f"{cv:.2f}",
         "PASS natural" if cv >= CV_MACHINE_RHYTHM else "REVIEW uniform")
    line(f">{LONG_SENTENCE} words", f"{over40} ({over40 / len(ss) * 100:.1f}%)", "review clause overload")
    line(f">{VERY_LONG_SENTENCE} words", f"{over60}", "")

    # 6. paragraph length
    pp = paragraphs(body)
    pl = [len(words(p)) for p in pp]
    print(f"\n[6] PARAGRAPH LENGTH ({len(pp)} paragraphs)")
    line("mean / median", f"{statistics.mean(pl):.0f} / {statistics.median(pl):.0f}",
         f"min {min(pl)} max {max(pl)}")

    # 7. repeated sentence openings
    opens = [" ".join(words(s)[:2]).lower() for s in ss]
    rep = [(o, c) for o, c in Counter(opens).most_common(8) if c >= REPEATED_OPENING_MIN]
    print(f"\n[7] REPEATED OPENINGS (>={REPEATED_OPENING_MIN}x)")
    if rep:
        for o, c in rep:
            line(f"'{o}'", f"x{c}", "check: abstract-vs-body repetition is IMRaD, not duplication")
    else:
        print("  none")

    # 8. connective distribution -- the repair for colon density shows up here
    conn = ["v\u00ec", "do", "n\u00ean", "khi", "n\u1ebfu", "tuy", "nh\u01b0ng", "song", "v\u00e0",
            "ho\u1eb7c", "theo \u0111\u00f3", "c\u1ee5 th\u1ec3 l\u00e0", "g\u1ed3m", "b\u1edfi v\u1eady",
            "v\u00ec v\u1eady", "cho n\u00ean", "trong \u0111\u00f3"]
    counts = {c: len(re.findall(rf"\b{re.escape(c)}\b", body, re.I)) for c in conn}
    tot = sum(counts.values())
    print(f"\n[8] CONNECTIVES ({tot} = {tot / n * 1000:.1f}/1000)")
    print("  " + " | ".join(f"{k}={v}" for k, v in
                            sorted(counts.items(), key=lambda x: -x[1]) if v))

    # 9. hedge inventory -- must never reach zero (hedges are content)
    hedges = ["c\u00f3 th\u1ec3", "ch\u01b0a", "kh\u00f4ng", "ch\u1ec9", "kho\u1ea3ng", "\u01b0\u1edbc",
              "d\u01b0\u1eddng nh\u01b0", "ph\u1ea7n n\u00e0o", "t\u01b0\u01a1ng \u0111\u1ed1i", "g\u1ea7n",
              "x\u1ea5p x\u1ec9", "\u00edt nh\u1ea5t", "t\u1ed1i \u0111a"]
    h = {x: len(re.findall(rf"\b{re.escape(x)}\b", body, re.I)) for x in hedges}
    print("\n[9] HEDGES (never drive to zero)")
    print("  " + " | ".join(f"{k}={v}" for k, v in sorted(h.items(), key=lambda x: -x[1]) if v))

    # 10. the document as grammatical subject -- meta-prose / internal register
    subj = re.findall(r"\b(B\u00e0i b\u00e1o|B\u00e0i|Nghi\u00ean c\u1ee9u n\u00e0y|M\u1ee5c n\u00e0y|Ph\u1ea7n n\u00e0y|"
                      r"\u0110o\u1ea1n n\u00e0y)\b", body)
    print(f"\n[10] DOCUMENT AS SUBJECT: {len(subj)}")
    for m in re.finditer(r"\b(B\u00e0i b\u00e1o|Nghi\u00ean c\u1ee9u n\u00e0y|M\u1ee5c n\u00e0y|Ph\u1ea7n n\u00e0y)", body):
        print("   ..." + body[max(0, m.start() - 60):m.start() + 80].replace("\n", " ") + "...")

    print("\n" + "=" * 78)
    if fails:
        print(f"HARD FAILURES: {', '.join(fails)}")
    else:
        print("No hard threshold failure. Measurements above are still partial verification.")
    print("=" * 78)
    return 1 if (args.strict and fails) else 0


if __name__ == "__main__":
    sys.exit(main())
