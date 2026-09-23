# Reviewer deep-read: theory ↔ deployed-code consistency

Khi người dùng nói "agent tự làm reviewer đọc sâu qua từng mục, đánh giá nghiêm khắc,
đồng thời có góc người đọc" và bảo "triển khai sửa liền". Đây là EXECUTE review
(không chỉ liệt kê comment): đọc kỹ TỪNG section, bắt lỗi, verify bằng CODE/SỐ
THẬT, sửa, build-gate, rồi báo verdict. Hai góc song song: reviewer khó tính (bắt
mâu thuẫn lý thuyết–code, overclaim) + người đọc (ký hiệu nhất quán, mạch dễ theo).

## Bug #1 hay gặp & nghiêm trọng nhất: theory giả định X, code chạy Y

Pattern thật (bài AoI-greenhouse): §5 chứng minh mọi thứ trên **Gaussian $\Phi$/$\bar\Phi(z)$**,
abstract gọi "deployed closed-form danger term", nhưng code dùng **empirical
residual bootstrap** (thậm chí có comment `v2 FIX: use empirical instead of
Gaussian erf`). Reviewer lý thuyết bắt ngay: "người dùng chứng minh trên Gaussian nhưng
chạy cái khác".

Cách xử lý — KHÔNG đoán, verify rồi reconcile:
1. **Đọc code thật** xác định deployed path: grep `pvio|empirical|norm.cdf|Phi`
   trong `src/`, đọc hàm tính danger. Tìm chỗ nạp dữ liệu thật
   (`set_empirical_residuals`) để biết nhánh nào CHẠY khi thí nghiệm, không phải
   nhánh fallback.
2. **Quantify data property để biết được phép claim gì.** Tính kurtosis/skew +
   tail-mass của residual đã chuẩn hoá từ `.venv` repo (có scipy). Ví dụ thật:
   excess kurtosis ≈ 4161, $P(|r|>4\sigma)$ gấp 62× Gaussian ⟹ bootstrap là BẮT
   BUỘC, Gaussian bỏ sót đuôi. Con số này vừa biện minh code, vừa thành bằng chứng
   trong bài.
3. **Reconcile bằng cách tách "chọn functional nào" khỏi "ước lượng thế nào".**
   Câu chữ an toàn: *Gaussian là mô hình giải tích để chứng minh exit-probability
   là leading-order Bayes danger (chọn functional); deployed ước lượng chính
   functional đó bằng empirical bootstrap vì đuôi nặng (ước lượng).* Lemma/Prop
   giữ nguyên, chỉ đổi diễn ngôn.
4. **Sửa ở MỌI nơi nhắc tới nó** — đây là điểm dễ sót. Lỗi sống ở **5 chỗ** (đừng
   dừng ở 4): abstract, **§1 intro contribution list** (câu "we show ... closed-form
   point-in-time danger term is the correct leading-order choice" — RẤT dễ quên vì
   nằm trong enumerate đóng góp), §methodology (câu "retain closed-form as deployed
   default"), §evaluation (bảng index rules ghi $\bar\Phi(z_i)$ + câu "only rule whose
   danger is exact $\bar\Phi$"), §theory intro. grep symbol/cụm từ ("closed-form",
   "$\bar\Phi$", "Gaussian") xuyên TOÀN bài kể cả abstract+intro, sửa hết, đổi ký
   hiệu bảng sang $\widehat P^{\mathrm{emp}}_{\mathrm{vio},i}$ cho khớp. Quy tắc:
   contribution list trong intro là nơi overclaim/diễn ngôn-cũ sống dai nhất vì nó
   được viết sớm và ít ai rà lại — luôn grep cụm từ vấn đề trong `01_introduction.tex`.

## Multi-perspective review qua subagent SONG SONG (khi người dùng nói "review nhiều lượt nhiều góc nhìn rồi sửa ready-submit")

Cách điều phối đã chạy tốt cho cả bài AoI-greenhouse và bài bandwidth-scheduling trong cùng phiên:
1. **Fan-out 3 subagent READ-ONLY song song**, mỗi cái MỘT lăng kính, qua
   `delegate_task` (toolsets `["terminal","file"]`): (a) **số liệu & nhất quán** —
   đối chiếu mọi số với CSV gốc bằng python; (b) **tham chiếu chéo & cấu trúc** —
   build + đọc log/.aux tìm undef ref/cite, label mồ côi, bib thừa/thiếu,
   overfull>60pt; (c) **notation + ngôn ngữ + overclaim** — ký hiệu kép/overload,
   acronym first-use, claim quá mạnh, grammar.
