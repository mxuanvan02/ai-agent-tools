# Backing manuscript numbers with a reproduction repo (results integrity)

Trigger: người dùng hỏi "số liệu/bảng/biểu trong bài đã chạy đúng chuẩn theo bài chưa",
"code có chuẩn 100% những gì bản thảo trình bày chưa", hoặc giao việc thay placeholder
bằng kết quả thật + bổ sung companion source-code repo.

## Nguyên tắc trung thực (quan trọng nhất — người dùng truy vấn rất gắt điểm này)

Phân biệt rõ HAI mức, KHÔNG được nhập nhằng:
1. **Reproducible / calibrated simulation** — có code chạy thật, deterministic (seed),
   regenerate được mọi bảng/hình trong Results; nhưng nhiều thành phần được *calibrate
   theo số bài* (additive energy model khớp Table III, payload table dùng raw/semantic
   sizes cố định, scalability dùng công thức analytic, DT là proxy-state).
2. **Full-fidelity implementation** — hiện thực đúng từng phương trình & module hệ thống
   (semantic encoder thật, channel R_v[t]/P_v/G_v/I0/β, energy tính per-slot từ
   trajectory, DT đủ layer). Code reproduction THƯỜNG KHÔNG đạt mức này.

→ Khi người dùng hỏi "chuẩn 100% chưa", trả lời theo đúng mức đạt được. Câu đúng:
"100% số liệu/hình trong Results được sinh từ code chạy thật, tái lập được" —
KHÔNG nói "full implementation toàn framework" nếu chỉ là calibrated reproduction.
Chủ động liệt kê bảng ✅ measured vs ⚠️ calibrated cho từng experiment.

## Wording an toàn trong manuscript (tránh overclaim)

- DÙNG: "The reproducible simulation code used to generate all numerical results and
  figures is publicly available at <repo>."
- TRÁNH: "complete source code", "full implementation of the framework",
  "all reported results" — dễ bị reviewer bắt bẻ khi mở code thấy calibration.

## Quy trình audit + sửa (đã chạy thật, khớp execution-contract của người dùng)

1. **Tìm generator thật.** Phân biệt file vẽ hình placeholder (chỉ `np.exp`, số
   hard-code, noise giả — KHÔNG chạy model) với repo reproduction nghiêm túc
   (có TD3/FedAvg/env/... chạy thật). Đọc code sinh số, đừng tin README.
2. **Clone + dựng venv + CHẠY THẬT** (`uv venv`; torch CPU-only nhẹ hơn bản CUDA nhiều —
   cài nền + notify_on_complete vì torch tải lâu). Đọc `results.json`, đối chiếu trực
   tiếp với từng con số trong `.tex`.
3. **Phát hiện số "mồ côi"**: con số trong bài KHÔNG có nguồn từ repo VÀ/HOẶC mâu thuẫn
   chính bảng của bài (vd "giảm 27.3%" trong khi bảng cho 3.4 vs 7.1 = 52%). Gỡ hoặc sửa.
4. **Thay placeholder bằng hình/số thật**, copy figures từ `results/` của repo.
5. **Đồng bộ MỌI nơi xuất hiện 1 con số**: abstract, contribution bullets, body,
   conclusion, summary table. Sau sửa, grep lại toàn bài tìm số cũ còn sót
   (vd 74.8 vs 73.8) — đây là bước dễ sót nhất.
6. **Nếu thiếu metric**: mở rộng repo để SINH thật metric đó từ cùng một rollout/mô hình
   (đừng hard-code vào .tex). Thêm hằng số có comment, chạy lại full pipeline, lấy số
   canonical từ results.json.
7. **Build kiểm chứng** (`latexmk`), xác nhận rc=0, đếm trang, kiểm "undefined refs" = NONE,
   kiểm còn markdown artifact (`**...**` lọt vào .tex sẽ in ra dấu sao) không.

## Companion repo phải khớp lời tuyên bố TRƯỚC khi nói "publicly available"

Nếu bài trỏ tới GitHub repo công khai và nói "reproduces all results", thì code mới sửa
(vd experiment DT bổ sung) phải được **push lên remote** — bản clone /tmp không tính.
Theo USER profile: companion repo ship CODE + SOURCE DATA only (strip results/drafts/.tex),
KHÔNG push khi chưa có phép. Sau khi được phép push: chỉ stage file code (đừng stage
`_backups/`), set git identity **local** (không đụng global), push HTTPS-tokenized
(SSH-exec bị chặn trên host này), rồi VERIFY thật trên remote qua `gh api`
(commit HEAD + nội dung file) — không tin self-report của git.

## Pitfalls

- `**bold**` kiểu markdown lọt vào LaTeX → in ra literal dấu sao. Grep dọn sạch.
- Email/tên tác giả: KHÔNG bịa. Lấy từ các bài cũ của người dùng (bài probe-transmit/bài bandwidth-scheduling/ICCSIT).
  Funding grant univ-logo lấy nguyên văn từ `\thanks{...DHHxxxx-xx-xx}` của bài trước.
- Co-first author: dùng dấu † + "These authors contributed equally to this work."
- grep toàn `/mnt/external-data` (HDD) rất chậm → timeout; khoanh vùng thư mục cụ thể.
