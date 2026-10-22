#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest the digitised Vietnamese epigraphy corpora that replace field survey.

Three corpora, all measured live before this script was written:

  1. Vietnamica (Viện Nghiên cứu Hán Nôm x EFEO) — 20,980 stele rubbings, 1910-1944.
     The catalogue is served by api/search.php. The api-token is bound to a PHP
     session, so the home page must be fetched first to obtain BOTH the meta
     token and the PHPSESSID cookie. Calling the API without the cookie yields
     {"error":"Access denied"} even with a correct token.
  2. NLV kho tàng thư tịch cổ Hán Nôm — the "by title" listing is a single HTML
     page (a=cl&cl=CL1) holding the whole catalogue, already bilingual Hán-Nôm.
  3. chonthieng.com — a JetEngine listing of 602 pages, 20 records per page.

Usage:
    python3 scripts/harvest_epigraphy.py --out DIR [--only vietnamica|nlv|chonthieng]
                                           [--limit N] [--probe]

Outputs (all UTF-8):
    DIR/vietnamica_vanbia.jsonl   one JSON object per stele, full API fields
    DIR/nlv_catalogue.csv          han_title, vn_title, volume, raw_label
    DIR/chonthieng_vanbia_index.json  VB code -> {title, url}

--probe only checks reachability and prints a verdict; it writes nothing.
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
import time
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

VIC_HOME = "https://gallery.vietnamica.online/"
VIC_API = "https://gallery.vietnamica.online/api/search.php"
NLV_CL1 = ("http://hannom.nlv.gov.vn/hannom/cgi-bin/hannom"
           "?a=cl&cl=CL1&e=-------vi-20--1--txt-txIN%7ctxME------")
CT_LIST = "https://chonthieng.com/van-bia/"

HAN = re.compile(r"[\u4e00-\u9fff]")