2. **Bắt buộc nói rõ "CHỈ ĐỌC, KHÔNG GHI/SỬA"** trong goal+context mỗi subagent, và
   yêu cầu trả về **bảng `file:dòng | số/vấn đề hiện tại | đúng (theo CSV) | đề xuất`**.
   Subagent ghi file dễ đè nhau (sibling lost-update) — tách đọc khỏi sửa.
3. **Parent tự sửa TUẦN TỰ**, không để subagent sửa. Trước mỗi patch: tự verify lại
   phát hiện của subagent với CSV/code thật (subagent self-report có thể sai — vd
   báo "2 CSV cho 2 số khác nhau" mà thực ra là 2 batch khác nhau hợp lệ).
4. Lưu ý JSON `delegate_task`: viết context bằng tiếng Việt KHÔNG dấu để tránh lỗi
   `Invalid \uXXXX escape` khi escape sai; hoặc cẩn thận escape Unicode.
5. Cảnh báo "modified by sibling subagent ... never read" thường là MARKER CŨ từ
   phiên trước (verify bằng `ps aux | grep` — không có process thật đang chạy thì
   bỏ qua); nhưng vẫn đọc lại vùng sửa trước patch cho chắc.

## Bug #2b: một HÀNG bảng lấy từ BIẾN THỂ ABLATION SAI (biến thể tinh vi của Bug #4)

Pattern thật (bài AoI-greenhouse phiên này): 3 bảng (results, ablation, whittle) in bài AoI-greenhouse =
`0.0027/0.041`, các hàng baseline khác (VoU/AoII/MaxAoI) thì đúng batch
`intel_benchmark`. Đối chiếu `ablation_results_30windows.csv` thấy `0.0027/0.041`
khớp CHÍNH XÁC biến thể **`+debt -corr`** (tắt channel-correlation), trong khi số
ĐÚNG phải là **`Full (corr+debt)` = 0.0024/0.120/0.0367**. Tức cả HÀNG method-chuẩn
bị lấy từ variant SAI, dù 6 cột trong hàng đó tự-nhất-quán với nhau (vì cùng từ một
run). Whittle CSV (`whittle_exact_comparison`) xác nhận bài AoI-greenhouse thật = 0.00238.

Cách bắt & xử lý:
1. **Khi một con số khớp KHÔNG batch chính nào, mở file ablation/variant CSV và so
   TỪNG cột** (loss, missed, Jain, age). Nếu khớp đủ 6 cột của một variant phụ →
   gần như chắc cả hàng lấy nhầm variant đó, không phải số cũ ngẫu nhiên.
2. **Đọc thẳng cột `variant` của ablation CSV** để biết tên biến thể deployed
   (`Full (corr+debt)`) vs các biến thể tắt thành phần (`+debt -corr`, `VoU-only`,
   `+corr -debt`). Lấy lại số từ ĐÚNG variant deployed cho mọi bảng + prose.
3. **Lợi ích phụ:** sửa hàng về variant đúng thường làm số abstract khớp luôn (vd
   78%/96% chỉ đúng khi dùng 0.0367/0.00238; dùng 0.041/0.0027 ra 75.6%/95.5%).
   Đây là cách chéo để xác nhận đã sửa đúng variant.
4. **Bội số phái sinh phải tính lại** (Whittle: 0.0932/0.0024=39× không phải 34×;
   0.0642/0.0024=27× không phải 24×) — grep mọi lần lặp bội số trong text.

## Bug #2: số trong abstract/headline không trace được về bảng nào

Abstract ghi "76% vs MaxAoI, 95% vs AoII". Recompute từ batch CSV gốc
(`intel_benchmark_*.csv`, 30-window) ⟹ thật là **78% / 96%**. Số stale từ batch cũ.
Quy tắc: mọi % trong abstract phải tính lại programmatically từ CSV deployed-variant
hiện tại; tên baseline trong abstract ("MaxAoI") phải khớp tên trong batch. Nếu
không tìm thấy policy cùng tên trong batch chính ⟹ số đến từ batch khác, truy nguồn
trước khi tin.

