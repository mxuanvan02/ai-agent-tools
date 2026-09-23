# Rà soát & làm sạch file .bib (BibTeX hygiene + đối chiếu CSDL)

Khi người dùng gửi file references (`.bib`, hoặc `.txt` đổi đuôi vì Telegram chặn `.bib`)
và yêu cầu "rà toàn bộ, đối chiếu CSDL, sửa đúng".

## Nguyên tắc cốt lõi (đắt giá nhất)

**Đối chiếu Crossref bằng title naïve sinh RẤT NHIỀU false positive.** Trong một
lần chạy thật: 90/125 entry bị flag "diff", nhưng re-verify chặt cho thấy gần như
toàn bộ là nhiễu. KHÔNG được sửa mù theo kết quả match lỏng — sẽ làm hỏng entry vốn đúng.

Hai loại nhiễu điển hình:
- **Year online-first vs năm số in**: Crossref trả năm xuất bản online (vd 2008),
  bib ghi năm của volume/issue in (vd 2009). Khi volume/issue/pages khớp → **bib ĐÚNG**, giữ nguyên.
- **Match nhầm reprint/erratum/record rác**: bài kinh điển (Random Forests 2001,
  Attention 2017, Rumelhart 1986) bị Crossref trả bản in lại năm khác. Bib đúng, giữ nguyên.

## Quy trình

1. **Tìm bản gốc trên đĩa, KHÔNG sửa bản cache.** `search_files` tên file để xác định
   path canonical và đếm số bản trùng. File người dùng gửi qua Telegram nằm trong
   `~/.hermes/cache/documents/` — chỉ để đọc, sửa bản thật trong project/Downloads.
2. **Backup trước khi đụng**: copy sang `_backups/bib_<ts>/`.
3. **Rà cục bộ (lỗi chắc chắn, sửa được ngay)** — parse entry bằng brace-matching, phát hiện:
   - Trùng key (BibTeX báo lỗi cứng) → xóa bản thứ 2 nếu nội dung y hệt.
   - Entry rác bọc `\hl{}` (artifact từ highlight-diff) → xóa, thường trùng nội dung bản sạch.
   - Cùng title khác key (content dupe) → **KHÔNG tự xóa**, hỏi người dùng key nào đang được cite.
   - Thiếu `author` (BibTeX warning "to sort, need author") → thêm corporate author
     dạng `author={{UniProt Consortium}}` (hai ngoặc nhọn giữ nguyên tên tổ chức).
4. **Đối chiếu CSDL Crossref** (`scripts/bibcheck.py`) — chạy nền, rate-limit 0.4s/query.
   Phân loại kết quả: tách "chỉ thiếu DOI" (không phải lỗi) khỏi "diff metadata thật".
5. **Re-verify CHẶT** mọi entry bị flag (`scripts/bibrecheck.py`): chỉ coi là lỗi thật khi
   token-Jaccard(title) ≥ 0.85 **VÀ** họ tác giả đầu xuất hiện trong author list Crossref.
   Verdict `no_strict_match` ⇒ bib gần như chắc đúng (preprint/book/record rác) ⇒ giữ nguyên.
6. **Verify cuối bằng compile thật**: chạy `bibtex` trên file .aux tối thiểu, yêu cầu
   **exit 0, 0 lỗi, 0 warning**. Đếm lại số entry khớp kỳ vọng (vd 125 → 121).
7. **Báo cáo**: tách rõ (a) lỗi cấu trúc đã sửa, (b) cái CSDL flag nhưng bib vốn đúng nên
   KHÔNG đụng (kèm lý do), (c) cần người dùng quyết (content-dupe). Giữ backup, gửi kèm bản `.txt`.

## Pitfalls

- `\hl{}` (soulutils highlight) trong bib là artifact từ bản "highlighted changes" — luôn là rác.
- Output JSON in ra stdout của process nền hay bị nuốt → ghi thẳng ra file `.json` rồi đọc.
- `search_files` regex thoát ngoặc `\{` báo "Unmatched \{" → dùng pattern đơn giản, không escape brace.
- Đừng dựa năm Crossref để "sửa" — năm số in mới là năm trích dẫn chuẩn.
- Telegram chặn đuôi `.bib`; bảo người dùng đổi sang `.txt` hoặc nén `.zip`, nhưng thường đọc thẳng từ đĩa được.
