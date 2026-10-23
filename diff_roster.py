#!/usr/bin/env python3
"""diff_roster.py — so sánh danh sách TRONG ẢNH (46 HS) với sheet TIN HỌC MOS & AI (39 HS).

Mục đích: biết chính xác ghi đè sẽ MẤT gì, trước khi đụng vào dữ liệu điểm danh thật.
CHỈ ĐỌC. In báo cáo diff.
"""
import glob
import json
import os
import unicodedata

SHEET_ID = "1Ri5reuE8Rg4Fgheao0AF3HCEnaelKnVExXz6R4F3TwI"
TAB = "Tin học MOS & AI"

# ── Danh sách TRONG ẢNH (đã verify 2 lần đọc độc lập, khớp nhau) ──────────────
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
    (28, "Phan Việt Hoàng", "12/2", "CLB BÓng chuyền"),   # dòng tô đỏ
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
    (44, "Tô Anh Thư", "10/1", "Có đăng ký nhưng chưa có tên"),   # chữ đỏ
    (45, "Tôn Thất Văn Quốc Anh", "12/2", "Có đăng ký nhưng chưa có tên"),  # chữ đỏ
    (46, "Trịnh Quốc Thiên Bảo", "12/2", "Có đăng ký nhưng chưa có tên"),   # chữ đỏ
]


def norm(s: str) -> str:
    """Chuẩn hoá tên để so sánh: bỏ dấu, lower, collapse space."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("đ", "d").replace("Đ", "D")
    return " ".join(s.lower().split())


def load_sheet():
    f = sorted(glob.glob(os.path.expanduser("~/opt/thu-ky/_backups/tin_hoc_mos_*.json")))[-1]
    d = json.load(open(f))
    rows = d["tabs"][TAB]["values"]
    left, right = [], []
    for r in rows[3:]:  # bỏ 2 dòng title + 1 dòng header
        cells = list(r) + [""] * (8 - len(r))
        if str(cells[0]).strip():
            left.append((str(cells[0]).strip(), str(cells[1]).strip(),
                         str(cells[2]).strip(), str(cells[3]).strip()))
        if str(cells[4]).strip():
            right.append((str(cells[4]).strip(), str(cells[5]).strip(),
                          str(cells[6]).strip(), str(cells[7]).strip()))
    return f, left, right


def main():
    f, left, right = load_sheet()
    sheet_all = left + right
    print(f"backup dùng: {os.path.basename(f)}")
    print(f"SHEET: {len(sheet_all)} học sinh (trái {len(left)} + phải {len(right)})")
    print(f"ẢNH  : {len(IMAGE)} học sinh")

    sheet_names = {norm(n): (stt, n, lop, note) for stt, n, lop, note in sheet_all}
    img_names = {norm(n): (stt, n, lop, note) for stt, n, lop, note in IMAGE}

    only_sheet = [v for k, v in sheet_names.items() if k not in img_names]
    only_image = [v for k, v in img_names.items() if k not in sheet_names]
    both = [k for k in sheet_names if k in img_names]

    print(f"\n=== CÓ TRONG SHEET NHƯNG KHÔNG TRONG ẢNH: {len(only_sheet)} (SẼ MẤT nếu ghi đè) ===")
    for stt, n, lop, note in sorted(only_sheet, key=lambda x: int(x[0]) if x[0].isdigit() else 999):
        print(f"  STT {stt:>3} | {n:<28} | {lop:<5} | note sheet: {note[:32]}")

    print(f"\n=== CÓ TRONG ẢNH NHƯNG CHƯA TRONG SHEET: {len(only_image)} (MỚI) ===")
    for stt, n, lop, note in sorted(only_image, key=lambda x: x[0]):
        print(f"  STT {stt:>3} | {n:<28} | {lop:<5} | note ảnh: {note[:32]}")

    print(f"\n=== TRÙNG TÊN CẢ HAI: {len(both)} ===")
    # trong số trùng, bao nhiêu có điểm danh (cột D/H) -> dữ liệu thật sẽ bị mất
    att = [(sheet_names[k][0], sheet_names[k][1], sheet_names[k][2], sheet_names[k][3])
           for k in both if sheet_names[k][3].strip()]
    print(f"  trong đó {len(att)} em CÓ ghi chú/điểm danh ở sheet (dữ liệu thật):")
    for stt, n, lop, note in sorted(att, key=lambda x: int(x[0]) if x[0].isdigit() else 999):
        img = img_names[k] if False else None
        print(f"    STT {stt:>3} | {n:<26} | {lop:<5} | sheet: {note[:34]}")

    # note của sheet có bao nhiêu ô khác rỗng (dữ liệu điểm danh tổng)
    all_notes = [x[3] for x in sheet_all if x[3].strip()]
    print(f"\n  TỔNG ô điểm danh/ghi chú đang có trong sheet: {len(all_notes)}")
    print(f"  giá trị: {sorted(set(all_notes))}")

    # STT lệch nhau ở em trùng tên (do danh sách khác độ dài)
    shifted = [(sheet_names[k][0], img_names[k][0], sheet_names[k][1]) for k in both
               if str(sheet_names[k][0]) != str(img_names[k][0])]
    print(f"\n=== EM TRÙNG TÊN NHƯNG STT LỆCH NHAU: {len(shifted)} ===")
    for s_stt, i_stt, n in sorted(shifted, key=lambda x: int(x[1]))[:12]:
        print(f"  {n:<28} | sheet STT {s_stt:>3} -> ảnh STT {i_stt:>3}")


if __name__ == "__main__":
    main()
