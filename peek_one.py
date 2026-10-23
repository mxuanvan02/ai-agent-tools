#!/usr/bin/env python3
"""peek_one.py — đọc thử 8 dòng đầu + các tab của MỘT sheet theo id (argv[1]).
CHỈ ĐỌC, không sửa. In cả sheet có nhiều tab."""
import importlib.util
import os
import sys

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
spec = importlib.util.spec_from_file_location("gapi", _SKILL)
gapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gapi)
sheets = gapi.build_service("sheets", "v4")

sid = sys.argv[1]
n_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 8

meta = sheets.spreadsheets().get(spreadsheetId=sid).execute()
print("TITLE:", meta.get("properties", {}).get("title"))
tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
print("TABS:", tabs)
for tab in tabs:
    print("-" * 60)
    print(f"TAB '{tab}':")
    try:
        resp = sheets.spreadsheets().values().get(
            spreadsheetId=sid, range=f"'{tab}'!A1:J{n_rows}",
            valueRenderOption="FORMATTED_VALUE").execute()
        rows = resp.get("values") or []
        if not rows:
            print("  (trống)")
        for i, r in enumerate(rows):
            cells = [str(c)[:24] for c in r][:10]
            print(f"  [{i+1}] " + " | ".join(cells))
    except Exception as e:
        print(f"  LỖI: {type(e).__name__}: {str(e)[:100]}")