# --------------------------------------------------------------------------
# generic HTTP
# --------------------------------------------------------------------------
def fetch(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "vi,en"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def reachability(url: str) -> str:
    """curl-ok / browser-only / dns-dead, matching the skill's registry classes."""
    host = re.sub(r"^https?://([^/]+).*$", r"\1", url)
    dns = subprocess.run(["getent", "hosts", host], capture_output=True).returncode == 0
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            code = r.status
    except Exception:
        code = 0
    if code and code < 400:
        return "curl-ok"
    return "browser-only" if dns else "dns-dead"


# --------------------------------------------------------------------------
# 1. Vietnamica
# --------------------------------------------------------------------------
class VietnamicaSession:
    """Token + cookie must come from the same fetch. Never cache the token alone."""

    def __init__(self) -> None:
        import http.cookiejar
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar))
        self.opener.addheaders = [("User-Agent", UA), ("Accept-Language", "vi,en")]
        self.token: str | None = None

    def refresh(self) -> str:
        page = self.opener.open(VIC_HOME, timeout=60).read().decode("utf-8", "replace")
        m = re.search(r'name=["\']api-token["\'][^>]*content=["\']([0-9a-f]{64})["\']', page)
        if not m:
            raise RuntimeError("api-token meta tag not found on home page")
        self.token = m.group(1)
        return self.token

    def search(self, page: int = 1, items_per_page: int = 100, **kw) -> dict:
        if not self.token:
            self.refresh()
        params = {"refNumber": "", "startYear": "", "endYear": "", "locationType": "",
                  "locationValue": "", "keyword": "", "page": page,
                  "itemsPerPage": items_per_page}
        params.update(kw)
        url = VIC_API + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Referer": VIC_HOME,
            "Origin": "https://gallery.vietnamica.online",
            "X-API-Token": self.token or "",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        })
        with self.opener.open(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8", "replace"))


def harvest_vietnamica(out_dir: str, limit: int = 0) -> int:
    sess = VietnamicaSession()
    sess.refresh()
    first = sess.search()
    total = first.get("totalItems", 0)
    pages = first.get("totalPages", 1)
    print(f"[vietnamica] totalItems={total} totalPages={pages}", flush=True)
    path = os.path.join(out_dir, "vietnamica_vanbia.jsonl")
    seen: set[tuple] = set()
    n = 0
    with open(path, "w", encoding="utf-8") as fh:
        for page in range(1, pages + 1):
            try:
                data = sess.search(page=page)
            except Exception as exc:                      # noqa: BLE001
                print(f"  page {page} error {exc}; refreshing session", flush=True)
                time.sleep(2)
                try:
                    sess.refresh()
                    data = sess.search(page=page)
                except Exception as exc2:                 # noqa: BLE001
                    print(f"  page {page} still failing: {exc2}", flush=True)
                    continue
            for item in data.get("items", []):
                key = (item.get("RefNumber"), item.get("Original_Title"),
                       item.get("CalendarYear"))
                if key in seen:
                    continue
                seen.add(key)
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
                n += 1
                if limit and n >= limit:
                    break
            if page % 20 == 0:
                print(f"  page {page}/{pages} rows={n}", flush=True)
            time.sleep(0.25)
            if limit and n >= limit:
                break
    print(f"[vietnamica] wrote {n} rows -> {path}", flush=True)
    return n


# --------------------------------------------------------------------------
# 2. NLV catalogue
# --------------------------------------------------------------------------
def harvest_nlv(out_dir: str) -> int:
    src = fetch(NLV_CL1, timeout=90)
    body = re.sub(r"(?is)<(script|style).*?</\1>", " ", src)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", body))
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]

    chrome = {"Trang chủ", "Tìm kiếm", "Tên tài liệu", "Năm", "Trợ giúp",
              "Kho tàng thư tịch cổ Hán Nôm", "> Liệt kê theo tên tài liệu",
              "Liệt kê theo tên tài liệu", "Liệt kê theo năm", "x"}
    rows: dict[tuple[str, str, str], str] = {}
    for ln in lines:
        if ln in chrome or not HAN.search(ln):
            continue
        # "[ Hán tự] - [Quốc ngữ]"
        m = re.match(r"^\[\s*(.+?)\s*\]\s*-\s*\[\s*(.+?)\s*\]$", ln)
        if m:
            rows.setdefault((m.group(1).strip(), m.group(2).strip(), ""), ln)
            continue
        # "Hán tự - - Quốc ngữ (q.xx)"
        m = re.match(r"^(.+?)\s+-\s+-\s+(.+?)(?:\s*\((q\.[^)]*)\))?$", ln)
        if m:
            rows.setdefault((m.group(1).strip(), m.group(2).strip(),
                             (m.group(3) or "").strip()), ln)
            continue
        # "Hán tự - Quốc ngữ (q.xx)"
        m = re.match(r"^(\S.*?)\s+-\s+([\s\S]*?)(?:\s*\((q\.[^)]*)\))?$", ln)
        if m:
            rows.setdefault((m.group(1).strip(), m.group(2).strip(),
                             (m.group(3) or "").strip()), ln)

    path = os.path.join(out_dir, "nlv_catalogue.csv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["han_title", "vn_title", "volume", "raw_label"])
        for key in sorted(rows):
            writer.writerow([key[0], key[1], key[2], rows[key]])
    print(f"[nlv] wrote {len(rows)} titles -> {path}", flush=True)
    return len(rows)


# --------------------------------------------------------------------------
# 3. chonthieng index
# --------------------------------------------------------------------------
def harvest_chonthieng(out_dir: str) -> int:
    first = fetch(CT_LIST, timeout=60)
    m = re.search(r'data-max-page="(\d+)"', first)
    max_page = int(m.group(1)) if m else 1
    records: dict[str, dict] = {}

    def parse(page_html: str) -> None:
        for block in re.findall(r"<article.*?</article>", page_html, re.S):
            hrefs = re.findall(r'href="(https://chonthieng\.com/van-bia/[^"]+)"', block)
            if not hrefs:
                continue
            codes = re.findall(r"VB\s?(\d{4,6})", block)
            if not codes:
                continue
            plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", block))).strip()
            plain = re.sub(r"\s*(Read more|Đọc tiếp).*$", "", plain, flags=re.I)
            plain = re.sub(r"\s*VB\s?\d{4,6}\s*$", "", plain).strip()
            records.setdefault("VB" + codes[0],
                               {"vb": "VB" + codes[0], "title": plain, "url": hrefs[0]})

    parse(first)
    for page in range(2, max_page + 1):
        try:
            parse(fetch(f"{CT_LIST}page/{page}/", timeout=45))
        except Exception as exc:                          # noqa: BLE001
            print(f"  page {page} error {exc}", flush=True)
            continue
        if page % 50 == 0:
            print(f"  page {page}/{max_page} records={len(records)}", flush=True)
        time.sleep(0.12)

    path = os.path.join(out_dir, "chonthieng_vanbia_index.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=1)
    print(f"[chonthieng] wrote {len(records)} records -> {path}", flush=True)
    return len(records)


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--only", choices=["vietnamica", "nlv", "chonthieng"],
                    action="append", help="restrict to one corpus (repeatable)")
    ap.add_argument("--limit", type=int, default=0, help="stop after N records")
    ap.add_argument("--probe", action="store_true",
                    help="only report reachability; writes nothing")
    args = ap.parse_args()

    if args.probe:
        for name, url in (("vietnamica", VIC_HOME), ("vietnamica-carto",
                         "https://carto.vietnamica.online/"),
                         ("nlv", NLV_CL1), ("chonthieng", CT_LIST)):
            print(f"  {name:18s} {reachability(url):12s} {url}")
        return 0

    os.makedirs(args.out, exist_ok=True)
    todo = args.only or ["vietnamica", "nlv", "chonthieng"]
    if "vietnamica" in todo:
        harvest_vietnamica(args.out, args.limit)
    if "nlv" in todo:
        harvest_nlv(args.out)
    if "chonthieng" in todo:
        harvest_chonthieng(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