## Bug #3: ký hiệu kép cho cùng một đại lượng (góc người đọc)

Cùng vật, hai tên xuyên section — reviewer hỏi "có phải một không?":
- predictive mean: §2 `μ_i(t)`, §3 `X̂_i(t)`.
- last reported value: §2 `x_i`, §3 `X_i^{rep}`.
- channel success: Algorithm `p_succ`, text `p_i(t)`.
- "AR(1) Kalman-filter posterior" nhưng KHÔNG có measurement-noise model ⟹ thực ra
  là AR(1) forecast thuần (predict-only), không phải Kalman update.

Fix rẻ nhất khi có sibling agent đang sửa song song: thêm **câu cầu nối** buộc hai
ký hiệu (`$\hat X_i(t)\equiv\mu_i(t)$ ... we write $\hat X_i$ in the scheduling
layer and $\mu_i$ in the estimator layer for the same quantity`), thay vì viết lại
toàn bộ. Với Kalman: đổi nhãn thành "AR(1) predictive belief ... pure forecast
rather than a measurement-update Kalman posterior". Thống nhất `p_succ`→`p_i(t)` ở
Algorithm + eq impl; giữ `p_succ(·)` CHỈ cho hàm-theo-mode (G/B) nếu đã định nghĩa
quan hệ `p_i = p_succ(c_i)` ở đâu đó.

## Bug #4: hằng số số học TỰ-KHỚP-NỘI-BỘ nhưng SAI so với dữ liệu thật

Cạm bẫy tinh vi nhất — không bắt được bằng đọc văn. Pattern thật (bài AoI-greenhouse): §4/§5.1
ghi innovation $\sigma=0.031$, one-step RMSE $0.0315$, và "$0.22\%$ của RANGE(14)".
Ba số này **khớp NHAU** (RMSE một bước ≈ innovation std, và $0.0031{\times}14{\approx}0.031$),
nên đọc lướt thấy rất hợp lý. Nhưng đo lại từ dữ liệu thật: $\sigma$ thật $=0.0797$,
RMSE thật $=0.0797$, $=0.57\%$ RANGE — tất cả lệch **~2.5×**. Cả cụm là số stale từ
một phiên bản data chuẩn hoá cũ; chúng tự-nhất-quán nên không section nào "tố" section
nào. §5.3 (validation) lại ghi $0.082$ — chính sự VÊNH giữa hai section (0.031 vs 0.082
cho cùng dataset) là manh mối duy nhất để nghi ngờ.

Cách bắt & xử lý:
1. **Khi hai section ghi hai giá trị khác nhau cho CÙNG đại lượng/dataset** (vd
   $\sigma{=}0.031$ ở §5.1 nhưng $0.082$ ở §5.3), ĐỪNG chọn bừa — đo lại từ raw
   data: fit lại AR(1) trong `.venv` repo, tính `np.std(residual)` pooled + per-mote
   median. Số thật quyết định, không phải số xuất hiện nhiều lần hơn.
2. **Phân biệt std vs robust-scale** trước khi kết luận "đâu là số đúng". Heavy-tail
   thì std (0.08) ≫ MAD·1.4826 (0.002) ≫ IQR-sigma (0.007). Kiểm xem 0.031 có phải
   một robust estimator không — ở case này KHÔNG khớp cái nào ⟹ đơn thuần là sai/stale.
3. **Verify chuỗi dẫn xuất phụ thuộc nó.** $\sigma$ sai kéo theo cả $s{=}\sigma\sqrt h$,
   $z{=}\text{dist}/s$, $\varepsilon{=}\sigma/\text{dist}$, suppression $\mathrm{ES}/P_{\mathrm{vio}}$.
   Tính lại TẤT CẢ ở $\sigma$ thật bằng execute_code. Tin tốt thường gặp: kết luận
   ĐỊNH TÍNH vẫn đúng (AR1 RMSE ≈ persistence ⟹ near-random-walk; severity bị nén
   ~2 bậc) — chỉ con số tuyệt đối đổi. Nói rõ điều này với người dùng để người dùng yên tâm
   narrative không sụp, chỉ số cần đồng bộ.
