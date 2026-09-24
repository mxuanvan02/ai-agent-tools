# Manuscript revision driven by peer-review feedback (+ companion repo)

Dùng khi người dùng đưa feedback phản biện và yêu cầu "giải quyết toàn bộ" / chạy lại thực
nghiệm / sửa manuscript + đồng bộ code lên GitHub. Rút ra từ vòng revise bài bài bandwidth-scheduling (hội nghị C1).

## Nguyên tắc lõi: TIN DỮ LIỆU, đừng vá claim

- Khi một đóng góp được đề xuất (vd một urgency term mới, một biến thể CVaR) mà **thực
  nghiệm lặp lại nhiều lần (≥2-3) đều bác bỏ**, DỪNG vá. Đó là tín hiệu claim sai, không
  phải bug. Ở bài bài bandwidth-scheduling, term CVaR thất bại **7 lần** trên 2 dataset thật trước khi bỏ —
  lẽ ra nên bỏ sớm hơn nhiều.
- DERIVE-then-verify vẫn đúng, NHƯNG derivation chỉ là giả thuyết. Nếu số thật mâu thuẫn
  derivation, số thắng. Trình bày "controlled negative result" là khoa học tốt, reviewer
  Q1 tôn trọng hơn là nhét một "Proposed" thua chính metric của nó.
- **Regime dữ liệu quyết định method nào thắng.** Một term tốt trên data dễ (đuôi nhẹ) có
  thể THUA trên data khó (đuôi nặng). Ví dụ VoU `4p(1-p)` cực đại ở p≈0.5, →0 khi p→1;
  trên heat-episode thật (p→1) nó de-rank đúng zone đang vi phạm ⇒ thua raw-p. Luôn
  validate đóng góp chính trên ĐÚNG regime mà bài tuyên bố (thường là data khó), không chỉ
  data dễ. Nếu user nói "greenhouse dễ rồi, chạy data khó" → chạy lại toàn bộ pipeline trên
  data khó, đừng chỉ thêm 1 bảng phụ.

## Liêm chính "oracle" / lower-bound

- Một "oracle" **greedy per-slot** (tối ưu từng slot bằng giá trị thật) KHÔNG phải cumulative
  lower bound. Proposed method có thể vượt nó ⇒ reviewer bắt ngay "sao vượt oracle".
- Không tự chế lại oracle cho "đúng" — LẤY định nghĩa oracle GỐC từ source code repo, chạy
  đúng nó. Nếu proposed vẫn vượt, **đổi nhãn trung thực**: "Greedy clairvoyant (per-slot
  reference), not a cumulative lower bound" + 1 câu giải thích (feedback thắng greedy nhờ
  quản lý AoI/động lực dài hạn). Nhãn phải khớp Ở CẢ bảng LẪN legend hình.

## Audit ký hiệu toán sau mỗi lần sửa lớn

- Sau khi thêm/sửa equation, quét **xung đột ký hiệu**: cùng một symbol dùng cho 2 đại
  lượng khác giá trị/vai trò là lỗi reviewer chắc chắn bắt. Ở bài bandwidth-scheduling: `c_B,c_A` vừa là trọng
  số Safety Objective (0.04/0.015) vừa là hằng số Lagrangian budget-rule (0.030/0.010).
  Fix: tách tên (`κ_B,κ_A` cho objective, giữ `c_B,c_A` cho rule) + 1 câu nói rõ chúng khác.
- Kiểm tra định nghĩa mọi symbol xuất hiện (vd `\check x_i` bị dùng mà chưa định nghĩa).
- Định nghĩa các composite metric bằng equation tường minh (vd "Safety Objective J") — đừng
  để ẩn trong bảng.

## Review markup (text agent thêm vào manuscript)

- Text MỚI do agent thêm = highlight để người dùng review, strip trước khi nộp.
- **PITFALL LaTeX:** `soul`'s `\hl{}` VỠ trong math mode → build fatal. Dùng màu thay thế,
  hoạt động cả text lẫn math:
  `\definecolor{reviewnew}{rgb}{0,0,0.75}\newcommand{\hlnew}[1]{{\color{reviewnew}#1}}`
  Strip bằng: `\renewcommand{\hlnew}[1]{#1}`.
- Đừng bọc `\hlnew{}` quanh cả block chứa `\subsection{...}` + `\input{...}` — dễ lệch ngoặc
  gây "File ended while scanning use of \hlnew". Bọc từng câu prose; subsection để riêng.

## Page-limit: cắt có chiến lược, không tỉa vô hạn

- Nếu tràn vài dòng bib sang trang cuối: tỉa prose lẻ tẻ thường KHÔNG dứt điểm. Cắt 1 câu
  tự-bình-luận thừa, hoặc `\small` cho bibliography (refs nhỏ hơn body là quy ước phổ biến).
- Build đủ pass (pdflatex → bibtex → pdflatex ×2) rồi mới đếm trang; đừng kết luận từ 1 pass.

## Đồng bộ companion repo ↔ paper (khi bài pivot)

Khi bài đổi hướng lớn (đổi dataset, bỏ một đóng góp), repo PHẢI pivot theo, nếu không reviewer
clone về thấy mớ trộn cũ+mới:
- Đưa script/data của hướng cũ vào `legacy/` bằng `git mv` (git giữ lại, reversible) — top-level
  chỉ còn pipeline khớp bài.
- Viết lại README (cả root và code/) cho khớp title/dataset mới.
- **Verify pipeline chạy end-to-end từ trạng thái sạch** (xoá outputs, chạy lại như reviewer
  clone), rồi **đối chiếu số regen KHỚP bảng manuscript** từng chữ số.
- Nếu Data Availability hứa "released fetch script" → script đó PHẢI tồn tại và tái lập
  được (lý tưởng: bit-identical, so md5). Đừng claim cái chưa tạo.
- Bảng manuscript thường được dựng bằng format riêng KHÁC tên file script sinh ra → viết một
  generator sinh thẳng đúng format manuscript từ CSV, để số không drift khỏi code.

## Verify push: git object, KHÔNG tin raw CDN

- Sau push, `raw.githubusercontent.com` có thể cache nội dung CŨ vài phút → tưởng push hỏng.
- Nguồn chân lý: đọc từ git object — `git show origin/main:path/to/file` (sau `git fetch`),
  hoặc so `git rev-parse HEAD` local vs `git ls-remote`. GitHub API contents cũng có thể cache;
  git object thì không.
- Tokenized HTTPS push (SSH blocked): nhúng token vào URL 1 lần, in redacted, rồi DỌN token
  khỏi git config ngay sau (`git remote set-url` về URL sạch); verify remote URL không lộ token.
