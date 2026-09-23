# Tái lập & kiểm chứng số liệu bản thảo — audit, integrity, scale

Dùng khi người dùng nhờ: "số liệu/bảng/biểu chạy đúng chuẩn chưa", "bổ sung kết quả",
"nâng code sát 100% bản thảo", hoặc bất kỳ task nào nối **manuscript ↔ code sinh số**.

## Bài học gốc (người dùng đã chỉnh — đừng lặp lại)

> "Ngay từ ban đầu agent phải đọc và liệt kê ra toàn bộ trước khi triển khai, tránh
> làm lệch. Chứ không phải cứ làm xong rồi sửa."

Lỗi đã mắc: nhảy vào sửa từng con số/từng hình rời rạc, rồi mới phát hiện bản chất
là "calibrated, không phải implementation thật" → phải kéo lại từ đầu. Đáng lẽ
phải **audit toàn cảnh trước**, trình ma trận, để người dùng duyệt phạm vi rồi mới code.

## Ma trận audit (làm TRƯỚC khi code, trình người dùng duyệt)

Bảng `# | claim trong bản thảo (Eq/Sec) | module code | trạng thái | khoảng cách tới 100%`.
Phân loại:
- 🟢 **REAL** — thuật toán thật, số phát sinh từ động học (vd TD3 actor-critic + replay,
  FedAvg NN trên non-IID Dirichlet clients, Bayesian IG reconstruction + F1).
- 🟡 **CALIBRATED** — có code chạy nhưng hằng số/đầu ra hiệu chỉnh bám số bài. Ví dụ thật:
  `energy_model.py` hard-code Table III (4.9/5.9…) và `prop_comm = 5.2*(1-0.456)`;
  `scalability.py` dùng `E = F + coef*workload/V` với coef chỉnh cho ra đúng 35.6%;
  payload table = số bài cố định, không chạy encoder thật.
- 🔴 **MISSING** — bản thảo mô tả nhưng repo chưa có (channel/comm model $R_v$, fusion
  log-odds/Dempster-Shafer, joint-opt, FedAvgM/personalized/sparsification).

## Quy tắc liêm chính (cấm vi phạm)

1. **KHÔNG calibrate-to-output.** Không tinh chỉnh hằng số để khớp headline. "Giữ
   propulsion rồi thổi công suất cảm biến lên" = calibrate trá hình = bịa → TỪ CHỐI.
2. **Số phải emerge từ input vật lý.** Neo vào Table tham số của bài (bandwidth W,
   noise PSD I₀, tx power P, battery Wh, mass, speed, altitude), KHÔNG neo vào output.
3. **Gặp mâu thuẫn nội tại của bài → DỪNG, báo cáo, đưa A/B/C, người dùng chọn.** Không
   tự ý chọn cách cứu số.

## Bài học SCALE (vật lý UAV) — rất dễ vấp

Khi tính **đúng vật lý**, propulsion của UAV là **hàng trăm W**, còn sensing/comm chỉ
**vài W → mW** (chênh 2–3 bậc độ lớn):

| Thành phần | Công suất | Trong tổng mission |
|---|---|---|
| Fly (= hover + drag) | ~182 W | }
| Hover | ~168 W | } ~23 Wh ≈ 95% tổng |
| Sense (5 cảm biến) | 2–3 W | ~0.8–1.6 Wh |
| Comm (A2G, kênh nhanh) | ~50 mW (khi phát) | ~0.01 Wh |
| Base avionics | ~5 W | nhỏ |

→ Hệ quả: nếu mẫu số = TOÀN BỘ năng lượng thì "tiết kiệm 18%" tụt còn ~2–3%, vì
framework (semantic/adaptive) chỉ điều khiển được sense+comm = ~5% tổng. **Đây là
mâu thuẫn nội tại của chính bản thảo**, không phải lỗi code.

3 phương án trình người dùng:
- **A (khuyến nghị):** mẫu số = "sensing+comm energy" (loại bay nền cố định), giữ
  headline ~18% TRUNG THỰC + 1 chú thích rõ "energy = sensing+comm". Nhiều bài
  semantic-communication làm vậy.
