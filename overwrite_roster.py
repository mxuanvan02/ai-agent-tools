#!/usr/bin/env python3
"""overwrite_roster.py — GHI ĐÈ tab chính 'Tin học MOS & AI' bằng 46 em từ ảnh.

Anh Văn đã duyệt "ghi đè đi" sau khi được báo rõ: mất 15 em + 21 ô điểm danh,
backup đã có và khôi phục được.

An toàn theo thứ tự cứng:
  0. assert backup tồn tại + đọc lại được + khớp sheet hiện tại (nếu ai sửa song song
     sau khi backup -> DỪNG, không ghi đè mù)
  1. clear values + reset format vùng data
  2. ghi title/phòng gốc (giữ nguyên), header gốc, 46 em (23 trái + 23 phải)
  3. định dạng theo ảnh: header đậm nền xanh, viền, canh giữa, STT28 nền đỏ,
     STT44-46 chữ đỏ
  4. VERIFY: từng ô khớp nguồn, format đỏ đúng, tab 'Phân phòng' + tab ảnh nguyên vẹn
"""
import datetime as dt
import glob
import importlib.util
import json
import os
import sys

SHEET_ID = "1Ri5reuE8Rg4Fgheao0AF3HCEnaelKnVExXz6R4F3TwI"
ORIG_TAB = "Tin học MOS & AI"
IMG_TAB = "DS 46 từ ảnh 29-09"
OTHER_TAB = "Phân phòng"

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
_spec = importlib.util.spec_from_file_location("gapi_ow", _SKILL)
_gapi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gapi)
sheets = _gapi.build_service("sheets", "v4")

IMAGE = [
    (1, "Nguyễn Ngọc Thành Đức", "10/1", ""),
    (2, "Phan Ngọc Hân", "10/1", ""),
    (3, "Trần Lê Nhật Tuệ", "10/1", ""),
    (4, "Tôn Nguyễn Phương Anh", "10/1", ""),
    (5, "Võ Cải Tiến Dũng", "10/1", ""),
    (6, "Nguyễn Anh Huy", "10/2", ""),
    (7, "Hoàng Minh Huy", "10/3", ""),
    (8, "Nguyễn Đức Anh Khoa", "10/3", ""),
    (9, "Tôn Thất Bảo Nguyên", "10/3", ""),
    (10, "Hà Hoàng Nguyên", "10/5", ""),
    (11, "Trần Thiện Nhân", "10/6", ""),
    (12, "Dương Minh Bảo Nhật", "12/1", ""),
    (13, "Lê Hoàng Gia Khang", "12/1", ""),
    (14, "Nguyễn Trung Quân", "12/1", ""),
    (15, "Trần Bảo Đức", "12/1", "Vắng học TA"),
    (16, "Phan Gia Phước Bảo", "12/1", ""),
    (17, "Hoàng Anh Khoa", "12/1", "Vắng học TA"),
    (18, "Lê Minh Đạt", "12/1", ""),
    (19, "Nguyễn Hồ Văn Khoa", "12/1", ""),
    (20, "Hoàng Lê Bảo Uyên", "12/2", "Vắng học Hoá"),
    (21, "Hồ Quốc Đạt", "12/2", "Vắng học Hoá"),
    (22, "Lê Quốc Huy", "12/2", "Vắng học Toán"),
    (23, "Lê Thị Anh Thư", "12/2", ""),
    (24, "Lê Văn Quốc Hùng", "12/2", ""),
    (25, "Nguyễn Phương Linh", "12/2", "Vắng học Toán"),
    (26, "Nguyễn Quốc Bảo", "12/2", ""),
    (27, "Nguyễn Vũ Đức Tài", "12/2", ""),
    (28, "Phan Việt Hoàng", "12/2", "CLB BÓng chuyền"),
    (29, "Phạm Xuân Gia Khánh", "12/2", ""),
    (30, "Trương Như Hiếu", "12/2", ""),
    (31, "Trần Quang Quốc Phong", "12/2", "Vắng học Hoá"),
    (32, "Trần Văn Thiện Tâm", "12/2", ""),
    (33, "Đào Mạnh Tấn", "12/2", ""),
    (34, "Phạm Khánh Hưng", "12/2", ""),
    (35, "Huỳnh Châu Gia Bảo", "12/2", ""),
    (36, "Lê Quang Khang", "12/3", "STEM"),
    (37, "Nguyễn Tống Khánh Băng", "12/3", ""),
    (38, "Phan Anh Khoa", "12/3", ""),
    (39, "Phạm Minh Tuấn", "12/3", ""),
    (40, "Văn Tiến Đạt", "12/3", "Nghỉ học"),
    (41, "Đặng Thanh Nhàn", "12/4", ""),
    (42, "Nguyễn Đức Bảo Hùng", "12/5", ""),
    (43, "Đoàn Khánh Đăng", "12/5", ""),
    (44, "Tô Anh Thư", "10/1", "Có đăng ký nhưng chưa có tên"),
    (45, "Tôn Thất Văn Quốc Anh", "12/2", "Có đăng ký nhưng chưa có tên"),
    (46, "Trịnh Quốc Thiên Bảo", "12/2", "Có đăng ký nhưng chưa có tên"),
]
LEFT, RIGHT = IMAGE[:23], IMAGE[23:]
DATA_START_ROW = 4  # 1-based


