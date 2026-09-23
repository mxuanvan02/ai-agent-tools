# Đồng bộ manuscript ↔ thí nghiệm + audit toàn vẹn (manuscript/experiment sync & integrity audit)

Dùng khi người dùng yêu cầu: "rà soát toàn diện", "đồng nhất tham số rồi chạy lại toàn bộ",
"đồng bộ kết quả với nội dung trình bày", hoặc khi sửa method/results làm lệch narrative giữa
abstract → intro → method → results → conclusion → slide. Đã chứng minh trên bài bài bandwidth-scheduling (hội nghị C1).

## Nguyên tắc cốt lõi (đã được người dùng xác nhận)

1. **Narrative đảo chiều ⇒ DỪNG, báo người dùng trước khi viết prose.** Chạy lại trên dataset khó hơn
   có thể lật luận điểm chính (vd trên dữ liệu VN, Fixed-B3 thắng objective so với phương pháp đề
   xuất vì vi phạm nhiều ⇒ polling đầy đủ đáng giá). KHÔNG tự ý gloss/hợp lý hoá. Báo số thật +
   xin quyết framing. Đây là DỪNG-khi-narrative-đảo, ngang hàng quy tắc "vá >2 lần thì chẩn đoán gốc".

2. **Không ép đồng nhất một dataset nếu nó buộc framing thiếu trung thực.** Lựa chọn trung thực
   thường là **hai nền tách bạch, khai báo rõ**: nền chính (so SoTA/baseline) + ca khó riêng
   (hard-regime case study cho biến thể mới). Phải khai báo minh bạch ở CẢ abstract, intro,
   method, conclusion VÀ slide — không để một chỗ nói "thắng mọi kênh" còn chỗ khác nói "marginal".

3. **Verify mọi con số từ CSV nguồn TRƯỚC khi sửa prose.** Recompute từng p-value/effect-size r/%
   bằng scipy trên raw CSV (Wilcoxon ghép theo seed×window). Đừng tin số trong .tex có sẵn.
   - Phân biệt nguồn của mỗi con số: "threshold-exit rate" (thuộc tính của TRACE gốc, vd
     true_violation ≈ 20.74%) KHÁC "missed_pct" (vi phạm bị bỏ sót SAU scheduling, vd 16–27%).
     Đừng đoán — mở trace gốc tính trực tiếp.
   - Dấu effect-size r phải khớp hướng dMean (policy xấu hơn baseline ⇒ r dương theo quy ước đang dùng).

4. **File mồ côi mang số cũ là bẫy stale điển hình.** Một `.tex` table KHÔNG được `\input` ở đâu
   nhưng vẫn nằm trong repo, mang số từ lần chạy cũ mâu thuẫn 1 bậc độ lớn với bảng hiện hành.
   Grep `\input` + `\ref{label}` để phát hiện. Xử lý: TÁI SINH từ CSV đã verify (không xóa —
   destructive; backup giữ nguyên), để repo công khai không còn artifact mâu thuẫn.

## Quy trình RLM (đã chạy thành công)

**Wave 0 — map bề mặt (tự làm, đừng giao subagent):** đọc TRỌN mọi file nguồn (sections +
bảng + abstract + slide) + định vị CSV thống nhất. Bạn là người giữ "hướng mới" trong đầu nên
phải tự lập bản đồ stale trước khi brief subagent — subagent không có ngữ cảnh narrative mới.

**Wave 1 — audit fresh-eyes, READ-ONLY, 3 subagent song song, không giẫm chân:**
- A = narrative manuscript (mọi claim có khớp hướng mới? còn "matched bandwidth/in every channel"/overclaim/mâu thuẫn nội tại?)
- B = toàn vẹn số (mọi số prose+bảng vs CSV; file mồ côi; dấu r; đồng bộ ký hiệu/eqref)
- C = slide vs manuscript + luật người dùng (narrative, cấu trúc, **rò rỉ chi tiết nội bộ**, overclaim, độ rõ phần toán)
Lý do fresh-eyes: người vừa sửa vòng trước bị "mù" do tự hợp lý hoá; subagent độc lập bắt được.
Read-only ⇒ zero rủi ro ghi đè; trả về punch-list theo severity.

**Wave 2 — vá tuần tự, từng chỗ một, có verify:** backup cả hai artifact dưới `_backups/<ts>/`
trước. Patch các file độc lập song song. Sau mỗi cụm: build + đếm trang + 0 undefined + grep
claim cũ = 0. Cuối: build-from-bundle (xoá aux, build lại từ đầu) để chắc tái lập.

## Pitfalls

- Grep "thắng/mọi/cả hai" sẽ bắt cả câu phủ định trung thực ("bài bandwidth-scheduling-PD KHÔNG thắng mọi metric") —
  đọc ngữ cảnh, đừng nhận bừa là claim cũ.
- Overfull khi thêm nội dung slide: phân biệt `\vbox` (tràn dọc, <8pt thường vô hại) vs `\hbox`
  (tràn ngang ra lề, phải sửa). Grep log lấy "Overfull \\vbox/\\hbox ... at line N".
- Rò rỉ nội bộ trên slide qua cửa hậu: liệt kê ĐÚNG 3 trạm/3 vùng ⇒ ngầm lộ N=3. Ký hiệu toán
  dùng mà không định nghĩa ($\widehat L,\widehat A,\widehat M$) là đứt gãy toán — thêm 1 dòng diễn giải.
- `rm` nhiều file aux trong build-from-bundle kích hoạt security scan "mass file deletion" — bình
  thường, chỉ cần approve; hoặc dùng `latexmk -C` thay cho `rm *.aux *.log ...` để gọn.
