#!/usr/bin/env python3
"""PASS 2 — re-verify CHẶT các entry mà bibcheck.py đã flag "diff".
Lọc false positive (Crossref match nhầm reprint/erratum/bài khác title gần giống).
Chỉ giữ REAL_DIFF khi: token-Jaccard(title) >= 0.85 VÀ họ tác giả đầu của bib
xuất hiện trong author list của record Crossref.
Usage: sửa list `keys` bên dưới (= các key status=='diff' từ pass 1), rồi:
  python3 bibrecheck.py /path/to/references.bib > _bibrecheck_out.json
Đọc _bibrecheck_out.json: chỉ entry "REAL_DIFF" mới đáng sửa; "confirmed_ok" và
"no_strict_match (bib likely correct / preprint / book)" => KHÔNG đụng."""
import re, json, urllib.request, urllib.parse, time, sys

BIB = sys.argv[1] if len(sys.argv) > 1 else "references.bib"
MAILTO = "research@example.com"
raw = open(BIB, encoding="utf-8").read()

entries = {}; i = 0
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
    entries[key] = fields; i = j + 1

def norm(s):
    s = re.sub(r"\\hl\{|\\['\"`^~={}\\]|[{}]", "", s or "")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()
def toks(s): return set(norm(s).split())
def first_surname(a):
    a = (a or "").split(" and ")[0]
    if "," in a: return norm(a.split(",")[0])
    return norm(a.split()[-1]) if a.strip() else ""
def cr_query(title):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": title, "rows": 5, "mailto": MAILTO})
    req = urllib.request.Request(url, headers={"User-Agent": "bibcheck/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)["message"]["items"]

# >>> EDIT THIS: paste the keys that came back status=='diff' from pass 1 <<<
keys = []

out = []
for k in keys:
    f = entries.get(k, {}); title = f.get("title", ""); surn = first_surname(f.get("author", ""))
    try: items = cr_query(title)
    except Exception: out.append({"key": k, "verdict": "query_err"}); time.sleep(0.4); continue
    bt = toks(title); matched = None
    for it in items:
        ctt = toks(" ".join(it.get("title", [""])))
        if not bt or not ctt: continue
        jac = len(bt & ctt) / len(bt | ctt)
        crauth = norm(" ".join((a.get("family","")+" "+a.get("given","")) for a in it.get("author", [])))
        if jac >= 0.85 and (surn in crauth if surn else True): matched = it; break
    if not matched:
        out.append({"key": k, "verdict": "no_strict_match (bib likely correct / preprint / book)"})
        time.sleep(0.4); continue
    cy = matched.get("issued", {}).get("date-parts", [[None]])[0][0]; diffs = {}
    by = re.sub(r"\D", "", f.get("year", "") or "")
    if by and cy and str(cy) != by: diffs["year"] = {"bib": f.get("year"), "cr": cy}
    cv = matched.get("volume")
    if f.get("volume") and cv and re.sub(r"\D","",f["volume"]) != re.sub(r"\D","",str(cv)): diffs["volume"] = {"bib": f["volume"], "cr": cv}
    out.append({"key": k, "verdict": "REAL_DIFF" if diffs else "confirmed_ok", "diffs": diffs, "cr_doi": matched.get("DOI")})
    time.sleep(0.4)
print(json.dumps(out, indent=1, ensure_ascii=False))
