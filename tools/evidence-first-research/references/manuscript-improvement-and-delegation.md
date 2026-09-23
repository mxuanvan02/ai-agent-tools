# Cải thiện manuscript + giao review cho coding-agent (bài học phiên bài bandwidth-scheduling)

Ghi lại các pattern lặp lại khi người dùng nhờ "feedback / cải thiện toàn diện" một manuscript
có kèm code thực nghiệm. Đây là kiến thức bền, không phải lỗi môi trường nhất thời.

## 1. Giao review cho Claude CLI qua SuperKiro / 9router (proxy nội bộ)

Khi giao feedback manuscript cho `claude -p` chạy qua proxy Anthropic-compatible nội bộ:

- **`503 No available accounts` / `500 quota exhausted on AmazonQ` là THEO TỪNG MODEL và tạm thời**,
  không phải "proxy hỏng". Mỗi model (opus-4.8 / sonnet-5 / sonnet-4.6 / haiku-4.5) map sang một
  pool account khác nhau. Cách xử đúng: **probe thẳng `/v1/messages` từng model**, chọn model trả
  HTTP 200 mà chạy. 503 trả về <1ms = pool trống thật cho model đó; 500 = quota; cứ đổi model.
  Người dùng xác nhận "dùng được sonnet-4.6 nghĩa là vẫn được" — đừng dừng lại báo blocker khi vẫn còn
  một model sống.
- **Pitfall `$HOME` phân kỳ:** shell của Hermes có `$HOME=~/.hermes/home`, KHÔNG phải
  `/home/<user>`. Wrapper `claude` (ở `~/.local/bin/claude`) source `$HOME/.claude/9router.env`,
  nên nó đọc file `~/.hermes/home/.claude/9router.env` (bản CŨ, có thể trỏ pool chết `20128`),
  chứ không phải `/home/<user>/.claude/9router.env` (bản tốt, trỏ SuperKiro `20131`).
  Triệu chứng: sửa "đúng file" mà base URL/model vẫn ra giá trị cũ. Fix: sync/đối chiếu cả hai
  file, và nhớ clear biến `ANTHROPIC_BASE_URL` còn tồn trong session shell (env persist giữa các call).
- Redact tuyệt đối API key/token khi probe. Không bao giờ in `NINEROUTER_API_KEY`.

## 2. Kỷ luật kết quả âm khi "cải thiện" một đóng góp của bài

Khi một thành phần được nêu là contribution (vd một term risk/CVaR trong công thức) **lặp lại
nhiều lần không cải thiện** dưới ablation/thử nghiệm:

- KHÔNG vá lặt vặt lần thứ 3-4. DERIVE root cause trước (đúng contract của người dùng: prove math BEFORE
  expensive runs). Thường gặp: một term **dư thừa vì trùng tín hiệu** đã có sẵn trong detector/loss
  (vd raw `p_vio` trong urgency score bị đếm hai lần vì `eval_step` đã dùng `p>=0.55`).
- Dạng đúng thường là **truncation bậc dẫn đầu của một đối tượng Bayes-optimal**: thay `p_vio` bằng
  **decision-uncertainty `g(p)=4p(1-p)`** (value-of-uncertainty) — cực đại ở biên `p≈0.5`, =0 khi đã
  chắc chắn (poll thêm vô ích). Đây là VoU/VoI đúng nghĩa, defensible với reviewer Q1.
- Kết quả âm CÓ THỂ là đóng góp sạch: "VoU + primal-dual đã hút hết lợi ích khả thi; tail-machinery
  không thêm gì trên regime đuôi-nhẹ" là thông điệp Occam mạnh. Nhưng nếu người dùng muốn GIỮ term và
  làm nó có ích (không bỏ vào future work), hãy tìm **đại lượng đuôi-nặng ĐÚNG** để áp: đuôi thời gian
  của loss thường quá nhẹ; đuôi **cross-sectional** (CVaR trên tập risk chưa-poll mỗi slot) hoặc
  miss-risk trong burst mới là chỗ tail-pricing có đất diễn. Luôn verify bằng paired Wilcoxon +
  CI trước khi ghi số vào bài; báo trung thực trade-off (giảm tail nhưng +objective/+missed).
- NEVER fabricate số. Nếu không regen được thì nói thẳng.

## 3. Thực tế tái lập (reproduction reality)

- Code companion của người dùng thường ở **GitHub (`OWNER/bài bandwidth-scheduling` ...), KHÔNG nằm local**. Trước khi
  kết luận "không có code", clone repo + kiểm tra mọi commit/branch + tất cả `_backups/`.
- **Dữ liệu nguồn có thể chưa từng được commit** (vd ERA5 3-station cho bảng CVaR): chỉ còn file
  `.tex` kết quả, không có script/data sinh ra nó → bảng đó KHÔNG tái lập được kể cả với method cũ.
  Đây là rủi ro thật cho mục "Data and Code Availability". Xử: dựng lại module trên dữ liệu thật đang
  có, frame trung thực (đổi "ERA5 Mekong" → "hard-regime replay từ data sẵn có") thay vì bịa lại data.
- Dữ liệu thật thường **hardcode N nhỏ** (vd 3 zone = 3 `loop` trong CSV). Muốn chạy N lớn phải sinh
  zone tổng hợp (bootstrap stream thật + offset/bias độc lập) và **frame rõ là "synthetic scalability
  stress test"**, giữ N thật làm anchor, không đụng claim real-data ở thí nghiệm chính.

## 4. Self-overlap giữa các manuscript của chính người dùng

Người dùng chạy song song nhiều manuscript (bài bandwidth-scheduling, bài AoI-greenhouse, dự án zero-touch, LVTN...). Nếu một thành phần method
(vd VoU `p(1-p)`) đã dùng ở bài khác (CAW), phải **chèn câu phân biệt trong related work** để tránh
tự trùng lặp (self-plagiarism) khi cả hai cùng vòng review. Người dùng ưu tiên an toàn cho cả hai bài.
