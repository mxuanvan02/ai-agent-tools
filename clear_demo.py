#!/usr/bin/env python3
"""clear_demo.py — xóa dữ liệu DEMO trong sheet trợ lý để anh nhập việc thật.

An toàn theo thứ tự cứng: BACKUP -> (chỉ khi backup OK) mới CLEAR -> VERIFY đọc lại.
Giữ nguyên header (row 1) của mọi tab; chỉ xóa data row từ A2 trở đi.
Không đụng schema/cấu trúc sheet.
"""
import datetime as dt
import json
import os
import sys

import gsh

SID = "1UwzKmcW1Yb5574y5gR--4RG7w01yNWIEGhdzbPVf1Pc"
TABS = ["tasks", "events", "habits", "log", "meta"]


def main() -> int:
    ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    backup_dir = os.path.expanduser(f"~/opt/thu-ky/_backups/{ts}")
    os.makedirs(backup_dir, exist_ok=True)

    # ── 1. BACKUP toàn bộ (đọc mọi tab) ────────────────────────────────────
    dump = {}
    for tab in TABS:
        dump[tab] = gsh.read_rows(SID, tab)
    counts_before = {t: len(dump[t]) for t in TABS}
    backup_path = os.path.join(backup_dir, "sheet_dump.json")
    with open(backup_path, "w") as f:
        json.dump({"sheet_id": SID, "backup_at": ts, "tabs": dump}, f, ensure_ascii=False, indent=1)

    print("=== 1. BACKUP ===")
    print("  path:", backup_path)
    print("  size:", os.path.getsize(backup_path), "bytes")
    print("  data rows sẽ xóa:", json.dumps(counts_before, ensure_ascii=False))

    # CHẶN: backup phải tồn tại và đọc lại được trước khi xóa
    try:
        re = json.load(open(backup_path))
        assert re["sheet_id"] == SID and set(re["tabs"]) == set(TABS)
        reload_counts = {t: len(re["tabs"][t]) for t in TABS}
        assert reload_counts == counts_before, f"backup lệch: {reload_counts} != {counts_before}"
    except Exception as e:
        print("  ✗ BACKUP VERIFY FAILED -> DỪNG, KHÔNG XÓA:", e)
        return 2
    print("  ✓ backup đọc lại khớp, an toàn để xóa")

    # ── 2. CLEAR data rows (A2:Z), giữ header row 1 ────────────────────────
    print("\n=== 2. CLEAR (giữ header) ===")
    svc = gsh.sheets()
    cleared = []
    for tab in TABS:
        rng = f"'{tab}'!A2:Z"
        resp = svc.spreadsheets().values().clear(spreadsheetId=SID, range=rng).execute()
        cleared.append((tab, resp.get("clearedRange")))
    for tab, cr in cleared:
        print(f"  {tab}: cleared {cr}")

    # ── 3. VERIFY đọc lại ───────────────────────────────────────────────────
    print("\n=== 3. VERIFY (đọc lại từ server) ===")
    ok = True
    for tab in TABS:
        rows = gsh.read_rows(SID, tab)
        hdr = gsh.header_of(SID, tab)
        status = "✓" if len(rows) == 0 and len(hdr) > 0 else "✗"
        if len(rows) != 0 or len(hdr) == 0:
            ok = False
        print(f"  {status} {tab}: data rows={len(rows)} (mong đợi 0) | header={len(hdr)} cột (giữ nguyên)")

    print("\nKẾT QUẢ:", "SẠCH — sheet trống, header nguyên, sẵn sàng nhập việc thật" if ok else "CÒN SÓT — kiểm tra lại")
    print("Khôi phục nếu cần: file", backup_path)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
