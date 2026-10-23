#!/usr/bin/env python3
"""peek_sheets.py — đọc thử vài dòng đầu của các sheet ứng viên để nhận diện
sheet 'việc cần làm' của anh. CHỈ ĐỌC (values.get), không sửa. In header + <=5 dòng."""
import importlib.util
import os
import sys

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
spec = importlib.util.spec_from_file_location("gapi", _SKILL)
gapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gapi)
sheets = gapi.build_service("sheets", "v4")

CANDIDATES = [
    ("TASK", "1-_E5FN8_izuNeVvegR8if2OKTJ2SrQcc0BRcQMC027c"),
    ("List task", "1kkoWF8yvPgheisflycCBWljYW3zB6KvRpsxGVPF_r0Q"),
    ("To-do list", "1-D2a6nUEDwuuBfuGlli4m-VX7nsOjCwQnl5Y8tPZy9I"),
    ("Lịch làm việc HOÀI.", "1Xtg1KAo9oyc6NwAqnnGYzEjiGH0IpG0bcg7wjQFOZYk"),
    ("Task EduHub - Unified Tech", "1zCzu1HFhtWW9NJvBuDqnzoivjzgsI6UzBT3VNNgXskE"),
    ("Task Intern", "143PiorQtnga5ySRQdoJ2ZnXfK2WQpVh0wbVAyVFwO4s"),
]

for name, sid in CANDIDATES:
    print("=" * 70)
    print(f"SHEET: {name}  (id={sid})")
    try:
        meta = sheets.spreadsheets().get(spreadsheetId=sid).execute()
        tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
        print(f"  các tab: {tabs}")
        first = tabs[0] if tabs else "Sheet1"
        rng = f"'{first}'!A1:H6"
        resp = sheets.spreadsheets().values().get(
            spreadsheetId=sid, range=rng, valueRenderOption="FORMATTED_VALUE").execute()
        rows = resp.get("values") or []
        print(f"  {len(rows)} dòng đầu của tab '{first}':")
        for i, r in enumerate(rows):
            cells = [str(c)[:22] for c in r][:8]
            print(f"    [{i+1}] " + " | ".join(cells))
    except Exception as e:
        print(f"  LỖI: {type(e).__name__}: {str(e)[:120]}")
