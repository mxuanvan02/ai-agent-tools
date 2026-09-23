# Scaling a simulation to larger N: regime flip, honest materialization, cost mis-scaling

Trigger: người dùng phát hiện manuscript ghi một quy mô (vd "N=30 sensors") nhưng code
thật chạy quy mô khác (vd `range(3)` = 3 sensors), và chọn **mở rộng code lên đúng
quy mô bài** (hướng B: "nâng code lên N=30 thật") thay vì hạ manuscript về quy mô
nhỏ (hướng A). Đây là EXECUTE re-run nặng — nhưng GATE kỹ trước khi chạy full.

## Bài học cốt lõi (xếp theo mức độ quan trọng)

### 1. Scale-up có thể ĐẢO CHIỀU regime và VỠ luận điểm — phải cảnh báo TRƯỚC và smoke-test
Khi `B/N` đổi bậc, bản chất bài toán đổi:
- Ở **N nhỏ, budget gần N** (vd N=3, B∈{1,2,3} ⟹ B/N tới 1.0): field gần như quan
  sát đầy đủ → khác biệt nằm ở *timing rủi ro* → risk-aware policy (bài bandwidth-scheduling-PD) thắng
  age-based.
- Ở **N lớn, budget ≪ N** (vd N=30, B∈{2,4,6,8} ⟹ B/N≈0.13–0.27): field bị quan
  sát thiếu nặng → **tracking-error/staleness thành chi phí trội** → policy tối ưu
  tuổi (Max-AoI) bỗng vượt trội; và nếu tín hiệu rủi ro `p` gần bão hòa (vd mean≈0.60,
  đa số > ngưỡng 0.55) thì nó **mất khả năng phân biệt** sensor nào nguy hơn → lợi
  thế "risk-aware" của method đề xuất **biến mất**. bài bandwidth-scheduling-PD smoke N=30 thua cả
  Max-AoI lẫn Fixed-B3, chỉ nhỉnh hơn Oracle.
- ⟹ Luận điểm "risk-aware + dynamic budget thắng age-based" KHÔNG còn đúng ở N lớn.
- **Quy trình bắt buộc:** (a) khi người dùng chọn scale-up, nói thẳng RỦI RO regime-flip
  ngay lúc chốt thiết kế; (b) chạy SMOKE (vài seed × vài window) TRƯỚC full run; (c)
  đọc số smoke bằng mắt khoa học — Oracle (lower bound) phải tốt nhất, method phải
  competitive; nếu vô lý thì hoặc bug hoặc regime-flip, CHẨN ĐOÁN trước khi full.

