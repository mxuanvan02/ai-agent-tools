#!/usr/bin/env python3
"""import_roster_from_image.py — nhập 46 học sinh (đã transcribe verbatim từ ảnh) vào
một TAB MỚI trong sheet TIN HỌC MOS & AI.

An toàn:
  * KHÔNG đụng tab gốc 'Tin học MOS & AI' (39 em + 21 ô điểm danh) — chỉ ADD tab mới.
  * Nếu tab đích đã tồn tại -> DỪNG, không ghi đè âm thầm.
  * Ghi xong VERIFY bằng cách đọc lại từng ô và so khớp 100% với dữ liệu nguồn.

Bố cục giống hệt ảnh: 2 khối song song (trái STT 1-23, phải STT 24-46),
mỗi khối STT | Họ và tên | Lớp | Ghi chú.
Định dạng theo ảnh: STT 28 tô nền đỏ; STT 44-46 chữ đỏ; header nền xanh nhạt + đậm.
"""
import datetime as dt
import importlib.util
import json
import os
import sys

SHEET_ID = "1Ri5reuE8Rg4Fgheao0AF3HCEnaelKnVExXz6R4F3TwI"
NEW_TAB = "DS 46 từ ảnh 29-09"

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
_spec = importlib.util.spec_from_file_location("gapi_import", _SKILL)
_gapi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gapi)
sheets = _gapi.build_service("sheets", "v4")

# ── Dữ liệu verbatim từ ảnh (đã verify bằng 2 lần đọc độc lập, tên khớp nhau) ──
# (STT, Họ và tên, Lớp, Ghi chú)  — ghi chú giữ NGUYÊN VĂN kể cả lỗi chính tả nguồn
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
    (28, "Phan Việt Hoàng", "12/2", "CLB BÓng chuyền"),          # dòng tô đỏ trong ảnh
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
    (44, "Tô Anh Thư", "10/1", "Có đăng ký nhưng chưa có tên"),  # chữ đỏ
    (45, "Tôn Thất Văn Quốc Anh", "12/2", "Có đăng ký nhưng chưa có tên"),  # chữ đỏ
    (46, "Trịnh Quốc Thiên Bảo", "12/2", "Có đăng ký nhưng chưa có tên"),   # chữ đỏ
]

TITLE = "DANH SÁCH HỌC SINH THAM GIA CLB TIN HỌC MOS & AI"
PROVENANCE = ("Nguồn: nhập từ ảnh anh Văn gửi 29/09/2026 · 46 học sinh · "
              "Tab gốc 'Tin học MOS & AI' (39 em + điểm danh) giữ nguyên, không đụng tới")
HEADER = ["STT", "Họ và tên", "Lớp", "Ghi chú", "STT", "Họ và tên", "Lớp", "Ghi chú"]

DATA_START_ROW = 4      # 1-based: row 1 title, row 2 provenance, row 3 header
LEFT = IMAGE[:23]       # STT 1-23
RIGHT = IMAGE[23:]      # STT 24-46


def build_rows():
    rows = []
    for i in range(23):
        l = LEFT[i]
        r = RIGHT[i]
        rows.append([str(l[0]), l[1], l[2], l[3], str(r[0]), r[1], r[2], r[3]])
    return rows


def row_of(stt: int) -> int:
    """STT 1-23 và 24-46 đều nằm trên cùng dải dòng; trả về row 1-based."""
    return DATA_START_ROW + ((stt - 1) if stt <= 23 else (stt - 24))


