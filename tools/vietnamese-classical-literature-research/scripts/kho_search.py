#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unified search client for the Vietnamese classical-literature corpora.

One command, one output format, so a future session does not have to re-derive
each site's request shape. Every corpus below was measured live; the measured
quirks are encoded in the code rather than left in prose.

Usage:
    python3 scripts/kho_search.py "Truyền kì mạn lục"        # search all corpora
    python3 scripts/kho_search.py --only vietnamica "bi ký"
    python3 scripts/kho_search.py --only openalex "văn học trung đại"
    python3 scripts/kho_search.py --list                     # corpora + what each indexes
    python3 scripts/kho_search.py --probe                    # reachability only

Each corpus indexes a DIFFERENT thing. Asking the wrong corpus for your term
returns 0 and looks like "no sources exist". Read the "indexes" line from
--list before concluding anything:

    vietnamica  full stele records (title + summary + place + date + image)
    nlv         BOOK TITLES only — searching an author name returns 0
    chonthieng  STELE TITLES only — searching an author name returns 0
    openalex    scholarly works (search the phrase, keep the diacritics)
    archive     digitised books, searchable by title/description
    wikipedia   spelling check only — never cite
    dspace-hcmussh  DSpace 7: theses, books and articles about Hán-Nôm
    dspace-vnu      DSpace 7: VNU-CRIS research repository
    openlibrary     book bibliographic records
    wikisource-zh   Classical Chinese text search (cross-check only)

Exit code is 0 when at least one corpus returned results, 1 otherwise, so this
can be used as a gate in a pipeline.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Harvested datasets. When present they make the two title-only corpora search
# the FULL catalogue instead of one web page.
DATA_DIR = os.path.expanduser(
    os.environ.get("VHOC_DATA_DIR", "~/.hermes/data/van-hoc-kho"))
NLV_CSV = os.path.join(DATA_DIR, "nlv_catalogue.csv")
CT_INDEX = os.path.join(DATA_DIR, "chonthieng_vanbia_index.json")


# --------------------------------------------------------------------------
# HTTP helpers
# --------------------------------------------------------------------------
def _opener_with_cookiejar():
    import http.cookiejar
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders = [("User-Agent", UA), ("Accept-Language", "vi,en")]
    return op, jar


