#!/usr/bin/env python3
"""BibTeX verification for hallucination detection (người dùng workflow).

Phát hiện reference sinh bằng LM: entry giữ DOI/journal thật nhưng bịa author/title.

Usage:
  python3 bib_verify.py --bib references.bib --aux main.aux --out result.json
  python3 bib_verify.py --bib references.bib --doi 10.1016/j.sbi.2024.102775   # DOI canonical lookup

Nguyên tắc:
  - Chỉ rà key THỰC SỰ được cite (đọc từ .aux), không toàn bộ .bib.
  - DOI là nguồn không nói dối -> dùng để xác minh canonical.
  - Crossref query.bibliographic hay xếp nhầm (Faculty Opinions / review / figure) -> dương tính giả.
  - Semantic Scholar không key bị 429 -> retry giãn cách, coi 429 là 'chưa biết' không phải 'không tồn tại'.
  - Năm lệch 1 thường là online-first vs số in -> bib thường ĐÚNG.
  - GHI kết quả ra FILE (stdout hay bị nuốt khi chạy nền).
"""
import re, json, urllib.request, urllib.parse, time, argparse, sys

MAILTO = "research@example.com"
UA = "bibverify/1.0 (mailto:%s)" % MAILTO


def parse_bib(path):
    """Parse .bib bằng depth-counting ngoặc — KHÔNG dùng grep (vỡ trên '{')."""
    raw = open(path, encoding="utf-8").read()
    entries, i = {}, 0
    while True:
        at = raw.find("@", i)
        if at == -1:
            break
        m = re.match(r"@(\w+)\s*\{", raw[at:])
        if not m:
            i = at + 1
            continue
        start = at + m.end() - 1
        depth, j = 0, start
        while j < len(raw):
            if raw[j] == "{":
                depth += 1
            elif raw[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = raw[start + 1:j]
        key = body.split(",", 1)[0].strip()
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries[key] = {"type": m.group(1).lower(), "fields": fields, "span": (at, j + 1)}
        i = j + 1
    return entries


def cited_keys(aux_path):
    raw = open(aux_path, encoding="utf-8").read()
    keys = set()
    for m in re.finditer(r"\\(?:abx@aux@cite|citation)\{([^}]*)\}", raw):
        for k in m.group(1).split(","):
            if k.strip():
                keys.add(k.strip())
    return keys


def norm(s):
    s = re.sub(r"\\hl\{|\\['\"`^~={}\\]|[{}]", "", s or "")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def jac(a, b):
    A, B = set(norm(a).split()), set(norm(b).split())
    return len(A & B) / len(A | B) if A and B else 0.0


def surnames(author):
    out = []
    for a in (author or "").split(" and "):
        a = a.strip()
        if not a:
            continue
        out.append(norm(a.split(",")[0]) if "," in a else norm(a.split()[-1]))
    return [x for x in out if x]


def get_json(url, tries=3):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 * (t + 1)); continue
            return {"_err": str(e)}
        except Exception as e:
            return {"_err": str(e)}
    return {"_err": "429_exhausted"}


def doi_lookup(doi):
    d = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if "_err" in d:
        return d
    msg = d.get("message", {})
    return {
        "title": " ".join(msg.get("title", [""]) or [""]),
        "authors": [(a.get("family", "") + ", " + a.get("given", "")).strip(", ")
                    for a in msg.get("author", [])],
        "journal": (msg.get("container-title", [""]) or [""])[0],
        "year": (msg.get("issued", {}).get("date-parts", [[None]])[0][0]),
        "volume": msg.get("volume"), "pages": msg.get("page"),
    }


def cr_search(title):
    d = get_json("https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": 5, "mailto": MAILTO}))
    return d.get("message", {}).get("items", []) if "_err" not in d else []


def s2_search(title):
    d = get_json("https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
        {"query": title, "limit": 5, "fields": "title,year,venue,authors,externalIds"}))
    return d.get("data", []) or [] if "_err" not in d else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", required=True)
    ap.add_argument("--aux")
    ap.add_argument("--out", default="bib_verify_result.json")
    ap.add_argument("--doi")
    args = ap.parse_args()

    if args.doi:
        print(json.dumps(doi_lookup(args.doi), indent=1, ensure_ascii=False))
        return

    entries = parse_bib(args.bib)
    keys = sorted(cited_keys(args.aux) & set(entries)) if args.aux else sorted(entries)
    results = []
    for k in keys:
        f = entries[k]["fields"]
        title = f.get("title", "")
        bib_sn = surnames(f.get("author", ""))
        rec = {"key": k, "bib_title": title[:90], "bib_author1": bib_sn[0] if bib_sn else "",
               "bib_doi": f.get("doi", ""), "flags": []}
        # nếu có DOI -> xác minh canonical (mạnh nhất)
        if f.get("doi"):
            can = doi_lookup(f["doi"])
            if "_err" not in can:
                can_sn = surnames(" and ".join(can["authors"]))
                if can_sn and bib_sn and can_sn[0] != bib_sn[0]:
                    rec["flags"].append("AUTHOR_MISMATCH_AT_DOI(bib=%s vs doi=%s)" % (bib_sn[0], can_sn[0]))
                if title and jac(title, can["title"]) < 0.6:
                    rec["flags"].append("TITLE_MISMATCH_AT_DOI(doi_title=%s)" % can["title"][:60])
                rec["doi_canonical"] = can
            time.sleep(0.3)
        else:
            cr = cr_search(title)
            best = max(cr, key=lambda it: jac(title, " ".join(it.get("title", [""]) or [""])), default=None)
            bj = jac(title, " ".join(best.get("title", [""]) or [""])) if best else 0
            if bj < 0.6:
                s2 = s2_search(title)
                sj = max((jac(title, it.get("title", "") or "") for it in s2), default=0)
                if sj < 0.6:
                    rec["flags"].append("NOT_FOUND(cr=%.2f,s2=%.2f) -> nghi bia, kiem bang mat" % (bj, sj))
            time.sleep(0.5)
        results.append(rec)
        if len(results) % 5 == 0:
            json.dump(results, open(args.out, "w"), indent=1, ensure_ascii=False)
            print("...%d/%d %s" % (len(results), len(keys), k), flush=True)

    json.dump(results, open(args.out, "w"), indent=1, ensure_ascii=False)
    suspect = [r for r in results if r["flags"]]
    print("DONE %d cited | %d FLAGGED (kiem bang mat, coi chung duong tinh gia)" % (len(results), len(suspect)))
    for r in suspect:
        print("  [%s] %s" % (r["key"], "; ".join(r["flags"])))


if __name__ == "__main__":
    main()
