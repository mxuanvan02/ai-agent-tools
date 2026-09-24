# Reproducibility trust-audit + theory-derivation for người dùng's papers

Dùng khi người dùng nói kiểu "sửa lui sửa tới nên không tin được kết quả nào là thật",
hoặc khi một paper có nhiều bản .tex/.zip song song và không rõ số nào đúng.

## Vấn đề gốc: mất niềm tin = lỗi quy trình, KHÔNG phải lỗi số

Triệu chứng điển hình (bài bandwidth-scheduling session): 3–4 bản `.tex` song song
(`X/`, `X_clean/`, `X_pkg/X/`) + 6–7 file `.zip` rải rác ở `~` và thư mục build,
cộng git log cho thấy một feature (vd VoU/CVaR) bị **thêm → bỏ → tống vào legacy/**
trong vài commit. Khi tồn tại N bản, "kết quả nào là thật" là câu hỏi không trả
lời được → người dùng mất niềm tin. ĐỪNG sửa thêm nội dung; hãy CHỐT 1 nguồn sự thật.

## Quy trình audit (làm THEO THỨ TỰ, chưa xóa/sửa gì ở bước điều tra)

1. **Định vị bản canonical = REPO tái lập được**, không phải bản .tex mtime mới nhất.
   Tìm repo git (`search_files '*.git'`), đọc `git log` đầy đủ + `README` để biết
   pipeline. Repo có code+data+script sinh bảng LaTeX mới là nguồn sự thật.
2. **Kiểm chứng tái lập (phép thử niềm tin)**: chạy lại toàn bộ pipeline vào thư mục
   TẠM (`/tmp`), rồi `diff` từng bảng `.tex` + CSV mới sinh với bản đã commit.
   - KHỚP 100% → số sinh tất định (deterministic) từ script + data thật → tin được.
   - Lệch → biết chính xác số nào "ảo". Báo thẳng con số nào lệch.
3. **PHÁT HIỆN QUAN TRỌNG — manuscript↔repo number drift**: bản PDF/submit "mới nhất"
   thường vẫn ôm **số cũ** (vd thời greenhouse/CVaR) trong khi repo đã chuyển dataset
   (vd sang ERA5 thật). Nguy hiểm nhất: hai bản kể **câu chuyện NGƯỢC nhau**
   (bản submit: "bài bandwidth-scheduling-PD *thua* Safety Obj, chỉ tiết kiệm băng thông"; repo:
   "bài bandwidth-scheduling-PD *thắng* cả obj lẫn băng thông"). Nếu nộp bản lệch, reviewer chạy lại code
   sẽ ra số khác → toang. LUÔN diff số trong prose/bảng của bản submit với repo trước
   khi gọi "submission-ready".
4. **Chốt & báo**: tuyên bố repo là canonical duy nhất; đề xuất đưa các bản .tex/.zip
   thừa vào `_backups/<ts>/` (KHÔNG xóa) để chỉ còn 1 bản làm việc. Chờ người dùng xác nhận.

## Trả lời "đề xuất cuối là gì / hàm lượng khoa học thế nào"

- ĐỌC THẲNG code đang sống (không nói theo trí nhớ) + lấy 2 bảng kết quả thật.
- Tách bạch cái còn sống vs cái đã bỏ (vd bài bandwidth-scheduling-PD sống; VoU/CVaR đã đẩy legacy).
- Nói CẢ điểm mạnh LẪN điểm yếu: hằng số heuristic chưa dẫn xuất, metric objective
  do chính tác giả định nghĩa (thắng gần như tất yếu → bằng chứng thật nằm ở
  bandwidth-saving + Wilcoxon effect size, không phải ở objective), N nhỏ, scaling synthetic.
- Sửa câu chuyện cho khớp số thật: "cắt >50% băng thông giữ NGUYÊN độ an toàn"
  (KHÔNG phải "an toàn HƠN" nếu Wilcoxon miss-rate p không ý nghĩa / effect size âm).

## "Dẫn xuất lý thuyết" = rigor, KHÔNG phải novelty (nói thẳng với người dùng)

Biến hằng số gõ tay thành đại lượng có nghĩa: viết bài toán tối ưu có ràng buộc
tường minh → Lagrangian → per-slot dual (drift-plus-penalty, Neely 2010) → projected
supergradient/dual ascent → cận hội tụ. Khi đó step size = α, penalty = shadow price,
target = ràng buộc. Reviewer hết hỏi "sao lại 0.010".
- **Trung thực**: khung Lyapunov/dual-ascent đã có sẵn → dẫn xuất cho CHẶT CHẼ
  (phòng thủ được), KHÔNG tạo cái mới về toán. Đừng thổi thành đóng góp lý thuyết.
- Ở tầm hội nghị (6–8 trang): Mức "dẫn xuất textbook + Lemma/Proposition hội tụ" là ĐỦ.
  Đừng ép novelty toán (regret bound riêng) vào bài 8 trang — loãng + dễ bị bắt "claim quá tay".

## Chèn toán vào manuscript (mechanics đã kiểm chứng)

- Text agent thêm mới = YELLOW review-markup, strip trước khi nộp. Preamble:
  `\usepackage{soul}\sethlcolor{yellow}\newcommand{\rev}[1]{\hl{#1}}` cho inline;
  `\usepackage{mdframed}\newmdenv[backgroundcolor=yellow!30,...]{revblock}` cho khối
  display math (soul `\hl` VỠ trên display math → phải dùng mdframed cho block).
- Build sạch: latexmk đa lượt (bibtex chạy lại). Latexmk có thể tái dùng `.bbl`/`.aux`
  cũ → "undefined references" giả; kiểm PASS CUỐI mới đáng tin (undefined=0).
- Đếm trang giữ trong limit (hội nghị C1 6–8). Vision-check TỪNG trang chứa math mới:
  Lemma/Proposition có thể tràn sang trang kế → check cả trang n và n+1.
- `rm` bị safety-guard chặn (kể cả trong /tmp). ĐỪNG xóa artifact build; latexmk tự
  tái sinh. Build in-place thay vì clean-dir.