def read_tab(tab):
    r = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{tab}'",
        valueRenderOption="FORMATTED_VALUE").execute()
    return r.get("values") or []


def main() -> int:
    # ── 0. CHẶN TRƯỚC KHI GHI: backup phải tồn tại, đọc lại được, khớp sheet ──
    baks = sorted(glob.glob(os.path.expanduser("~/opt/thu-ky/_backups/tin_hoc_mos_*.json")))
    if not baks:
        print("✗ DỪNG: không tìm thấy backup. Không ghi đè khi không có đường lùi.")
        return 2
    bak_path = baks[-1]
    bak = json.load(open(bak_path))
    bak_rows = bak["tabs"][ORIG_TAB]["values"]
    print(f"backup: {os.path.basename(bak_path)} ({os.path.getsize(bak_path)} bytes)")

    cur = read_tab(ORIG_TAB)
    if cur != bak_rows:
        print("✗ DỪNG: sheet đã THAY ĐỔI so với lúc backup (có người/agent sửa song song).")
        print(f"   backup {len(bak_rows)} dòng vs hiện tại {len(cur)} dòng")
        print("   Hãy dump lại sheet rồi mới ghi đè.")
        return 3
    print(f"✓ sheet khớp backup ({len(cur)} dòng) — an toàn để ghi đè")

    meta = sheets.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    tabs = {s["properties"]["title"]: s["properties"]["sheetId"]
            for s in meta.get("sheets", [])}
    if ORIG_TAB not in tabs:
        print(f"✗ DỪNG: không thấy tab '{ORIG_TAB}'. tabs={list(tabs)}")
        return 4
    sid = tabs[ORIG_TAB]
    print(f"✓ tab gốc sheetId={sid} | các tab: {list(tabs)}")

    # giữ title + phòng + header gốc (đọc từ backup, không hardcode chuỗi bị cắt)
    title_row = (bak_rows[0] + [""] * 8)[:8] if len(bak_rows) > 0 else [""] * 8
    room_row = (bak_rows[1] + [""] * 8)[:8] if len(bak_rows) > 1 else [""] * 8
    header_row = (bak_rows[2] + [""] * 8)[:8] if len(bak_rows) > 2 else [
        "STT", "Họ và tên", "Lớp", "Ngày 15/10/2026"] * 2
    print(f"  giữ title : {title_row[0][:60]!r}")
    print(f"  giữ phòng : {room_row[0][:60]!r}")
    print(f"  giữ header: {[h for h in header_row if h]}")

    # baseline các tab KHÔNG được đụng
    base_other = {t: read_tab(t) for t in (OTHER_TAB, IMG_TAB) if t in tabs}

    # ── 1. reset format vùng data ───────────────────────────────────────────
    # KHÔNG clear values trước khi ghi: lần chạy đầu đã clear xong rồi mới fail ở
    # bước format (HTTP 400) -> tab trống hoàn toàn, phải khôi phục từ backup.
    # Thứ tự an toàn: reset format -> GHI giá trị đè lên -> clear phần dư bên dưới.
    reset_reqs = [{
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 30,
                      "startColumnIndex": 0, "endColumnIndex": 10},
            "cell": {"userEnteredFormat": {
                "backgroundColor": {"red": 1, "green": 1, "blue": 1},
                "textFormat": {"foregroundColor": {"red": 0, "green": 0, "blue": 0},
                               "bold": False, "italic": False, "fontSize": 10},
                # Sheets API đòi style rõ ràng; {} rỗng -> HTTP 400
                # "Invalid requests[0].repeatCell: No border style specified"
                "borders": {k: {"style": "NONE"} for k in ("top", "bottom", "left", "right")},
                "horizontalAlignment": "LEFT"}},
            "fields": ("userEnteredFormat(backgroundColor,textFormat("
                       "foregroundColor,bold,italic,fontSize),borders,horizontalAlignment)")}}]
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body={"requests": reset_reqs}).execute()
    print("✓ đã reset format A1:J30 về trắng/đen/không viền (xóa nền màu cũ)")

    # ── 2. ghi giá trị ──────────────────────────────────────────────────────
    rows = [title_row, room_row, header_row]
    for i in range(23):
        l, r = LEFT[i], RIGHT[i]
        rows.append([str(l[0]), l[1], l[2], l[3], str(r[0]), r[1], r[2], r[3]])
    resp = sheets.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f"'{ORIG_TAB}'!A1",
        valueInputOption="USER_ENTERED", body={"values": rows}).execute()
    upd = resp.get("updatedData", {})
    print(f"✓ đã ghi {len(rows)} dòng | updatedRange={upd.get('range')} "
          f"rows={upd.get('rows')} cols={upd.get('columns')}")

    # 2b. clear phần dữ liệu cũ còn dư BÊN DƯỚI vùng vừa ghi (sheet cũ dài hơn)
    last_written = len(rows)
    sheets.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range=f"'{ORIG_TAB}'!A{last_written + 1}:Z200", body={}).execute()
    print(f"✓ đã clear phần dư A{last_written + 1}:Z200")

    # ── 3. định dạng theo ảnh ───────────────────────────────────────────────
    RED = {"red": 1, "green": 0, "blue": 0}
    LIGHT_BLUE = {"red": 0.80, "green": 0.88, "blue": 0.98}
    BORDER = {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}}
    reqs = []

    # title đậm 13pt
    reqs.append({"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1,
                  "startColumnIndex": 0, "endColumnIndex": 1},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 13}}},
        "fields": "userEnteredFormat.textFormat"}})
    # phòng đậm 11pt
    reqs.append({"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 2,
                  "startColumnIndex": 0, "endColumnIndex": 1},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 11}}},
        "fields": "userEnteredFormat.textFormat"}})
    # header: đậm + nền xanh nhạt
    reqs.append({"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": 2, "endRowIndex": 3,
                  "startColumnIndex": 0, "endColumnIndex": 8},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True},
                                       "backgroundColor": LIGHT_BLUE}},
        "fields": "userEnteredFormat(textFormat.bold,backgroundColor)"}})
    # viền cho 2 khối bảng (không viền cột ghi chú — đúng như ảnh)
    for c0, c1 in ((0, 3), (4, 7)):
        reqs.append({"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 2, "endRowIndex": 26,
                      "startColumnIndex": c0, "endColumnIndex": c1},
            "cell": {"userEnteredFormat": {"borders": {
                "top": BORDER, "bottom": BORDER, "left": BORDER, "right": BORDER}}},
            "fields": "userEnteredFormat.borders"}})
    # STT + Lớp căn giữa
    for c in (0, 2, 4, 6):
        reqs.append({"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 3, "endRowIndex": 26,
                      "startColumnIndex": c, "endColumnIndex": c + 1},
            "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
            "fields": "userEnteredFormat.horizontalAlignment"}})
    # STT 28 -> nền đỏ (khối phải: cột E,F,G)
    reqs.append({"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": DATA_START_ROW - 1 + 4,
                  "endRowIndex": DATA_START_ROW + 4,
                  "startColumnIndex": 4, "endColumnIndex": 7},
        "cell": {"userEnteredFormat": {"backgroundColor": RED}},
        "fields": "userEnteredFormat.backgroundColor"}})
    # STT 44,45,46 -> chữ đỏ (cả cột ghi chú H)
    for stt in (44, 45, 46):
        ri = DATA_START_ROW - 1 + (stt - 24)
        reqs.append({"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": ri, "endRowIndex": ri + 1,
                      "startColumnIndex": 4, "endColumnIndex": 8},
            "cell": {"userEnteredFormat": {"textFormat": {"foregroundColor": RED}}},
            "fields": "userEnteredFormat.textFormat.foregroundColor"}})
    # độ rộng cột
    for start, px in ((0, 45), (1, 215), (2, 55), (3, 200),
                      (4, 45), (5, 215), (6, 55), (7, 200)):
        reqs.append({"updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "COLUMNS",
                      "startIndex": start, "endIndex": start + 1},
            "properties": {"pixelSize": px}, "fields": "pixelSize"}})

    sheets.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body={"requests": reqs}).execute()
    print(f"✓ đã áp dụng {len(reqs)} yêu cầu định dạng")

    # ── 4. VERIFY ───────────────────────────────────────────────────────────
    errors = []
    got = read_tab(ORIG_TAB)

    # 4a. header giữ nguyên
    hdr = (got[2] + [""] * 8)[:8] if len(got) > 2 else []
    if hdr != header_row:
        errors.append(f"header bị đổi: {hdr}")
    # 4b. title + phòng giữ nguyên
    if len(got) > 0 and (got[0] + [""] * 8)[:8] != title_row:
        errors.append("title bị đổi")
    if len(got) > 1 and (got[1] + [""] * 8)[:8] != room_row:
        errors.append("phòng bị đổi")

    # 4c. 46 em khớp verbatim
    by_stt = {}
    for row in got[3:]:
        row = list(row) + [""] * (8 - len(row))
        for off in (0, 4):
            s = str(row[off]).strip()
            if s:
                by_stt[s] = (row[off + 1].strip(), row[off + 2].strip(), row[off + 3].strip())
    for stt, name, lop, note in IMAGE:
        g = by_stt.get(str(stt))
        if g is None:
            errors.append(f"THIẾU STT {stt} ({name})")
            continue
        if g[0] != name:
            errors.append(f"STT {stt} TÊN lệch: {g[0]!r} != {name!r}")
        if g[1] != lop:
            errors.append(f"STT {stt} LỚP lệch: {g[1]!r} != {lop!r}")
        if g[2] != note:
            errors.append(f"STT {stt} GHI CHÚ lệch: {g[2]!r} != {note!r}")
    extra = set(by_stt) - {str(s) for s, _, _, _ in IMAGE}
    if extra:
        errors.append(f"dòng thừa: {sorted(extra)}")

    # 4d. format đỏ
    fmt = sheets.spreadsheets().get(
        spreadsheetId=SHEET_ID,
        fields=("sheets(properties(title,sheetId),data(rowData(values("
                "userEnteredFormat(backgroundColor,textFormat(foregroundColor,bold)),"
                "formattedValue))))")).execute()
    tabf = next((s for s in fmt["sheets"]
                 if s.get("properties", {}).get("title") == ORIG_TAB), None)
    if tabf:
        rf = (tabf.get("data") or [{}])[0].get("rowData") or []

        def c(ri, ci):
            try:
                return rf[ri]["values"][ci]
            except Exception:
                return None
        b28 = ((c(7, 5) or {}).get("userEnteredFormat", {}) or {}).get("backgroundColor")
        if not (b28 and b28.get("red", 0) > 0.9 and b28.get("green", 0) < 0.1):
            errors.append(f"STT28 nền đỏ không áp dụng: {b28}")
        for stt, ri in ((44, 23), (45, 24), (46, 25)):
            fg = (((c(ri, 5) or {}).get("userEnteredFormat", {}) or {})
                  .get("textFormat", {}) or {}).get("foregroundColor")
            if not (fg and fg.get("red", 0) > 0.9 and fg.get("green", 0) < 0.1):
                errors.append(f"STT{stt} chữ đỏ không áp dụng: {fg}")
        hb = (((c(2, 1) or {}).get("userEnteredFormat", {}) or {})
              .get("textFormat", {}) or {}).get("bold")
        if not hb:
            errors.append("header không bold")
    else:
        errors.append("không đọc được format tab gốc")

    # 4e. các tab khác nguyên vẹn
    for t, base in base_other.items():
        now = read_tab(t)
        if now != base:
            errors.append(f"tab '{t}' BỊ THAY ĐỔI ({len(base)} -> {len(now)} dòng)")

    print("\n=== VERIFY ===")
    print(f"  tab gốc: {len(got)} dòng | {sum(1 for r in got for c in r if str(c).strip())} ô có dữ liệu")
    print(f"  STT đọc được: {len(by_stt)} (mong đợi 46) | thừa {len(extra)}")
    print(f"  tab khác nguyên vẹn: {list(base_other)}")
    for e in errors[:15]:
        print("   ✗", e)

    # ── 5. backup thêm bản NGAY TRƯỚC khi ghi (đã có) + ghi nhật ký ─────────
    log = os.path.expanduser("~/opt/thu-ky/_backups/overwrite_log.json")
    entry = {"at": dt.datetime.now().isoformat(timespec="seconds"),
             "sheet_id": SHEET_ID, "tab": ORIG_TAB,
             "backup_used": os.path.basename(bak_path),
             "rows_before": len(bak_rows), "rows_after": len(got),
             "students_written": len(IMAGE), "errors": errors}
    hist = json.load(open(log)) if os.path.exists(log) else []
    hist.append(entry)
    json.dump(hist, open(log, "w"), ensure_ascii=False, indent=1)

    print("\nKẾT QUẢ:", "✓ GHI ĐÈ THÀNH CÔNG — 46/46 khớp verbatim, format đúng, tab khác nguyên vẹn"
          if not errors else f"✗ CÓ {len(errors)} LỆCH")
    print(f"backup để khôi phục: {bak_path}")
    print(f"link: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
