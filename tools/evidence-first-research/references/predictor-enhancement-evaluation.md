# Predictor / value-function enhancement evaluation (decoupled, Bayes-optimal ceiling)

Khi người dùng yêu cầu "nâng hàm lượng toán" cho phần *dự đoán / value function* của một
scheduler/estimator (vd: đổi VoU từ "confirm" sang "predict", thử ML/DL, thử
first-passage, thử trend model), KHÔNG nhảy thẳng vào wiring + full re-run. Theo
quy trình kiểm chứng tách lớp dưới đây. Mục tiêu: trả lời "predictor nào đúng về
mặt toán" bằng SỐ LIỆU, không bằng phỏng đoán (người dùng nói thẳng: "đừng đoán").

## Nguyên tắc cốt lõi

1. **Đo chất lượng dự đoán TÁCH KHỎI hệ thống trước.** Trước khi cắm predictor vào
   scheduler (đắt, nhiều biến nhiễu), build một harness đo *chất lượng dự đoán thuần*
   trên held-out data: trích (feature, label) nhân-quả, label = biến cố tương lai cần
   dự đoán (vd "tín hiệu rời band trong [t, t+H]"), rồi chấm bằng **AUC + AP +
   Brier**. AUC/AP = discrimination (xếp hạng), Brier = calibration. Đây là tầng rẻ
   nhất để loại các hướng vô vọng.
2. **Chẩn đoán model-mismatch từ THAM SỐ ĐÃ FIT, đừng giả định.** Khi một predictor
   analytic thất bại, đọc tham số đã fit để tìm nguyên nhân thật. Ví dụ thực tế:
   first-passage Brownian "over-trigger" — giả thuyết ban đầu là "AR(1) mean-reverting
   nên Brownian sai". Nhưng `α̂ ≈ 0.9998` ⟹ near-unit-root ⟹ tín hiệu LÀ near-random-walk
   ⟹ Brownian KHÔNG sai. Tham số fit sửa lại chẩn đoán. Luôn in tham số (α, σ, drift)
   và kiểm `|α|<1` trước khi quy kết.
3. **Tính Bayes-optimal predictor làm TRẦN LÝ THUYẾT.** Predictor tối ưu dưới đúng mô
   hình sinh dữ liệu (vd AR(1) + empirical-residual first-passage qua Monte-Carlo
   rollout) là trần không thể vượt dưới mô hình đó. Nếu **ngay cả nó** cũng không cải
   thiện metric đích, đó là bằng chứng MẠNH NHẤT rằng không predictor nào (analytic hay
   học máy) làm được — vấn đề nằm ở bản chất ngẫu nhiên của tín hiệu, không ở độ tinh
   vi của predictor. Kết quả này mạnh hơn nhiều so với chỉ "ML thua".
4. **Calibration ≠ ranking (scale vs discrimination).** Predictor có Brier tốt nhất có
   thể làm LOSS scheduler TỆ HƠN. Lý do: scheduler là hệ XẾP HẠNG (top-B index), cần
   *độ phân tán* (discrimination) của tín hiệu urgency, không cần xác suất tuyệt đối
   đúng. First-passage "anytime" (P vượt band ở bất kỳ τ∈[1,H]) với α≈1 luôn cao hệ
   thống ⟹ **nén dải urgency** (ai cũng "sắp nguy hiểm") ⟹ ranking xấu ⟹ loss tăng dù
   calibration tốt. Đây là lý do cấu trúc, citable. ⟹ Point-in-time confirm thường
   ĐÚNG cho ranking vì bảo toàn spread.
5. **Vẫn phải verify ở tầng scheduler (full N + Wilcoxon).** Prediction-quality tốt là
   ĐIỀU KIỆN CẦN, không đủ. Cắm vào scheduler, chạy đủ N window + paired Wilcoxon. 3-win
   smoke đầy nhiễu và HAY ĐẢO CHIỀU (vd mc-fp: 3-win cho 13× rồi 0.49×; 30-win cho 2.4×
   ổn định). Đừng kết luận từ smoke.

## Thứ tự thực thi (cheap → expensive)

1. Held-out prediction-quality harness (AUC/AP/Brier): analytic baseline hiện tại vs
   các ứng viên (logistic/GBM calibrated; analytic biến thể; Bayes-optimal MC).
