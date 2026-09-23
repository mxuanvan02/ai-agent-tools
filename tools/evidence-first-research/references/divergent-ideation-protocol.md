# Divergent Ideation — sinh ý tưởng trước khi chấm (chống "sáng tạo thấp")

Trigger: người dùng nói "tính sáng tạo chưa được nhiều", "thiếu ý tưởng mới", "brainstorm đề tài",
"hướng nào mới", hoặc cần mở rộng không gian đề tài TRƯỚC khi viết RQ Brief (Stage 1).

## Chẩn đoán (tại sao workflow cũ sinh ít ý tưởng)

Pipeline nghiên cứu của người dùng lệch hẳn về khâu HỘI TỤ: claim-check, gap-scan, integrity audit,
baseline-comparison — tất cả đều là bộ lọc. Khâu PHÁT TÁN (sinh thô, số lượng lớn, chưa phê phán)
không có bước nào được thiết kế. Hậu quả: ý tưởng bị chấm ngay khi vừa sinh → con mới lạ chết
trước khi kịp phát triển. Model tự nhiên luôn trả về ý phổ biến nhất = theo định nghĩa là không mới,
nên nếu không có cơ chế ép phân kỳ thì output luôn hội tụ về trung bình của corpus.

## Quy tắc vận hành (thứ tự CỐ ĐỊNH, cấm đảo)

1. **PHÁT TÁN** — rẻ, rộng, CẤM phê phán, cấm hỏi "có mới không". Mục tiêu số lượng.
2. **LỌC KHẢ THI** — bằng tài sản sẵn có (simulator, dataset, code, venue đích, thời gian).
3. **GAP-SCAN** — chỉ chạy trên những con sống sót ở bước 2 (đắt, không scan cả 20 hướng).
4. **CLAIM-CHECK** — `references/jev-systemone-claim-gate.md` cho các khẳng định novelty.
5. **NGƯỜI DÙNG QUYẾT** — model mở rộng không gian ứng viên; con người nhận ra tổ hợp nào đáng giá.

Nếu người dùng hỏi "hướng này mới không" ngay trong bước 1 → trả lời "để agent ghi lại, mình chấm ở bước 3",
đừng cắt ngang vòng phân kỳ.

## 5 kỹ thuật phát tán (dùng ≥3, không dùng 1)

### A. Ép analogie cross-domain CÓ QUOTA

Bắt sinh **N phép cấy** (N ≥ 10) từ lĩnh vực XA vào đúng bài toán lõi. Quota là cơ chế bắt buộc —
không có quota, model sinh 3 ý rồi tự dừng ở vùng quen thuộc.

Cấu trúc mỗi phép cấy: `<nguồn domain> → <đối tượng ánh xạ> → <bài toán đích> → <metric/guarantee có thể derive>`.
Domain nên đổi hẳn trục (dịch tễ, tài chính, sinh thái, giao thông, miễn dịch học, lý thuyết hàng đợi,
cơ học chất lỏng...), không đổi trong cùng domain láng giềng.

### B. Subagent CHỐNG NEO (anti-anchoring)

Cơ chế từ skill `council`: subagent fresh chỉ nhận **câu hỏi + context tối thiểu**, KHÔNG nhận
hội thoại đang chạy, KHÔNG nhận các ý đã sinh. Mỗi con một persona khác trục
(kẻ hoài nghi / người thực dụng / nhà sinh học / kỹ sư vận hành...). Song song 3–4 con,
đọc kết quả SAU khi đã ghi lại ý của chính mình (để synthesis không mirror theo con nào).

### C. Đảo ràng buộc (constraint inversion)

Liệt kê mọi constraint trong bài hiện tại, với mỗi cái hỏi "nếu đảo ngược / bỏ hẳn / nhân đôi thì sao?".
Mỗi phép đảo là một biến thể đề tài. Ví dụ đã dùng: bandwidth khan hiếm → bandwidth dư thừa nhưng
energy khan hiếm; sensor thụ động → sensor chủ động (probe, giống bài AoI-greenhouse); N cố định → N học online.

### D. Negative result = NGUYÊN LIỆU, không phải rác