- **B:** tính cả propulsion → trung thực tuyệt đối nhưng headline rớt 2–3%, phải đổi
  số trong prose (đụng claim).
- **C:** thổi công suất sense → BỊA, từ chối.

Mô hình T-slot đúng: nhiệm vụ bị giới hạn bởi T slot (mỗi slot bay v·Δt hoặc
hover-sensing), KHÔNG phủ kín lưới mịn. Buộc năng lượng theo T-slot mới đúng vật lý
*và* tự rơi về thang ~20 Wh, với fly+hover là sàn cố định.

## Mô hình kênh A2G first-principles (P1 — đã verify, 10/10 test pass)

```
PL(d) = FSPL(d3d) + p_LoS·η_LoS + (1−p_LoS)·η_NLoS     # Al-Hourani LoS/NLoS mix
p_LoS = 1/(1 + a·exp(−b·(θ−a)))                          # θ = elevation angle (deg)
N     = I₀(dBm/Hz) + 10·log₁₀(W)  → W                    # thermal noise (I₀=−174, W=3MHz)
R     = β·W·log₂(1 + P·G/N),  G = 10^(−PL/10)            # Shannon rate, β = OMA fraction
E_com = P_tx · (payload_bits / R)  → /3600 = Wh          # air-time energy
```
Smoke test hợp lý (xa hơn → PL tăng, R giảm, E/MB tăng): 50m→81dB/45Mbps, 1000m→116dB/10Mbps.
Test pytest kiểm: rate đơn điệu giảm theo d, E_com tăng theo payload & d, thứ nguyên đúng.

## Quy trình chuẩn (test-driven)

1. Tìm bài; phân biệt project đầy đủ vs file `.tex` lẻ. Liệt kê figures tham chiếu
   trong `.tex` vs figures thật trên đĩa.
2. **Phân biệt vẽ tay vs chạy thật:** mở script sinh hình. Nếu chỉ `np.exp`/hard-code/
   noise giả → placeholder, KHÔNG phải output mô phỏng.
3. Cờ đỏ trong `.tex`: `**...**` (markdown lọt vào LaTeX → in ra dấu sao), số "mồ côi"
   không nguồn (vd "27.3%" trong khi bảng cho ra 52%), hai bảng cùng đại lượng lệch
   đơn vị (MB vs KB).
4. Clone repo; venv bằng `uv`; cài CPU-only torch ở **nền** (`background=true,
   notify_on_complete=true`) vì wheel nặng; chạy thật `run_simulation.py`; lấy số
   canonical từ `results.json`. KHÔNG tin README/self-report.
5. Mỗi module → `tests/test_*.py` pytest kiểm tính chất vật lý.
6. Regen MỌI hình từ data thật; patch `.tex` (giữ prose, chỉ số/bảng/hình); `latexmk`
   build sạch; rà undefined ref + số mồ côi + còn sót `**`.

## Code không nằm trong thư mục bản thảo → tìm trên GitHub

Thư mục `*_submission_ready` có thể chỉ chứa `.tex` + `outputs/` (bảng/hình đã render),
**KHÔNG có script sinh số**. Đừng kết luận "mất code" — code thường ở repo companion.

Quy trình định vị (nhanh, tránh `find` quét cả `/mnt/external-data` → timeout):
1. `gh repo view <user>/<repo> --json name,pushedAt` xác nhận repo tồn tại.
2. `gh api repos/<user>/<repo>/git/trees/HEAD?recursive=1 --jq '.tree[].path'` để xem
   cây file remote mà không cần clone — thấy ngay `code/*.py`, `data/source/*.csv`.
3. Clone vào workspace riêng có timestamp (`rabs_repro_<ts>`), KHÔNG đụng thư mục bản thảo.
4. Đọc script chính trước khi chạy: xác định tham số bị hard-code (vd `N`, `range(3)`,
   `/3`, seed list) và nguồn dữ liệu thật (bao nhiêu sensor/loop/window thực sự có).

