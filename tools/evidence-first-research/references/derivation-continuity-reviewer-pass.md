# Derivation-Continuity Reviewer Pass (no-blind-reader)

Khi người dùng yêu cầu "review như reviewer", "các công thức đã nối liền nhau chưa",
"chỗ nào chưa rõ thì bổ sung công thức với =/<=>/==> để có từng bước, không làm mù
người đọc". Đây là vòng review RIÊNG về *derivation continuity* (mạch nối từng bước),
KHÁC với review consistency/correctness (xem `reviewer-deep-read-theory-code-consistency.md`)
và khác với audit số liệu (xem `manuscript-experiment-sync-audit.md`).

## Quy trình (đã chạy thành công trên bài AoI-greenhouse / bài probe-transmit IoTJ)

1. **Chạy song hai luồng fresh-eyes.** Dispatch một reviewer subagent (background) soi
   "bước nhảy" trong từng chuỗi derivation; ĐỒNG THỜI tự đọc lại các file toán nặng nhất.
   Khi subagent về thì CHÉO KIỂM hai danh sách — không phụ thuộc một nguồn. Thường trùng
   80% + mỗi bên bắt thêm vài chỗ.
2. **Phân loại bước nhảy theo severity** (CAO/VỪA/THẤP) theo mức "làm mù người đọc": một
   số hạng/thừa số xuất hiện mà không có dấu `=` dẫn ra nó = CAO; bước đại số một dòng bị
   nói-bằng-lời = VỪA; ẩn một đẳng thức hiển nhiên (vd `s^2=v`) = THẤP.
3. **Chèn dòng trung gian**, mỗi đề xuất kèm LaTeX sẵn dùng, dùng `=` / `\Leftrightarrow`
   / `\Rightarrow`. Ưu tiên `\underbrace{...}_{...}` để gắn nhãn "dạng khái niệm + refinement".
4. **Build đủ chuỗi** (latexmk hoặc 2x pdflatex): thêm equation mới ⇒ cross-ref cần pass 2.
   "undefined: N" sau 1 pass + log "Label(s) may have changed. Rerun" KHÔNG phải lỗi —
   chạy lại cho về 0. Đừng báo lỗi non khi mới 1 pass.
5. **Đồng bộ slide** nếu mạch đổi — nhưng slide ở mức trình bày thường KHÔNG cần chuỗi `=`
   chi tiết như manuscript; chỉ cần nhất quán (vd payload index trên slide đã có `p_i`).

## Các pattern "bước nhảy" hay gặp + cách vá (tái dùng được)

- **Tổng hình học AR(1):** cho thẳng dạng đóng `μ=α^h x+β Σα^k` rồi nói "relaxes toward
  β/(1−α)" mà không hiện `Σ_{k=0}^{h-1}α^k=(1−α^h)/(1−α) --→_{h→∞} 1/(1−α)`. Chèn dòng tổng
  đóng + giới hạn.
- **Hai-đuôi → một-đuôi:** `1−[Φ(a)−Φ(b)] = Φ̄(a)+Φ(b) ≈ Φ̄(z)` (giữ biên gần, bỏ đuôi xa).
  Bước tách bracket + `1−Φ=Φ̄` + xấp xỉ đuôi gần phải hiện, dùng `=` rồi `≈`.
- **Recursion affine → nghiệm hình học:** (a) giải điểm cố định `π=π(1−p)+(1−π)q ⟺ π=...`;
  (b) trừ điểm cố định để thuần nhất hoá; (c) tháo k bước thành `(slope)^k`. Ba bước, đừng
  để nghiệm geometric "rơi từ trên trời".
- **Dạng khái niệm → dạng triển khai (chỗ NẶNG nhất):** index khái niệm `VoU+wD` đột ngột
  thành `p_i V·values − w_res r + mask·danger·w_pd`. Chèn `VoU(t|metadata)=V·values` rồi
  viết bản impl bằng `\underbrace{...}_{dạng khái niệm}` + `\underbrace{...}_{refinement}`.
  Nói rõ phạm vi từng trọng số (vd `p_i` chỉ nhân số hạng giá trị, debt/gate không phụ thuộc kênh).
- **Magic constant trong định lý dẫn xuất từ nguồn:** `C=256 r_max λ_W² |S|²/γ_B²` chỉ
  "Instantiate Thm 1 of [ref]". Thêm một dòng `\underbrace` ánh xạ TỪNG thừa số về nguồn
  (|S|²=state size, λ_W²=mixing, γ_B⁻²=budget margin, 256 r_max=meta-theorem) để hết "magic number".
- **Proof step nói-bằng-lời:** vd Dominance `gap≥V_max/w ⟹ w·gap≥V_max≥u_j−u_i ⟹ S_i≥S_j`
  và Counting `⌈(N−1)/B⌉≤⌈N/B⌉` — viết thành chuỗi `\Rightarrow` tường minh.

## Pitfalls
- **Đề xuất LaTeX của subagent THƯỜNG có lỗi cú pháp** (`\Rightarow` thiếu chữ, `\underbrace`
  thiếu ngoặc đóng `}`, `\overset` sai). KHÔNG bê verbatim — viết lại sạch rồi mới chèn.
- Giữ nguyên TOÁN, chỉ chèn bước hiển thị: không đổi kết quả, không đổi ký hiệu (ký hiệu là
  vòng khác). Đổi tên biến lẫn vào pass này dễ gây sai sót chéo.
- Mỗi equation mới nên có `\label` đồng bộ phong cách (vd `eq:geom_sum`), kể cả khi chưa
  `\eqref` ngay — để nhất quán và tham chiếu được về sau.
