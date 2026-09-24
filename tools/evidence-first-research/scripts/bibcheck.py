#!/usr/bin/env python3
"""Đối chiếu file .bib với Crossref. Chạy nền (rate-limit 0.4s/query).
Usage: python3 bibcheck.py /path/to/references.bib
Ghi kết quả ra <bib_dir>/_bibcheck_result.json và in tổng kết.
PASS 1 — match LỎNG (chỉ để lọc ra danh sách cần re-verify chặt bằng bibrecheck.py).
Đừng sửa mù theo output này: phần lớn "diff" là false positive."""
import re, json, urllib.request, urllib.parse, time, sys, os

BIB = sys.argv[1] if len(sys.argv) > 1 else "references.bib"
MAILTO = "research@example.com"
raw = open(BIB, encoding="utf-8").read()

def parse(raw):
    entries = []; i = 0
    while True:
        at = raw.find("@", i)
        if at == -1: break
        m = re.match(r"@(\w+)\s*\{", raw[at:])
        if not m: i = at + 1; continue
        start = at + m.end() - 1; depth = 0; j = start
        while j < len(raw):
            if raw[j] == "{": depth += 1
            elif raw[j] == "}":
                depth -= 1
                if depth == 0: break
            j += 1
        body = raw[start+1:j]; key = body.split(",", 1)[0].strip()
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries.append({"type": m.group(1).lower(), "key": key, "fields": fields})
        i = j + 1
    return entries

def norm(s):
    s = re.sub(r"\\hl\{|\\['\"`^~={}\\]|[{}]", "", s or "")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def cr_query(title):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": title, "rows": 3, "mailto": MAILTO})
    req = urllib.request.Request(url, headers={"User-Agent": "bibcheck/1.0 (mailto:%s)" % MAILTO})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["message"]["items"]

entries = parse(raw)
# report local structural issues first
from collections import Counter
keyc = Counter(e["key"] for e in entries)
print("DUP KEYS:", {k: c for k, c in keyc.items() if c > 1})
print("HL ARTIFACTS:", [e["key"] for e in entries if e["key"].endswith("_hl")])

results = []
for e in entries:
    f = e["fields"]; title = norm(f.get("title", ""))
    if not title: results.append({"key": e["key"], "status": "no_title"}); continue
    try: items = cr_query(f.get("title", ""))
    except Exception as ex: results.append({"key": e["key"], "status": "query_err"}); continue
    best = None
    for it in items:
        ct = norm(" ".join(it.get("title", [""])))
        if ct and (ct == title or title in ct or ct in title): best = it; break
    if not best:
        results.append({"key": e["key"], "status": "not_found"}); time.sleep(0.4); continue
    diffs = {}
    cy = best.get("issued", {}).get("date-parts", [[None]])[0][0]
    if f.get("year") and cy and str(cy) != re.sub(r"\D", "", f["year"]): diffs["year"] = {"bib": f["year"], "cr": cy}
    cv = best.get("volume")
    if f.get("volume") and cv and re.sub(r"\D","",f["volume"]) != re.sub(r"\D","",str(cv)): diffs["volume"] = {"bib": f["volume"], "cr": cv}
    if best.get("DOI") and not f.get("doi"): diffs["doi_missing"] = best["DOI"]
    results.append({"key": e["key"], "status": "ok" if not diffs else "diff", "diffs": diffs})
    time.sleep(0.4)

out = os.path.join(os.path.dirname(os.path.abspath(BIB)), "_bibcheck_result.json")
open(out, "w").write(json.dumps(results, indent=1, ensure_ascii=False))
df = [r for r in results if r["status"] == "diff"]
print("TOTAL", len(results), "| OK", sum(1 for r in results if r["status"]=="ok"),
      "| DIFF", len(df), "| NOT_FOUND", sum(1 for r in results if r["status"]=="not_found"))
print("-> re-verify all DIFF entries with bibrecheck.py before changing anything")
