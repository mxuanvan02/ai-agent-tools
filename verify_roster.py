#!/usr/bin/env python3
"""verify_roster.py — VERIFY (chỉ đọc) kết quả nhập 46 em vào tab mới.

Bước ghi đã chạy xong nhưng script import crash ở đoạn verify (fields mask thiếu
properties.title). Script này verify độc lập, không ghi gì.

Kiểm 4 thứ:
  1. 46/46 em khớp verbatim (STT, tên, lớp, ghi chú) — so từng ký tự
  2. định dạng đỏ: STT28 nền đỏ, STT44-46 chữ đỏ
  3. tab gốc 'Tin học MOS & AI' nguyên vẹn (23 dòng / 148 ô)
  4. header + không có dòng thừa
"""
import glob
import importlib.util
import json
import os
import sys

SHEET_ID = "1Ri5reuE8Rg4Fgheao0AF3HCEnaelKnVExXz6R4F3TwI"
NEW_TAB = "DS 46 từ ảnh 29-09"
ORIG_TAB = "Tin học MOS & AI"

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
_spec = importlib.util.spec_from_file_location("gapi_verify", _SKILL)
_gapi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gapi)
sheets = _gapi.build_service("sheets", "v4")

EXPECTED = [
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
HEADER = ["STT", "Họ và tên", "Lớp", "Ghi chú", "STT", "Họ và tên", "Lớp", "Ghi chú"]
errors = []


def main() -> int:
    meta = sheets.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    print("tabs trong sheet:", tabs)
    if NEW_TAB not in tabs:
        print(f"✗ KHÔNG TÌM THẤY tab '{NEW_TAB}' — bước ghi đã thất bại")
        return 2

    # ── 1. giá trị ──────────────────────────────────────────────────────────
    resp = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{NEW_TAB}'!A1:H30",
        valueRenderOption="FORMATTED_VALUE").execute()
    got = resp.get("values") or []
    print(f"đọc được {len(got)} dòng")

    hdr = (got[2] + [""] * 8)[:8] if len(got) > 2 else []
    print("header:", hdr)
    if hdr != HEADER:
        errors.append(f"header lệch: {hdr}")

    by_stt = {}
    for row in got[3:]:
        row = list(row) + [""] * (8 - len(row))
        for off in (0, 4):
            stt = str(row[off]).strip()
            if stt:
                by_stt[stt] = (row[off + 1].strip(), row[off + 2].strip(), row[off + 3].strip())

    for stt, name, lop, note in EXPECTED:
        g = by_stt.get(str(stt))
        if g is None:
            errors.append(f"THIẾU STT {stt} ({name})")
            continue
        if g[0] != name:
            errors.append(f"STT {stt} TÊN lệch: sheet={g[0]!r} ảnh={name!r}")
        if g[1] != lop:
            errors.append(f"STT {stt} LỚP lệch: sheet={g[1]!r} ảnh={lop!r}")
        if g[2] != note:
            errors.append(f"STT {stt} GHI CHÚ lệch: sheet={g[2]!r} ảnh={note!r}")
    extra = set(by_stt) - {str(s) for s, _, _, _ in EXPECTED}
    if extra:
        errors.append(f"dòng thừa không có trong ảnh: {sorted(extra)}")
    print(f"đối chiếu giá trị: {len(EXPECTED)} em mong đợi, đọc được {len(by_stt)} STT, thừa {len(extra)}")

    # ── 2. định dạng (fields mask ĐÚNG — kèm properties.title + sheetId) ─────
    fmt = sheets.spreadsheets().get(
        spreadsheetId=SHEET_ID,
        fields=("sheets(properties(title,sheetId),data(rowData(values("
                "userEnteredFormat(backgroundColor,textFormat(foregroundColor,bold)),"
                "formattedValue))))")
    ).execute()
    tab = next((s for s in fmt["sheets"]
                if s.get("properties", {}).get("title") == NEW_TAB), None)
    if tab is None:
        errors.append("không tìm thấy tab mới trong response format")
    else:
        sid_new = tab["properties"]["sheetId"]
        rows_fmt = (tab.get("data") or [{}])[0].get("rowData") or []

        def cell(ri, ci):
            try:
                return rows_fmt[ri]["values"][ci]
            except Exception:
                return None

        # STT 28 nằm ở khối phải (cột E-H = index 4-7), row = 4 + (28-24) = 8 (1-based) -> index 7
        c28 = cell(7, 5)   # cột F = tên STT28
        bg = (c28 or {}).get("userEnteredFormat", {}).get("backgroundColor") if c28 else None
        print("STT28 nền:", bg, "| formattedValue:", (c28 or {}).get("formattedValue"))
        if not (bg and bg.get("red", 0) > 0.9 and bg.get("green", 0) < 0.1):
            errors.append(f"STT28 nền ĐỎ không áp dụng: {bg}")

        # STT 44: row = 4 + (44-24) = 24 (1-based) -> index 23, cột F
        for stt, idx in ((44, 23), (45, 24), (46, 25)):
            c = cell(idx, 5)
            fg = (c or {}).get("userEnteredFormat", {}).get("textFormat", {}).get("foregroundColor") if c else None
            print(f"STT{stt} chữ:", fg, "| formattedValue:", (c or {}).get("formattedValue"))
            if not (fg and fg.get("red", 0) > 0.9 and fg.get("green", 0) < 0.1):
                errors.append(f"STT{stt} chữ ĐỎ không áp dụng: {fg}")

        # header bold
        h = cell(2, 1)
        hb = (h or {}).get("userEnteredFormat", {}).get("textFormat", {}).get("bold") if h else None
        print("header bold:", hb)
        if not hb:
            errors.append("header không bold")
        print("sheetId tab mới:", sid_new)

    # ── 3. tab gốc nguyên vẹn? ──────────────────────────────────────────────
    orig = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{ORIG_TAB}'",
        valueRenderOption="FORMATTED_VALUE").execute()
    orows = orig.get("values") or []
    ocells = sum(1 for r in orows for c in r if str(c).strip())
    print(f"tab gốc '{ORIG_TAB}': {len(orows)} dòng, {ocells} ô khác rỗng (kỳ vọng 23 / 148)")
    if len(orows) != 23 or ocells != 148:
        errors.append(f"TAB GỐC BỊ THAY ĐỔI: {len(orows)} dòng/{ocells} ô (kỳ vọng 23/148)")

    # ── 4. so với backup gốc (đảm bảo byte-level không đổi) ─────────────────
    baks = sorted(glob.glob(os.path.expanduser("~/opt/thu-ky/_backups/tin_hoc_mos_*.json")))
    if baks:
        b = json.load(open(baks[-1]))
        bo = b["tabs"][ORIG_TAB]["values"]
        if bo == orows:
            print(f"✓ tab gốc GIỐNG HỆT backup ({os.path.basename(baks[-1])})")
        else:
            errors.append("tab gốc khác backup — có thay đổi ngoài ý muốn")
            for i, (x, y) in enumerate(zip(bo, orows)):
                if x != y:
                    errors.append(f"  dòng {i+1}: backup={x} now={y}")
                    break

    print("\n" + "=" * 60)
    if errors:
        print(f"✗ CÓ {len(errors)} VẤN ĐỀ:")
        for e in errors[:20]:
            print("   -", e)
        return 1
    print("✓ VERIFY ĐẠT: 46/46 em khớp verbatim · header đúng · định dạng đỏ đúng "
          "(STT28 nền, STT44-46 chữ) · tab gốc nguyên vẹn giống hệt backup")
    print(f"  link: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