## Phản biện "N quá nhỏ / thiếu scale" → biến điểm yếu thành điểm mạnh

Reviewer chê "N=3 quá nhỏ, không generalize" là cờ đỏ hay gặp. Cách xử lý mạnh nhất
**không phải** cãi mà là **chạy thêm scaling experiment** cho thấy xu hướng đơn điệu:

- Viết script scaling MỚI (không sửa script gốc), tổng quát hóa N, tái dùng đúng logic
  policy + primal-dual/urgency. Chạy N∈{3,8,12,20}, số ra từ chạy thật.
- Ví dụ kết quả bài bandwidth-scheduling: ở N=3 (worst case) phương pháp hòa/hơi thua full-polling, nhưng
  lợi thế **tăng đơn điệu** theo N (N=20 → tốt hơn 42% ở ~43% bandwidth). Framing:
  *"N=3 là worst case cho phương pháp của chúng tôi; giá trị của adaptive budget xuất
  hiện khi mạng lớn — đúng bối cảnh triển khai thực tế."*

**Ràng buộc trung thực khi dataset chỉ có ít sensor thật:** nếu nguồn chỉ có 3 zone thật
(3 loop trong CSV), N>3 **bắt buộc là sensor tổng hợp**. Phải:
- Giữ stream thật làm anchor, sinh thêm zone bằng bootstrap + noise/phase-shift độc lập.
- Frame RÕ trong bài là **"synthetic scalability stress test"**, KHÔNG trộn vào thí
  nghiệm chính, KHÔNG đụng claim real-data. (Claude reviewer cũng chấp nhận "dù synthetic".)
- Text mới thêm vào manuscript = **đánh dấu vàng** (YELLOW-highlight review markup) để
  người dùng review, strip trước khi submit.

## Git push (companion repo)

- SSH-exec bị chặn ⇒ **HTTPS tokenized qua gh credential helper**; git identity set
  **local** (chỉ repo này, không đụng global).
- Chỉ stage file code; KHÔNG commit `_backups/`, results, drafts, `.tex`.
- **Verify trên remote qua gh API** (commit HEAD + nội dung file đã lên) — không tin
  self-report của lệnh push.
- Repo public = PART of submission ⇒ nếu bài tuyên bố "source code reproduces all
  results", code trên remote PHẢI khớp; nếu không, hoặc push bản đã sửa, hoặc gỡ câu
  tuyên bố. Đừng để repo public lệch với claim trong bài.

## Bảng manuscript ≠ output script (mapping thủ công — kiểm TRƯỚC khi ghi đè)

Bảng `.tex` trong bản thảo thường **KHÔNG** phải file script sinh ra trực tiếp:
- Tên khác nhau: manuscript `sota_comparison.tex` / `wilcoxon.tex` ↔ script sinh
  `table_rabs_summary.tex` / `table_rabs_wilcoxon.tex`.
- Định dạng khác: manuscript = tiếng Anh, tập con policy, thêm cột (vd `p vs PD`),
  `\resizebox`, `\best{}`; script = tiếng Việt, đầy đủ policy, thô.
- Nghĩa là có **bước reformat thủ công** ở giữa → KHÔNG có cầu tự động.

Quy trình an toàn:
1. `diff` nội dung bảng manuscript vs bảng script sinh để hiểu mapping (cột nào, policy
   nào, đơn vị nào) TRƯỚC khi đổi số.
2. Sau khi đổi cơ chế/urgency → viết 1 script sinh THẲNG bảng đúng format manuscript từ
   CSV mới (đảm bảo số khớp tuyệt đối & tái lập), thay vì sửa tay từng ô.
3. Xác định file nào manuscript THỰC SỰ include (đọc `\input{outputs/tables/...}` trong
   `.tex`) — chỉ regen đúng những file đó.

## Đổi 1 cơ chế → truy vết mọi script phụ thuộc (import vs re-copy)

Khi đổi một hàm lõi (vd urgency score), phải phân loại script phụ:
- **Import module chính** (`import run_rabs_adaptive_bandwidth as base`; gọi
  `base.choose_sensors`/`base.run_fixed`) → **tự thừa hưởng** thay đổi, KHÔNG cần sửa.
