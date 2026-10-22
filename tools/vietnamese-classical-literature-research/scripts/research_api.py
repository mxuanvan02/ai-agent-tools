#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open research APIs for Vietnamese classical-literature discovery.

This complements kho_search.py. It connects repositories/journals that expose
structured metadata rather than only HTML pages:

  dspace-hcmussh  DSpace 7 discover search, Hán-Nôm theses/articles
  dspace-vnu      VNU-CRIS DSpace 7 discover search
  oai-vnu         VNU Journal of Science SSH OAI-PMH
  oai-generic     any OJS OAI-PMH endpoint passed via --base
  oai-dlu         Da Lat University Journal OAI-PMH
  columbia-iiif   Columbia Hán-Nôm IIIF Presentation 3 manifest
  calames         EFEO manuscript catalogue record
  openlibrary     book metadata/search
  archive         Internet Archive item metadata + OCR file list
  kanripo         raw Classical Chinese text from GitHub
  wikisource-zh   Chinese Wikisource MediaWiki search API

Examples:
    python3 scripts/research_api.py --list
    python3 scripts/research_api.py dspace-hcmussh "Hán Nôm"
    python3 scripts/research_api.py dspace-vnu "Hán Nôm"
    python3 scripts/research_api.py oai-vnu --from-date 2024-01-01
    python3 scripts/research_api.py columbia-iiif
    python3 scripts/research_api.py archive "Truyền kì mạn lục"
    python3 scripts/research_api.py --probe

The output deliberately includes the source URL and a small real response
sample. It is a discovery tool, not a citation generator: verify any
load-bearing claim against the item record or full text.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
# OAI-PMH is fetched from the network; use defusedxml to block XXE/billion-laughs.
from defusedxml import ElementTree as ET

UA = "research-client/1.0 (Vietnamese classical literature; contact via user)"


def get(url: str, accept: str = "*/*", timeout: int = 60) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", "replace")
        return r.status, r.headers.get("content-type", ""), body


def get_json(url: str) -> tuple[int, str, dict]:
    status, ctype, body = get(url, "application/json")
    return status, ctype, json.loads(body)


def dspace_search(base: str, term: str, size: int = 10) -> dict:
    url = (base.rstrip("/") + "/server/api/discover/search/objects?" +
           urllib.parse.urlencode({"query": term, "size": size}))
    status, ctype, data = get_json(url)
    embedded = data.get("_embedded", {})
    search_result = embedded.get("searchResult", {})
    page = search_result.get("page", {})
    result = {"endpoint": url, "status": status, "content_type": ctype,
              "query": term, "total": page.get("totalElements"), "items": []}
    objects = search_result.get("_embedded", {}).get("objects", [])
    for obj in objects:
        # DSpace 7 nests the item under _embedded.indexableObject; the flat
        # "indexableObject" key only holds a _links dict.
        idx = obj.get("_embedded", {}).get("indexableObject") or {}
        md = idx.get("metadata", {})

        def md_values(key: str) -> list[str]:
            return [m.get("value", "") for m in md.get(key, []) if m.get("value")]

        result["items"].append({
            "uuid": idx.get("uuid"),
            "name": idx.get("name"),
            "handle": idx.get("handle"),
            "type": md_values("dspace.entity.type")[0] if md_values("dspace.entity.type") else None,
            "date_issued": md_values("dc.date.issued"),
            "authors": md_values("dc.contributor.author"),
            "journal": md_values("dc.relation.journal"),
            "subjects": md_values("dc.subject"),
            "extent": md_values("dc.format.extent"),
            "uri": md_values("dc.identifier.uri"),
        })
    result["total"] = result["total"] or len(result["items"])
    return result


