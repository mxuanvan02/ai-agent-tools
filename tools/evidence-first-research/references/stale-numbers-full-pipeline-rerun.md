# Stale numbers & full-pipeline re-run to resync a manuscript

Trigger: người dùng chỉ vào MỘT con số "li ti" sai/không khớp (vd effective rank), nói
"vẫn còn nhiều sạn", "rà kỹ những chỗ nội dung cũ chưa đụng vào", hoặc thẳng thừng
"xoá hết kết quả rồi chạy lại một lượt toàn bộ rồi đưa vào cho đồng bộ". Đây là tín
hiệu rằng số trong manuscript có thể đã **trôi khỏi code** — không chỉ một số mà cả
bảng. EXECUTE: re-run pipeline, không chỉ sửa một ô.

## Vì sao xảy ra (root cause)

Repo code tiến hóa qua nhiều phiên, nhưng các bảng trong manuscript được dán số từ
những lần chạy KHÁC NHAU ở các thời điểm khác nhau. Hậu quả điển hình (phiên bài AoI-greenhouse):
- **SOTA table reproduce 100%** (chạy gần nhất, khớp code hiện tại).
- **Table I, Whittle table, ablation, robustness table** đều STALE — sinh từ code cũ
  hơn; chạy lại bằng code hiện tại cho số khác hẳn (vd CAW loss 0.0024→0.0028, MaxAoI
  0.0104→0.0140, VoU 0.0128→0.0230, Whittle-exact 0.064→0.096).

## Manh mối phát hiện (trước khi re-run)

Cross-table inconsistency cho CÙNG một method là dấu hiệu mạnh nhất:
- Table I ghi bài AoI-greenhouse = 0.0024 nhưng SOTA table ghi 0.0028 cho cùng method, cùng
  setup → hai bảng từ hai batch/phiên bản code khác nhau. Con số "fresh" là cái xuất
  hiện nhất quán ở NHIỀU script (SOTA + benchmark mới + Whittle mới đều 0.0028);
  cái lẻ loi (0.0024) là stale.
- Một derived stat không reproduce được (eff. rank) ⟹ nghi ngờ TẤT CẢ số cùng họ.

## Recipe (đã chạy thật)

1. **Liệt kê script sinh số.** Đọc README phần reproducibility + grep `to_csv|savefig`
   trong `scripts/*.py` để map script → CSV output. Ghi rõ script nào sinh bảng nào.
2. **Backup docs cũ:** `mkdir docs/_backup_<ts> && cp docs/*.csv docs/*.json docs/_backup_<ts>/`.
3. **Smoke test trước** (`verify/*.py --quick`) để chắc môi trường chạy được.
4. **Chạy lại lần lượt** các script production (benchmark chính, SOTA, Whittle,
   robustness, ablation). Dùng `PYTHONPATH=$PWD/src:$PWD` nếu repo yêu cầu (lệnh sẽ
   bị security-gate hỏi duyệt — bình thường). Script nặng (robustness 8 policy × 2
   dataset × 30 windows) chạy background + `process wait`, có thể >6 phút.
5. **So old-vs-new bằng script** (đọc cả `docs/_backup_*/X.csv` và `docs/X.csv`,
   in delta, flag `<-- CHANGED`). Đừng so bằng mắt.
6. **Trích MỌI số manuscript từ CSV mới bằng MỘT script tổng** (`_extract_all.py`):
   mean ± 1.96·sd/√n cho từng bảng, kèm claim phái sinh (vd 78%→80%, 96%→95% reduction).
   Một nguồn duy nhất, tránh retype tay từng ô.
7. **Thay đồng bộ vào .tex** theo thứ tự: Table I → Whittle → SOTA (chỉ cột runtime
   nếu body đã khớp) → ablation → abstract claims → số lý thuyết (σ, s, z, ε) →
   robustness → conclusion. grep số cũ (`0\.0024|0\.0642|78\\%|96\\%|0\.080|0\.57`)
   để không sót chỗ nội dung cũ.
8. Build full chain + grep undef=0 + `pdftotext` xác nhận số mới render.

## Pitfalls riêng

- **Runtime phụ thuộc máy.** loss/RMSE/miss tái hiện được (độc lập máy); runtime thì
  KHÔNG (máy này 22.8/206/0.5ms vs bản gốc 97/434/1.3ms). Phải HỎI người dùng: giữ
  runtime gốc (máy nhóm) hay thay bằng số máy này (đồng bộ từ một lần chạy). Phiên
  này người dùng chọn thay hết bằng số máy hiện tại + caption ghi "wall-clock on the
  evaluation machine".
- **Narrative có thể ĐẢO khi số đổi.** Whittle-exact cũ loss 0.064 < heuristic 0.093
  ("exact mua được loss gain") → mới 0.096 ≈ heuristic 0.096 (exact KHÔNG còn rẻ hơn
  về loss, chỉ cải thiện RMSE). Phải viết LẠI đoạn diễn giải + p-value, không chỉ
  thay số trong bảng. Tương tự ablation "5×"→"8×" khi gap nới rộng.
- **CI có thể lệch chữ số cuối** giữa cách tính (ddof, multiplier) dù mean khớp —
  không phải số bịa; thống nhất một công thức CI (1.96·sd/√n) cho mọi bảng.
- **Bảng dùng CSV riêng.** DT+AoI rows lấy từ `dt_aoi_comparison_30windows.csv`
  (không phải SOTA csv); debt ablation "no-debt vs debt" lấy từ `intel_benchmark`
  (VoU vs bài AoI-greenhouse + fairness/age), KHÔNG phải `debt_mode_ablation` (cái đó so
  accumulating-vs-bounded, khác mục đích). Map đúng CSV→bảng trước khi trích.
- **p-value robustness phải tính lại** từ per-window paired delta (Wilcoxon) trên CSV
  mới — ordering/parity có thể đổi (vd Beijing MaxWeight-VoU từ parity p=0.82 → p=0.084),
  kéo theo câu "comparable to MaxWeight-VoU and VoI ($p\ge0.81$)" phải sửa.
- **Verify số neo cùng họ:** T (số dòng panel `.npy` thật qua `np.load(...).shape`,
  không retype), α̂, σ, kurtosis — tính trực tiếp từ data, đừng tin số trong text.
  Phiên này: α=0.9997 ✓, kurtosis 4161≈4200 ✓, 62.3×≈62× ✓, nhưng σ=0.076 (0.54%)
  vs text 0.080 (0.57%) lệch ~5% → sửa cho khớp số verify.

## Dọn dẹp

Xoá script tạm (`_cmp.py`, `_cmp2.py`, `_extract_all.py`) sau khi xong, hoặc giữ
trong repo nếu muốn reproducible — nhưng đừng để lẫn ở root manuscript. Backup CSV
cũ ở `docs/_backup_<ts>/` cho an toàn.
