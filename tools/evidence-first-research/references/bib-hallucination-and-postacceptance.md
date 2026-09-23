# Rà BibTeX hallucination + ràng buộc post-acceptance (IEEE)

Đúc kết từ phiên rà references HybridStackPPI (IEEE Access). Dùng khi người dùng nói
"nhiều bibtex hallucination", "rà references cho đúng", hoặc khi xử lý proof/camera-ready.

## A. Phát hiện reference bịa (LM-generated hallucination)

Pattern điển hình của reference sinh bằng LM: **giữ đúng DOI/journal/năm nhưng BỊA tên
tác giả hoặc tiêu đề**, hoặc dựng hẳn một bài không tồn tại từ một bài thật gần đó.

Quy trình đã chứng minh hiệu quả (KHÔNG tin máy chấm tự động — nhiều false positive):

1. **Chỉ rà entry ĐƯỢC CITE.** Lấy cited keys từ `.aux`:
   `grep -o '\\citation{[^}]*}' file.aux` → tách comma → unique. Bib thường có nhiều
   entry thừa không xuất hiện trong bài in (BibTeX chỉ render cái `\cite`).
2. **Đối chiếu 2 nguồn độc lập**: Crossref (`api.crossref.org/works?query.bibliographic=`)
   + Semantic Scholar (`api.semanticscholar.org/graph/v1/paper/search`). LƯU Ý: S2 hay
   bị HTTP 429 rate-limit (không key) → retry với backoff `time.sleep(3*(t+1))`, và khi
   S2 rỗng thì thực chất chỉ còn Crossref.
3. **Lọc false positive — bước quan trọng nhất.** Crossref hay xếp nhầm lên đầu:
   "Faculty Opinions recommendation of ...", bài review, supplement, figure record,
   hoặc bài mới cùng chủ đề. Match phải CHẶT: token Jaccard ≥ 0.85 trên title (chuẩn
   hóa lowercase, bỏ ký tự đặc biệt) VÀ họ tác giả đầu khớp. Bài kinh điển (SHAP/Lundberg
   NeurIPS, Attention/Vaswani, Random forests/Breiman, Rumelhart 1986) thường bị CR trả
   record rác/reprint năm sai — bib gốc ĐÚNG, không được sửa mù.
4. **Xác nhận ca nghi vấn bằng DOI lookup chính tắc** (nguồn không nói dối):
   `api.crossref.org/works/{DOI}` → lấy author/title/journal/volume/pages thật. Đây là
   bằng chứng để khẳng định lỗi và sửa.
5. **Lệch năm online-first vs in KHÔNG phải lỗi**: Crossref hay trả năm online-first;
   bib ghi năm số in (khớp volume/issue) là đúng quy ước trích dẫn — giữ nguyên.

Phân loại kết quả: (a) sai metadata, bài thật → sửa tác giả/title/volume theo DOI;
(b) bịa hẳn → thay bằng bài thật verify DOI, chọn bài KHỚP NGỮ CẢNH câu đang cite;
(c) false positive → giữ nguyên. Luôn báo người dùng quyết với nhóm (b) trước khi thay.

## B. Khi đổi/thay reference, phải viết lại prose đang cite nó

Khi tên/tiêu đề bị bịa, câu văn trong bài có thể đang mô tả nội dung của bài bịa. Trích
ngữ cảnh `\cite` (`grep -n 'cite{key}'`), đọc câu, và viết lại cho khớp bài THẬT. Ví dụ
phiên này: "KG-PPI draws logical relations" (bài bịa) → mô tả đúng bài Yang et al.
"end-to-end knowledge-graph-fused GNN". Đổi key sang bài cùng chủ đề/loại method để câu
vẫn đúng (vd handcrafted-feature + RF, computational-prediction review).

## C. Ràng buộc POST-ACCEPTANCE của IEEE (rất quan trọng)

Email copyediting IEEE Access nói rõ:
- **CẤM thêm/bớt tác giả** post-acceptance (kể cả reviewer yêu cầu) — request sẽ bị từ chối.
- **CẤM thêm/bớt references** post-acceptance.
- **ĐƯỢC + khuyến khích**: sửa độ chính xác bibliographic, định dạng theo IEEE style
  (https://journals.ieeeauthorcenter.ieee.org/.../ieee-editorial-style-manual/), sửa
  ngữ pháp/chính tả (bài chỉ được light-edit trước khi in).

⇒ Hệ quả thao tác:
- Đối chiếu bản HIỆN TẠI với bản ACCEPTED (giải nén zip gốc đã nộp), so cited keys.
  Bất kỳ cite THÊM MỚI (vd self-citation) phải GỠ để về đúng số ref accepted. Self-cite
  để dành bài sau.
- Sửa metadata sai (cùng bài, đúng lại tác giả/title) = "bibliographic accuracy" → HỢP LỆ.
- Đổi reference bịa sang bài thật mà GIỮ NGUYÊN cite key: kỹ thuật không phải "thêm/bớt",
  nhưng bài được trỏ tới đã khác → minh bạch bằng 1 dòng khai báo cho editor trong thư
  trả proof (vd: "corrected N reference entries that contained bibliographic errors in
  the accepted version; no references added or removed, citation count unchanged at K").
- IEEE style: tên journal viết hoa nhất quán (Title Case theo tên chính thức); IEEEtran.bst
  KHÔNG in trường `publisher` cho `@article` nên tên journal là phần hiển thị chính.

## D. Đóng gói camera-ready < 20MB (giới hạn Telegram)

- Thủ phạm phình file thường là ẢNH BIO tác giả PDF (vd 5.7MB) → phình cả source lẫn PDF
  biên dịch. Nén ảnh xuống (300dpi ở cỡ 1×1.25in chỉ cần ~375px là thừa) bằng Ghostscript
  `-dPDFSETTINGS=/ebook` hoặc tương đương; verify còn nét bằng `pdfinfo` (page size pt)
  thay vì nén mù. PDF 11.4MB → 5.6MB sau tối ưu ảnh.
- Gói gồm: `.tex`, `.bib`, `.bbl` (IEEE cần cho camera-ready), `.pdf`, `.cls`, `.bst`,
  toàn bộ figures. Verify build-from-staging (giải nén → compile từ 0) để chứng minh gói
  tự tái lập. File >20MB không gửi được Telegram — nén hoặc đưa đường dẫn local.

## E. Pitfall công cụ
- ripgrep/search_files vỡ với pattern chứa `{` `}` (BibTeX) → dùng Python parse entry
  (quét `@type{`, đếm ngoặc cân bằng) thay vì grep.
- Script verify nhiều entry chậm (query API + sleep) → chạy nền `background=true,
  notify_on_complete=true`, ghi kết quả ra JSON file rồi đọc, đừng block foreground.
- Subagent rà grammar nên trả danh sách sửa dạng exact old/new string để patch đúng chỗ,
  không đụng số liệu/`\cite`/math/tên method.