### 2. KHÔNG được tinh chỉnh hằng số phạt để ép kết quả đẹp = bịa số
Khi smoke cho thấy method thua, cám dỗ là chỉnh hệ số penalty cho method thắng lại.
Đó là fudge/bịa. Thay vào đó: DỪNG, báo người dùng số thật, trình A/B/C trung thực
(A: quay về N nhỏ giữ kết quả đã verify; B: đổi regime có nguyên tắc để risk-aware
có ý nghĩa — band chặt hơn cho `p` phân tán, hoặc budget khác; C: pivot luận điểm
theo đúng cái dữ liệu nói). Khuyến nghị thường là A (bảo toàn kết quả đã verify +
liêm chính), nhưng để người dùng quyết. Phân biệt rạch ròi: *rescale có nguyên tắc để
giữ calibration bất biến theo N* (được phép, xem #4) vs *fudge hằng số để ép thắng*
(cấm).

### 3. Materialize sensor ảo từ ÍT trace thật phải TRUNG THỰC, khai báo rõ
Dataset chỉ có K trace đo thật (vd 3 microclimate loops). Không có "N=30 sensor độc
lập thật". Mọi N>K đều bán tổng hợp → nếu im lặng bootstrap rồi gọi "30 real sensors"
là overclaim. Thiết kế trung thực đã dùng:
- N sensor ảo chia K nhóm (N/K mỗi nhóm), mỗi nhóm dẫn động bởi 1 trace đo thật.
- Mỗi sensor quan sát trace ẩn chung qua **time-offset ngẫu nhiên độc lập** (pha thời
  gian khác nhau) + (tuỳ chọn) nhiễu đo, và chịu **một realization kênh G-E riêng
  (per-arm channel state `bad[i]`)**.
- GIỮ NGUYÊN các giá trị đo thật `(x, mu, p, v)` của trace — KHÔNG tái sinh `p` bằng
  Φ tự bịa. (Phiên này có reverse-engineer Φ band [22,30], σ per-loop ~1.5–2.2 chỉ
  để HIỂU dữ liệu, không để thay thế giá trị thật.)
- Layout (group, offset) deterministic theo (seed, window) và GIỐNG NHAU across
  policies ⟹ so sánh vẫn paired (giữ Wilcoxon n=320 hợp lệ).
- Manuscript phải nói rõ "N virtual sensors derived from K measured traces via
  independent time phases + per-arm channels", tự định danh bán tổng hợp.

### 4. Mis-scaling hằng số theo N — chẩn đoán từ cấu trúc objective, đừng đoán
Objective dạng `mean_loss + c_bw·B + c_aoi·aoi`. `c_bw·B` là chi phí TUYỆT ĐỐI theo
B, nhưng mỗi sensor được phục vụ chỉ giảm loss ~`1/N`. Ở N nhỏ lợi ích/B lớn (1/K),
ở N lớn lợi ích/B nhỏ (1/N) trong khi `c_bw` giữ nguyên → Oracle "thấy" phục vụ
không đáng, chọn B thấp, thành tệ nhất (dấu hiệu chẩn đoán: lower-bound policy hóa
ra tệ nhất). Đây là MIS-SCALING hằng số, KHÔNG phải bug logic.
- **Fix N-invariant có nguyên tắc:** nhân MỌI hệ số phạt-theo-B với
  `BW_SCALE = K/N` (=1 khi N=K, giữ nguyên calibration gốc; =K/N khi mở rộng). Áp
  vào: từng nhánh rabs_l/rabs_pd, oracle, objective cuối — grep mọi `*B` có hệ số.
- Tương tự AoI: chuẩn hóa `AOI_NORM = (B_target/N)/(B_target_old/K)` để cân bằng số
  hạng aoi khớp calibration cũ.
- Sau khi rescale: smoke lại, regime phải hợp lý (Oracle tốt nhất). Nếu regime VẪN
  flip thì đó là #1 (bản chất bài toán), không phải scaling.

### 5. Budget set khi scale-up: giữ tỷ lệ
Chọn `B_max ≈ 0.27·N`, `B_target ≈ B_max/2`, budget set vài mức (vd {2,4,6,8} cho
N=30, target 4). Baseline 3-level (low/mid/high) map sang các mức tương ứng. Chốt
các con số này VỚI người dùng trước khi full run (re-run đắt, chỉ chạy 1 lần).

## Refactor checklist (generalize `range(K)` → `range(NSENS)`)
- Backup 4 script vào `code/_backups/<ts>/` trước.
- Tham số hóa: `NSENS, GROUPS, PER_GROUP, BUDGET_SET, BMIN, BMAX, BTARGET, BW_SCALE,
  AOI_NORM`. Thay MỌI `range(3)`, `/3`, `age=[0,0,0]`, `[1,2,3]` hardcode.
- `read_steps` đổi `if len==3` → `if len==GROUPS`.
- `random.Random(seed)` KHÔNG nhận tuple → dùng hash số (`1_000_003*seed_start+97`).
- Kênh: scalar `bad` → vector `bad=[False]*NSENS`, index `bad[i]` trong loop phục vụ.
- Script phụ (nonstationary, weight-sweep) import base qua `importlib`/`import base`
  → tự thừa hưởng NSENS; wilcoxon chỉ đọc CSV → không sửa. Vẫn phải re-run cả chuỗi.
- Smoke (Pyright báo lỗi import pandas/numpy vì python hệ thống — bỏ qua, chạy bằng
  venv repo).