- **Tự chép lại logic** (định nghĩa riêng `0.55*p`...) → PHẢI sửa đồng bộ tay.
Cách quét nhanh: `grep -l '0.55\*.*p' code/*.py` (tìm bản sao công thức) và
`grep -l 'import run_rabs' code/*.py` (tìm bản kế thừa). Sửa đúng 1 chỗ trong module lõi,
giữ nguyên nhánh baseline (max_aoi, voi_b2...) để không nhiễm chéo.

## Thiếu script/dữ liệu để regen 1 bảng = BLOCKER, không phải cớ để bịa

Nếu đã đổi cơ chế cho toàn bộ thí nghiệm chính nhưng 1 bảng (vd CVaR/ERA5) KHÔNG có
script sinh + KHÔNG có dữ liệu nguồn trong repo → bảng đó giờ **không nhất quán** với
phần còn lại. KHÔNG bịa số để đồng bộ. Dừng, báo blocker, đưa 3 hướng cho người dùng:
(1) người dùng cấp dữ liệu/script → regen đồng bộ; (2) giữ bảng cũ + ghi chú đánh giá độc lập,
chấp nhận rủi ro nhỏ; (3) tạm chuyển mục đó sang future work cho mạch lạc. Trong lúc chờ,
tiếp tục các phần regenerable khác — không đứng im.

## Cơ chế người dùng MUỐN đưa vào bài nhưng thực nghiệm bác bỏ (kết quả âm)

Tình huống lặp lại: người dùng muốn giữ một biến thể/cơ chế (vd bài bandwidth-scheduling-CVaR tail-risk) như
đóng góp, và yêu cầu "chỉnh cho nó tốt hơn / chạy data khó / chốt là được". Kỷ luật:

1. **DERIVE trước, verify sau** — không grid-search mù tìm số đẹp (reviewer bắt overfit).
   Phải có lập luận vì sao dạng mới đúng hơn (vd VoU `4p(1-p)` = leading-order value-of-
   information cho quyết định nhị phân, cực đại ở p≈0.5, =0 khi đã chắc), RỒI mới chạy.
2. **Đo đúng metric mà cơ chế sinh ra để tối ưu.** CVaR phải xét trên đại lượng đuôi-nặng
   thật; nếu áp lên loss trung bình đuôi-nhẹ thì vô ích. Thử lần lượt: loss-tail →
   miss-risk tail → cross-sectional tail. Đổi bản chất, KHÔNG vá lặt vặt.
3. **Kiểm định paired (Wilcoxon) + đọc ĐÚNG DẤU.** Cạm bẫy đã mắc: `p<10⁻³` significant
   nhưng `meanΔ = PD − CVaR < 0` nghĩa là CVaR *thua* — đừng khoe "cải thiện" khi dấu
   ngược. Luôn in kèm chiều ("PD better / CVaR better") cạnh p-value.
4. **Ngưỡng "được": phải THẮNG có ý nghĩa trên metric của chính nó.** Chỗ cơ chế nhỉnh
   mà `p` không đạt (vd missed% p=0.26/0.88) KHÔNG tính là thắng.
5. **Sau ~2 lần thất bại cùng hướng → chẩn đoán gốc rễ, đừng lặp.** Nếu ≥3 phép thử độc
   lập (ablation + on/off + biến thể) đều cho "cơ chế X vô dụng" → đó là **phát hiện khoa
   học nhất quán**, không phải xui. Trên data này: "VoU + primal-dual đã hút gần hết lợi
   ích khả thi; thêm tail-machinery chỉ tăng chi phí."
