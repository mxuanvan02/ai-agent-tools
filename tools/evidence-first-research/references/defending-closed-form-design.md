# Defending a closed-form / point-in-time design with math + measured data

## Khi nào dùng

Người dùng hỏi (đã xảy ra, verbatim-ish):
- "Vì sao hiện tại classic làm được những điều như thế — là do dữ liệu hả?"
- "Tại sao việc dự đoán trước tương lai lại không tốt hơn được?"
- "Chứng minh đầy đủ, minh chứng, dẫn chứng, từ ngữ đơn giản, có toán học vào."

Tức: cần GIẢI THÍCH (không phải sửa code) vì sao một dạng đơn giản (point-in-time
`P_vio`, TrackGap closed-form) lại tối ưu, và vì sao biến thể "sang hơn"
(predictive first-passage, error-covariance reduction, expected-shortfall) KHÔNG
thắng. Yêu cầu lõi: **toán + số đo thật từ data, từ ngữ đơn giản, không nói chay.**

## Nguyên tắc trả lời

Trả lời thẳng câu hỏi trong 1-3 câu ("Đúng, do bản chất dữ liệu: trường biến đổi
cực chậm + nhảy nhỏ mỗi bước, nên giá-trị-hiện-tại gần như là toàn bộ thông tin"),
RỒI mới chứng minh. Chia làm hai trục: (A) vì sao classic tối ưu, (B) vì sao dự
đoán tương lai không giúp. Mỗi claim phải có một CON SỐ ĐO ĐƯỢC chống lưng.

## A. Vì sao classic tối ưu — ε-expansion + suppression lemma

Lấy danger "đúng" theo Bayes = kỳ vọng chi phí vận hành dưới belief Gaussian
`X ~ N(x̂_i, σ_i²)`, với cost `c(x) = 1[x>u] + κ(x-u)_+/RANGE`:

    Danger_i = E[c(X)] = Φ̄(z_i)            (classic P_vio, số hạng bậc 0)
                       + (κ/RANGE)·ES_i      (severity, dạng đóng)
    ES_i = σ_i(φ(z_i) - z_i·Φ̄(z_i)),   z_i = (u - x̂_i)/σ_i

Khai triển theo tỉ lệ nhỏ ε = σ_i/(u - x̂_i) (nhiễu / khoảng-cách-tới-ngưỡng):

    Danger_i = Φ̄(z_i)·(1 + (κ/RANGE)·σ_i·ε + O(ε²))

**Suppression lemma** (verify số bằng `scripts/verify_vou_lemma.py`):

    ES_i / Φ̄(z_i)  →  σ_i·ε   khi ε → 0

→ Hai kết luận citable:
- **P2 — classic KHÔNG ad-hoc:** `Φ̄(z_i)` chính là số hạng zeroth-order `d_0` của
  danger Bayes-tối-ưu. Mọi cải tiến chỉ thêm ở bậc O(ε). λ chính là d_0 với
  severity tắt (κ=0). Đây là câu trả lời toán cho reviewer "sao dùng dạng đóng
  đơn giản / sao bình phương / sao cộng tuyến tính λ".
- **Điều kiện regime:** correction chỉ đáng kể khi ε LỚN (field volatile σ lớn,
  hoặc sensor sát ngưỡng u-μ nhỏ). Đây là giới hạn áp dụng trung thực + future work.

## B. Vì sao dự đoán tương lai không giúp — hai tầng

### B1. Mô hình không biết gì hơn "giá trị hiện tại" (đo forecast skill)
So dự báo AR(1) với baseline ngây thơ "ngày mai = hôm nay":

    RMSE(AR1 1-step) / RMSE(naive persistence) ≈ 1.00  ⟹ không có trend để khai thác

Vì α̂≈1 nên E[X(t+h)] = α^h·X(t) ≈ X(t). Dự đoán xa chỉ THÊM bất định (4-step RMSE
phình so với 1-step), không thêm tín hiệu.

### B2. First-passage làm HỎNG xếp hạng (range compression)
First-passage anytime: `P_fp(z) = 1 - ∏_{k=1}^h (1 - Φ̄(z_k))`. Khi α≈1, hàm này
BÃO HÒA về {0,1}: mọi sensor an toàn → ~0, mọi sensor nguy → ~1, ép dải giữa dồn
lại → MẤT discrimination. Mà scheduler chọn top-B chỉ cần THỨ TỰ đúng, không cần
xác suất tuyệt đối đúng. Classic `Φ̄(z_i)` là hàm đơn điệu mượt của khoảng-cách →
bảo toàn ranking → chọn đúng top-B → loss thấp.

→ Nghịch lý mà toán giải sạch: **predictor chính xác hơn (Brier thấp hơn) nhưng
loss scheduler tệ hơn**, vì top-B cần spread/order chứ không cần calibration.

## Số đo data-property để chống lưng (recipe — xem scripts/measure_regime_properties.py)

Năm đại lượng, mỗi cái một câu giải thích đơn giản:
1. **Persistence:** α̂ (mean/min/max) + half-life `t½ = ln0.5/ln(α̂)`. α̂≈0.9998 →
   t½≈4271 bước → "một lệch tồn tại >4000 bước, hiện tại≈tương lai".
2. **Innovation size:** σ_ω và σ_ω/RANGE (vd 0.031 = 0.22% RANGE). Nhìn h bước:
   σ√h. Sensor cách ngưỡng d sd: z = d/(σ√h) (vd 8 sd ⟹ "xa khủng khiếp").
3. **Approach frequency:** % readings trong 1 đơn vị của ngưỡng, % thực sự vượt band.
4. **Forecast skill ratio** (B1): RMSE(AR1)/RMSE(naive) ≈ 1 ⟹ no exploitable trend.
5. **Range compression** (B2): minh họa P_fp bão hòa.

## ev_cost spike — số thật (exemplar, đừng giả định)
8-window Intel per-arm, `vou_mode="ev_cost"` (error-covariance reduction +
expected-shortfall, ρ vô thứ nguyên, bỏ λ):

| mode | loss | ×classic |
|---|---|---|
| classic | 0.00506 | 1.00 |
| ev_cost ρ=6 | 0.00995 | ×1.96 |
| ev_cost ρ=1 | 0.01559 | ×3.08 |
| severity ρ=6 | 0.00496 | ~×0.98 (hòa) |

→ ev_cost THUA 2-3× (σ_i² gần đồng đều trên field near-unit-root → track-reduction
nén dải, mất discrimination — cùng cơ chế B2). severity HÒA (ES bị suppress, P1).
Bật biến thể mới phải SPIKE đo trước, không claim "đẹp lý thuyết ⟹ tốt hơn".

## Đóng gói cho manuscript (Q1 Discussion)
Một mục §Discussion "When does point-in-time VoU suffice?" gồm: (1) ba+ số đo data
(α̂, t½, σ/RANGE, forecast-skill ratio); (2) khai triển ε + suppression lemma (P2);
(3) bảng ablation 3-mode (classic/ev_cost/severity) với số thật; (4) điều kiện đảo
ngược ε lớn. Biến chuỗi negative result thành đòn bẩy: không chỉ "classic đủ tốt"
mà CHỨNG MINH nó tối ưu trong regime ĐO ĐƯỢC + nêu rõ regime nào thì khác.