def oai_listrecords(base: str, from_date: str | None = None,
                    set_spec: str | None = None, limit: int = 5) -> dict:
    params = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
    if from_date:
        params["from"] = from_date
    if set_spec:
        params["set"] = set_spec
    url = base.rstrip("/") + "?" + urllib.parse.urlencode(params)
    status, ctype, body = get(url, "application/xml")
    root = ET.fromstring(body)
    ns = {"oai": "http://www.openarchives.org/OAI/2.0/",
          "dc": "http://purl.org/dc/elements/1.1/"}
    error = root.find("oai:error", ns)
    records_all = root.findall(".//oai:record", ns)
    records = []
    deleted = 0
    for rec in records_all[:limit]:
        header = rec.find("oai:header", ns)
        meta = rec.find("oai:metadata", ns)
        if header is None:
            continue
        is_deleted = header.get("status") == "deleted"
        deleted += int(is_deleted)
        # oai_dc nests every dublin-core element under <oai_dc:dc>, and each field
        # usually appears twice: once per language. Collect all of them.
        fields: dict[str, list[str]] = {}
        langs: dict[str, list[str]] = {}
        if meta is not None:
            for el in meta.iter():
                tag = el.tag.split("}")[-1]
                if tag in ("title", "creator", "date", "subject", "description", "identifier", "type"):
                    text = (el.text or "").strip()
                    if not text:
                        continue
                    fields.setdefault(tag, []).append(text)
                    lang = el.get("{http://www.w3.org/XML/1998/namespace}lang")
                    if lang:
                        langs.setdefault(tag, []).append(lang)
        records.append({
            "identifier": header.findtext("oai:identifier", "", ns),
            "datestamp": header.findtext("oai:datestamp", "", ns),
            "status": header.get("status", "active"),
            "set_specs": [s.text for s in header.findall("oai:setSpec", ns) if s.text],
            "title": fields.get("title", [""])[0],
            "titles_all": fields.get("title", []),
            "title_langs": langs.get("title", []),
            "creator": fields.get("creator", [""])[0],
            "date": fields.get("date", [""])[0],
            "subject": fields.get("subject", []),
            "description": fields.get("description", [""])[0][:300],
            "type": fields.get("type", [""])[0],
        })
    token = root.find(".//oai:resumptionToken", ns)
    return {"endpoint": url, "status": status, "content_type": ctype,
            "oai_error": ({"code": error.get("code"), "message": (error.text or "").strip()}
                          if error is not None else None),
            "records_sample": records, "record_count_in_response": len(records_all),
            "deleted_in_sample": deleted, "has_resumption_token": token is not None}


def iiif_manifest(url: str) -> dict:
    status, ctype, data = get_json(url)
    canvases = data.get("items", [])
    return {"endpoint": url, "status": status, "content_type": ctype,
            "id": data.get("id"), "label": data.get("label"),
            "canvas_count": len(canvases),
            "first_canvases": [{"id": x.get("id"), "label": x.get("label")} for x in canvases[:5]]}


def openlibrary(term: str, limit: int = 10) -> dict:
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode({"q": term, "limit": limit})
    status, ctype, data = get_json(url)
    docs = data.get("docs", [])
    return {"endpoint": url, "status": status, "content_type": ctype,
            "num_found": data.get("numFound"),
            "items": [{"title": x.get("title"), "author": x.get("author_name", [])[:3],
                       "year": x.get("first_publish_year"),
                       "key": x.get("key")} for x in docs]}


def archive(term: str, limit: int = 10) -> dict:
    query = urllib.parse.quote(f'title:("{term}") OR description:("{term}")')
    url = ("https://archive.org/advancedsearch.php?" + query_string({
        "q": f'title:("{term}") OR description:("{term}")',
        "fl[]": ["identifier", "title", "creator", "year"],
        "rows": limit, "output": "json"}))
    status, ctype, data = get_json(url)
    docs = data.get("response", {}).get("docs", [])
    return {"endpoint": url, "status": status, "content_type": ctype,
            "num_found": data.get("response", {}).get("numFound"),
            "items": docs}


def query_string(params: dict) -> str:
    # urlencode with doseq=True is needed for IA's repeated fl[] fields.
    return urllib.parse.urlencode(params, doseq=True)