Chuỗi negative đã ghi trong skill (predictor enhancement thua → closed-form near-sufficient;
CVaR suy biến trên tín hiệu zero-inflated) đã thành pattern đóng góp Q1: *"đã thử cái phức tạp,
chứng minh cái đơn giản là đủ"*. Với mỗi negative result, hỏi: (1) regime nào làm nó thua?
(2) đảo regime đó có thành đề tài mới không? (3) guarantee nào giải thích được vì sao thua?

### E. Đảo chiều gap-scan (máy ĐÀO ý tưởng, không phải máy BẢO VỆ ý tưởng)

Skill `literature-gap-recon` vốn dùng để bảo vệ novelty claim sau khi có ý tưởng. Đảo nó thành
nguồn sinh: quét components **dense** trước, mỗi **empty join** tìm được là một vùng đất chưa ai
cắm cờ → ý tưởng sinh ra từ bằng chứng trống có sẵn, thay vì từ trí nhớ model (model memory có
cutoff đúng 12–18 tháng = đúng chỗ gap claim chết).

## Bài học đo thật: System-One là bộ lọc tốt nhưng là GIÁM KHẢO NOVELTY TỆ

Thí nghiệm 2026-09-24 trên jev-1.13.0 (backend=jev, 680 token in / 80 out, 359ms):
mồi 5 hướng cho bài AoI/greenhouse IoT (Whittle non-stationary, dịch tễ SIR, portfolio tài chính,
Lotka-Volterra, Jev semantic urgency), hỏi "đáng spike 1 tuần nhất cho Q1".

| Hướng | probability |
|---|---|
| whittle_nonstat (mở rộng lý thuyết từ bài cũ — AN TOÀN nhất) | **0.59** |
| epi_sir_scheduling (cấy ghép sáng tạo) | 0.19 |
| finance_portfolio (cấy ghép sáng tạo) | 0.19 |
| jev_semantic_urgency | 0.02 |
| lotka_volterra | 0.01 |

Choice confidence tổng = **0.49** → rơi đúng dải giữa của claim-gate → escalate cho người.

Hai kết luận:
1. **Jev bị kéo về cái quen thuộc.** Nó xếp cao nhất hướng ít rủi ro nhất (mở rộng từ prior work của chính
   tác giả) và cho điểm gần 0 hai hướng cross-domain. Nếu để nó chấm ở BƯỚC 1 thì chính nó giết ý tưởng mới.
   → Chỉ dùng Jev/System-One ở bước 3–4 (lọc claim, gate hành động), KHÔNG dùng để xếp hạng novelty.
2. **Confidence 0.49 trên lựa chọn mở là tín hiệu đúng, không phải lỗi.** Docs TypeSafe: nhiều lựa chọn
   chấp nhận được cũng làm phân bố dẹt → low confidence. Với câu hỏi giá trị/mở, dải giữa = "cần người quyết".
   Đừng vặn câu hỏi cho đến khi confidence cao — đó là ép model giả vờ chắc.

## Chi phí & ROI

- Bước phát tán: rẻ (subagent + LLM, không cần API ngoài). Chạy được nhiều vòng.
- Bước gap-scan: đắt (OpenAlex/arXiv/ACL/DBLP nhiều vòng) → CHỈ chạy trên 2–3 hướng sống sót.
- Chống chỉ định: đừng phát tán khi người dùng đã chốt đề tài và chỉ cần thực thi — lúc đó vào thẳng
  Stage 2, vòng phân kỳ chỉ làm loãng tiến độ.

## Deliverable chuẩn của một vòng ideation

`Ideation Log` (file markdown trong repo bài):
- Danh sách ≥10 hướng thô, mỗi cái 1–2 câu + kỹ thuật sinh ra nó (A–E).
- Bảng lọc khả thi: hướng × (có simulator? có data? có venue? effort tuần?) → sống/chết + lý do.
- Gap-scan result cho các con sống sót: dense components, empty joins, closest prior art có DOI.
- Dòng cuối: khuyến nghị + câu hỏi mở cho người dùng quyết. KHÔNG tự chốt.
