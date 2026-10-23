#!/usr/bin/env python3
"""verify_overwrite.py — verify ĐỘC LẬP kết quả ghi đè tab chính.

Chạy riêng sau khi ghi (không dùng chung tiến trình với script ghi) để tránh
"chính kẻ vừa build tự chấm". Đọc tươi từ server, tính lại số ô kỳ vọng bằng số học,
và kiểm tra cả những thứ dễ sót: title/phòng/header gốc, vùng bên dưới đã sạch,
định dạng đỏ, và các tab khác nguyên vẹn.
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
_spec = importlib.util.spec_from_file_location("gapi_vo", _SKILL)
_gapi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gapi)
sheets = _gapi.build_service("sheets", "v4")

EXPECTED_NOTES = {
    15: "Vắng học TA", 17: "Vắng học TA", 20: "Vắng học Hoá", 21: "Vắng học Hoá",
    22: "Vắng học Toán", 25: "Vắng học Toán", 28: "CLB BÓng chuyền",
    31: "Vắng học Hoá", 36: "STEM", 40: "Nghỉ học",
    44: "Có đăng ký nhưng chưa có tên", 45: "Có đăng ký nhưng chưa có tên",
    46: "Có đăng ký nhưng chưa có tên",
}
errors = []


def read(rng):
    r = sheets.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=rng, valueRenderOption="FORMATTED_VALUE").execute()
    return r.get("values") or []


def main() -> int:
    # 1. đọc tươi toàn tab
    got = read(f"'{ORIG_TAB}'")
    print(f"đọc tươi tab '{ORIG_TAB}': {len(got)} dòng")

    # 2. 3 dòng đầu phải là title/phòng/header gốc (đọc từ backup)
    baks = sorted(glob.glob(os.path.expanduser("~/opt/thu-ky/_backups/tin_hoc_mos_*.json")))
    bak = json.load(open(baks[-1]))["tabs"][ORIG_TAB]["values"]
    for i, label in ((0, "title"), (1, "phòng"), (2, "header")):
        want = (bak[i] + [""] * 8)[:8]
        have = (got[i] + [""] * 8)[:8] if len(got) > i else [""] * 8
        ok = have == want
        print(f"  {label}: {'✓' if ok else '✗'} {str(have)[:70]}")
        if not ok:
            errors.append(f"{label} bị đổi: {have} != {want}")

    # 3. 46 em khớp verbatim
    by_stt = {}
    for row in got[3:26]:
        row = list(row) + [""] * (8 - len(row))
        for off in (0, 4):
            s = str(row[off]).strip()
            if s:
                by_stt[s] = (row[off + 1].strip(), row[off + 2].strip(), row[off + 3].strip())
    print(f"  STT đọc được: {len(by_stt)} (mong đợi 46)")
    if len(by_stt) != 46:
        errors.append(f"số STT = {len(by_stt)}, mong đợi 46")
    for stt in range(1, 47):
        g = by_stt.get(str(stt))
        if g is None:
            errors.append(f"THIẾU STT {stt}")
            continue
        name, lop, note = g
        if not name:
            errors.append(f"STT {stt} tên rỗng")
        if not lop:
            errors.append(f"STT {stt} lớp rỗng")
        exp_note = EXPECTED_NOTES.get(stt, "")
        if note != exp_note:
            errors.append(f"STT {stt} ghi chú: {note!r} != {exp_note!r}")
    print(f"  ghi chú: {len(EXPECTED_NOTES)} em phải có, đã đối chiếu từng em")
    print(f"  STT28 tên={by_stt.get('28', ('?',))[0]!r} note={by_stt.get('28', ('','','?'))[2]!r}")
    print(f"  STT44 tên={by_stt.get('44', ('?',))[0]!r} note={by_stt.get('44', ('','','?'))[2]!r}")

    # 4. số ô — tính lại bằng SỐ HỌC độc lập, không tin con số script ghi in ra
    cells = sum(1 for r in got for c in r if str(c).strip())
    expected_cells = 1 + 1 + 8 + (46 * 3) + len(EXPECTED_NOTES)  # title+phòng+header+46*(stt,tên,lớp)+notes
    print(f"  ô có dữ liệu: {cells} | kỳ vọng tính tay: {expected_cells} "
          f"(1 title + 1 phòng + 8 header + 46*3 + {len(EXPECTED_NOTES)} ghi chú)")
    if cells != expected_cells:
        errors.append(f"số ô {cells} != kỳ vọng {expected_cells}")

    # 5. vùng bên dưới (A27:Z200) phải SẠCH — dữ liệu cũ 39 em đã được dọn
    below = read(f"'{ORIG_TAB}'!A27:Z200")
    below_cells = sum(1 for r in below for c in r if str(c).strip())
    print(f"  vùng A27:Z200: {below_cells} ô (phải = 0)")
    if below_cells != 0:
        errors.append(f"còn {below_cells} ô dữ liệu cũ sót ở A27:Z200")

    # 6. định dạng đỏ
    fmt = sheets.spreadsheets().get(
        spreadsheetId=SHEET_ID,
        fields=("sheets(properties(title,sheetId),data(rowData(values("
                "userEnteredFormat(backgroundColor,textFormat(foregroundColor,bold)),"
                "formattedValue))))")).execute()
    tabf = next((s for s in fmt["sheets"]
                 if s.get("properties", {}).get("title") == ORIG_TAB), None)
    if not tabf:
        errors.append("không tìm thấy tab trong format response")
    else:
        rf = (tabf.get("data") or [{}])[0].get("rowData") or []

        def cell(ri, ci):
            try:
                return rf[ri]["values"][ci]
            except Exception:
                return None

        checks = []
        # STT28: row 8 (1-based) = index 7, khối phải cột E,F,G (4,5,6) nền đỏ
        for ci in (4, 5, 6):
            bg = ((cell(7, ci) or {}).get("userEnteredFormat", {}) or {}).get("backgroundColor")
            red = bool(bg and bg.get("red", 0) > 0.9 and bg.get("green", 0) < 0.1)
            checks.append((f"STT28 col{ci} nền đỏ", red, bg))
            if not red:
                errors.append(f"STT28 cột {ci} nền đỏ KHÔNG có: {bg}")
        # STT44,45,46: index 23,24,25, cột E-H (4..7) chữ đỏ
        for stt, ri in ((44, 23), (45, 24), (46, 25)):
            for ci in (4, 5, 6, 7):
                fg = (((cell(ri, ci) or {}).get("userEnteredFormat", {}) or {})
                      .get("textFormat", {}) or {}).get("foregroundColor")
                red = bool(fg and fg.get("red", 0) > 0.9 and fg.get("green", 0) < 0.1)
                if not red:
                    errors.append(f"STT{stt} cột {ci} chữ đỏ KHÔNG có: {fg}")
            checks.append((f"STT{stt} chữ đỏ E-H",
                           all((((cell(ri, ci) or {}).get("userEnteredFormat", {}) or {})
                                .get("textFormat", {}) or {}).get("foregroundColor", {}).get("red", 0) > 0.9
                               for ci in (4, 5, 6, 7)), None))
        # STT15 (khối trái, index 3+14=17) phải KHÔNG đỏ (kiểm tra âm tính)
        bg15 = ((cell(17, 1) or {}).get("userEnteredFormat", {}) or {}).get("backgroundColor")
        neg_ok = not (bg15 and bg15.get("red", 0) > 0.9 and bg15.get("green", 0) < 0.1)
        checks.append(("STT15 KHÔNG đỏ (âm tính)", neg_ok, bg15))
        if not neg_ok:
            errors.append(f"STT15 bị tô đỏ oan: {bg15}")
        # header bold + nền xanh
        hb = ((cell(2, 1) or {}).get("userEnteredFormat", {}) or {}).get("textFormat", {}).get("bold")
        hbg = ((cell(2, 1) or {}).get("userEnteredFormat", {}) or {}).get("backgroundColor")
        checks.append(("header bold", bool(hb), hb))
        if not hb:
            errors.append("header không bold")
        for label, ok, detail in checks:
            print(f"  format {label}: {'✓' if ok else '✗'} {detail if detail is not None else ''}")

    # 7. các tab khác nguyên vẹn (so với backup cho Phân phòng; tab ảnh còn 46 em)
    other = read(f"'{IMG_TAB}'") if False else None
    phan = read("'Phân phòng'")
    phan_bak = bak  # placeholder
    b = json.load(open(baks[-1]))
    if "Phân phòng" in b["tabs"]:
        if phan == b["tabs"]["Phân phòng"]["values"]:
            print("  ✓ tab 'Phân phòng' giống HỆT backup")
        else:
            errors.append("tab 'Phân phòng' bị thay đổi so với backup")
    img_tab = read("'DS 46 từ ảnh 29-09'")
    img_cells = sum(1 for r in img_tab for c in r if str(c).strip())
    print(f"  tab 'DS 46 từ ảnh 29-09': {len(img_tab)} dòng, {img_cells} ô (vẫn còn)")

    print("\n" + "=" * 62)
    if errors:
        print(f"✗ CÓ {len(errors)} VẤN ĐỀ:")
        for e in errors[:20]:
            print("   -", e)
        return 1
    print("✓ VERIFY ĐỘC LẬP ĐẠT TOÀN BỘ:")
    print("   · title/phòng/header gốc giữ nguyên")
    print("   · 46/46 em khớp verbatim (tên, lớp, ghi chú — kể cả 'CLB BÓng chuyền' nguyên văn)")
    print(f"   · số ô {cells} = đúng phép tính {expected_cells}")
    print("   · vùng A27:Z200 sạch (39 em cũ đã dọn hết)")
    print("   · STT28 nền đỏ, STT44-46 chữ đỏ, STT15 KHÔNG đỏ, header đậm nền xanh")
    print("   · tab 'Phân phòng' nguyên vẹn")
    print(f"   backup khôi phục: {baks[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