def archive_metadata(identifier: str) -> dict:
    url = "https://archive.org/metadata/" + urllib.parse.quote(identifier)
    status, ctype, data = get_json(url)
    files = data.get("files", [])
    useful = [x for x in files if str(x.get("name", "")).endswith(("_djvu.txt", ".pdf", ".jp2.zip"))]
    return {"endpoint": url, "status": status, "content_type": ctype,
            "identifier": identifier, "title": data.get("metadata", {}).get("title"),
            "download_candidates": [{"name": x.get("name"), "size": x.get("size"),
                                     "format": x.get("format")} for x in useful[:20]]}


def wikisource_zh(term: str, limit: int = 10) -> dict:
    params = {"action": "query", "list": "search", "srsearch": term,
              "srlimit": limit, "format": "json", "utf8": 1}
    url = "https://zh.wikisource.org/w/api.php?" + urllib.parse.urlencode(params)
    status, ctype, data = get_json(url)
    return {"endpoint": url, "status": status, "content_type": ctype,
            "total_hits": data.get("query", {}).get("searchinfo", {}).get("totalhits"),
            "items": [{"title": x.get("title"), "snippet": re.sub(r"<[^>]+>", "", x.get("snippet", ""))}
                      for x in data.get("query", {}).get("search", [])]}


def kanripo(path: str) -> dict:
    url = "https://raw.githubusercontent.com/kanripo/KR1a0001/master/" + path
    status, ctype, body = get(url, "text/plain")
    return {"endpoint": url, "status": status, "content_type": ctype,
            "bytes": len(body.encode("utf-8")), "preview": body[:400]}


def _oai_generic(args) -> dict:
    """Any OJS/OAI-PMH endpoint supplied by the caller via --base."""
    base = getattr(args, "base", None)
    if not base:
        raise ValueError("oai-generic needs --base <oai-endpoint-url>")
    return oai_listrecords(base, args.from_date, args.set_spec, args.limit)


def _local_endpoints() -> dict:
    """Endpoints kept OUT of the public repo, loaded from a private local file.

    The public hygiene gate blocks employer and submission-target identifiers
    (including hostnames) from shipping in this skill's public copy. Some
    useful journal endpoints are therefore stored in a local file under
    ~/.hermes/data/, and the connector picks them up by name at runtime.
    """
    path = Path.home() / ".hermes" / "data" / "van-hoc-kho" / "endpoints.local.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out = {}
    for name, cfg in data.items():
        # Keys starting with "_" are comments; a value must be a dict.
        if name.startswith("_") or not isinstance(cfg, dict):
            continue
        base = cfg.get("base")
        if not base:
            continue
        out[f"local:{name}"] = (
            lambda term, args, base=base: oai_listrecords(
                base, getattr(args, "from_date", None),
                getattr(args, "set_spec", None), getattr(args, "limit", 5)))
    return out


CORPORA = {
    "dspace-hcmussh": lambda term, args: dspace_search("https://elib.hcmussh.edu.vn", term, args.limit),
    "dspace-vnu": lambda term, args: dspace_search("https://scholar.vnu.edu.vn", term, args.limit),
    "oai-vnu": lambda term, args: oai_listrecords("https://js.vnu.edu.vn/SSH/oai", args.from_date, args.set_spec, args.limit),
    "oai-generic": lambda term, args: _oai_generic(args),
    "oai-dlu": lambda term, args: oai_listrecords("https://tckh.dlu.edu.vn/index.php/tckhdhdl/oai", args.from_date, args.set_spec, args.limit),
    "columbia-iiif": lambda term, args: iiif_manifest("https://dlc.library.columbia.edu/iiif/3/presentation/10.7916/d8-rzke-ja79/manifest"),
    "calames": lambda term, args: _calames(),
    "openlibrary": lambda term, args: openlibrary(term, args.limit),
    "archive": lambda term, args: archive(term, args.limit),
    "archive-metadata": lambda term, args: archive_metadata(term),
    "wikisource-zh": lambda term, args: wikisource_zh(term, args.limit),
    "kanripo": lambda term, args: kanripo(term or "KR1a0001_001.txt"),
}


