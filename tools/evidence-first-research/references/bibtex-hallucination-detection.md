# Phát hiện & sửa BibTeX hallucination (references sinh bằng LM)

## Bối cảnh
Bài có tên người dùng dùng `references.bib` mà một phần entry do LLM sinh ra. Loại lỗi
nguy hiểm nhất KHÔNG phải sai cú pháp — mà là **entry trông hợp lệ nhưng bịa nội dung**:
giữ đúng DOI/journal/năm nhưng **bịa tác giả hoặc tiêu đề**, hoặc dựng hẳn một bài
không tồn tại từ một bài thật gần đó. Reviewer Q1/IEEE bắt được một ref bịa là mất uy tín.

## Nguyên tắc cốt lõi
1. **DOI là nguồn không nói dối.** Khi nghi ngờ, fetch metadata trực tiếp theo DOI
   (`https://api.crossref.org/works/<DOI>`) để lấy title/author/volume/pages chính tắc,
   rồi so với entry. Đây là bằng chứng mạnh nhất.
2. **KHÔNG tin máy chấm tự động.** Crossref `query.bibliographic` hay xếp nhầm lên đầu:
   "Faculty Opinions recommendation of ...", bài review (`/review1`), figure/supplement
   (`.s001`, `/fig-6`), hoặc bài mới cùng chủ đề. → rất nhiều "diff"/"not found" là
   DƯƠNG TÍNH GIẢ, không phải bịa.
3. **Semantic Scholar không key bị rate-limit (HTTP 429)** rất nhanh → trả rỗng hàng loạt,
   làm "2 nguồn" sụp về 1 nguồn. Phải retry có giãn cách (sleep 3·(t+1)) và xem 429 là
   "chưa biết", KHÔNG phải "không tồn tại".
4. **Chỉ rà các key THỰC SỰ được cite** (lấy từ `.aux`, không phải toàn bộ .bib) — tiết
   kiệm và đúng trọng tâm.

## Quy trình 3 vòng (lọc nhiễu → xác minh chặt → DOI canonical)
1. **Vòng thô:** query Crossref + S2 cho mọi cited key, so title (Jaccard) + year/vol/pages.
   Phân loại: chỉ-thiếu-DOI (bỏ qua, không phải lỗi) vs có-sai-lệch.
2. **Vòng chặt:** với entry bị flag, match khi Jaccard ≥ 0.85 VÀ họ tác giả đầu khớp.
   Năm lệch 1 thường là online-first vs năm số in → bib THƯỜNG ĐÚNG, không sửa.
3. **Vòng DOI canonical:** với 3 dấu hiệu nguy hiểm — (a) DOI thật nhưng tác giả đầu khác,
   (b) title không khớp bài ở DOI đó, (c) không tìm thấy ở cả Crossref+S2+arXiv — fetch
   metadata theo DOI và đọc BẰNG MẮT. Đây là bước phân biệt "Crossref xếp nhầm" với "bịa thật".

## Phân loại kết quả
- **Sai metadata (bài có thật):** vá đúng author/title/volume/pages theo DOI. Giữ nguyên cite key.
- **Bịa hẳn (không tồn tại):** mặc định của người dùng = **thay bằng bài thật gần nhất cùng
  journal/năm/chủ đề** (xác minh DOI trước khi điền). Giữ nguyên cite key để không gãy `\cite`.
- **Dương tính giả (bài kinh điển/preprint Crossref index kém: SHAP/NeurIPS, arXiv, Nature cũ):**
  KHÔNG đụng. Báo người dùng là "báo động giả".

## BẮT BUỘC: viết lại prose khi citation target bị bịa
Khi tên/tiêu đề một ref bị bịa, **câu văn đang cite nó có thể đang mô tả nội dung của bài bịa**.
Sau khi thay ref → trích ngữ cảnh `\cite` trong .tex và viết lại câu cho khớp bài THẬT.
(Ví dụ session này: "KG-PPI draws logical relations from databases" — tên+nội dung giả →
thay bằng Yang et al. "end-to-end knowledge-graph-fused GNN" và viết lại câu cho đúng.)
Ref mô tả chung chung (RF + handcrafted features, correlation filter…) thì bài thật thường
vẫn khớp, không cần đổi chữ — nhưng phải kiểm từng cái, không mặc định.

## Lỗi cấu trúc luôn kèm rà (bắt trước khi đối chiếu CSDL)
- Trùng cite key (BibTeX báo lỗi) → xóa bản thừa.
- Entry rác bọc `\hl{}` (artifact highlight) → xóa, trùng bản gốc.
- Trùng nội dung khác key (vd `chen2019multifaceted` ↔ `Chen2019PIPR`): **grep .aux/.tex xem
  key nào ĐƯỢC CITE**, giữ key đó, xóa key không dùng. KHÔNG đoán.
- Entry thiếu `author` (consortium) → thêm corporate author dạng `author={{UniProt Consortium}}`
  (ngoặc kép để BibTeX không tách tên).

## Pitfalls công cụ
- **ripgrep/search_files vỡ trên `{`** ("Unmatched \\{" / "Invalid content of \\{\\}") khi
  pattern chứa ngoặc nhọn của .bib/.tex → dùng Python parse (quét `@`, đếm depth ngoặc) thay vì grep.
- Script tự `&`-background trong shell làm session theo dõi nhầm wrapper → chạy foreground có
  timeout đủ, hoặc background=true của tool với notify; GHI kết quả ra FILE rồi đọc (stdout hay bị nuốt).
- Verify cuối: pdflatex×1 → bibtex → pdflatex×2 → đếm `Citation .* undefined` = 0,
  bibtex warning = 0, và grep tác giả/title mới trong `.bbl` để chắc bib mới đã được nạp.

## Script tái dùng
`scripts/bib_verify.py` — parse .bib (depth-counting, không grep), lấy cited keys từ .aux,
đối chiếu Crossref + S2 (retry 429), DOI-canonical lookup, ghi JSON. Chạy nền, ghi ra file.
