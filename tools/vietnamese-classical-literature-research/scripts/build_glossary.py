#!/usr/bin/env python3
"""Generate references/han-nom-keyword-glossary.md and
references/source-corpus-verified.md from assets/verified_terms.json.

Why generated: the two largest reference files are tables of characters and URLs.
Transcribing either by hand is how a wrong 漢字 or a dead link enters a skill, and
both errors are invisible to a reader. Generating them means the evidence file is
the single source of truth and `tests/test_skill_integrity.py` can assert the
markdown has not drifted from it.

Usage:
    python3 scripts/build_glossary.py            # write both files
    python3 scripts/build_glossary.py --check     # exit 1 if files are stale
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1]
ASSETS = TOOL / "assets" / "verified_terms.json"
REFS = TOOL / "references"

CAT_TITLE = {
    "work":    "Tác phẩm (works)",
    "author":  "Tác giả, tự, hiệu (authors, courtesy names, pen names)",
    "genre":   "Thể loại (genres)",
    "form":    "Niêm luật, thi pháp (versification and poetics)",
    "script":  "Văn tự, ngôn ngữ (scripts and language)",
    "thought": "Tư tưởng (thought vocabulary)",
    "exam":    "Khoa cử, quan chế (examination system)",
}
CAT_ORDER = ["work", "author", "genre", "form", "script", "thought", "exam"]

LAYER_TITLE = {
    1: "Layer 1 — Primary / manuscript",
    2: "Layer 2 — Peer-reviewed scholarship",
    3: "Layer 3 — Reference works (bibliographies, dictionaries)",
    4: "Layer 4 — Open corpora (verify spelling, do not cite as scholarship)",
}

REACH_LABEL = {
    "curl-ok":       "curl OK",
    "browser-only":  "browser only (blocks non-browser clients)",
    "dns-dead":      "DNS DEAD — do not cite",
}


def _evidence_cell(ev: list[dict]) -> str:
    """One compact cell naming the strongest source for the row."""
    named = [e["where"] for e in ev if e.get("kind") == "named-source"]
    if named:
        return named[0].split(",")[0].split(":")[0].strip()[:70]
    wiki = [e["where"] for e in ev if e.get("kind") == "wiki-corpus"]
    if wiki:
        return "wiki corpus: " + wiki[0].split(",")[0]
    return ""


def build_glossary(data: dict) -> str:
    terms = data["terms"]
    L: list[str] = []
    A = L.append
    A("# Bảng tra từ khoá Hán – Nôm đã kiểm chứng")
    A("")
    A("Generated file. Do not edit by hand — edit `assets/verified_terms.json` and run")
    A("`python3 scripts/build_glossary.py`. `tests/test_skill_integrity.py` fails on drift.")
    A("")
    A("## Contract for every row")
    A("")
    A("Each row below carries a Han string that was **matched byte-for-byte in a fetched")
    A("source during the verification session that built this file** (`status` column). No")
    A("character in this table was recalled from memory. Evidence is named in")
    A("`assets/verified_terms.json` (`evidence[].where`).")
    A("")
    A("Status values:")
    A("")
    A("- `CONFIRMED-INDEPENDENT` — matched in a layer-1/2/3 named source: a library catalogue")
    A("  record with shelfmark, a full-text edition, a dictionary entry, or a peer-reviewed")
    A("  paper. Strongest. Safe to print in a deliverable.")
    A("- `CONFIRMED+GLOSS` — the Han string and its Vietnamese gloss co-occur in the same")
    A("  window of a fetched page. Strong for search terms; for a citation, upgrade to a")
    A("  named source first.")
    A("- `CONFIRMED` — the Han string occurs in a fetched page but not adjacent to the gloss")
    A("  (common for generic vocabulary such as 科舉, 平仄). Usable as a query term.")
    A("")
    A("## How to use a row")
    A("")
    A("A row is a **query term**, not a citation. Searching `傳奇漫錄` retrieves Chinese-language")
    A("scholarship and digitised editions that `Truyền kỳ mạn lục` cannot reach. But before the")
    A("characters appear in a paper, confirm them against a layer-1/2 source and record that")
    A("source in the evidence ledger.")
    A("")
    A("Rules that cost nothing to follow and prevent the common failures:")
    A("")
    A("1. **Query the genre term separately from the title.** `傳奇` (genre) retrieves")
    A("   comparative studies of the form; `傳奇漫錄` retrieves one book. They answer")
    A("   different questions and both are usually needed.")
    A("2. **Query the author's courtesy name too.** Catalogues index by both: Nguyễn Trãi and")
    A("   `Ức Trai` `抑齋`; Nguyễn Bỉnh Khiêm and `Bạch Vân am` `白雲庵`, `程國公`.")
    A("3. **Include Vietnamese spelling variants.** `kí`/`ký`, `tùy`/`tuỳ`, `kỳ`/`kì`,")
    A("   `Truyện`/`Chuyện`. Reputable sources differ and one form loses hits.")
    A("4. **Never emit a character that is not in this table without labelling it")
    A("   unverified.** An unverified character is a hypothesis, not a search term — and a")
    A("   wrong one returns zero results, which reads as \"no sources exist\".")
    A("5. **When this table lacks a term, verify it; do not fill it in.** Run")
    A("   `scripts/verify_han_terms.py` against fetched pages, or find a layer-1/2 source")
    A("   that prints the title, and add the row with its evidence.")
    A("")

    by_cat: dict[str, list[dict]] = {}
    for t in terms:
        by_cat.setdefault(t["cat"], []).append(t)

    for cat in CAT_ORDER:
        rows = by_cat.get(cat, [])
        if not rows:
            continue
        A("## " + CAT_TITLE.get(cat, cat))
        A("")
        A("| Thuật ngữ | 漢字 | Status | Evidence anchor |")
        A("|---|---|---|---|")
        for t in sorted(rows, key=lambda r: r["label"]):
            A("| %s | `%s` | %s | %s |" % (
                t["label"], t["han"], t["status"], _evidence_cell(t.get("evidence", []))))
        A("")

    A("## Corrections discovered during verification")
    A("")
    A("These are recorded because they are exactly the errors a recall-based glossary makes:")
    A("the recalled character is plausible, and a search using it silently returns nothing.")
    A("")
    A("| Term | Recalled (wrong) | Verified | Verified from |")
    A("|---|---|---|---|")
    A("| Nguyễn Huy Tự | 阮輝似 | `阮輝嗣` | vi.wikipedia page for the author |")
    A("| Trần Văn Giáp | 陳文甲 | `陳文玾` | vi.wikipedia page for the author (8 occurrences) |")
    A("| Thượng kinh ký sự | 上京紀事 | `上京記事` | vi.wikipedia + vi.wikisource title line |")
    A("| Vịnh Hoa Yên tự phú | 花煙寺賦 (missing 詠) | `詠花煙寺賦` | Tự điển chữ Nôm trích dẫn; CHIBS paper full title |")
    A("")

    A("## Notes from the verification session")
    A("")
    for n in data.get("notes", []):
        A("- " + n)
    A("")

    rej = data.get("discovery_heuristic_rejections", [])
    if rej:
        A("## Why the \"most frequent Han run near the gloss\" heuristic is rejected")
        A("")
        A("A cheap way to fill a glossary is: find the Vietnamese gloss in a page, then take the")
        A("most frequent Han string nearby. Measured on this corpus it produced **5 wrong answers")
        A("out of 12 attempts**, each wrong in a way that looks correct:")
        A("")
        A("| Term asked for | Heuristic returned | Why it is wrong |")
        A("|---|---|---|")
        for r in rej:
            A("| %s | `%s` | %s |" % (r["label"], r["wrong_output"], r["why"]))
        A("")
        A("The failure mode is structural: Han strings adjacent to a title belong to whatever")
        A("else that sentence is about — the author, a sibling work, a shelfmark, a filename.")
        A("Frequency is not evidence. **Only an exact-string match of the candidate inside a")
        A("source that actually names the work counts.** That is what")
        A("`scripts/verify_han_terms.py` implements, and why `DISCOVERED` output is printed for")
        A("human judgement instead of being accepted automatically.")
        A("")

    return "\n".join(L) + "\n"


def build_sources(data: dict) -> str:
    srcs = data["sources"]
    L: list[str] = []
    A = L.append
    A("# Nguồn tư liệu đã kiểm chứng khả năng truy cập")
    A("")
    A("Generated file. Do not edit by hand — edit `assets/verified_terms.json` and run")
    A("`python3 scripts/build_glossary.py`. `tests/test_skill_integrity.py` fails on drift.")
    A("")
    A("Every row was measured with `curl` (HTTP status) and `getent hosts` (DNS) during the")
    A("session that built this file. Reachability is a property of a network and a moment in")
    A("time, so re-probe with `python3 scripts/probe_sources.py --live` before relying on a")
    A("`dns-dead` verdict, and before concluding that a `browser-only` source is unusable.")
    A("")
    A("## Reachability classes")
    A("")
    A("| Class | Meaning | Consequence |")
    A("|---|---|---|")
    A("| `curl-ok` | Plain HTTP fetch returns a usable status | Scriptable; safe to fetch in bulk |")
    A("| `browser-only` | Host resolves, but returns 000/403 to non-browser clients | **Not dead.** Use a browser session. Never conclude the source is gone from a curl failure |")
    A("| `dns-dead` | Domain does not resolve | Do not put this URL in a deliverable. Find the same content elsewhere |")
    A("")
    A("The distinction between the last two classes is the expensive lesson here: three domains")
    A("that are commonly cited in this field were measured DNS-dead, while four important")
    A("catalogues merely block `curl`. A source list assembled from memory gets both wrong, in")
    A("opposite directions.")
    A("")

    by_layer: dict[int, list[dict]] = {}
    for s in srcs:
        by_layer.setdefault(s["layer"], []).append(s)

    for layer in sorted(by_layer):
        A("## " + LAYER_TITLE.get(layer, "Layer %d" % layer))
        A("")
        for s in by_layer[layer]:
            A("### %s" % s["name"])
            A("")
            A("- URL: %s" % s["url"])
            A("- Reachability: **%s** (`%s`)" % (REACH_LABEL.get(s["reach"], s["reach"]), s["reach"]))
            A("- %s" % s["note"])
            A("")

    A("## Search order that follows from the layering")
    A("")
    A("1. **Settle a textual fact** (title characters, author, shelfmark, edition year, page")
    A("   count) at layer 1. `hannom.nlv.gov.vn` gives the record with `Mã kho R.xxx` and")
    A("   `nlvnpf-xxxx`; `lib.nomfoundation.org` gives the same record bilingually.")
    A("2. **Find the scholarly conversation** at layer 2. Vietnamese textual criticism")
    A("   (văn bản học) lives in university faculty sites and journals; the Chinese-language")
    A("   side of Buddhist and genre questions lives in venues like the CHIBS bulletin.")
    A("3. **Confirm a reading or a definition** at layer 3 (dictionaries, bibliographies).")
    A("4. **Read fast, verify spelling** at layer 4 — then go back up a layer before citing.")
    A("   `識典古籍` gives a complete 傳奇漫錄 text; that is enough to confirm 傘圓祠判事錄")
    A("   character by character, and still not a citable edition.")
    A("5. **Never ship a `dns-dead` URL.** If a claim depends on such a source, the claim needs")
    A("   a different source, not a different link.")
    A("")

    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the reference files differ from generated output")
    args = ap.parse_args()

    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    REFS.mkdir(parents=True, exist_ok=True)

    targets = {
        REFS / "han-nom-keyword-glossary.md": build_glossary(data),
        REFS / "source-corpus-verified.md": build_sources(data),
    }

    if args.check:
        stale = []
        for path, text in targets.items():
            cur = path.read_text(encoding="utf-8") if path.exists() else None
            if cur != text:
                stale.append(path.name)
        if stale:
            print("STALE (regenerate with scripts/build_glossary.py): " + ", ".join(stale))
            return 1
        print("OK: generated references match assets/verified_terms.json")
        return 0

    for path, text in targets.items():
        path.write_text(text, encoding="utf-8")
        print("wrote %s (%d bytes)" % (path.relative_to(TOOL), len(text.encode("utf-8"))))
    print("terms: %d | sources: %d" % (len(data["terms"]), len(data["sources"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