def _calames() -> dict:
    url = "https://calames.abes.fr/pub/ms/Calames-202141415248109875"
    status, ctype, body = get(url, "text/html")
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    return {"endpoint": url, "status": status, "content_type": ctype,
            "bytes": len(body.encode("utf-8")), "preview": text[:700]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus", nargs="?")
    ap.add_argument("term", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--from-date")
    ap.add_argument("--set-spec")
    ap.add_argument("--base", help="OAI-PMH endpoint URL for oai-generic")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    corpora = dict(CORPORA)
    corpora.update(_local_endpoints())

    if args.list:
        for k in corpora:
            print(k)
        return 0
    if args.probe:
        probes = {
            "dspace-hcmussh": "https://elib.hcmussh.edu.vn/server/api/discover/search/objects?query=H%C3%A1n%20N%C3%B4m&size=1",
            "dspace-vnu": "https://scholar.vnu.edu.vn/server/api/discover/search/objects?query=h%C3%A1n%20n%C3%B4m&size=1",
            "oai-vnu": "https://js.vnu.edu.vn/SSH/oai?verb=Identify",
            "oai-dlu": "https://tckh.dlu.edu.vn/index.php/tckhdhdl/oai?verb=Identify",
            "columbia-iiif": "https://dlc.library.columbia.edu/iiif/3/presentation/10.7916/d8-rzke-ja79/manifest",
            "openlibrary": "https://openlibrary.org/search.json?q=Truyen+ki+man+luc&limit=1",
            "archive": "https://archive.org/advancedsearch.php?q=test&rows=1&output=json",
            "wikisource-zh": "https://zh.wikisource.org/w/api.php?action=query&list=search&srsearch=%E8%B6%8A%E5%8D%97&format=json",
            "kanripo": "https://raw.githubusercontent.com/kanripo/KR1a0001/master/KR1a0001_001.txt",
        }
        for k, url in probes.items():
            try:
                status, ctype, body = get(url, "*/*", 30)
                print(f"{k}\t{status}\t{ctype}\t{len(body)} bytes\t{url}")
            except Exception as exc:
                print(f"{k}\tERROR\t{exc}\t{url}")
        # Endpoints from the private local registry are probed too, but their
        # URLs are never printed here: the output of this command can be pasted
        # into a public issue or a log.
        local_path = Path.home() / ".hermes" / "data" / "van-hoc-kho" / "endpoints.local.json"
        if local_path.exists():
            try:
                local = json.loads(local_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                local = {}
            for name, cfg in local.items():
                if name.startswith("_") or not isinstance(cfg, dict):
                    continue
                base = cfg.get("base")
                if not base:
                    continue
                try:
                    status, ctype, body = get(base + "?verb=Identify", "*/*", 30)
                    print(f"local:{name}\t{status}\t{ctype}\t{len(body)} bytes\t[local registry]")
                except Exception as exc:
                    print(f"local:{name}\tERROR\t{exc}\t[local registry]")
        return 0
    if not args.corpus:
        ap.error("choose a corpus or use --list/--probe")
    if args.corpus not in corpora:
        ap.error(f"unknown corpus {args.corpus!r}; try --list")
    if args.corpus == "kanripo" and not args.term:
        args.term = "KR1a0001_001.txt"
    if args.corpus == "calames" and args.term is None:
        args.term = ""
    if args.term is None and args.corpus not in ("columbia-iiif", "oai-vnu", "oai-dlu", "oai-generic") \
            and not args.corpus.startswith("local:"):
        ap.error("this corpus needs a term/identifier")
    try:
        result = corpora[args.corpus](args.term or "", args)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2)[:12000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
