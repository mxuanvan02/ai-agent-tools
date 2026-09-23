# Audit & sửa bibtex hallucination (references sinh bằng LM)

Dùng khi người dùng nghi "nhiều bibtex hallucination" hoặc yêu cầu rà references của bài
(đặc biệt bài có tên người dùng — sai 1 ref bị reviewer bắt là mất uy tín).

## Nguyên tắc cốt lõi
- **DOI lookup là nguồn sự thật duy nhất.** LM-generated refs thường GIỮ ĐÚNG
  journal/year/volume nhưng **bịa tên tác giả hoặc tiêu đề**. Chỉ fetch metadata
  theo DOI chính tắc (Crossref `/works/{doi}`) mới khẳng định được.
- **KHÔNG tin chấm điểm tự động bằng title-match.** Crossref `query.bibliographic`
  hay xếp nhầm "Faculty Opinions recommendation", bài review, hoặc bài mới lên đầu →
  tạo HÀNG LOẠT dương tính giả. Phải re-verify chặt: token Jaccard ≥ 0.85 **VÀ**
  họ tác giả đầu khớp, mới coi là "cùng bài".
- **Semantic Scholar hay bị rate-limit (HTTP 429)** → trả rỗng. Nếu 1 nguồn rỗng,
  ĐỪNG kết luận "không tồn tại"; retry có giãn cách (sleep 3·n) hoặc chuyển DOI lookup.
- **Lệch year online-first vs in KHÔNG phải lỗi.** Crossref trả năm online-first,
  bib ghi năm số in (khớp volume/issue) → đúng quy ước trích dẫn, GIỮ NGUYÊN.
- Bài có tên người dùng = **không tự sửa citation gây đổi luận điểm**; báo phân loại, hỏi
  hướng cho nhóm nghi vấn nặng trước khi đụng.

## Quy trình (đã chạy thật, hiệu quả)
1. **Parse bib** bằng brace-matching (đếm `{}` để cắt entry), KHÔNG dùng regex thô.
   Bắt ngay: trùng key (BibTeX báo lỗi fatal), entry rác `\hl{...}` (artifact
   highlight-diff), trùng nội dung khác key, thiếu `author` (warning "empty author").
2. **Chỉ rà entry ĐƯỢC CITE.** Lấy cited keys từ `.aux`
   (`grep -oP '\\(?:abx@aux@cite|citation)\{...\}' file.aux` hoặc parse `\citation{}`).
   62/120 entry có thể là rác không cite → không ảnh hưởng PDF.
3. **Đối chiếu Crossref** cho từng entry cited; phân loại OK / diff / not_found.
4. **Re-verify chặt** các entry bị flag (Jaccard 0.85 + surname) để gạt false positive.
5. **DOI lookup trực tiếp** cho nhóm còn nghi (sai tác giả / sai title / không tồn tại)
   → đây là bước KHẲNG ĐỊNH hallucination.
6. **Nhóm bịa hẳn**: thay bằng bài THẬT verify DOI, chọn bài khớp ngữ cảnh câu cite
   (không thay bừa). **Giữ nguyên cite key** để không gãy `\cite`.
7. **Viết lại prose**: khi title/tên bị bịa, câu trong bài có thể đang mô tả nội dung
   bài bịa → đọc ngữ cảnh `\cite` trong .tex, sửa câu cho khớp bài thật.
8. **Khi đổi/bỏ ref ở 1 cụm cite**, kiểm ref thay có đúng ngữ cảnh không; nếu lệch,
   chuyển cite xuống câu phù hợp và/hoặc đưa ref đúng chủ đề (verify DOI) vào chỗ trống.
9. **Dọn entry thừa**: prune mọi entry không có trong cited-keys. Backup `_backups/`
   trước. Lưu ý self-citation (vd bài của chính người dùng) — entry không cite vẫn HỎI
   người dùng có muốn self-cite không trước khi xóa.
10. **Rebuild đầy đủ**: pdflatex → bibtex → pdflatex ×2. Verify: 0 undefined citation,
    0 undefined ref, `warning$ -- 0` trong `.blg`, bbl ref count == số cite.

## Pitfalls
- ripgrep/`search_files` vướng `{}` trong pattern (`Unmatched \{`, `Invalid content
  of \{\}`) → dùng Python brace-match thay vì grep cho thao tác trên .bib.
- Script ghi JSON ra stdout dễ bị nuốt qua wrapper background → ghi thẳng ra file rồi
  đọc, đừng dựa vào stdout.
- Query Crossref 100+ entry mất 5–10 phút (timeout/sleep) → chạy background, checkpoint
  mỗi 5 entry để resume được.
- Telegram chặn file >20MB ("size could not be verified") → bộ source LaTeX kèm font
  .pfb thường >20MB; gửi PDF riêng (thường <20MB) hoặc đóng gói bỏ build artifacts.
- `.bib` không gửi được qua Telegram (đuôi không hỗ trợ) → đổi `.txt` hoặc `.zip`.