2. Đọc tham số fit để chẩn đoán mismatch nếu một ứng viên thua bất ngờ.
3. Nếu một ứng viên thắng prediction-quality → mới wire vào scheduler sau một flag
   opt-in (vd `use_first_passage`, `fp_mode`), giữ default = deployed path.
4. Scheduler spike: 3-win smoke (bắt bug) → full N + Wilcoxon (kết luận).
5. Nếu không ứng viên nào cải thiện metric đích → ĐÓNG hướng, gói thành Proposition.

## Negative results = đòn bẩy viết bài (turn weakness into strength)

Một chuỗi negative result nhất quán (vd: corr-submodular ✗, trend+first-passage ✗,
ML predictor ✗, Bayes-optimal MC ✗) KHÔNG phải thất bại — là một **phát hiện khoa
học** và là lập luận Q1 mạnh: "chúng tôi đã thử cái phức tạp hơn (learned classifiers,
trend-aware first-passage, Bayes-optimal hitting probability) và chứng minh closed-form
là near-sufficient vì bài toán near-Markov-Gaussian; do đó độ phức tạp toán nằm ở
SCHEDULING (per-arm channel + asymptotic-optimality), không ở predictor — lựa chọn có
cơ sở, không phải đơn giản hóa." Reviewer Q1 thích loại lập luận này. Ghi negative
results vào `docs/negative_result_*.md` với bảng số + diễn giải cấu trúc + một câu
"manuscript framing". Nêu rõ ĐIỀU KIỆN mà predictor học máy SẼ thắng (tín hiệu
fast/bursty/nonlinear) — đó là scope condition, không phải gap.

## Mệnh đề mẫu (predictor optimality)

> Trên các trường near-unit-root (α̂≈0.9998), VoU point-in-time bảo toàn discrimination
> của tín hiệu urgency; first-passage Bayes-optimal tuy calibration tốt hơn (Brier
> 0.00137 vs 0.00144) lại nén dải urgency và làm loss scheduler tệ 2.4×. Vì (giá trị,
> khoảng-cách-ngưỡng, σ) là near-sufficient statistic, không predictor nào — analytic
> hay học máy — vượt đáng kể closed-form. Độ phức tạp toán nằm ở scheduling.

## Pitfalls

- Đừng cài lib nặng (torch) khi "học máy đơn giản" đủ — sklearn (logistic +
  HistGradientBoosting + isotonic calibration + class_weight balanced) là đủ cho
  rare-event tabular. Chỉ cài cái cần.
- Rare-event (pos-rate <1%): luôn dùng AP (average precision) + Brier bên cạnh AUC;
  AUC một mình lạc quan trên imbalanced. Dùng balanced class weights + Platt/isotonic.
- Background subagent dispatch có thể lỗi im lặng (chạy vài giây, 1 API call, không
  search). Nếu brief literature là writing-support (không chặn quyết định kỹ thuật),
  đừng re-dispatch vô hạn — tự search inline khi cần citation, KHÔNG bịa.
- Giữ mọi biến thể predictor sau flag, default = deployed path; verify code path sống
  vẫn dùng đúng biến thể (in `use_first_passage`/`fp_mode` trong smoke) trước re-run.
- LSP "import numpy/sklearn could not be resolved" trong script venv là interpreter sai
  của linter, không phải lỗi thật — chạy bằng `.venv/bin/python` rồi tin runtime.

## Khi người dùng nói value-term "chưa đủ chuyên nghiệp / thiếu hàm lượng khoa học"

Tín hiệu: người dùng chỉ vào một số hạng trong value/objective (vd `TrackGap =
(mu - xh)²/RANGE²`, hay `VoU = TrackGap + λ·P_vio` với λ chọn tay) và nói nó quá
thô. Đây KHÔNG phải lời khen — reviewer Q1 sẽ hỏi "tại sao bình phương, tại sao
cộng tuyến tính, λ ở đâu ra". Đọc định nghĩa thật trong code trước (grep
`track_gap`, `vou`, `lambda`), rồi đề xuất một LADDER reformulation theory-grounded,
từ nhẹ → nặng, kèm rủi ro:

1. **Estimation-theoretic (khuyến nghị, nền vững nhất):** đổi heuristic squared-
   error thành **expected error-covariance reduction** dưới Kalman:
   E[‖x-x̂‖²|not served] − E[‖x-x̂‖²|served] = trace giảm được của ma trận hiệp
   phương sai sai số. Đây chính là *value of information* Bayesian (Howard 1966),
   khớp Gauss-Markov remote-estimation literature. Biến "bình phương lệch" thành
   "độ giảm uncertainty kỳ vọng" — citable, đúng chuẩn.
