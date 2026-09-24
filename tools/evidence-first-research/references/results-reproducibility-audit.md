# Kiểm chứng số liệu/bảng/biểu manuscript phải khớp code chạy thật

Dùng khi người dùng hỏi đại loại "số liệu/bảng/biểu trong bài đã chạy đúng chuẩn chưa",
"verify số liệu", "bổ sung source code", "tất cả phải thật" cho một manuscript.
Tiêu chí cốt lõi của người dùng: **KHÔNG được có số/hình đặt tay (placeholder, vẽ bằng
hàm tổng hợp, hard-code)** — mọi con số trong bài phải tái lập được từ code chạy thật.

## Quy trình (đã chạy thành công)

1. **Định vị manuscript + nguồn số liệu.** Đọc hết `.tex` (đừng dừng ở 1 phần).
   Liệt kê: bảng nào, hình nào, con số % nào trong text. Tìm thư mục code đi kèm
   (`simulation_code/`, repo GitHub reproduction…).

2. **Phân loại nguồn của mỗi con số** thành 3 nhóm:
   - **THẬT**: sinh ra từ script chạy mô hình thật (TD3/FedAvg/simulation) → `results.json`.
   - **VẼ TAY (placeholder)**: hình/số sinh bằng `np.exp`, hằng số hard-code, noise
     giả trong file kiểu `generate_all_plots.py` — KHÔNG chạy mô hình. Đây là rủi ro
     lớn nhất: reviewer mở file sinh hình sẽ thấy ngay.
   - **MỒ CÔI**: số trong text không có nguồn từ code VÀ thường mâu thuẫn với chính
     bảng của bài (ví dụ "giảm 27.3%" trong khi bảng cho 3.4 vs 7.1 = 52%). Phải gỡ
     hoặc sửa cho khớp bảng/`results.json`.

3. **Chạy thật, đừng đọc README rồi tin.** Clone repo → dựng venv (`uv venv` +
   `uv pip install`; torch dùng wheel **CPU-only** `--index-url .../whl/cpu` cho nhẹ,
   cài nền `background=true notify_on_complete=true` vì torch nặng) → chạy
   `run_simulation.py` → lấy số canonical từ `results.json` (không lấy từ bảng README,
   README có thể lệch).

4. **Đồng bộ .tex theo `results.json`.** Thay hình placeholder bằng hình repo thật
   (`fig*.png`), thay block số/bảng, GỠ số mồ côi. Sửa NHẤT QUÁN ở **mọi** nơi: abstract,
   contribution bullets, body, bảng Summary, Conclusion — đừng sót. Sau đó grep lại các
   số cũ (vd 18.2/45.6/12.3/74.8) để chắc không còn sót; grep các số mới để xác nhận
   xuất hiện đủ.

5. **Nếu thiếu metric → mở rộng code để sinh THẬT, tuyệt đối không hard-code số vào bài.**
   Bổ sung experiment vào module tương ứng (vd `digital_twin.py`), thêm hằng số chi phí
   có chú thích vào `config.py`, tính metric như HÀM của event quan sát được từ rollout.
   Chạy lại full pipeline, lấy số mới, cập nhật bài. Số mới có thể lệch số cũ (74.8→73.8)
   — đó là dấu hiệu tốt (số thật), cập nhật cho khớp.

6. **Build kiểm chứng**: `latexmk` rc=0, đếm trang, kiểm "undefined references/citations"
   = NONE. Font warning kiểu `TU/ptm ... undefined` dưới xelatex là vô hại.

## Pitfalls

- **Hai bảng cùng đại lượng nhưng lệch đơn vị/giá trị** (vd payload MB vs KB) → reviewer soi ra. Thống nhất.
- **Markdown lọt vào LaTeX**: `**...**` in ra dấu sao thay vì in đậm → đổi thành `\textbf{...}`. Grep `\*\*` để quét sạch.
- **"publicly available" mà repo public chưa khớp code mới**: nếu bài tuyên bố source code
  tái lập mọi kết quả nhưng code vừa sửa mới chỉ ở bản clone `/tmp`, repo GitHub vẫn cũ →
  reviewer clone về KHÔNG tái lập được. Phải flag: (A) push code (chỉ code, không
  results/drafts) — CẦN NGƯỜI DÙNG DUYỆT trước khi push, (B) người dùng tự push, (C) gỡ câu
  "publicly available". KHÔNG tự push khi chưa có phép (xem gate artifact của người dùng).

## Affiliation/author/funding lấy từ bài cũ — không bịa

Khi điền affiliation/tác giả/funding "theo mấy bài trước": grep author block + `\thanks`/
`\affil` trong các manuscript cũ của người dùng (ACM iccsit, IEEEAccess, bài probe-transmit, bài bandwidth-scheduling).
- Lấy ĐÚNG: tên đơn vị, ORCID, email, **Grant No.** (vd `DHH2025-19-07`), ai là corresponding,
  ai co-first (`\thanks{... contributed equally}`).
- KHÔNG bịa email/ORCID nếu bài cũ không có — để trống và flag cho người dùng điền.
- "co-first author" → đánh dấu `$^{\dagger}$` + footnote "These authors contributed equally".
- Backup `.tex` về `_backups/<ts>/` trước khi sửa (gate artifact của người dùng).
