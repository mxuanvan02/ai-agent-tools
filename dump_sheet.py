#!/usr/bin/env python3
"""dump_sheet.py — dump TOÀN BỘ nội dung một Google Sheet ra JSON (backup) + in tóm tắt.

CHỈ ĐỌC. Dùng trước khi ghi bất cứ thứ gì vào sheet của người dùng.
  python3 dump_sheet.py <sheet_id> [label]
"""
import datetime as dt
import importlib.util
import json
import os
import sys

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
spec = importlib.util.spec_from_file_location("gapi", _SKILL)
gapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gapi)
sheets = gapi.build_service("sheets", "v4")

sid = sys.argv[1]
label = sys.argv[2] if len(sys.argv) > 2 else "sheet"

meta = sheets.spreadsheets().get(spreadsheetId=sid).execute()
title = meta.get("properties", {}).get("title")
tabs = [s["properties"] for s in meta.get("sheets", [])]
print("TITLE:", title)
print("SHEET_ID:", sid)
print("TABS:", [t["title"] for t in tabs])

dump = {"sheet_id": sid, "title": title,
        "dumped_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tabs": {}}

total_cells = 0
for t in tabs:
    name = t["title"]
    gp = t.get("gridProperties", {})
    rows_n, cols_n = gp.get("rowCount"), gp.get("columnCount")
    try:
        resp = sheets.spreadsheets().values().get(
            spreadsheetId=sid, range=f"'{name}'",
            valueRenderOption="FORMATTED_VALUE").execute()
        values = resp.get("values") or []
    except Exception as e:
        values = []
        print(f"  tab '{name}': LỖI đọc {type(e).__name__}")
    nonempty = sum(1 for r in values for c in r if str(c).strip())
    total_cells += nonempty
    dump["tabs"][name] = {"grid": [rows_n, cols_n], "values": values}
    print(f"  tab '{name}': grid={rows_n}x{cols_n} | rows có dữ liệu={len(values)} | ô khác rỗng={nonempty}")
    for i, r in enumerate(values[:6]):
        print(f"      [{i+1}] " + " | ".join(str(c)[:26] for c in r[:9]))
    if len(values) > 6:
        print(f"      ... còn {len(values)-6} dòng nữa")

out_dir = os.path.expanduser("~/opt/thu-ky/_backups")
os.makedirs(out_dir, exist_ok=True)
ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
path = os.path.join(out_dir, f"{label}_{ts}_{sid[:12]}.json")
with open(path, "w") as f:
    json.dump(dump, f, ensure_ascii=False, indent=1)
print(f"\nBACKUP: {path} ({os.path.getsize(path)} bytes, {total_cells} ô)")

# verify backup đọc lại được
chk = json.load(open(path))
assert chk["sheet_id"] == sid
print("BACKUP verify: OK | tabs trong backup:", list(chk["tabs"].keys()))