2. **Hợp nhất qua một expected-cost duy nhất (bỏ được λ tùy ý — điểm reviewer hay
   bắt):** thay `track + λ·P_vio` (hai số hạng rời, λ tay) bằng một E[c(x)] với
   c(x) = hàm phạt tăng theo khoảng cách vượt ngưỡng (quadratic-in-band + barrier
   gần biên). VoU = độ giảm kỳ vọng của cost này nếu cập nhật. λ được *suy ra* từ
   hình dạng cost, không còn tùy ý. Đây là **risk-sensitive / CVaR** framing.
3. **Information-theoretic (nặng nhất, rủi ro cao):** VoU = mutual information
   giữa quan sát và biến cố vượt ngưỡng, hoặc KL giữa belief trước/sau. Sang về
   toán nhưng trên field near-stationary thường KHÔNG cải thiện (xem negative
   results ở trên) — chỉ làm nếu đổi regime.

Khuyến nghị mặc định: kết hợp 1+2 (TrackGap → trace error-covariance reduction;
safety → expected threshold-crossing cost reduction; gộp thành một VoU = tổng kỳ
vọng cost giảm được). Vừa có nền estimation-theory + risk-aware, vừa bỏ λ tùy ý,
vừa không phụ thuộc predictor phức tạp đã thất bại. CẢNH BÁO: đây là thay đổi
*định nghĩa method cốt lõi* ⟹ phải SPIKE đo trên dữ liệu thật + re-run toàn bộ +
có thể đổi số. Báo người dùng trade-off + chi phí re-run TRƯỚC khi sửa manuscript,
đừng tự đổi.

### BẪY ĐÃ ĐO THẬT: "reduction" tự triệt tiêu trên field near-stationary

Đã implement đúng cách 1+2 (reduction-based ev_cost) và nó THẤT BẠI — ghi lại để
lần sau không lặp. Trên field near-unit-root (α̂≈1), ở age thấp predictive
variance `v ≈ σ²`, nên CẢ HAI số hạng reduction triệt tiêu:
- `track_reduction = (est_now − σ²)₊ ≈ 0` (est_now = bias²+v, mà bias≈0, v≈σ²),
- `safety_reduction = (risk_now − risk_after)₊ ≈ 0` (vì v≈σ² nên serving không
  giảm risk đáng kể).
⟹ VoU ≈ 0 ở MỌI state, kể cả sensor sát ngưỡng. Sanity-check bắt được ngay
(near-threshold VoU=0.00000, "near-threshold is max: False"). Đo full: ev_cost
TỆ HƠN classic 2.09× trên safety-loss (nhưng TỐT HƠN RMSE 0.1176 vs 0.1334 —
đúng vì nó tối ưu estimation, buông safety). Bài học: "reduction" đo *uncertainty
đã tích lũy*, KHÔNG đo *nguy hiểm vị trí* — sai thứ cần đo cho safety scheduling.

**FIX có nền lý thuyết (dùng cái này, không dùng reduction cho safety term):** giữ
cấu trúc `track + ρ·safety` (nó hoạt động), nhưng safety = **expected boundary
exceedance tại VỊ TRÍ HIỆN TẠI** (không phải reduction), dạng đóng cho Gaussian
belief N(μ,v): `E[(x−Smax)₊] + E[(Smin−x)₊]` với
`E[(X−u)₊] = σ·φ(z) + (μ−u)·Φ(z)`, `z=(μ−u)/σ`. Đây là **expected shortfall /
partial moment**, risk measure citable, và nó KHÁC 0 ĐÚNG CHỖ (sensor gần ngưỡng).
Tracking term có thể vẫn dùng reduction (error-covariance) vì RMSE là metric phụ
hợp lý ở đó; nhưng safety term PHẢI là position-based exceedance, không reduction.

### CẬP NHẬT ĐÃ ĐO: position-based exceedance (severity-VoU) cũng CHỈ HÒA classic trên field near-stationary