4. **Đồng bộ ở MỌI section** dùng con số đó (grep `0.031`, `0.0315`, `0.22\%`,
   `0.082`, `0.9996` xuyên `sections/*.tex`+`main.tex`), cẩn thận PHÂN BIỆT con số
   là tham số (σ, α) — phải sửa — với con số TRÙNG nhưng là giá trị bảng (vd cột
   missed-vio cũng tình cờ $0.082$) — KHÔNG đụng. Đọc context mỗi match.

Quy tắc tổng: bất kỳ hằng số dẫn xuất nào (σ, α, half-life, ε, z, %RANGE, bội số ×,
forecast-skill ratio) phải verify PROGRAMMATICALLY từ raw data/CSV ÍT NHẤT MỘT LẦN,
không retype từ trí nhớ/log/bản nháp cũ. Self-consistency giữa vài số KHÔNG chứng
minh chúng đúng — chúng có thể cùng sai theo cùng một hệ số.

## Cái KHÔNG sửa (ghi nhận minor, để người dùng quyết)

- Sai khác số-window đã KHAI BÁO minh bạch (sensitivity 12 vs core 30) không phải
  lỗi giấu; chạy lại 12→30 là việc lớn, hỏi trước.
- Hằng số định lý mượn nguyên từ paper khác (đã cite Theorem 1 of [ref]) — không tự
  xác minh nội bộ paper khác được; cách trích dẫn hợp lệ là đủ.
- **Ref thừa trong `.bib`** (vd 47 entry nhưng chỉ 40 được `\cite`): BibTeX CHỈ in
  ref được cite nên **vô hại với PDF render** — KHÔNG xóa (người dùng có thể để dành cho
  vòng revision). Chỉ flag. Check nhanh bằng execute_code: regex `@\w+\{([^,]+),` lấy
  bib keys, regex `\\cite[tp]?\{([^}]+)\}` lấy cited keys, in `uncited = bibkeys -
  cited` và `missing = cited - bibkeys`. **`missing` (cite tới ref không tồn tại) MỚI
  là lỗi thật** phải sửa; `uncited` chỉ là rác file.

## Khi người dùng DUYỆT nâng số-window của sweep lên cho khớp core (12/8 → 30)

Item \"sai khác số-window\" ở trên là GHI-NHẬN-hỏi-trước. Khi người dùng nói \"chạy lại
đi\" / \"làm cả hai\", đây là EXECUTE đắt — chạy nền, notify_on_complete, rồi PROPAGATE
đầy đủ. Bốn thứ phải đồng bộ, dễ sót #3 và #4:

1. **Backup CSV cũ trước** (`cp docs/sensitivity_*.csv docs/_<name>_OLD_<ts>.csv`),
   chạy sweep ở N mới trong nền. Sweep N-scalability đắt theo ~N² (N=30→132s,
   N=50→256s, N=100 nhiều phút) — tổng 4 sweep có thể 30-50 phút; đặt
   `notify_on_complete=true`, đừng block. Nếu log đứng im lâu, KIỂM tra worker con
   thật sự 100% CPU (`ps -o %cpu,stat`, stat phải `Rl`/`R`) chứ không phải parent
   bash 0% — parent idle là bình thường, chỉ lo nếu CHILD chết.
2. **Cập nhật số trong prose + bảng** từ CSV mới (đọc CSV programmatically, không
   retype từ log).
3. **TÁI TẠO FIGURE PNG — dễ quên nhất.** Sweep script thường CHỈ ghi CSV, KHÔNG vẽ
   lại PNG; hình cũ vẫn là plot từ dữ liệu cũ ⟹ hình mâu thuẫn text. Tìm script vẽ
   riêng (`plot_sensitivity.py`), chạy nó (đọc CSV mới), rồi CHÚ Ý nó hay xuất vào
   thư mục repo (`<repo>/../manuscript/figures`) KHÁC thư mục manuscript clean của
   người dùng — backup PNG cũ, copy PNG mới sang đúng `<project>/figures/`, kiểm mtime
   đã đổi. VERIFY bằng `vision_analyze` một hình: trục/giá trị khớp số mới, chữ
   không vỡ. Build sạch KHÔNG chứng minh hình đúng dữ liệu.