def fetch(url: str, timeout: int = 60, headers: dict | None = None) -> str:
    h = {"User-Agent": UA, "Accept-Language": "vi,en"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def fetch_json(url: str, timeout: int = 60, headers: dict | None = None) -> dict:
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def reachability(url: str) -> str:
    host = re.sub(r"^https?://([^/]+).*$", r"\1", url)
    dns = subprocess.run(["getent", "hosts", host],
                         capture_output=True).returncode == 0
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            code = r.status
    except Exception:
        code = 0
    if code and code < 400:
        return "curl-ok"
    return "browser-only" if dns else "dns-dead"


def fold(s: str) -> str:
    """Diacritic- and punctuation-insensitive key. Keeps Han characters."""
    import unicodedata
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", s.lower())


# --------------------------------------------------------------------------
# Corpus 1 — Vietnamica stele rubbings
# --------------------------------------------------------------------------
VIC_HOME = "https://gallery.vietnamica.online/"
VIC_API = "https://gallery.vietnamica.online/api/search.php"


class _Vic:
    """Token and cookie must be fetched together; the token is session-bound."""

    def __init__(self) -> None:
        self.op, self.jar = _opener_with_cookiejar()
        self.token: str | None = None

    def refresh(self) -> str:
        page = self.op.open(VIC_HOME, timeout=60).read().decode("utf-8", "replace")
        m = re.search(r'name=["\']api-token["\'][^>]*content=["\']([0-9a-f]{64})["\']', page)
        if not m:
            raise RuntimeError("api-token meta tag not found")
        self.token = m.group(1)
        return self.token

    def query(self, **kw) -> dict:
        if not self.token:
            self.refresh()
        params = {"refNumber": "", "startYear": "", "endYear": "",
                  "locationType": "", "locationValue": "", "keyword": "",
                  "page": 1, "itemsPerPage": 25}
        params.update(kw)
        url = VIC_API + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Referer": VIC_HOME,
            "Origin": "https://gallery.vietnamica.online",
            "X-API-Token": self.token or "",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        })
        with self.op.open(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8", "replace"))


def search_vietnamica(term: str, limit: int = 25) -> list[dict]:
    s = _Vic()
    s.refresh()
    out = []
    for page in (1, 2):
        d = s.query(keyword=term, page=page, itemsPerPage=limit)
        items = d.get("items", [])
        for it in items:
            out.append({
                "ref": it.get("RefNumber", ""),
                "han": it.get("Original_Title", ""),
                "vn": it.get("Vietnamese_Title", ""),
                "year": it.get("CalendarYear", ""),
                "date": it.get("Full_Date", ""),
                "place": " / ".join(str(it.get(k, "")) for k in
                                   ("TinhVN", "HuyenVN", "XaVN") if it.get(k)),
                "size": it.get("Dimension", ""),
                "faces": it.get("Number_Faces", ""),
                "content": (it.get("Content") or "")[:220],
                "composer": it.get("Composer1_Name", ""),
                "image": (it.get("Picture_Link") or "").split(",")[0],
            })
        if len(items) < limit:
            break
    return out


# --------------------------------------------------------------------------
# Corpus 2 — NLV catalogue. BOOK TITLES ONLY.
# --------------------------------------------------------------------------
NLV_CL1 = ("http://hannom.nlv.gov.vn/hannom/cgi-bin/hannom"
           "?a=cl&cl=CL1&e=-------vi-20--1--txt-txIN%7ctxME------")
HAN_RE = re.compile(r"[\u4e00-\u9fff]")


def _nlv_rows_from_csv() -> list[dict]:
    with open(NLV_CSV, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _nlv_rows_live() -> list[dict]:
    src = fetch(NLV_CL1, timeout=90)
    body = re.sub(r"(?is)<(script|style).*?</\1>", " ", src)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", body))
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    chrome = {"Trang chủ", "Tìm kiếm", "Tên tài liệu", "Năm", "Trợ giúp",
              "Kho tàng thư tịch cổ Hán Nôm", "> Liệt kê theo tên tài liệu",
              "Liệt kê theo tên tài liệu", "Liệt kê theo năm", "x"}
    out = []
    for ln in lines:
        if ln in chrome or not HAN_RE.search(ln):
            continue
        han = vn = vol = ""
        m = re.match(r"^\[\s*(.+?)\s*\]\s*-\s*\[\s*(.+?)\s*\]$", ln)
        if m:
            han, vn = m.group(1), m.group(2)
        else:
            m = re.match(r"^(.+?)\s+-\s+-\s+(.+?)(?:\s*\((q\.[^)]*)\))?$", ln)
            if m:
                han, vn, vol = m.group(1), m.group(2), (m.group(3) or "")
            else:
                m = re.match(r"^(\S.*?)\s+-\s+([\s\S]*?)(?:\s*\((q\.[^)]*)\))?$", ln)
                if m:
                    han, vn, vol = m.group(1), m.group(2), (m.group(3) or "")
        out.append({"han_title": han.strip(), "vn_title": vn.strip(),
                    "volume": vol.strip(), "raw_label": ln})
    return out


def search_nlv(term: str, limit: int = 25) -> list[dict]:
    """Search NLV by WORK TITLE. An author name legitimately returns nothing:
    the NLV catalogue is a title list, not an authority list."""
    if os.path.exists(NLV_CSV):
        rows = _nlv_rows_from_csv()
        source = "harvested CSV"
    else:
        rows = _nlv_rows_live()
        source = "live scrape of CL1"
    key = fold(term)
    out = []
    for r in rows:
        if key and key not in fold(r["han_title"]) and key not in fold(r["vn_title"]):
            continue
        out.append(r)
        if len(out) >= limit:
            break
    for r in out:
        r["_source"] = source
    return out


# --------------------------------------------------------------------------
# Corpus 3 — chonthieng stele index. STELE TITLES ONLY.
# --------------------------------------------------------------------------
CT_LIST = "https://chonthieng.com/van-bia/"


def _ct_records_from_index() -> dict:
    with open(CT_INDEX, encoding="utf-8") as fh:
        return json.load(fh)


def _ct_records_live() -> dict:
    src = fetch(CT_LIST, timeout=60)
    out = {}
    for block in re.findall(r"<article.*?</article>", src, re.S):
        hrefs = re.findall(r'href="(https://chonthieng\.com/van-bia/[^"]+)"', block)
        codes = re.findall(r"VB\s?(\d{4,6})", block)
        if not hrefs or not codes:
            continue
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", block))).strip()
        plain = re.sub(r"\s*(Read more|Đọc tiếp).*$", "", plain, flags=re.I)
        plain = re.sub(r"\s*VB\s?\d{4,6}\s*$", "", plain).strip()
        out["VB" + codes[0]] = {"vb": "VB" + codes[0], "title": plain, "url": hrefs[0]}
    return out


def search_chonthieng(term: str, limit: int = 25) -> list[dict]:
    """Search chonthieng by STELE TITLE. An author name legitimately returns
    nothing: this index holds stele headings, not stele contents."""
    if os.path.exists(CT_INDEX):
        recs = _ct_records_from_index()
        source = "harvested index"
    else:
        recs = _ct_records_live()
        source = "live page 1 only (run harvest_epigraphy.py for the full 12,025)"
    key = fold(term)
    out = []
    for vb, r in recs.items():
        if key and key not in fold(r.get("title", "")):
            continue
        r = dict(r)
        r["_source"] = source
        out.append(r)
        if len(out) >= limit:
            break
    return out


# --------------------------------------------------------------------------
# Corpus 4 — OpenAlex (scholarly discovery, open, no key)
# --------------------------------------------------------------------------
OPENALEX = "https://api.openalex.org/works"


def search_openalex(term: str, limit: int = 25) -> list[dict]:
    """Use title_and_abstract.search (phrase-level) rather than the loose
    `search=` param, which returns medical papers for Vietnamese names.
    Keep the diacritics: the Vietnamese-language index is separate.
    A literal double quote inside the term makes OpenAlex return HTTP 500."""
    safe = term.replace('"', " ")
    params = {"filter": f'title_and_abstract.search:"{safe}"',
              "per-page": min(limit, 50)}
    url = OPENALEX + "?" + urllib.parse.urlencode(params)
    d = fetch_json(url, timeout=60)
    out = []
    for w in d.get("results", []):
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        out.append({
            "title": w.get("title") or w.get("display_name", ""),
            "year": w.get("publication_year", ""),
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "venue": src.get("display_name", ""),
            "type": w.get("type", ""),
            "oa": (w.get("open_access") or {}).get("is_oa", ""),
            "cited": w.get("cited_by_count", 0),
            "url": loc.get("landing_page_url") or w.get("id", ""),
        })
    return out


# --------------------------------------------------------------------------
# Corpus 5 — Internet Archive (digitised old books)
# --------------------------------------------------------------------------
IA_SEARCH = "https://archive.org/advancedsearch.php"


def search_archive(term: str, limit: int = 25) -> list[dict]:
    q = urllib.parse.quote(f'title:("{term}") OR description:("{term}")')
    url = (f"{IA_SEARCH}?q={q}&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=year"
           f"&fl[]=language&rows={min(limit, 50)}&page=1&output=json")
    d = fetch_json(url, timeout=60)
    out = []
    for doc in d.get("response", {}).get("docs", []):
        out.append({
            "identifier": doc.get("identifier", ""),
            "title": doc.get("title", ""),
            "creator": doc.get("creator", ""),
            "year": doc.get("year", ""),
            "language": doc.get("language", ""),
            "url": "https://archive.org/details/" + doc.get("identifier", ""),
        })
    return out


# --------------------------------------------------------------------------
# Corpus 6 — Wikipedia / Wikisource (spelling check, never a citable source)
# --------------------------------------------------------------------------
WIKI_API = "https://vi.wikipedia.org/w/api.php"


def search_wikipedia(term: str, limit: int = 10) -> list[dict]:
    params = {"action": "query", "list": "search", "srsearch": term,
              "srlimit": min(limit, 50), "format": "json", "utf8": 1}
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    d = fetch_json(url, timeout=45)
    out = []
    for s in d.get("query", {}).get("search", []):
        out.append({
            "title": s.get("title", ""),
            "snippet": re.sub(r"<[^>]+>", "", s.get("snippet", ""))[:200],
            "url": "https://vi.wikipedia.org/wiki/" +
                   urllib.parse.quote(s.get("title", "").replace(" ", "_")),
        })
    return out


# --------------------------------------------------------------------------
# Corpus 6 — DSpace 7 repositories (theses, books, articles about Hán-Nôm)
# --------------------------------------------------------------------------
# DSpace 7 nests the item at _embedded.searchResult._embedded.objects[]
# ._embedded.indexableObject; the flat "indexableObject" key only holds _links.
# The total count lives at _embedded.searchResult.page.totalElements, NOT at the
# JSON root.
def _dspace_search(base: str, term: str, limit: int = 25) -> list[dict]:
    url = (base.rstrip("/") + "/server/api/discover/search/objects?" +
           urllib.parse.urlencode({"query": term, "size": min(limit, 100)}))
    d = fetch_json(url, timeout=60)
    sr = (d.get("_embedded") or {}).get("searchResult") or {}
    objects = (sr.get("_embedded") or {}).get("objects") or []
    out = []
    for obj in objects:
        idx = (obj.get("_embedded") or {}).get("indexableObject") or {}
        md = idx.get("metadata") or {}

        def vals(key: str) -> list[str]:
            return [m.get("value", "") for m in md.get(key, []) if m.get("value")]

        out.append({
            "name": idx.get("name", ""),
            "handle": idx.get("handle", ""),
            "uuid": idx.get("uuid", ""),
            "year": (vals("dc.date.issued") or [""])[0],
            "authors": vals("dc.contributor.author")[:3],
            "subjects": vals("dc.subject")[:4],
            "extent": (vals("dc.format.extent") or [""])[0],
            "url": (vals("dc.identifier.uri") or [""])[0],
            "repo": base,
        })
    return out


def search_dspace_hcmussh(term: str, limit: int = 25) -> list[dict]:
    return _dspace_search("https://elib.hcmussh.edu.vn", term, limit)


def search_dspace_vnu(term: str, limit: int = 25) -> list[dict]:
    return _dspace_search("https://scholar.vnu.edu.vn", term, limit)


# --------------------------------------------------------------------------
# Corpus 7 — Open Library (bibliographic records, not scans)
# --------------------------------------------------------------------------
def search_openlibrary(term: str, limit: int = 25) -> list[dict]:
    # Open Library's Vietnamese full-text search is noisy: a query for a title
    # can return unrelated books. Search broadly, then require every meaningful
    # query token to occur in the bibliographic title before emitting a result.
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(
        {"q": term, "limit": min(max(limit * 5, 25), 100)})
    d = fetch_json(url, timeout=60)
    wanted = [x for x in fold(term).split() if len(x) > 1]
    out = []
    for doc in d.get("docs", []):
        title = doc.get("title", "")
        title_folded = fold(title)
        if wanted and not all(token in title_folded for token in wanted):
            continue
        key = doc.get("key", "")
        out.append({
            "title": title,
            "authors": (doc.get("author_name") or [])[:3],
            "year": doc.get("first_publish_year", ""),
            "editions": doc.get("edition_count", ""),
            "url": f"https://openlibrary.org{key}" if key else "",
        })
        if len(out) >= limit:
            break
    return out


# --------------------------------------------------------------------------
# Corpus 8 — Chinese Wikisource (cross-check Classical Chinese wording)
# --------------------------------------------------------------------------
def search_wikisource_zh(term: str, limit: int = 25) -> list[dict]:
    params = {"action": "query", "list": "search", "srsearch": term,
              "srlimit": min(limit, 50), "format": "json", "utf8": 1}
    url = "https://zh.wikisource.org/w/api.php?" + urllib.parse.urlencode(params)
    d = fetch_json(url, timeout=60)
    out = []
    for hit in (d.get("query") or {}).get("search", []):
        out.append({
            "title": hit.get("title", ""),
            "snippet": re.sub(r"<[^>]+>", "", hit.get("snippet", "")),
            "url": "https://zh.wikisource.org/wiki/" + urllib.parse.quote(
                hit.get("title", "").replace(" ", "_")),
        })
    return out


# --------------------------------------------------------------------------
CORPORA = {
    "vietnamica": (
        search_vietnamica,
        "FULL stele records: title, summary, place, date, dimensions, image URL"),
    "nlv": (
        search_nlv,
        "BOOK TITLES ONLY (1,778 Hán-Nôm titles) — an author name returns 0"),
    "chonthieng": (
        search_chonthieng,
        "STELE TITLES ONLY (12,025 records) — an author name returns 0"),
    "openalex": (
        search_openalex,
        "Scholarly works; use the phrase WITH diacritics for the Vietnamese index"),
    "archive": (
        search_archive,
        "Digitised books by title/description, OCR downloadable"),
    "wikipedia": (
        search_wikipedia,
        "Spelling/title check only — never cite"),
    "dspace-hcmussh": (
        search_dspace_hcmussh,
        "DSpace 7: theses, books and articles about Hán-Nôm"),
    "dspace-vnu": (
        search_dspace_vnu,
        "DSpace 7: VNU-CRIS research repository"),
    "openlibrary": (
        search_openlibrary,
        "Book bibliographic records — not proof of digitisation"),
    "wikisource-zh": (
        search_wikisource_zh,
        "Classical Chinese text search — cross-check only"),
}

PROBE_URLS = {
    "vietnamica": VIC_HOME,
    "nlv": NLV_CL1,
    "chonthieng": CT_LIST,
    "openalex": "https://api.openalex.org/works?search=test&per-page=1",
    "archive": "https://archive.org/advancedsearch.php?q=test&rows=1&output=json",
    "wikipedia": "https://vi.wikipedia.org/w/api.php?action=query&meta=siteinfo&format=json",
    "dspace-hcmussh": "https://elib.hcmussh.edu.vn/server/api/discover/search/objects?query=H%C3%A1n%20N%C3%B4m&size=1",
    "dspace-vnu": "https://scholar.vnu.edu.vn/server/api/discover/search/objects?query=h%C3%A1n%20n%C3%B4m&size=1",
    "openlibrary": "https://openlibrary.org/search.json?q=Truyen+ki+man+luc&limit=1",
    "wikisource-zh": "https://zh.wikisource.org/w/api.php?action=query&list=search&srsearch=%E8%B6%8A%E5%8D%97&format=json",
}


def emit(rows: list[dict], name: str) -> None:
    print(f"\n### {name} — {len(rows)} hit")
    if not rows:
        print("     (khong co ket qua — kiem tra xem corpus nay index gi truoc khi ket luan)")
        return
    for r in rows[:30]:
        if name == "vietnamica":
            print(f"  [{r['ref']}] {r['han']} / {r['vn']}")
            print(f"      {r['date'] or r['year']} | {r['place']} | {r['size']} | {r['faces']} mat")
            print(f"      {r['content'][:170]}")
            print(f"      {r['image']}")
        elif name == "nlv":
            print(f"  {r.get('vn_title','')} | {r.get('han_title','')} | {r.get('volume','')}")
        elif name == "chonthieng":
            print(f"  [{r['ref']}] {r['title'][:110]}")
            print(f"      {r['url']}")
        elif name == "openalex":
            print(f"  ({r['year']}) {r['title'][:100]}")
            print(f"      {r['venue'][:70]} | OA={r['oa']} | cited={r['cited']} | doi:{r['doi']}")
        elif name == "archive":
            print(f"  {r['identifier']} | {r['title'][:80]}")
            print(f"      {r['creator']} | {r['year']} | {r['language']}")
            print(f"      {r['url']}")
        elif name in ("dspace-hcmussh", "dspace-vnu"):
            print(f"  {r['name'][:110]} | {r['year']} | {', '.join(r['authors'])}")
            print(f"      {r['subjects']} | {r['extent']} | {r['url']}")
        elif name == "openlibrary":
            print(f"  {r['title'][:100]} | {r['year']} | {', '.join(r['authors'])}")
            print(f"      editions={r['editions']} | {r['url']}")
        elif name == "wikisource-zh":
            print(f"  {r['title']} — {r['snippet'][:120]}")
            print(f"      {r['url']}")
        else:
            print(f"  {r['title']} — {r['snippet'][:120]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("term", nargs="?", help="search term")
    ap.add_argument("--only", action="append", choices=list(CORPORA),
                    help="restrict to one corpus (repeatable)")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--list", action="store_true", help="list corpora")
    ap.add_argument("--probe", action="store_true", help="reachability only")
    ap.add_argument("--json", action="store_true", help="emit JSON lines instead of text")
    args = ap.parse_args()

    if args.list:
        print(f"  data dir: {DATA_DIR} "
              f"({'harvested datasets present' if os.path.isdir(DATA_DIR) else 'not harvested'})")
        for k, (_, desc) in CORPORA.items():
            print(f"  {k:14s} {desc}")
        return 0

    if args.probe:
        for k, url in PROBE_URLS.items():
            print(f"  {k:14s} {reachability(url):12s} {url}")
        return 0

    if not args.term:
        ap.error("a search term is required (or use --list / --probe)")

    todo = args.only or list(CORPORA)
    total = 0
    for name in todo:
        fn, _ = CORPORA[name]
        try:
            rows = fn(args.term, args.limit)
        except Exception as exc:                        # noqa: BLE001
            print(f"\n### {name} — ERROR {exc}", file=sys.stderr)
            continue
        if args.json:
            for r in rows:
                print(json.dumps(r, ensure_ascii=False))
        else:
            emit(rows, name)
        total += len(rows)
    return 0 if total else 1


if __name__ == "__main__":
    sys.exit(main())