Đã implement đúng FIX trên (severity-VoU: `Danger = P_vio + (κ/RANGE)·ES`, ES dùng
LEVEL không reduction) và sanity-check PASS (near-threshold = max, fix đúng bug
reduction). NHƯNG đo full 8-window: severity-VoU **HÒA classic** trên mọi metric —
mean loss gần trùng (cải thiện ~2% ở κ cao), và **tail P90/P99/max TRÙNG KHÍT từng
chữ số**. Hai lý do, cả hai derive được TRƯỚC khi chạy (xem mục math-first dưới):
1. **Suppression lemma**: ES/P_vio → v/(u−μ) = s·ε, ε=s/(u−μ). Trên Intel σ̂≈0.031,
   predictive sd 4-bước ≈0.062, sensor cách ngưỡng 0.5°C ⟹ z≈8 sd ⟹ ES bị nén
   ~1800× dưới P_vio. Severity term là O(ε) ⟹ severity-VoU → classic, KHÔNG THỂ tệ
   hơn nhưng cũng không hơn đáng kể trên mean.
2. **Tail near-zero vì classic đã bắt gần hết vi phạm** (KHÔNG phải do channel —
   xem cảnh báo metric-bug dưới): sau khi sửa metric đúng, undetected-overshoot
   P90/P99 = 0 cho MỌI policy kể cả classic (missed-rate ~0.08%). Tail vi-phạm-bị-
   bỏ-sót gần như rỗng ⟹ không có gì cho severity reweight cải thiện. ⟹ Tail KHÔNG
   cải thiện được vì classic đã near-perfect ở detection, không vì \"channel chi phối\".

Bài học cập nhật: position-based exceedance là FIX ĐÚNG cho cái bug reduction (nó
khác 0 đúng chỗ), nhưng trên field near-stationary nó vẫn chỉ HÒA classic, không
thắng. Đừng kỳ vọng nó cải thiện số; giá trị của nó là LÝ THUYẾT (đặt classic vào
khung Bayes — xem dưới), không phải empirical lift.

## MATH-FIRST: derive-then-verify (người dùng yêu cầu rõ, lặp 2 lần)

Người dùng nói thẳng: **"Có chứng minh toán học trước khi chạy thì có vẻ hay hơn"** và
**"Dựa vào những điểm yếu trong toán học đó để tìm ra giải pháp mạnh hơn đúng đắn và
triển khai"**. Đây là PREFERENCE WORKFLOW, không phải gợi ý: với mọi value/predictor
redesign, DERIVE TRƯỚC, CHẠY SAU. Quy trình:

1. **Tìm điểm yếu toán THẬT** (không phải predictor tinh vi hơn). Ví dụ đã tìm đúng:
   classic `P_vio` là xác suất 0/1 ⟹ Bayes-optimal cho *kỳ vọng SỐ LẦN* vi phạm
   nhưng MÙ severity (vượt 0.1°C vs 5°C xếp ngang). Điểm yếu này độc lập với σ/trend
   và tấn công đúng tail metric P99 — đúng loại điểm yếu đáng theo.
2. **Derive giải pháp dạng đóng + chứng minh TÍNH CHẤT trước khi chạy.** Viết
   derivation vào `docs/<name>_derivation.md`: định nghĩa cost c(x), tính Bayes danger
   = E[c(X)] dạng đóng, rồi chứng minh các tính chất (reduces-to-classic, classic =
   leading-order truncation, dominates-on-tail...). Mỗi tính chất là một dự đoán CÓ
   HƯỚNG để verify, không phải hy vọng.
3. **Verify bằng TOÁN THUẦN trước (không sim).** Viết `scripts/verify_*_lemma.py` so
   closed-form với numerical integration (scipy.integrate.quad) + đo hệ số trên DATA
   THẬT (vd σ̂ từ innovations). Đây rẻ hơn sim và bắt được kết quả TRƯỚC khi chạy nặng.
4. **Chỉ chạy scheduler spike SAU khi toán đứng** — và lúc đó đã biết trước số sẽ ra
   sao, lần chạy chỉ để xác nhận + lấy số chính xác cho bảng.

### Suppression lemma (mẫu vũ khí: một bất đẳng thức giải thích CẢ CỤM negative result)

Khi nhiều enhancement (corr, first-passage, ML, expected-shortfall) đều thua/hòa trên
field near-stationary, tìm MỘT lý do cấu trúc chung thay vì giải thích rời rạc. Mẫu đã
chứng minh + verify số (rel.err 1e-14 so với tích phân):