def main() -> int:
    # ── 0. kiểm tra tab chưa tồn tại (không ghi đè âm thầm) ──────────────────
    meta = sheets.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    existing = [s["properties"]["title"] for s in meta.get("sheets", [])]
    print("tabs hiện có:", existing)
    if NEW_TAB in existing:
        print(f"✗ DỪNG: tab '{NEW_TAB}' đã tồn tại. Không ghi đè âm thầm.")
        print("  Đổi tên tab trong script, hoặc xóa tab đó trước nếu muốn nhập lại.")
        return 2

    # ── 1. tạo tab mới ──────────────────────────────────────────────────────
    add = sheets.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={
        "requests": [{
            "addSheet": {"properties": {
                "title": NEW_TAB,
                "gridProperties": {"rowCount": 60, "columnCount": 10, "frozenRowCount": 3},
            }}
        }]
    }).execute()
    new_id = None
    for r in add.get("replies", []):
        if "addSheet" in r:
            new_id = r["addSheet"]["properties"]["sheetId"]
    print(f"✓ đã tạo tab '{NEW_TAB}' (sheetId={new_id})")

    # ── 2. ghi giá trị ──────────────────────────────────────────────────────
    values = [[TITLE] + [""] * 7,
              [PROVENANCE] + [""] * 7,
              HEADER] + build_rows()
    sheets.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f"'{NEW_TAB}'!A1",
        valueInputOption="USER_ENTERED", body={"values": values}).execute()
    print(f"✓ đã ghi {len(values)} dòng (2 tiêu đề + 1 header + {len(values)-3} dòng dữ liệu)")

    # ── 3. định dạng theo ảnh ───────────────────────────────────────────────
    RED = {"red": 1, "green": 0, "blue": 0}
    LIGHT_BLUE = {"red": 0.80, "green": 0.88, "blue": 0.98}
    BORDER = {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}}
    reqs = []

    # 3a. header: đậm + nền xanh nhạt
    reqs.append({"repeatCell": {
        "range": {"sheetId": new_id, "startRowIndex": 2, "endRowIndex": 3,
                  "startColumnIndex": 0, "endColumnIndex": 8},
        "cell": {"userEnteredFormat": {
            "textFormat": {"bold": True}, "backgroundColor": LIGHT_BLUE}},
        "fields": "userEnteredFormat(textFormat.bold,backgroundColor)"}})

    # 3b. tiêu đề đậm
    reqs.append({"repeatCell": {
        "range": {"sheetId": new_id, "startRowIndex": 0, "endRowIndex": 1,
                  "startColumnIndex": 0, "endColumnIndex": 1},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 13}}},
        "fields": "userEnteredFormat.textFormat"}})

    # 3c. provenance in nghiêng xám
    reqs.append({"repeatCell": {
        "range": {"sheetId": new_id, "startRowIndex": 1, "endRowIndex": 2,
                  "startColumnIndex": 0, "endColumnIndex": 1},
        "cell": {"userEnteredFormat": {"textFormat": {
            "italic": True, "fontSize": 9,
            "foregroundColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}}},
        "fields": "userEnteredFormat.textFormat"}})

    # 3d. viền đen cho 2 khối bảng (KHÔNG viền cột ghi chú, đúng như ảnh)
    for c0, c1 in ((0, 3), (4, 7)):
        reqs.append({"repeatCell": {
            "range": {"sheetId": new_id, "startRowIndex": 2, "endRowIndex": 26,
                      "startColumnIndex": c0, "endColumnIndex": c1},
            "cell": {"userEnteredFormat": {"borders": {
                "top": BORDER, "bottom": BORDER, "left": BORDER, "right": BORDER}}},
            "fields": "userEnteredFormat.borders"}})

    # 3e. STT + Lớp căn giữa
    for c in (0, 2, 4, 6):
        reqs.append({"repeatCell": {
            "range": {"sheetId": new_id, "startRowIndex": 3, "endRowIndex": 26,
                      "startColumnIndex": c, "endColumnIndex": c + 1},
            "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
            "fields": "userEnteredFormat.horizontalAlignment"}})

    # 3f. STT 28 -> TÔ NỀN ĐỎ (cột STT/tên/lớp = E,F,G), ghi chú để chữ đen như ảnh
    r28 = row_of(28)
    reqs.append({"repeatCell": {
        "range": {"sheetId": new_id, "startRowIndex": r28 - 1, "endRowIndex": r28,
                  "startColumnIndex": 4, "endColumnIndex": 7},
        "cell": {"userEnteredFormat": {"backgroundColor": RED}},
        "fields": "userEnteredFormat.backgroundColor"}})

    # 3g. STT 44,45,46 -> CHỮ ĐỎ (cả ghi chú), đúng như ảnh
    for stt in (44, 45, 46):
        rr = row_of(stt)
        reqs.append({"repeatCell": {
            "range": {"sheetId": new_id, "startRowIndex": rr - 1, "endRowIndex": rr,
                      "startColumnIndex": 4, "endColumnIndex": 8},
            "cell": {"userEnteredFormat": {"textFormat": {"foregroundColor": RED}}},
            "fields": "userEnteredFormat.textFormat.foregroundColor"}})

    # 3h. độ rộng cột
    widths = [(0, 1, 45), (1, 2, 215), (2, 3, 55), (3, 4, 230),
              (4, 5, 45), (5, 6, 215), (6, 7, 55), (7, 8, 230)]
    for start, end, px in widths:
        reqs.append({"updateDimensionProperties": {
            "range": {"sheetId": new_id, "dimension": "COLUMNS",
                      "startIndex": start, "endIndex": end},
            "properties": {"pixelSize": px}, "fields": "pixelSize"}})

    sheets.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body={"requests": reqs}).execute()
    print(f"✓ đã áp dụng {len(reqs)} yêu cầu định dạng (đỏ STT28 nền, STT44-46 chữ, header, viền, canh giữa, width)")

    # ── 4. VERIFY: đọc lại và so khớp 100% từng ô ───────────────────────────
    resp = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{NEW_TAB}'!A1:H26",
        valueRenderOption="FORMATTED_VALUE").execute()
    got = resp.get("values") or []
    errors = []

    # 4a. header
    hdr = (got[2] + [""] * 8)[:8] if len(got) > 2 else []
    if hdr != HEADER:
        errors.append(f"header lệch: {hdr}")
    # 4b. từng em
    by_stt = {}
    for row in got[3:]:
        row = list(row) + [""] * (8 - len(row))
        for off in (0, 4):
            stt = str(row[off]).strip()
            if stt:
                by_stt[stt] = (row[off + 1].strip(), row[off + 2].strip(), row[off + 3].strip())
    for stt, name, lop, note in IMAGE:
        g = by_stt.get(str(stt))
        if g is None:
            errors.append(f"THIẾU STT {stt} ({name})")
            continue
        if g[0] != name:
            errors.append(f"STT {stt} tên lệch: sheet={g[0]!r} ảnh={name!r}")
        if g[1] != lop:
            errors.append(f"STT {stt} lớp lệch: sheet={g[1]!r} ảnh={lop!r}")
        if g[2] != note:
            errors.append(f"STT {stt} ghi chú lệch: sheet={g[2]!r} ảnh={note!r}")
    extra = set(by_stt) - {str(s) for s, _, _, _ in IMAGE}
    if extra:
        errors.append(f"dòng thừa không có trong ảnh: {sorted(extra)}")

    # 4c. verify định dạng đỏ (đọc cell background/font thật)
    fmt = sheets.spreadsheets().get(
        spreadsheetId=SHEET_ID,
        fields=("sheets(data(rowData(values("
                "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat.foregroundColor))))")
    ).execute()
    tab = next((s for s in fmt["sheets"] if s["properties"]["title"] == NEW_TAB), None)
    if tab:
        rows_fmt = tab["data"][0]["rowData"]

        def bg(ri, ci):
            try:
                c = rows_fmt[ri]["values"][ci]
                return c.get("userEnteredFormat", {}).get("backgroundColor")
            except Exception:
                return None

        def fg(ri, ci):
            try:
                c = rows_fmt[ri]["values"][ci]
                return c.get("userEnteredFormat", {}).get("textFormat", {}).get("foregroundColor")
            except Exception:
                return None

        b28 = bg(row_of(28) - 1, 5)   # cột F (tên) dòng STT28
        if not (b28 and b28.get("red", 0) > 0.9 and b28.get("green", 0) < 0.1):
            errors.append(f"STT28 nền đỏ KHÔNG áp dụng: {b28}")
        f44 = fg(row_of(44) - 1, 5)
        if not (f44 and f44.get("red", 0) > 0.9 and f44.get("green", 0) < 0.1):
            errors.append(f"STT44 chữ đỏ KHÔNG áp dụng: {f44}")
    else:
        errors.append("không đọc lại được tab mới để kiểm định dạng")

    # 4d. tab gốc còn nguyên?
    meta2 = sheets.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    tabs_now = [s["properties"]["title"] for s in meta2.get("sheets", [])]
    orig = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="'Tin học MOS & AI'",
        valueRenderOption="FORMATTED_VALUE").execute()
    orig_rows = orig.get("values") or []
    orig_cells = sum(1 for r in orig_rows for c in r if str(c).strip())
    print(f"\n=== VERIFY ===")
    print(f"  tabs sau khi ghi: {tabs_now}")
    print(f"  tab gốc 'Tin học MOS & AI': {len(orig_rows)} dòng, {orig_cells} ô khác rỗng (trước: 23 dòng, 148 ô)")
    if orig_cells != 148 or len(orig_rows) != 23:
        errors.append(f"TAB GỐC BỊ THAY ĐỔI: {len(orig_rows)} dòng/{orig_cells} ô (kỳ vọng 23/148)")
    else:
        print("  ✓ tab gốc NGUYÊN VẸN")
    print(f"  đối chiếu {len(IMAGE)} em + header + định dạng: {len(errors)} lỗi")
    for e in errors[:12]:
        print("   ✗", e)

    link = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid={new_id}"
    print(f"\nLINK TAB MỚI: {link}")
    print("KẾT QUẢ:", "✓ THÀNH CÔNG — 46/46 em khớp verbatim, tab gốc nguyên vẹn"
          if not errors else f"✗ CÓ {len(errors)} LỆCH — xem chi tiết trên")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