4. **Cập nhật câu METADATA mô tả số-window.** grep `12 paired windows`,
   `12-window`, `fewer windows`, `exploratory because` — câu kiểu \"sensitivity
   sweeps are exploratory because they use fewer windows per operating point\" giờ
   SAI (đã bằng core) ⟹ đổi thành \"exploratory single-factor scans over a shared
   30-window batch\". Caption bảng ablation (\"8 matched windows\") cũng phải đổi 30.

**Narrative có thể ĐẢO khi tăng N — viết lại trung thực, đừng giữ câu cũ.** Số nhiều
window hơn = ground truth hơn, và câu chuyện định tính có thể đổi:
- B_probe: bản 12-window đỉnh gap ở B=6; bản 30-window đỉnh ở **B=4** (6.2×) rồi thu
  hẹp 4.3×/3.4× — phải viết lại chỗ \"peaking at B=6\".
- Danger ablation: severity ρ=3 từng \"identical to five significant figures\" với
  classic; ở 30-window thành **1.27×** (hơi tệ hơn). Bỏ \"identical\", viết \"within
  run-to-run spread\" trung thực. ev-cost từ \"2-3×\" thành \"3-4×\".
Đừng giả định kết luận cũ sống sót; re-verify từng câu so/đỉnh/bội số với CSV mới.

## Condensation Discussion/Limitation/Conclusion = cũng re-verify số nhúng

Khi người dùng nói \"viết ngắn gọn đúng trọng tâm\", ngoài cắt prose còn phải VERIFY mọi
số so sánh nhúng trong đoạn đó so với CSV hiện tại — đoạn văn xuôi là nơi số stale
trốn kỹ. Bug thật: Discussion ghi \"against MaxAoI ... better in 13, tied in 17, worse
in none\" — recompute per-window từ `intel_benchmark_*.csv` (group theo `window_id`,
so loss CAW vs MaxAoI) ⟹ thật là **27 win, 0 tie, 3 loss**. Cũng đồng bộ ε≈0.12→0.16
nếu phiên trước đã sửa σ. RMSE \"0.110 vs 0.126\" verify khớp (0.1103/0.1262) thì giữ.
Lưu ý cột policy trong CSV intel_benchmark nằm ở `policy_name` (cột cuối), không phải
`policy`; tên policy là `MaxAoI`/`AoII`/`bài AoI-greenhouse`/`VoU` (khác batch sota dùng
`MaxWeight-AoI`).

## Acronym first-use expansion audit (khi người dùng nói "viết tắt thì giải trình lần đầu, lần sau viết tắt luôn")

Quy tắc người dùng: mỗi acronym phải viết ĐẦY ĐỦ + (viết tắt) ở LẦN ĐẦU trong THÂN
bài, các lần sau dùng viết tắt. **Abstract KHÔNG tính** (người dùng nói rõ) — abstract
là self-contained, được phép viết tắt độc lập; lần đầu trong thân bài vẫn phải giải
trình lại.

Cách audit programmatically (execute_code):
1. Liệt kê acronym ứng viên trong domain (IoT, VoU, AoI, AoII, VoI, bài AoI-greenhouse, LP,
   MDP, POMDP, RMSE, CDF, AR, ES, CI, GE, CVaR...).
2. Quét các file `sections/*.tex` THEO THỨ TỰ `\input` trong main.tex (không theo
   alphabet) để tìm lần xuất hiện ĐẦU TIÊN của mỗi acronym, BỎ QUA preamble/title/
   `\definecolor`/comment màu (match `(?<![A-Za-z])ABBR(?![A-Za-z])` word-boundary).
3. Với mỗi acronym, đọc dòng first-occurrence: có dạng đầy đủ kế bên không? grep
   thêm cụm full-form ("Value of Information", "linear program", "root-mean-square",
   "cumulative distribution function") để xác nhận đã định nghĩa ở đâu đó TRƯỚC điểm
   dùng tắt.

