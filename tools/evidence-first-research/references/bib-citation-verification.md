# Rà soát citation học thuật + thay ref ảo (đối chiếu CSDL, build-verified)

Quy trình đã chạy thật cho HybridStackPPI (IEEE Access). Dùng khi người dùng nói "rà
references cho kĩ bằng API tới CSDL chuẩn" hoặc nghi 1-2 ref bị "AI ghép sai".

## 1. Lấy nội dung ref nghi vấn
- Giải nén package, đọc `references.bib` lấy đúng entry (title/author/journal/vol/no/pages/year).
- Tìm chỗ `\cite{...}` trong `.tex` để biết NGỮ CẢNH ref đang phục vụ (intro? related work? evaluation?). Câu thay phải khớp nghĩa ref thật.

## 2. Đối chiếu CSDL (Crossref + OpenAlex, dùng execute_code)
Query theo 3 trục, KHÔNG chỉ theo title:
- **Title** chính xác trên Crossref và OpenAlex.
- **Author + journal + năm** (Crossref filter `query.bibliographic` / `query.author` + `container-title`).
- **Toạ độ vol/issue/pages**: hỏi "cái gì THỰC SỰ nằm ở journal X vol Y issue Z pp A-B" — nếu toạ độ đó chứa bài KHÁC (hoặc trống) ⇒ entry là phantom.

Pitfall API:
- Terminal cắt output ở mốc ~20000 ký tự ⇒ OpenAlex JSON dài bị `Invalid control character`/`Expecting delimiter`. GHI RA FILE rồi parse, đừng in thẳng.
- Crossref `message.items`, OpenAlex `results`. Lọc abstract/inverted-index ra cho gọn.

## 3. Dấu hiệu citation AI ghép sai (phantom / mis-spliced)
Một entry là NGỤY TẠO khi hội đủ vài dấu hiệu:
- Tên tác giả CÓ THẬT nhưng bị gán vào title + journal + toạ độ KHÔNG tồn tại.
  (vd: "Richard B. Silverman" là tác giả sách Organic Chemistry of Drug Design,
   không hề viết review PPI; "Ian Walsh" thật làm protein stability/aggregation,
   không có bài "evaluating accuracy of PPI predictions".)
- Coauthor mơ hồ "and others" / "Zhang, J and others" ngay ở entry chính.
- Thiếu `number`, thiếu `pages`, hoặc chỉ có mỗi vol+year.
- Title nghe rất hợp lý + journal Q1 đúng ngành ⇒ chính vì "quá khớp ngữ cảnh" mà dễ lọt.
Kết luận chỉ chốt SAU khi cả title-search, author-search, và toạ-độ-search đều miss.

## 4. Thay ref thật, KHỚP NGỮ CẢNH
- Verify DOI ứng viên qua Crossref lấy metadata đầy đủ (author list, vol/issue/pages/artnum).
- Chọn bài đi cặp tự nhiên với ref bên cạnh (vd `park2012flaws` + `hamp2015challenges`
  cho ngữ cảnh data-leakage/đánh giá quá cao ML-PPI).
- Đổi cả BibTeX key cho có nghĩa; sửa câu văn nếu nghĩa ref mới lệch.

## 5. PITFALL LỚN — package "final" có sẵn `.bbl`
Nếu thư mục có file `.bbl` đã render (dấu hiệu submission "final"), thì sửa MỖI `.bib`
là KHÔNG đủ — `.bbl` mới là cái LaTeX đọc khi build, nên ref ảo VẪN lọt vào PDF.
Phải sửa ĐỒNG BỘ 3 file:
- `references.bib` — entry + DOI.
- `*.tex` — đổi key trong mọi `\cite{}` (grep hết các lần xuất hiện).
- `*.bbl` — đổi `\bibitem{key}` + format author kiểu IEEEtran (`H.~Lu, Q.~Zhou, ... and J.~Shi`).

Backup cả 3 vào `_backups/<ts>/` trước khi sửa.

## 6. Verify bằng build thật (bắt buộc)
- `latexmk -pdf` (pdflatex→bibtex→pdflatex×2), kỳ vọng EXIT 0.
- Kiểm tra PDF render đúng số + nội dung ref mới (pdftotext rồi grep tên tác giả/journal).
- Grep chuỗi ref ảo trong PDF ⇒ phải NONE. Grep `[?]` trong body ⇒ phải NONE.

### FALSE ALARM khi đọc log (đừng hoảng)
- latexmk gộp MỌI pass vào 1 `.log`. "LaTeX Warning: Citation `x' undefined" ở pass
  ĐẦU (trước khi bibtex resolve) là BÌNH THƯỜNG. Bằng chứng quyết định = PDF cuối +
  việc KHÔNG có dòng tổng kết "There were undefined references" ở pass cuối.
- `LaTeX Font Warning: Font shape 'T1/formata/m/sl' undefined` là noise cosmetic của
  template IEEEtran/ieeeaccess, có sẵn từ trước, KHÔNG liên quan citation. Đếm "undefined"
  thô trong log sẽ lẫn các dòng font này — phải phân loại trước khi kết luận.

## 7. Phát hiện phụ thường gặp
Rà tới đâu hay lòi ra key SAI khác: BibTeX key (tên+năm) không khớp nội dung entry
(vd key `srinivasan2007protein` nhưng metadata là Park 2009 BMC Bioinformatics 10:419).
Báo người dùng, KHÔNG tự sửa ngoài phạm vi được giao — chờ người dùng chốt.