6. **Khi thất bại: báo thẳng, đưa 3 hướng, để người dùng quyết** — (a) negative result có
   kiểm soát ("cài đúng RU, chứng minh nó KHÔNG cải thiện → khẳng định gain từ VoU+PD");
   (b) giữ làm "knob" nhưng nói rõ đánh đổi + hạn chế ý nghĩa (rủi ro reviewer hỏi "để làm
   gì"); (c) bỏ về Future Work. Người dùng thường chốt "thất bại thì bỏ luôn, tập trung
   proposed tốt nhất". LIÊM CHÍNH: không gắn nhãn "Proposed" cho phương pháp thua sạch
   metric của chính nó — nhét vào là tự bẫy khi reviewer chạy lại code companion.
7. **"Data yếu" vs "data khó":** greenhouse đuôi-nhẹ (violation thưa) là data DỄ; ERA5
   nhiệt độ thật có heat episode (>34°C 2-4%, đỉnh 38°C) là data KHÓ. Người dùng ưu tiên
   validate trên data khó. Data VN "mất" thường chỉ là chưa lưu — fetch lại được từ
   Open-Meteo ERA5 archive API (`fetch_real_vn_data.py`: lat/lon Cần Thơ/Sóc Trăng/Cà Mau,
   `hourly=temperature_2m`), KHÔNG phải bịa.

## Oracle / lower-bound phải là bound THẬT (nếu proposed "vượt oracle" → nghi ngay)

Nếu policy đề xuất có objective TỐT HƠN "Oracle/lower bound" → gần như chắc oracle định
nghĩa sai. Cạm bẫy đã gặp: "oracle" chỉ là *greedy per-slot clairvoyant* — thấy giá trị
thật nhưng (a) vẫn chọn sensor bằng urgency thường thay vì brute-force subset tối ưu, và
(b) dùng bộ hằng số hiệu chỉnh cho dataset khác. Nó tối ưu từng slot, bỏ qua động học AoI
tích lũy → policy có feedback vượt được.
- Oracle đúng: brute-force MỌI subset sensor × MỌI budget, áp giá trị thật, minimize đúng
  objective báo cáo (cùng trọng số, không thừa term). Khi đó không policy causal nào vượt.
- Oracle tích lũy tối ưu thật = NP-hard, không tính được → nếu chỉ có greedy clairvoyant,
  đổi nhãn "Oracle" → "Clairvoyant (greedy) reference" và nói rõ đây là tham chiếu per-slot,
  không phải bound; "proposed vượt greedy-clairvoyant nhờ quản lý AoI theo thời gian" là
  luận điểm mạnh + trung thực, hơn là giấu.

## Review markup: dùng color, KHÔNG dùng soul `\hl` (vỡ trong math)

Text mới thêm vào `.tex` = đánh dấu để người dùng review, strip trước submit. `\usepackage
{soul}` + `\hl{}` **vỡ build trong math mode** (`! File ended while scanning use of \hl`).
Dùng color macro chạy được cả text lẫn math:
```latex
\definecolor{reviewnew}{rgb}{0.00,0.00,0.75}
\newcommand{\hlnew}[1]{{\color{reviewnew}#1}}   % strip: \renewcommand{\hlnew}[1]{#1}
```
Pitfall ngoặc: `\hlnew{\subsection{...}}` phải đóng ngay; đừng để `\hlnew{` mở trùm qua
`\input` rồi chồng với `\hlnew` khác → lệch 1 ngoặc, fatal. Đếm `{` vs `}` mỗi dòng khi debug.

## Page-limit: tỉa prose không dứt điểm → nén references

Quá 1 trang so với limit mà tỉa từng câu prose không về được: refs tràn vài dòng thì thêm
`\small` vào bibliography macro (refs nhỏ hơn body là quy ước phổ biến, chấp nhận được),
thay vì cắt nội dung khoa học. Build đủ pass (latexmk lo, hoặc 3× pdflatex + bibtex) để
`.aux` đồng bộ trước khi kết luận số trang / undefined ref.

## Cách gọi tên cho đúng (tránh overclaim)

- "deterministic, paper-faithful simulation/reproduction of the reported results" ✓
- "complete/full implementation of the framework" ✗ khi vẫn còn phần CALIBRATED/MISSING.
- Câu an toàn cho `.tex`: "The reproducible simulation code used to generate all
  numerical results and figures is publicly available at …"