Hai cạm bẫy thật (bài AoI-greenhouse):
- **Acronym lần đầu nằm trong BẢNG (cột), không phải prose** (vd RMSE đầu tiên xuất
  hiện ở header bảng dòng 59, prose mãi dòng 140). Bảng/cột KHÔNG phải chỗ giải
  trình hợp lệ — thêm định nghĩa ở câu prose mô tả metric TRƯỚC bảng ("the three
  primary metrics: safety-critical loss, root-mean-square error (RMSE), and ...").
- **Tên method-of-bài chưa bao giờ viết đầy đủ.** bài AoI-greenhouse dùng khắp nơi nhưng không
  chỗ nào ghi "Channel-Aware Value-of-Update" — bổ sung ngay ở câu giới thiệu method
  trong intro. Đây là acronym dễ sót nhất vì nó "hiển nhiên" với tác giả.
- Các acronym thường ĐÃ đúng (đừng đụng): AoI/AoII (intro), AR (Auto-Regressive,
  system model), POMDP (Partially Observable Markov Decision Process, methodology),
  ES (expected shortfall, theory), CI (confidence interval, eval setup).
Sửa = thêm "(Full Form)" hoặc "Full Form (ABBR)" tại first body use; build chain xác
nhận 0 lỗi. Tiện thể bắt số stale gần đó (sibling agent hay ghi đè lại "12 windows"
sau khi mình đã đổi 30 — re-grep `\$12\$` sau mỗi acronym pass).

## Giải nghĩa từng Lemma/Theorem bằng lời (khi người dùng hỏi "Lemma/Theorem ý nghĩa là gì")

Người dùng không sâu notation; khi người dùng hỏi "các Lemma và Theorem lần lượt ý nghĩa là
gì", trả lời = MỘT câu intuition đời thường cho TỪNG kết quả, KHÔNG đọc lại phát
biểu toán. Cấu trúc đã chạy tốt:
1. **Nhóm theo MẠCH chứng minh, không theo thứ tự xuất hiện.** Bài bài AoI-greenhouse có 2 mạch:
   Mạch 1 (Lemma suppression → Prop leading-order → Cor no-richer) = *biện minh CHỌN
   hàm danger nào*; Mạch 2 (Prop unichain → Thm O(1/√N) → Cor index; Def gap → Thm
   bounded-gap → Cor design-rule → Thm regularity; Prop no-deadline) = *tối ưu tiệm
   cận + công bằng*. Nói rõ mạch trước, rồi từng item.
2. **Mỗi item: tên + 1 câu "nói gì" + 1 câu "ý nghĩa/để làm gì".** Dùng blockquote
   cho câu phát biểu rút gọn, rồi "Ý nghĩa: ...". Ví dụ: *Lemma suppression — khi
   sensor còn cách ngưỡng an toàn, mức-vượt-trung-bình nhỏ hơn xác-suất-vượt theo hệ
   số ε. Ý nghĩa: dùng xác suất vượt là đủ, thêm độ nghiêm trọng không đổi gì.*
3. **Đánh dấu kết quả ĐẶC BIỆT:** ⭐ định lý chính (O(1/√N)); ⚠️ kết quả TRUNG THỰC
   về giới hạn (Prop "bounded deficit không cho deadline cứng") — nhấn mạnh đây là
   chỗ bài tự thừa nhận yếu điểm, tăng độ tin trước reviewer.
4. **Nối ngược về empirical:** chỉ ra Corollary nào được bài tiên đoán rồi ablation
   §4 xác nhận (vd Cor no-richer ⟹ ev-cost/severity không thắng — số thật khớp).
5. **Hỏi lại người dùng có muốn NHÚNG các câu intuition này vào bài** (1 câu plain-
   language ngay sau mỗi phát biểu theorem) — đúng preference "pair equation với
   plain-language + symbol table". Đừng tự nhúng khi người dùng chỉ hỏi để hiểu; hỏi trước.

## Verify + báo cáo

- Mỗi lần sửa: full build chain `pdflatex→bibtex→pdflatex→pdflatex`, grep pass cuối:
  errors=0, undef cross-ref=0, undef cite=0, multiply-defined=0, overfull>60pt=0.
  Khi thêm `\ref{alg:...}` vào dòng algorithm, nhớ thêm `\label` tương ứng kẻo undef.
- Verdict mở đầu (Major/Minor) trong 1-3 câu, rồi bảng "vấn đề | bằng chứng & cách
  sửa" theo severity, tách rõ ĐÃ SỬA (kèm số verify) vs GHI NHẬN-chưa-sửa.
- Giữ góc người đọc tích cực ở cuối: nêu điểm mạnh (mạch chặt, phần trung thực tạo
  niềm tin) để người dùng biết cái gì NÊN GIỮ, không chỉ liệt kê lỗi.
