# Giải thích pipeline/figure bằng lời, chứng minh cơ chế bằng số, và đưa toán cơ chế vào System Model

Dùng khi người dùng (sau khi đã có figure/method) yêu cầu một trong các việc sau — đây
là chuỗi việc rất hay đi liền nhau trong cùng một đợt củng cố manuscript:

1. "Giải thích qua pipeline từ đầu đến cuối, giải nghĩa TỪNG KÝ TỰ trong hình bằng lời."
2. "Làm rõ hơn ý nghĩa công thức toán (bộ lọc Bayes là gì, xác suất ... tính kiểu gì, dùng gì)."
3. Một câu hỏi cơ chế sâu, thường lộ ra HIỂU NHẦM khi đọc ngang (vd "channel lane có
   phải là metadata node gửi lên không?", "node bị bỏ thì xác suất hồi lại thế nào?").
4. "Đưa toàn bộ những yếu tố đó vào System Model, chỉ cần công thức + giải thích để
   người đọc nắm cách hoạt động tường minh nhất."

## Bài học cốt lõi

### A. Thuyết minh figure/pipeline bằng lời + glossary từng ký tự
- ĐỌC LẠI file figure thật (`figures/fig_architecture.tex`) TRƯỚC khi giải thích — giải
  thích đúng cái đang vẽ, không theo trí nhớ. Mỗi node/mũi tên/nhãn trong TikZ là một ý
  cần nói.
- Cấu trúc trả lời: (1) tổng quan "hình vẽ cái gì" (liệt kê các khối + nghĩa màu mũi tên
  DL/UL/feedback), (2) BẢNG glossary `ký hiệu | tên | ý nghĩa` cho MỌI biến trong hình,
  (3) thuyết minh luồng đánh số ①②③… đi từ đầu đến cuối "nhận gì → tính ra gì → gửi đi
  đâu", (4) một câu tóm mạch end-to-end, (5) map lại các challenge (C1/C2/C3) về đúng vị
  trí trong sơ đồ.
- Đây là ANSWER (giải thích), KHÔNG sửa file — trừ khi người dùng nói "đưa vào bài".

### B. Bắt và sửa HIỂU NHẦM của người đọc NGAY, lên đầu phản hồi
- Khi câu hỏi của người dùng chứa một giả định sai ("người dùng đang nghĩ nó là X hả?"), mở đầu
  bằng đính chính dứt khoát (✓/❌) rồi mới giải thích — vì hiểu nhầm đó thường là gốc rễ
  của cả loạt câu hỏi sau. Ví dụ thật: "Channel lane KHÔNG phải metadata node gửi lên;
  nó là bộ lọc Bayes chạy TẠI gateway, chỉ ăn 1 bit kết quả giao o_i." Phân biệt rõ hai
  luồng dễ lẫn (belief-update tự suy đoán phía gateway vs metadata uplink ở Stage 2).

### C. Chứng minh cơ chế bằng SỐ THẬT, reproduce thẳng từ code (không hand-wave)
- Khi giải thích một cơ chế động (bộ lọc Bayes, hội tụ, self-healing), ĐỪNG chỉ viết
  công thức — chạy một mô phỏng nhỏ (execute_code) tái hiện ĐÚNG hàm trong code
  (`channel.py`), in ra bảng số minh họa. Ví dụ: belief Bad sau khi rớt 1 gói = 0.933 →
  chỉ chạy bước predict (không observation) → 0.755 → 0.633 → … → 0.387 sau ~10 vòng,
  hội tụ về stationary π^B = p_gb/(p_gb+p_bg) = 0.375. Số thật trả lời thẳng câu "hồi
  lại thế nào" mạnh hơn mọi đoạn văn.
- Lấy tham số THẬT từ code (`severe_burst`: p_gb=0.12, p_bg=0.20, p_ok_G=0.97,
  p_ok_B=0.30), không bịa.

### D. Đưa toán cơ chế vào System Model (EXECUTE, build-gated)
Khi người dùng duyệt "đưa toàn bộ vào System Model, chỉ cần công thức + giải thích":
- Backup `sections/02_system_model.tex` vào `_backups/sysmodel_<ts>/` trước khi sửa tại chỗ.
- ĐỌC §2 hiện có TRƯỚC để biết phần nào ĐÃ có (tránh trùng) — vd §2 đã có predict/update/
  p_succ rồi thì chỉ thêm phần CÒN THIẾU.
- Ba khối toán điển hình cần đủ cho một method "channel-aware + threshold-aware":
  1. **Gateway-side state estimator**: mean/variance dự báo theo TUỔI a_i(t):
     μ_i=α^{h}x_i+β·Σα^k, σ_i²=σ_ω²·Σα^{2k}; giải nghĩa "node tươi σ²=0, càng cũ variance
     phình về σ_ω²/(1−α²) ⟹ bất định là hàm tăng của độ cũ". Kèm P_vio,i qua Φ và margin
     chuẩn hóa z_i, đuôi Φ̄(z_i).
  2. **Kênh G-E đầy đủ**: ma trận chuyển P (2×2), phân phối dừng π^B=p_gb/(p_gb+p_bg) —
     cũng là PRIOR khi lâu không probe.
  3. **Belief self-healing (đúng câu hỏi reviewer "node có bị starve vĩnh viễn không?")**:
     khi không served, belief chỉ chạy predict ⟹ đệ quy affine, hệ số co (1−p_gb−p_bg)∈
     (−1,1), điểm bất động = π^B. Hội tụ HÌNH HỌC:
     p̂^B(t0+k)−π^B = (1−p_gb−p_bg)^k (p̂^B(t0)−π^B) → 0, timescale ~1/(p_gb+p_bg) slot.
     Diễn giải: "một gói rớt không blacklist node vĩnh viễn; cộng service debt D_i là hai
     cơ chế chống đói bổ trợ."
- Mỗi `\eqref` mới ⟹ phải gắn `\label` cho phương trình được tham chiếu (vd AR(1) phải có
  `\label{eq:ar1}` nếu estimator `\eqref{eq:ar1}`), nếu không "undefined reference".
- Công thức PHẢI khớp 1-1 với code (đọc `channel.py::update_bad_belief_vec`,
  `forecast.py::AR1Model.forecast_stats`), cite đúng (`gilbert1960burst` đã có sẵn .bib).
- Build gate: pdflatex→bibtex→pdflatex→pdflatex, grep pass cuối `Citation.*undefined`=0,
  undefined ref=0, overfull>60pt. CHÚ Ý false-positive: dòng `LaTeX Font Warning: Font
  shape ... undefined` khớp nhầm grep "undefined" — kiểm lại bằng grep "LaTeX Warning:
  Reference" / "There were undefined references" mới là ref thật.
- VERIFY layout: render trang §2 ra PNG (`pdftoppm -png -r 130 -f <page> -l <page>`) +
  vision-check ma trận/đa-dòng có tràn cột / đè không. Build sạch KHÔNG đủ để biết math
  có tràn lề trong cột IEEE hẹp.

### E. Trình bày chứng minh step-by-step trong chat (proof walkthrough, không sửa bài)
Khi người dùng nói \"trình bày step-to-step phần chứng minh, làm rõ từng công thức\" (đây\nlà ANSWER/giảng giải, KHÔNG nhất thiết sửa manuscript):\n- Mở đầu bằng MỘT bảng glossary ký hiệu dùng chung cho mọi proof, rồi đi từng chứng minh\n  từ DỄ tới KHÓ (Bổ đề → Mệnh đề → Định lý), không theo thứ tự xuất hiện trong bài.\n- Mỗi proof: chia bước đánh số **B1/B2/B3…**, mỗi bước = một dòng công thức + một dòng\n  diễn giải bằng lời (dùng blockquote `>` cho phần trực giác). Kết quả chính đóng khung\n  `\\boxed{...}` (hoặc **bold** trong chat) để mắt bắt ngay.\n- Với bước dùng kỹ thuật chuẩn (khai triển Mills, mô-men riêng phần Gaussian, telescoping,\n  projection chỉ-tăng), GỌI ĐÚNG TÊN kỹ thuật + một câu vì sao số hạng triệt tiêu — đừng\n  nhảy bước bằng \"dễ thấy\".\n- Kèm trực giác đời thường cho kết quả chốt (vd \"ε nhỏ = ngưỡng nằm xa tâm chuông nhiều σ\n  ⟹ phần đuôi vừa hiếm vừa mỏng nên 'vượt bao xa' không kịp đóng góp\").\n- KẾT THÚC bằng cách HỎI người dùng muốn (1) nhúng các bước này vào Appendix cho tường minh,\n  hay (2) để riêng một file \"proof walkthrough\" giữ manuscript gọn — đừng tự nhúng vào bài\n  khi người dùng chỉ xin giảng giải. (Bản slide proof-sketch 3-bước xem\n  `references/manuscript-to-beamer-slides.md` §5f.)\n\n## Liên quan
- Vẽ/sửa figure để lộ chiều sâu: `references/manuscript-figure-algorithmic-depth.md`
  (đã bổ sung lesson DL/UL data-flow).
- Bảo vệ thiết kế closed-form & vì sao dự đoán tương lai không tốt hơn:
  `references/defending-closed-form-design.md`.
- Audit nhất quán xuyên section sau khi thêm equation: xem subsection "Cross-section
  notation + consistency audit" trong SKILL.md.
