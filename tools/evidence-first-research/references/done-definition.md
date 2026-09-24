# Định nghĩa "XONG" cho manuscript của người dùng (BẮT BUỘC)

> Bài học lặp lại nhiều lần: người dùng bực vì mình báo "xong" nhưng mỗi lần người dùng
> bảo dò lại thì mới lòi lỗi. "Build chạy" KHÔNG phải "xong". Đọc file này
> TRƯỚC khi định nói bất kỳ artifact nào là xong / ready / submit-ready.

## Nguyên tắc lõi

**"Xong" = trạng thái đạt được SAU KHI tự động dò lại LẶP đến 0 lỗi — không
phải điểm mình tuyên bố sau một lần build.** Mình phải là người dò, không để
người dùng làm người dò. Nếu người dùng nhắc "dò lại" mà lòi lỗi → quy trình đã sai, không
phải người dùng khó tính.

### build-pass ≠ xong
Trình biên dịch LaTeX KHÔNG đọc nghĩa. Nó pass trong khi vẫn còn:
- Số trong văn xuôi mâu thuẫn số trong bảng/CSV (vd bài bandwidth-scheduling-PD "1.49" trong text vs "1.37" trong bảng).
- Abstract nói "about half" còn Conclusion nói "one third" cho cùng một tỉ số (1.37/3.00≈0.46 → "half" đúng).
- Hàm mục tiêu phát biểu ở System Model (min $\widehat M_t$) KHÁC hàm mà code/selector thật sự tối ưu (min $\widehat L_t$). Đây là lỗi toán học nặng nhất, build vẫn pass.
- Reference bịa: DOI không resolve, hoặc tiêu đề .bib ≠ tiêu đề thật.
- Cite sai nguồn: text nói "dữ liệu ERA5" nhưng `\cite` trỏ vào dataset greenhouse Nam Phi.

→ Đây đều là lỗi NGỮ NGHĨA. Phải có cổng verify riêng, không tin build.

## Vòng lặp bắt buộc trước khi nói "xong"

Lặp cho đến khi CẢ 3 gate xanh cùng một lần chạy:

1. **Gate build**: pdflatex + full bibtex cycle → 0 undefined ref, 0 bibtex error, 0 overfull >5pt, đúng số trang (hội nghị C1 6–8).
2. **Gate semantic** (`scripts/verify_manuscript.py`): số văn xuôi ↔ bảng/CSV; abstract ↔ conclusion; mọi `\ref`↔`\label`; mọi `\cite`↔entry .bib + không entry mồ côi.
3. **Gate hallucination**: MỖI reference → query Crossref API, DOI phải resolve + tiêu đề khớp. Bài bịa fail ở đây, không fail ở build. (Xem thêm skill `latex-reference-audit`.)

**Verify cả chính verifier**: lần này script verify ban đầu cũng có bug (gọi hàm đã đổi tên) → phải chạy nó và đọc exit code, đừng tin nó đúng chỉ vì mình vừa viết.

## Cách báo cáo
- Chỉ nói "xong/submit-ready" khi dẫn được exit=0 của cả 3 gate trong một lần chạy.
- Luôn nói thẳng việc CHƯA làm (vd "text mới vẫn highlight vàng, chưa bỏ") thay vì im để tỏ ra hoàn tất.
- Không dùng "half"/"one third"… ước lượng bằng lời khi đã có số chính xác — kiểm lại tỉ số trước khi viết.

## Liên kết
- Anti-hallucinate references chi tiết: skill `latex-reference-audit`.
- Kỹ thuật 2 bản .tex sạch/highlight từ 1 bộ `sections/`: `references/manuscript-clean-review-split.md`.
