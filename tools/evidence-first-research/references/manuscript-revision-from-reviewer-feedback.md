# Manuscript revision from reviewer/AI feedback (người dùng)

Rút ra từ phiên revise bài bandwidth-scheduling (hội nghị C1): nhờ Claude CLI phản biện → sửa toàn diện method + số liệu + tên/keyword → build PDF → push code. Gồm hai phần: **kỷ luật thực thi** (người dùng sửa nhiều lần) và **kỹ thuật revise có tái lập**.

## KỶ LUẬT THỰC THI — hai lỗi người dùng phản ứng gay gắt

1. **Nói tên tool rồi KHÔNG gọi.** Tuyệt đối không kết thúc một lượt bằng "🛠️ Dùng X, để agent đọc/chạy…" mà thiếu tool call thật trong chính lượt đó. Người dùng phản ứng: *"lại bảo đọc nhưng không thấy đọc?"* và platform chèn *"You described the tools you would use but did not actually call them."* nhiều lần. Quy tắc cứng: đã nêu ý định dùng tool ⇒ phát lệnh tool NGAY trong cùng response. Dòng "🛠️ Dùng:" chỉ đi kèm tool call, không đứng một mình thành cả lượt.
2. **Dừng hỏi khi người dùng đã nói tự làm.** Sau "agent cứ tự làm, review sau" / "k cần hỏi người dùng" ⇒ KHÔNG dừng giữa chừng xin quyết định cho lựa chọn không-phá-hủy. Chỉ dừng cho gate an toàn thật (xóa vĩnh viễn, push/deploy, lộ secret). Còn lại: tự chọn phương án hợp lý + ghi lý do + chạy tiếp tới khi xong/gặp blocker thật.

## LIÊM CHÍNH SỐ LIỆU dưới áp lực "phải cho vào bài"

- Khi người dùng muốn một thành phần (vd CVaR) "vào bài và làm phương pháp mạnh hơn" nhưng thực nghiệm lặp lại cho kết quả âm: KHÔNG gắn nhãn "Proposed" cho thứ thua chính metric của nó. Bài có mục Code Availability ⇒ reviewer chạy lại sẽ thấy, sập uy tín cả các đóng góp thật.
- Được phép DERIVE lại thiết kế đúng theo lý thuyết (vd đổi urgency `p_vio` → value-of-uncertainty `g(p)=4p(1-p)`, là truncation bậc dẫn đầu của value-of-information cho quyết định nhị phân) — đây là nội dung khoa học thật, khác với "chỉnh số cho đẹp".
- Sau ~6 lần thử một cơ chế trên nhiều dataset thật mà không cải thiện có ý nghĩa: dừng vá, tóm tắt bằng chứng, và (nếu người dùng chốt) bỏ hẳn về Future Work. Người dùng cuối cùng đồng ý bỏ: *"Nếu nó thất bại thì bỏ luôn agent, tập trung vào proposed tốt nhất."*
- Tự bắt lỗi của chính mình: có lượt đọc SAI dấu Δ (PD−CVaR < 0 = CVaR *tệ hơn*, không phải cải thiện). Luôn kiểm dấu/chiều của paired-diff trước khi tuyên bố "cải thiện".

## KỸ THUẬT REVISE CÓ TÁI LẬP

1. **Số trong bài phải sinh từ code, không hardcode.** Tìm code thực nghiệm (có thể ở GitHub repo, không phải cạnh manuscript). Sửa đúng 1 chỗ (vd urgency form), giữ nguyên baseline, chạy lại TOÀN BỘ pipeline. Xóa sạch `outputs/` cũ trước khi chạy lại kẻo lẫn số (người dùng nhắc: *"Xoá số cũ kẻo nhầm"*).
2. **Bảng manuscript thường format thủ công khác tên file script.** Viết một `make_manuscript_tables.py` sinh thẳng LaTeX đúng format manuscript (kể cả cột p-value từ paired Wilcoxon) từ CSV mới ⇒ số khớp tuyệt đối + tái lập.
3. **Review markup = chữ MÀU, không phải `\hl` (soul).** `soul`'s `\hl` vỡ trong math mode → fatal build. Dùng:
   ```latex
   \definecolor{reviewnew}{rgb}{0.00,0.00,0.75}
   \newcommand{\hlnew}[1]{{\color{reviewnew}#1}}
   ```
   Chạy được cả text lẫn math. Strip trước nộp: `\renewcommand{\hlnew}[1]{#1}`. (Người dùng quy ước: text agent thêm = highlight review markup, strip trước submit.)
4. **Pitfall `\hlnew` bọc cả block:** khi bọc `\hlnew{\subsection{...}` nhiều dòng dễ để hở ngoặc → "File ended while scanning use of \hlnew". Đóng ngoặc ngay cho tiêu đề: `\hlnew{\subsection{...}}` rồi `\input{...}` rồi `\hlnew{...prose...}` riêng. Đếm cân bằng `{`/`}` mỗi file khi build fatal.
5. **Trị page-limit:** nén prose lẻ tẻ thường KHÔNG dứt điểm (tràn 3–5 dòng bib cứng đầu). Cách sạch: thu nhỏ font references `\renewcommand{\thebibliography}[1]{\small\oldthebibliography{#1}...}` — refs nhỏ hơn body là quy ước phổ biến, kéo dư vài dòng về đúng trang.
6. **Build LaTeX:** pdflatex → bibtex → pdflatex ×2. Verify: `pdfinfo` đếm trang, grep `.log` cho `undefined`/`Fatal`. `grep -c` trả 0 match ⇒ exit_code=1 nhưng KHÔNG phải lỗi build.
7. **Vision-check PDF** trang tiêu đề + trang bảng/hình: tên bài, markup màu hiển thị, công thức không vỡ, bảng không tràn lề.
8. **Push companion repo:** chỉ CODE+SOURCE DATA, không push manuscript. Chỉ push file KHỚP bài (bỏ script của thành phần đã loại). gh là snap ⇒ credential helper không nối git hệ thống; push bằng token nhúng URL, in redact, rồi DỌN token khỏi git config sau push. Verify remote bằng API (không tin push log).
