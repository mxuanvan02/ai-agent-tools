#!/usr/bin/env python3
"""restore_from_backup.py — khôi phục tab 'Tin học MOS & AI' từ backup JSON.

Dùng khi một lần ghi bị hỏng giữa chừng (đã clear values rồi mới lỗi).
Khôi phục GIÁ TRỊ. Format cũ không bị clear (batchUpdate atomic, đã fail toàn bộ)
nên không cần dựng lại format ở đây.
"""
import glob
import importlib.util
import json
import os
import sys

SHEET_ID = "1Ri5reuE8Rg4Fgheao0AF3HCEnaelKnVExXz6R4F3TwI"
ORIG_TAB = "Tin học MOS & AI"

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
_spec = importlib.util.spec_from_file_location("gapi_rs", _SKILL)
_gapi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gapi)
sheets = _gapi.build_service("sheets", "v4")


def read_tab(tab):
    r = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{tab}'",
        valueRenderOption="FORMATTED_VALUE").execute()
    return r.get("values") or []


def main() -> int:
    baks = sorted(glob.glob(os.path.expanduser("~/opt/thu-ky/_backups/tin_hoc_mos_*.json")))
    if not baks:
        print("✗ không có backup nào")
        return 2
    bak_path = baks[-1]
    bak = json.load(open(bak_path))
    want = bak["tabs"][ORIG_TAB]["values"]
    print(f"backup: {os.path.basename(bak_path)} | {len(want)} dòng")

    cur = read_tab(ORIG_TAB)
    cur_cells = sum(1 for r in cur for c in r if str(c).strip())
    print(f"sheet hiện tại: {len(cur)} dòng, {cur_cells} ô có dữ liệu")

    if cur == want:
        print("✓ sheet đã khớp backup, không cần khôi phục")
        return 0

    # clear rồi ghi lại toàn bộ từ backup
    sheets.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID, range=f"'{ORIG_TAB}'!A1:Z200", body={}).execute()
    resp = sheets.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f"'{ORIG_TAB}'!A1",
        valueInputOption="USER_ENTERED", body={"values": want}).execute()
    print("đã ghi lại từ backup:", resp.get("updatedData", {}).get("range"))

    # VERIFY
    after = read_tab(ORIG_TAB)
    if after == want:
        print(f"✓ KHÔI PHỤC THÀNH CÔNG — {len(after)} dòng, giống HỆT backup")
        return 0
    print(f"✗ KHÔI PHỤC LỆCH: {len(after)} dòng vs {len(want)} dòng backup")
    for i, (a, b) in enumerate(zip(after, want)):
        if a != b:
            print(f"   dòng {i+1} lệch:\n     now={a}\n     bak={b}")
            break
    return 1


if __name__ == "__main__":
    sys.exit(main())