> Với belief Gaussian X~N(μ,v), s=√v, ngưỡng u, z=(u−μ)/s>0:
> P_exit = Φ̄(z),  ES = E[(X−u)₊] = s(φ(z) − z·Φ̄(z))
> ⟹ **ES/P_exit = s(φ(z)/Φ̄(z) − z) → s/z = v/(u−μ) khi z lớn.**

Diễn giải: mọi safety term dạng moment bậc cao (expected shortfall, covariance-
reduction, first-passage) bằng safety term dạng xác suất (classic) nhân hệ số
v/(u−μ) = s·ε → 0 khi field càng tĩnh. ⟹ trên field σ nhỏ, KHÔNG enhancement nào
thắng classic về safety — đây là TRẦN cấu trúc, không phải "thử chưa đủ". Verify số:
in bảng ES/P (exact) cạnh v/(u−μ) (asymptotic) qua grid s∈[0.1,2], xác nhận hội tụ;
caveat trung thực: ô s nhỏ + dist lớn báo rel.err lớn là UNDERFLOW (cả hai ~1e-23),
không phải lỗi công thức — nói rõ.

### Đòn bẩy Q1: đặt rule đang chạy vào khung Bayes (classic = leading-order truncation)

Severity-VoU không cải thiện số NHƯNG cho bài 3 thứ có hàm lượng toán thật:
1. **Suppression lemma** giải thích MỌI negative result bằng một hệ số ε.
2. **Classic = ε⁰ truncation của Bayes-optimal expected-cost VoU** ⟹ "đơn giản vì
   TỐI ƯU CÓ CHỨNG MINH cho regime này", không phải "đơn giản vì sơ sài". Đây là câu
   trả lời mạnh nhất cho "thuật toán quá đơn giản, đủ Q1 không".
3. **Phát hiện tail-do-channel** (overshoot không đổi across reweight) ⟹ motivate đúng
   trụ novelty còn lại: per-arm channel + theorem asymptotic-optimality.
⟹ Khi mọi empirical lever đã đóng, GIÁ TRỊ nằm ở proof-layer + regime characterization,
KHÔNG ở việc cố ép một cải thiện số. Nói thẳng điều này với người dùng, đừng vẽ ra lợi ích
không có.

### CẢNH BÁO METRIC-BUG: tail metric so sánh policy PHẢI policy-dependent

Đã mắc lỗi này và suýt rút sai kết luận. Khi thêm tail metric (P90/P99 overshoot)
để so sánh các policy, ĐỪNG đo `overshoot = max(x_true − Smax, 0)` — `x_true` là
tín hiệu THẬT, KHÔNG phụ thuộc policy (cùng data + seed) ⟹ mọi policy cho số GIỐNG
HỆT, Wilcoxon p=nan, tie 100%. Nhìn thấy all-ties/p=nan ⟹ nghi ngay đo nhầm đại
lượng policy-independent. Lần này nó còn dẫn tới chẩn đoán SAI \"tail do channel\".
FIX: tail metric đúng cho safety monitor = **severity của vi phạm BỊ BỎ SÓT** —
overshoot của `x_true` CHỈ tại các sensor mà held-estimate `xh` vẫn báo an toàn
(`x_true` ngoài band AND `xh` trong band). Cái này policy-dependent (scheduler tốt
phát hiện kịp ⟹ giảm undetected overshoot). Quy tắc chung: bất kỳ metric so sánh
policy nào cũng phải là hàm của BIẾN DO POLICY ĐIỀU KHIỂN (ở đây là `xh`/quyết
định phục vụ), không chỉ của ground-truth.

### Quy tắc bắt buộc: SANITY-CHECK value function trên hand-crafted states TRƯỚC khi đo scheduler

Trước khi cắm value function mới vào scheduler, viết một unit-check trên vài state
tự tạo: (a) sensor centered+fresh → VoU thấp; (b) sensor sát ngưỡng → VoU CAO NHẤT;
(c) sensor stale/uncertain → VoU trung bình. Assert `all >= 0` và
`near_threshold == max`. Nếu fail (như ev_cost ở trên), DỪNG — công thức đo sai
thứ, đừng chạy 30-window phí thời gian. Đây là tầng kiểm rẻ nhất, đặt TRƯỚC cả
prediction-quality harness cho value-function redesign.
