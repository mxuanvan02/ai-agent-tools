#!/usr/bin/env python3
"""Verify candidate Han characters for Vietnamese literary terms against real
fetched pages. Dependency-free: stdlib + curl.

WHY THIS EXISTS

Recalling 漢字 for a Vietnamese title produces plausible-looking characters. A wrong
one does not fail loudly: the search returns nothing, and the agent concludes no
sources exist. This script makes the check mechanical.

It answers two different questions, and keeps them separate because conflating them
is what produces false confidence:

  --check   Does my candidate Han string actually occur in a fetched page?
            (exact-string match; the only result that counts as evidence)
  --discover  My candidate failed. What Han runs sit near the Vietnamese gloss?
            (candidates for a human to read; printed, NEVER auto-accepted)

Discovery is advisory on purpose. Measured on the corpus this skill was built from,
the "most frequent Han run near the gloss" heuristic returned a wrong answer in 5
of 12 cases — it grabs whatever else the sentence is about: the author's name, a
sibling work, a shelfmark, a filename. See
references/han-nom-keyword-glossary.md, final section.

USAGE

  # 1. fetch pages into a corpus dir (MediaWiki API, batched to avoid rate limits)
  python3 scripts/verify_han_terms.py --fetch-vi "Truyền kỳ mạn lục;Nguyễn Dữ" --corpus /tmp/c

  # 2. check candidates from a terms file
  python3 scripts/verify_han_terms.py --corpus /tmp/c --terms terms.txt

  # 3. discovery for the failures
  python3 scripts/verify_han_terms.py --corpus /tmp/c --terms terms.txt --discover

TERMS FILE FORMAT (one term per line, `;` separated)

  label ; han ; gloss
  Truyền kỳ mạn lục ; 傳奇漫錄 ; Truyền kỳ mạn lục
  Nguyễn Dữ ; 阮嶼 ; Nguyễn Dữ

`label` is what you call it; `han` is the candidate to test; `gloss` is the
Vietnamese string whose neighbourhood should also contain the Han if the match is
genuine (not an incidental occurrence of a common character).

Exit code: 0 = every candidate CONFIRMED, 1 = at least one NOT-FOUND, 2 = usage or
I/O error. So it can gate a build.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# CJK Unified Ideographs + Extension A + Compatibility Ideographs. Deliberately
# EXCLUDES the Extension B+ planes (U+20000+) that Nom characters live on: this
# tool verifies Han titles, and including Nom ranges would let a rare Nom
# character pass a Han check.
HAN = re.compile(r'[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]{2,}')


def strip_markup(s: str) -> str:
    """Remove wiki templates/refs and collapse whitespace, for readable context."""
    s = re.sub(r'\{\{[^{}]*\}\}', ' ', s)
    s = re.sub(r'<ref[^>]*>.*?</ref>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


# ---------------------------------------------------------------- fetch ----

def fetch_batch(lang: str, titles: list[str], corpus: str, delay: float = 3.0) -> int:
    """Fetch up to 50 wikitexts in ONE request.

    One request per title gets rate-limited after ~15 calls on a shared IP; this
    was measured while building the skill (33 of 44 titles came back empty).
    Batching is not an optimisation here, it is what makes the fetch work.
    """
    os.makedirs(corpus, exist_ok=True)
    saved = 0
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        api = "https://%s.wikipedia.org/w/api.php" % lang
        r = subprocess.run([
            "curl", "-sG", "--max-time", "90", "--connect-timeout", "15", "-A", UA,
            "--data-urlencode", "action=query",
            "--data-urlencode", "prop=revisions",
            "--data-urlencode", "rvprop=content",
            "--data-urlencode", "rvslots=main",
            "--data-urlencode", "format=json",
            "--data-urlencode", "formatversion=2",
            "--data-urlencode", "redirects=1",
            "--data-urlencode", "titles=" + "|".join(chunk),
            api], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except Exception:
            print("  fetch chunk %d failed: %s" % (i // 40, r.stdout[:160]), file=sys.stderr)
            continue
        for pg in d.get("query", {}).get("pages", []):
            revs = pg.get("revisions") or []
            txt = revs[0]["slots"]["main"]["content"] if revs else ""
            if not txt:
                continue
            safe = re.sub(r'[^\w\u00C0-\u1EFF\u4E00-\u9FFF-]+', '_', pg.get("title", "x"))[:60]
            open(os.path.join(corpus, "%s_%s.txt" % (lang, safe)), "w",
                 encoding="utf-8").write(txt)
            saved += 1
        time.sleep(delay)
    return saved


def load_corpus(corpus: str, min_bytes: int = 200) -> dict[str, str]:
    """Load .txt pages, skipping files under `min_bytes`.

    The floor exists to skip failed fetches, which write an empty or stub file and
    would otherwise be counted as corpus content. 200 is right for wiki pages and
    wrong for a hand-written fixture, hence the knob: a test that builds a
    three-line corpus must pass --min-bytes 1 rather than have its fixture
    silently discarded and the run reported as 'empty corpus'.
    """
    if not os.path.isdir(corpus):
        return {}
    out = {}
    for f in sorted(os.listdir(corpus)):
        p = os.path.join(corpus, f)
        if os.path.isfile(p) and f.endswith(".txt") and os.path.getsize(p) >= min_bytes:
            out[f[:-4]] = open(p, encoding="utf-8", errors="replace").read()
    return out


# --------------------------------------------------------------- verify ----

def check_term(corpus: dict[str, str], label: str, han: str, gloss: str) -> dict:
    """Exact-string match of `han`; optionally require `gloss` in the same window."""
    pages = [k for k, t in corpus.items() if han in t]
    if not pages:
        return {"label": label, "han": han, "gloss": gloss,
                "status": "NOT-FOUND", "pages": [], "context": ""}
    # Prefer a page where the gloss sits next to the Han: that is the occurrence
    # that actually labels this term rather than an incidental one.
    for k in pages:
        t = corpus[k]
        i = t.find(han)
        w = t[max(0, i - 170):i + len(han) + 170]
        cw = strip_markup(w)
        if gloss.lower() in cw.lower():
            return {"label": label, "han": han, "gloss": gloss,
                    "status": "CONFIRMED+GLOSS", "pages": pages[:5],
                    "context": cw[:230]}
    t = corpus[pages[0]]
    i = t.find(han)
    return {"label": label, "han": han, "gloss": gloss, "status": "CONFIRMED",
            "pages": pages[:5], "context": strip_markup(
                t[max(0, i - 170):i + len(han) + 170])[:230]}


def discover(corpus: dict[str, str], label: str, han: str, gloss: str) -> list[dict]:
    """Han runs near the gloss, ranked by frequency. ADVISORY ONLY."""
    hits: dict[str, list[str]] = {}
    for k, t in corpus.items():
        for m in re.finditer(re.escape(gloss), t, re.I):
            w = t[max(0, m.start() - 300):m.end() + 300]
            for h in HAN.findall(w):
                hits.setdefault(h, []).append(k)
    ranked = sorted(hits.items(), key=lambda kv: -len(kv[1]))
    return [{"han": h, "count": len(p), "pages": p[:3]} for h, p in ranked[:8]]


# ----------------------------------------------------------------- main ----

def parse_terms(path: str) -> list[tuple[str, str, str]]:
    out = []
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(";")]
        if len(parts) < 2:
            print("terms:%d: need 'label ; han [; gloss]', got %r" % (ln, line),
                  file=sys.stderr)
            continue
        label, han = parts[0], parts[1]
        gloss = parts[2] if len(parts) > 2 else label
        out.append((label, han, gloss))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verify Han characters for Vietnamese literary terms against fetched pages.")
    ap.add_argument("--corpus", default="/tmp/hannom_corpus",
                    help="directory of fetched .txt pages")
    ap.add_argument("--terms", help="terms file: 'label ; han ; gloss' per line")
    ap.add_argument("--fetch-vi", dest="fetch_vi",
                    help="';'-separated vi.wikipedia titles to fetch first")
    ap.add_argument("--fetch-zh", dest="fetch_zh",
                    help="';'-separated zh.wikipedia titles to fetch first")
    ap.add_argument("--min-bytes", type=int, default=200,
                    help="ignore corpus files smaller than this (default 200, "
                         "which skips failed fetches; use 1 for hand-made fixtures)")
    ap.add_argument("--discover", action="store_true",
                    help="for NOT-FOUND terms, print Han runs near the gloss (ADVISORY)")
    ap.add_argument("--json", help="write the full result table to this path")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    try:
        if a.fetch_vi or a.fetch_zh:
            n = 0
            if a.fetch_vi:
                t = [x.strip() for x in a.fetch_vi.split(";") if x.strip()]
                n += fetch_batch("vi", t, a.corpus)
            if a.fetch_zh:
                t = [x.strip() for x in a.fetch_zh.split(";") if x.strip()]
                n += fetch_batch("zh", t, a.corpus)
            print("fetched %d pages into %s" % (n, a.corpus))

        corpus = load_corpus(a.corpus, a.min_bytes)
        if not corpus:
            print("empty corpus at %s — fetch something first (--fetch-vi/--fetch-zh)"
                  % a.corpus, file=sys.stderr)
            return 2
        if not a.terms:
            print("loaded %d corpus pages; pass --terms to verify" % len(corpus))
            return 0

        terms = parse_terms(a.terms)
        if not terms:
            print("no usable term lines in %s" % a.terms, file=sys.stderr)
            return 2

        results = [check_term(corpus, *t) for t in terms]
        nf = [r for r in results if r["status"] == "NOT-FOUND"]

        if not a.quiet:
            print("\ncorpus: %d pages | terms: %d" % (len(corpus), len(results)))
            for r in results:
                mark = {"CONFIRMED+GLOSS": "+", "CONFIRMED": "~", "NOT-FOUND": "x"}[r["status"]]
                print(" %s %-34s %-10s %s" % (mark, r["label"], r["han"], r["status"]))
                if r["context"]:
                    print("     pages=%s" % ",".join(r["pages"][:3]))
                    print("     …%s…" % r["context"][:190])
            from collections import Counter
            c = Counter(r["status"] for r in results)
            print("\nsummary: %s" % dict(c))
            if nf:
                print("NOT-FOUND (%d): %s" % (len(nf), ", ".join(r["label"] for r in nf)))

        if a.discover and nf:
            print("\n=== DISCOVERY (ADVISORY — read before using) ===")
            print("A Han run near the gloss is a CANDIDATE, not evidence. The heuristic")
            print("that accepts the most frequent one was measured wrong in 5 of 12 cases.")
            for r in nf:
                print("\n%s  (rejected candidate: %s, gloss: %r)" % (r["label"], r["han"], r["gloss"]))
                d = discover(corpus, r["label"], r["han"], r["gloss"])
                if not d:
                    print("   gloss absent from corpus — fetch a page that names the work")
                    continue
                for x in d:
                    print("   %-14s x%-3d %s" % (x["han"], x["count"], ",".join(x["pages"][:2])))
                print("   -> verify the top candidate in a source that NAMES this work,")
                print("      then re-run --check with the corrected string.")

        if a.json:
            json.dump(results, open(a.json, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print("\nwrote %s" % a.json)

        return 1 if nf else 0
    except KeyboardInterrupt:
        return 130
    except OSError as e:
        print("I/O error: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
