# Manuscript → Beamer slides + math-chain audit (người dùng)

Hai quy trình bổ trợ cho việc "soạn slide báo cáo từ manuscript" và "rà soát mạch
công thức". Đã chạy thực tế trên bài bandwidth-scheduling và bài AoI-greenhouse.

## A. Pattern: fresh-eyes read-only audit bằng subagent

Khi người dùng yêu cầu "rà soát toàn diện / đồng bộ / kiểm mạch toán", KHÔNG tự audit
một mình — người vừa sửa bài bị "mù" vì tự hợp lý hoá. Bung subagent **chỉ-đọc**
(không sửa file) với các trục audit tường minh, trả về punch-list xếp theo severity
(CAO/VỪA/THẤP), mỗi mục ghi: file + dòng, trích nguyên văn, vấn đề, đề xuất sửa.

Phân rã không-giẫm-chân (mỗi subagent một gói):
- **Narrative**: mọi claim có khớp hướng mới chưa? Còn sót claim cũ / overclaim /
  mâu thuẫn nội tại?
- **Numbers integrity**: mọi số trong prose + mọi bảng vs CSV gốc; file mồ côi
  (`.tex` không `\input` ở đâu) mang số cũ mâu thuẫn; recompute p/r bằng scipy.
- **Slides vs manuscript + luật người dùng**: đồng bộ narrative/cấu trúc; rò rỉ chi
  tiết nội bộ; độ rõ phần toán.

Các trục cho audit MẠCH TOÁN (giao nguyên văn cho subagent):
1. Reference resolution: đếm `\label` vs `\ref`/`\eqref` — 0 orphan, 0 dangling, 0 trùng.
2. Symbol collision: cùng đại lượng một ký hiệu; soi ký hiệu dùng-nhiều-nghĩa
   (vd `u`, `β`, `α`, `s`, `ℓ` mỗi cái mang 2-3 nghĩa là lỗi VỪA điển hình).
3. Derivation flow: mỗi eq có nối bước rõ ràng từ eq trước không (liệt kê từng chuỗi).
4. Constant arithmetic: verify số dẫn xuất khớp nhau (vd z=(u−μ)/s, ε=s/(u−μ)).
5. Logic contradiction: ví dụ thật đã bắt — bảng ablation in đậm "deployed default"
   = biến thể KHÁC với biến thể mô tả "deployed" ở methodology; số runtime trong
   prose trích bảng nhưng không khớp bảng (sai 4-7×).
6. Assumption/scope: định lý có nêu rõ giả thiết + phạm vi (vd leading-order cần ε≪1).

Read-only audit là zero-rủi-ro-ghi-đè ⇒ luôn chạy WAVE 1 audit trước, WAVE 2 mới
sửa từng chỗ một có verify.

## B. Khi chạy lại unified pipeline làm ĐẢO luận điểm

DỪNG, báo người dùng trước khi viết prose (đừng tự gloss). Nếu đồng nhất 1 bộ tham số trên
1 dataset làm đảo narrative (vd baseline polling đầy đủ bỗng tốt hơn method trên
dataset khó hơn), KHÔNG ép đồng nhất. Giữ **hai nền tách bạch** + khai báo minh
bạch (nền chính cho SoTA/baseline; dataset khó = case-study regime-khó riêng cho
biến thể tail-risk). Trung thực hơn và nhẹ hơn full re-run.

## C. Beamer build pitfalls (xelatex, theme Huế tái dùng từ deck bài bandwidth-scheduling)

Theme dùng lại: `\documentclass[aspectratio=169,11pt]{beamer}`, fontspec DejaVu Sans,
màu HueBlue(0,72,135)/HueOrange(235,120,25), block title nền HueBlue, alertblock nền
HueOrange. Mỗi frame toán có một block "Diễn giải (mạch dẫn)" nối eq này sang eq kia.

### Pitfall 1 — Double subscript từ macro đã chứa subscript
`\newcommand{\Pvio}{P_{\mathrm{vio}}}` rồi viết `\Pvio_{,i}` ⇒ lỗi `! Double subscript`.
Build dừng giữa chừng (chỉ render tới frame lỗi). Fix: viết tường minh
`P_{\mathrm{vio},i}` ở chỗ cần chỉ số node, HOẶC định nghĩa macro riêng `\Pvioi`.
Tìm nhanh: `grep -n 'Pvio_'`.

### Pitfall 2 — Overfull \vbox trên frame toán dày (ladder siết, không cắt nội dung)
Phân biệt: **\vbox** = tràn DỌC (nội dung cao hơn vùng text; <8pt thường vô hại,
không cắt chữ ngang); **\hbox** = tràn NGANG ra lề (thấy được, ưu tiên sửa).
Định vị frame: `grep 'Overfull \\vbox.*detected at line' file.log` → ra số dòng
`\end{frame}` hoặc dòng trong frame.

Thang siết (theo thứ tự, dừng khi sạch), KHÔNG bỏ nội dung khoa học:
1. Hạ block "Diễn giải"/alertblock cuối frame: `\small` → `\footnotesize` → `\scriptsize`.
2. Bỏ `\vspace{...}` thừa giữa columns và alertblock.
3. Hạ cả frame toán dày xuống `\footnotesize` (đặt ngay sau `\begin{frame}{...}`).
4. Giảm `\itemsep` trong itemize (0.3em → 0.12em).
5. **Cú nén toàn cục ở preamble** (hạ TẤT CẢ frame cùng lúc) — hiệu quả nhất cho
   bài nặng toán:
   ```latex
   \addtobeamertemplate{block begin}{%
     \setlength{\abovedisplayskip}{2pt}\setlength{\belowdisplayskip}{2pt}%
     \setlength{\abovedisplayshortskip}{1pt}\setlength{\belowdisplayshortskip}{1pt}}{}
   \setlength{\abovedisplayskip}{2pt}\setlength{\belowdisplayskip}{2pt}
   \setbeamersize{text margin left=6pt,text margin right=6pt}
   ```

### Verify mỗi lần build
`xelatex -interaction=nonstopmode`; check: số trang, `grep -c overfull>5pt`, errors=0,
và grep rò rỉ nội bộ = 0 (theo luật slide của người dùng). Lưu ý false-positive khi grep
claim cũ: câu phủ định trung thực ("không thắng mọi metric") sẽ match — đọc context
trước khi nhận là lỗi.

## D. Đóng gói .zip sạch cho người dùng
Staging dir → loại file build (.aux/.log/.fls/.fdb/.bl g/.out), backup, venv, file
PDF/notes CŨ mâu thuẫn (kiểm mtime — bản cũ hơn bản synced hôm nay là rác), .md nhật
ký nội bộ. Giữ: .tex nguồn + .bbl + bảng + figure + PDF mới. Verify md5 PDF staged ==
bản synced trước khi zip; `unzip -t` test integrity. Lưu ý: xoá nhiều file nhanh có
thể trigger security-scan "mass file deletion" — bình thường, approve.
