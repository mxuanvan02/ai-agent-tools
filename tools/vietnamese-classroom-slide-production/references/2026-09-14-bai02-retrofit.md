# Retrofit BAI_02 — 2026-09-14 (§1.2 Thiết bị thông minh)

Mẫu retrofit deck cũ → chuẩn BAI_14–30. Dùng cho toàn bộ chuỗi BAI_03→13 tiếp theo.

## Số liệu khóa KHBD §1.2 (tuần 2, tiết 3–4)
- 3 TB cố định: đồng hồ thông minh, camera giám sát kết nối mạng, loa thông minh.
- 2 đối chứng: quạt cơ → KHÔNG phải hệ xử lí thông tin; máy giặt cảm biến khối lượng → CÓ.
- Mỗi TB đủ 3 ô vào–xử lí–ra; 3 đóng góp + 3 ví dụ trường/nhà; mã `B2_NhomXX`.

## Deck cũ (trước retrofit)
- `slide_bai2_rebuild/SLIDE_02_THIET_BI_THONG_MINH_XA_HOI.pptx`: 25 slide, chỉ 3 ghi vở [9,17,22].
- Script cũ `bai_02/rebuild_bai02.py` (430 dòng) tự định nghĩa textbox/box/circle/card/table — không dùng `deck_helper`, header/footer cũ, còn 2 slide bài tập, hộp nền tối 112.7 in².

## Cách retrofit (đã chạy thật)
- `SRC = slide_bai30_rebuild/BAI_30_...pptx` (deck chuẩn mới nhất), `OUTDIR = slide_bai02_retrofit/`, `H.MUC='1.2'`, `H.HEADER='BÀI 02 · THIẾT BỊ THÔNG MINH'`.
- Viết lại script `bai_02_retrofit/rebuild_bai02.py` chỉ import từ `deck_helper`: `card, table_like, note_slide, codebox, section_divider, put_icon`.
- `items` 27 mục + cover = 28 slide; 5 ghi vở `ghivo1–4 + summary`; không slide bài tập; `notes` đủ mọi slide.
- Quét cấm token bài nguồn (5.18/5.19/dien_tich/tien_sau_giam/xep_loai) = 0 hit.

## QA + phát hành
- `ink_clip_check`: 2229 từ, `so_van_de=0`; nền tối thật = 0 (15 box accent nhỏ 9.1 in², không chặn); `empty_notes=[]`.
- Drive `06_SLIDE`: PPTX `2b6b7805…` 438353B / PDF `908db7bf…` 944675B, `all_match:true`, `drive_slides:28`, ghi vở [8,15,21,25,27], `_ARCHIVE/RETROFIT_BAI02_20260914_012330`.

## BAI_02 polish + phát hành lại (cùng ngày, sau feedback giáo viên)
- 2 lỗi chặn tái phát: bìa lộ `\n` thô (literal `\n` = 1) → tách 2 `add_text` riêng; `B2_NhomXX` trơ 7 hit → `B2_NhómXX (VD: B2_Nhóm03)` + dòng `thay XX bằng số nhóm` ở bìa/naming/notes/closing.
- Build lại: 28 slide, QA `forbidden=[]`, `literal/raw=[]`, `empty_notes=[]`, `ink_clip_check` 2257 từ `so_van_de=0`, PDF 28 trang 16:9 `960×540 pt`.
- Phát hành: PPTX `83e9795b…acac` 438593B / PDF `5a6d752b…df4f` 952401B, `all_match:true`, `drive_slides:28`, ghi vở [8,15,21,25,27], `_ARCHIVE/BAI02_VA_LOI_NHOMXX_20260914_063130`.

## BAI_03 retrofit hoàn tất (§1.7 — 12 tệp / 3 thư mục / 45 MB)
- 3 lỗi chặn giống hệt BAI_02, tái hiện 1:1: bìa `TH: SỬ DỤNG THIẾT BỊ\\nSỐ THÔNG DỤNG` (literal-n = 1); `B7_NhomXX` thô 11 hit; `VẬN DỤNG` 3 hit (mục lục ô 04 + `Phần 04/Luyện tập và vận dụng` + section_divider `KIỂM TRA & VẬN DỤNG`).
- Vá: tách bìa 2 dòng; `B7_NhomXX` → `B7_NhómXX (VD: B7_Nhóm03)` 11 vị trí (cover label, requirements, naming 3 dòng, closing, cover/notes naming); `VẬN DỤNG` → `ỨNG DỤNG` + `Phần 04/Kiểm tra và ứng dụng` + divider `KIỂM TRA & ỨNG DỤNG`; patch xong `raw=0`, `VAN DUNG=0`, `literal-n=0`, COMPILE OK.
- Build lại: 29 slide, `forbidden=[]`, `literal/raw=[]`, `empty_notes=[]`, ghi vở [9,15,21,26,28], `ink_clip_check` 2183 từ `so_van_de=0`, PDF 29 trang 16:9.
- Phát hành: PPTX `7842684d…302c` 406890B / PDF `503f6cf8…185` 924535B, `all_match:true`, `drive_slides:29`, `_ARCHIVE/BAI03_VA_LOI_CHUNG_20260914_063323`.

## Checklist tái phát cho mọi bài retrofit (rút từ BAI_02→BAI_03)
1. Quét bìa literal `\\n` trước mọi build — tách 2 `add_text`, không nhúng `\n` trong một textbox.
2. Quét mã nhóm thô `B\d+_NhomXX` không dấu — mọi nơi hiện mã phải có `(VD: Bxx_Nhóm0y)` + dòng thay XX.
3. Quét cấm `Vận dụng/Luyện tập/Bài tập` trên tiêu đề slide (không quét notes) — Phần 04 đặt `Kiểm tra và ứng dụng`, mục lục ô 04 đặt `ỨNG DỤNG`.
4. `titles sample` toàn `TRƯỜNG THPT THUẬN HOÁ` là âm giả dò (header đứng trước) — soi text từng slide nghi ngờ, không kết luận bằng sample.
5. Nền tối `2A6FBE lum 0.4` ở vạch accent/thanh nhãn là âm giả — so baseline deck đạt (BAI_23: 26 box / 52.9 in²); BAI_02 15 box / 9.1 in² và BAI_03 10 box / 7.3 in² là sạch hơn, không chặn.
