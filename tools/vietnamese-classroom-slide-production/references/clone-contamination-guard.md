# Clone Contamination Guard — Bài 22 → Bài 23 (2026-09-13)

## Sự cố
`rebuild_bai23.py` được tạo bằng `replace('Bài 22','Bài 23')` + vài `replace` lẻ tẻ trên file Bài 22. Kết quả:
- `OUTDIR` vẫn trỏ `$HOME/slide_bai22_rebuild` → deck Bài 23 ghi đè thư mục Bài 22, `SLIDE_22`/`SLIDE_23` lẫn nhau.
- `H.MUC='5.27'` đổi nhưng `PROG`, `CODE_SERIES` (`declare`/`returnvsprint`/`reuse` với `dien_tich(3,4)=12, 30, 20.0`), `items`, `cover` (label `B26_NhomXX.py`, output `12·30·20.0`), các nhánh `elif kind ==` (`toc`/`requirements`/`actual`/`naming`/`pitfall`/`application`), `notes` dict vẫn là Bài 22.
- QA sau dựng: `forbidden scan` vẫn hit `B26` (3 lần), `12/30/20.0`, `dien_tich`; `B27`/`180 000`/`200 000` = 0 hit. Checker tưởng đạt vì `so_van_de=0` nhưng nội dung sai nguồn.

## Bài học
Đổi `H.MUC/H.HEADER` + tên file không đủ. Một deck clone phải quét toàn bộ script/notes/slide text của bài nguồn.

## Checklist bắt buộc khi clone từ deck trước
Duyệt tuần tự và đối chiếu với KHBD mới; không dùng `replace` hàng loạt:

1. `H.MUC`, `H.HEADER`
2. `SRC` / `OUTDIR` / `OUT` — mỗi bài một thư mục `slide_bai<NN>_rebuild` riêng, không chia sẻ.
3. `core_properties` — `title`/`subject`/`comments` (tuần-tiết)
4. `PROG` + toàn bộ `CODE_SERIES` — `label`/`lines`/`output`/`steps`
5. `items` — `heading`/`kicker`/`kind` theo 4 phần của KHBD mới
6. `cover` — `BÀI · MỤC`, tiêu đề lớn, 3 bullet, `codebox` `label`/`output`
7. Mọi nhánh `elif kind ==` — `toc`, `requirements`, `actual`, `naming`, `pitfall`, `application`, `ghivo*`, `summary`, `closing`, `sec*`
8. `notes` dict — mọi key `cover`/`objectives`/`requirements`/`toc`/`ghivo*`/...

## QA chặn
- **Trước dựng:** `grep -n "B26\|12.*30\|dien_tich\|MỤC 5.26"` trên script nguồn để lập danh sách token cấm.
- **Sau dựng:** `forbidden scan` trên *cả* `pptx` text + `pdf` text + `notes`:
  - 0 hit với mọi token bài nguồn (kể cả không dấu)
  - đủ hit với token bài mới (`B27`, `180 000`, `150 000`, `200 000`, `tham số`/`đối số`)
- Nếu còn sót → sửa script, xóa artifact cũ (`rm .../BAI_23_*` trong thư mục sai), dựng lại, rồi mới `publish`.

## Ghi vở & note_slide — hai lỗi cùng phiên
- **Ghi vở phải là khái niệm, không phải bảng số.** Bài 14–16 ban đầu ghi `55, 110, 55` / `9.0, 8.0...` → user sửa: ghi vở là định nghĩa + ý chính của mục (ví dụ Bài 16-phần 02: *Biến tích luỹ là biến giữ kết quả trung gian...*). Quy tắc đã ghi ở SKILL.md §5a/5b.
- **Bug `note_slide`:** `icon` tham số che hàm toàn cục `icon()` → `TypeError`; và `y=3.115` cố định cho 3 dòng ghi vở → số 2,3 đè lên số 1. Sửa: tham số đổi thành `pic`, `y = 3.085 + j*0.9`.

## Đổi tên Drive `SLIDE_xx` → `BAI_<NN>_<TEN>` (cùng phiên)
Snapshot toàn bộ `06_SLIDE/*.pptx|*.pdf` vào `_ARCHIVE/LEGACY_SLIDE_NAMES_<ts>` + đối chiếu MD5/SHA-256 trước khi `rclone moveto`. Nếu `archive_count != root_count` thì dừng. Dùng list args (`['rclone',...]`), không `shell=True`.
