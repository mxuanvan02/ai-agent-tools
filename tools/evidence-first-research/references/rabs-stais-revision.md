# bài bandwidth-scheduling / hội nghị C1 Revision Notes

Use this reference when revising hội nghị C1-style bài bandwidth-scheduling manuscripts for người dùng.

## Workspace
- Put the project under `SAS/Research/<project>/`.
- Keep generated packages under `SAS/Research/_packages/` and external cloned code under `SAS/Research/_repos/`.
- Canonical bài bandwidth-scheduling code repository from người dùng: `https://github.com/OWNER/bài bandwidth-scheduling`; clone/pull this repo before asserting bài bandwidth-scheduling numbers or code availability.

## Core narrative
- bài bandwidth-scheduling contribution is adaptive bandwidth scaling for safety-critical greenhouse IoT, not absolute safety superiority.
- Frame bài bandwidth-scheduling-PD as a practical/primal-dual-inspired heuristic, not a proven optimal primal-dual algorithm unless convergence is actually proved.
- Prefer: “favorable composite safety--bandwidth trade-off” and “reduces manual penalty tuning”.
- Avoid overclaims: “plug-and-play”, “eliminates tuning”, “strictly dominates”, “no degradation in safety”, “deployable solution”, “identical safety”.

## Section-writing preferences for người dùng
- Introduction should briefly add deployment context, failure mode of fixed-budget scheduling, and why adaptive bandwidth matters before contributions.
- Contribution bullets should be short and pointed; avoid long multi-clause contribution paragraphs.
- Related Work should usually be written as connected thematic paragraphs, not divided into many subsections, unless người dùng explicitly asks for a structured review.
- Conclusion should be concise: framework, mechanism, key measured trade-off, and practical implication only.
- Limitations and Future Work should be compact and direct: list the main limitations in prose, then one sentence of future work; do not over-expand into journal-style caveats for a short hội nghị C1 manuscript.

## Metric integrity pitfalls
- Distinguish composite `Safety Obj.` from `Missed (%)`. A lower composite objective does not mean every safety metric improves.
- In the bài bandwidth-scheduling_STAIS session, Fixed-B3 had fewer missed violations than bài bandwidth-scheduling-PD, while bài bandwidth-scheduling-PD used much less bandwidth and had comparable/better composite objective depending on scenario. Narrative must say this explicitly.
- If a table has `p vs. PD`, do not caption “lower is better for every column”; p-value is not a performance metric.
- If objective is lower-is-better, an Oracle row is a reference lower bound, not an upper bound.

## Mathematical clarity rules used
- Define the slot timeline: pre-transmission estimate, polling decision, success/failure, update.
- Do not use unavailable ground truth in a scheduling score. Replace terms like `|xhat_t - x_{t-1}|` with gateway-observable quantities such as predicted deviation from last received estimate/value.
- Define violation probability explicitly if using a Kalman/Gaussian predictor:
  `P(x notin [tau_min,tau_max]) = Phi((tau_min-xhat)/sigma) + 1 - Phi((tau_max-xhat)/sigma)`.
- Polling cannot directly change the true physical violation incidence unless an actuator/control loop is modeled; formulate the objective as expected missed/delayed detection risk or unobserved violation probability.
- Define `Benefit_t(b)` concretely, e.g. sum of top-`b` urgency scores, before using a penalized reward `Benefit_t(b) - eta_t b`.

## Regenerate outputs before verifying numbers (results CSVs may be missing)
- The bài bandwidth-scheduling manuscript ships tables as committed `.tex` (sota_comparison/wilcoxon/sensitivity) but the underlying result CSVs (`outputs/rabs/rabs_summary.csv`, etc.) are often NOT in the clean tree — only `data/source/safety_probability_calibration_raw.csv` is. So numbers cannot be verified until you re-run the pipeline.
- The run scripts are stdlib-only and reproducible (fixed `SEEDS`). Regenerate with the project venv before any number audit:
  `cd _repos/bài bandwidth-scheduling && /mnt/external-data/hermes-agent/venv/bin/python3 code/run_rabs_adaptive_bandwidth.py` → writes `outputs/rabs/rabs_summary.csv` (cols `objective_mean`, `avg_bandwidth_mean`, `missed_pct_mean`, plus `_ci95`). Then verify every table cell against it (open with pandas/csv). In this session the sota_comparison table matched the CSV 100% after regenerating.
- `p`-values and effect-size `r` in `wilcoxon.tex` are NOT recoverable from the summary CSV (need the paired per-window arrays). To verify them, re-run the paired test script (`analyze_rabs_wilcoxon.py`), don't try to back them out of means/CIs. This session it DID verify 100% (Δmean, r, p_holm all matched the table) after regenerating.
- **venv gotcha:** `run_rabs_adaptive_bandwidth.py` is stdlib-only so the hermes venv runs it, but `analyze_rabs_wilcoxon.py` imports `numpy`/`scipy` which the hermes venv (`/mnt/external-data/hermes-agent/venv`) lacks. Use the bài probe-transmit repo venv instead — `/home/<user>/SAS/Research/_repos/bài probe-transmit/.venv/bin/python3` has numpy 2.4 + scipy. The raw per-window CSV (`outputs/rabs/rabs_raw.csv`, ~2.8MB) is produced by the main run, so regenerate that first, then run the wilcoxon script against it.

## Weight-count and CV pitfalls (found this session)
- **3-weight formula vs 5-weight table mismatch.** `eq:rabs_urgency` has 3 top-level weights ($w_{AoI},w_{dev},w_{risk}$) but the sensitivity table sweeps 5 sub-weights $w_1$–$w_5$. They are NOT the same level: the 5 sub-weights are the internal composition of the risk cue $p^{vio}$ (peak/mean exit-prob, normalized age, channel-bad belief, worst-case deviation — see `patched_risk_score` in `run_rabs_weight_sensitivity.py`). Fix by adding one sentence mapping the 5 sub-weights to the risk composite before the sensitivity table; do NOT silently let reviewer infer a 3↔5 contradiction.
- **CV rounding.** Recompute CV from the table rows, don't trust the printed value. This session the bài bandwidth-scheduling-PD CV was printed 0.2% but true (pop) CV = 0.255% → rounds to 0.3% (sample-std CV = 0.286%). bài bandwidth-scheduling-L 0.16%→0.2% and bài bandwidth-scheduling-H 2.5% were correct. Fix both `sensitivity.tex` CV row and the prose.
- Terminology: $\eta$ is a penalty, not a threshold. Call bài bandwidth-scheduling-H/bài bandwidth-scheduling-L "static-penalty variant", not "static threshold-based". There is no $\tau_1/\tau_2$ grid-tuning in the paper; $[\tau_{\min},\tau_{\max}]$ is only the physical safety band.
- Overclaim to soften: "requires no manual intervention" (the weights, step size, $B_{target}$, $\eta$ init, budget set are all hand-set — the sensitivity sweep itself tunes them) → "reduces manual penalty tuning". Notation: unify state estimate to $\hat{x}_{i,t^-}$ (method section had a stray $\hat{X}$).

## Elevating bài bandwidth-scheduling-PD theory: dual-convergence (derive-then-verify, run real)

Khi người dùng nói \"phân tích chặt hơn\" và limitation tự nêu là \"primal-dual-inspired heuristic, no convergence guarantee\", đây là lỗ hổng Q1 lớn nhất. Lấp bằng MỘT lớp lý thuyết khớp ĐÚNG cái code đang chạy, không bịa định lý mạnh:
- Cập nhật penalty trong `run_rabs_adaptive_bandwidth.py` chính là **projected dual ascent**: `eta_{t+1} = max(0, eta_t + alpha*(B_t - B_target))`. Viết đúng dạng này (khớp hằng số code: `alpha=0.010`, `B_target=1.55`).
- **Proposition 1 (Bounded penalty):** primal gain mỗi slot bị chặn (loss/AoI/miss đều trong [0,1]) ⟹ có ngưỡng `eta*` mà trên đó luôn chọn `B_min`, drift `alpha*(B_min-B_target)<0` kéo `eta` xuống ⟹ `eta_t ≤ eta_max`.
- **Proposition 2 (Asymptotic budget feasibility):** telescoping. Projection chỉ làm tăng giá trị ⟹ `alpha*(B_t-B_target) ≤ eta_{t+1}-eta_t`; cộng `t=1..T` ⟹ `(1/T)Σ(B_t-B_target) ≤ (eta_{T+1}-eta_1)/(alpha T) ≤ eta_max/(alpha T) → 0`. Trung bình ngân sách hội tụ về target với tốc độ O(1/T) — đủ để bỏ penalty hand-tune.
- **VERIFY bằng script chạy thật trước khi viết** (`code/verify_dual_convergence.py`, import primitives của simulator chính qua `importlib`, log quỹ đạo `eta_t` + running-avg budget). Phiên này: `sup eta = 0.61` (bounded ✓), max time-avg vi phạm `+0.060 ≤` chặn lý thuyết `eta_sup/(alpha*T)=0.061` ✓, `mean avg B = 1.51 ≤ B_target=1.55` ✓. Chỉ viết Proposition sau khi số khớp chặn.
- **Preamble gotcha:** template `article` của bài bandwidth-scheduling KHÔNG có sẵn môi trường `proposition`/`proof`. Thêm `\usepackage{amsthm}` + `\newtheorem{proposition}{Proposition}` vào preamble NGAY, nếu không build vỡ \"Environment proposition undefined\" + cả loạt undefined ref ăn theo (exit 12).

## Non-stationary channel extension (run real, không bịa số)

Khi người dùng xin mở rộng thực nghiệm (đa-band, non-stationary channel):
- Viết extension script tái dùng primitive simulator gốc qua `importlib` (chỉ thay đúng phần kênh, GIỮ NGUYÊN policy logic để byte-identical với main results). Kênh drift = tham số Gilbert–Elliott dao động theo thời gian (vd `f = 1 + 0.5*sin(2πt/250)` cho loss rates) — mô phỏng điều kiện ngày/đêm/độ ẩm.
- Chạy THẬT đủ N (320 windows = 20 seeds × 16 windows), xuất CSV + bảng `.tex`. Phiên này: bài bandwidth-scheduling-PD obj 0.158 ≤ Fixed-B3 0.161, tiết kiệm ~50% bw — cùng qualitative trade-off với stationary.
- **Verify bảng vs CSV bằng execute_code** (mean per policy) TRƯỚC khi nhúng số vào `.tex` — số trong bảng phải khớp CSV 100%.
- Sau khi có bằng chứng non-stationary, cập nhật Limitations: bỏ ý \"chỉ test stationary channel\", đổi thành \"stationary và drifting\"; limitation 2 đổi từ \"no convergence guarantee\" → \"establish bounded penalty + asymptotic budget feasibility (Prop 1–2), but not full optimality for joint budget-and-selection\".
- **f-string + LaTeX backslash gotcha:** không nhúng `'\\\\_'` trong biểu thức f-string (SyntaxError \"f-string expression part cannot include a backslash\"); gán `pol_tex = pol.replace('_','\\_')` ra biến tạm trước rồi mới dùng trong f-string.
- **cwd gotcha với write_file/read_file path tương đối:** sau khi chạy nhiều lệnh trong `_repos/bài bandwidth-scheduling`, tool file đôi khi giải path tương đối theo cwd cũ và tạo thư mục lồng sai (`_repos/bài bandwidth-scheduling/SAS/Research/...`). Luôn dùng đường dẫn TUYỆT ĐỐI cho write_file/read_file/patch khi thao tác file manuscript ở repo khác cwd; dọn `rm -rf` nhánh lồng nếu lỡ tạo.

## Formula linkage: connecting disjoint math clusters (derive-then-verify)

Khi người dùng nói \"chưa có sự liên kết giữa các công thức toán học\" (sửa vào file gốc), đây là EXECUTE — bài thường có 3 cụm toán rời: (1) bài toán tối ưu ràng buộc dài hạn ở §System Model, (2) một hàm chi phí $J_t(b)$ xuất hiện ĐỘT NGỘT trong Algorithm box, (3) dual updates viết tách rời. Cầu nối còn thiếu là một dẫn xuất biến (2)+(3) thành hệ quả toán của (1). Recipe đã chạy thật cho bài bandwidth-scheduling-PD:
- **Viết derivation ra `docs/*_derivation.md` TRƯỚC, verify 1-1 với code** (đọc `choose_B_rabs_family`, `predict_candidate`, `risk_score`, dual updates trong `run_fixed`), rồi mới sửa `.tex`. Mọi hằng số/hệ số trong eq phải khớp code.
- **Bổ sung ràng buộc dài hạn TƯỜNG MINH** vào bài toán P ở §System Model cho ĐỦ số dual mà code chạy: bài bandwidth-scheduling-PD có 3 dual (bandwidth + AoI + missed-event) ⟹ §System Model phải có 3 ràng buộc $\\limsup_T \\frac1T\\sum_t \\mathbb{E}[\\cdot]\\le\\text{target}$ với `\\label{eq:cons_bw/aoi/miss}`. Bài cũ chỉ có 1 ràng buộc bandwidth.
- **Viết phương trình tường minh cho các đại lượng chỉ-tả-bằng-lời.** $\\widehat{L}_t,\\widehat{A}_t,\\widehat{M}_t$ dùng trong Algorithm nhưng không có eq ⟹ thêm `\\begin{align}` định nghĩa khớp code (vd $\\widehat{M}_t(b)=\\frac1N\\sum_{i\\notin\\mathcal{U}_t}p^{vio}_i$ chính là objective của P).
- **Dẫn xuất $J_t$ = Lagrangian theo-slot của P** (drift-plus-penalty / dual decomposition, cite Neely): gắn multiplier $\\lambda^B,\\lambda^A,\\lambda^M\\ge0$ vào 3 ràng buộc, minimize per-slot Lagrangian ⟹ ra ĐÚNG $J_t$ code đang dùng. Dual update = projected stochastic subgradient ascent $\\lambda^c_{t+1}=[\\lambda^c_t+\\alpha_c(\\text{realized}-\\text{target})]_+$. Câu chốt: \\\"$J_t$ không ad hoc — nó là per-slot Lagrangian của P, penalty là dual variable\\\".\n- **Lemma nối per-sensor score ↔ objective.** Thêm Lemma (modular set function ⟹ greedy top-$b$ theo $p^{vio}$ tối ưu chính xác $\\widehat{M}_t$); deployed score $S$ reduces về rule này khi $w_{dev},w_{AoI}\\to0$ — phát biểu trung thực \\\"reduces to optimal on the risk component\\\", KHÔNG claim global optimality.\n- **Hợp nhất ký hiệu kép.** $\\Delta_{i,t^-}$ (deviation ở per-sensor) và $e_{i,t^-}$ (proxy error ở risk score) thực ra CÙNG là `proxy_error` trong code ⟹ gộp thành một $\\delta_{i,t^-}$ với eq định nghĩa, dùng ở cả $S$ và $R$. Ghi trọng số deployed THẬT của $S$ (đọc code: 0.55/0.25/0.20) — bài cũ để $w_{AoI},w_{dev},w_{risk}$ trừu tượng.\n- **Preamble gotcha:** thêm Lemma cần `\\newtheorem{lemma}{Lemma}` (template `article` bài bandwidth-scheduling chỉ có sẵn `proposition` sau khi đã thêm `amsthm`). Thiếu ⟹ build vỡ \\\"Environment lemma undefined\\\".\n\n## Page-count overflow from FLOAT GAPS, not excess prose (đo per-page trước khi cắt)\n\nBug thật phiên formula-linkage: thêm toán làm bài 8→9 trang (hội nghị C1 trần 8). Cắt prose nhiều lần (gộp subsection, rút câu trùng, Algorithm tham chiếu eq thay vì in lại, nén Conclusion/Limitations/Intro) NHƯNG vẫn đứng yên 9 trang. Nguyên nhân KHÔNG phải thừa chữ — là **float gaps**: bảng/hình nổi đẩy text để lại khoảng trắng nửa trang, khiến Conclusion+refs tràn sang trang cuối. Quy tắc:\n- **ĐO phân bố ký tự per-page TRƯỚC khi cắt thêm:** `for p in $(seq 1 N); do pdftotext -f $p -l $p main.pdf - | wc -c; done`. Trang đầy ~3000-3700 chars; trang có float gap chỉ ~2000-2500 chars. Nếu các trang giữa underfull mà trang cuối tràn ⟹ vấn đề là sắp xếp float, cắt prose sẽ KHÔNG kéo được trang về.\n- **Fix đúng cho float gap:** (a) thu nhỏ figure (`width=0.50→0.42\\linewidth`, `\\resizebox` ratio nhỏ hơn) để hình lọt cùng trang text; (b) nới float placement trong preamble: `\\renewcommand{\\textfraction}{0.06}`, `\\topfraction`/`\\bottomfraction` lên 0.95, `\\floatpagefraction` 0.85 — cho phép text+float chung trang; (c) đổi `[htbp]` ưu tiên `t`/`b` để float không tạo trang nổi riêng. Cắt prose chỉ là đòn phụ.\n- Đừng lặp lại sai lầm: nén prose 6-7 lần liên tiếp mà page count không nhúc nhích là tín hiệu RÕ rằng nguyên nhân nằm ở float, dừng cắt chữ và đo per-page ngay.\n\n## Packaging and verification
- Build clean PDF and package source + required `outputs/tables` and `outputs/figures`; the bài bandwidth-scheduling manuscript is not self-contained inside `manuscript/`.
- Include a short `README_PACKAGE.txt` in the clean ZIP.
- Before calling ready-submit, compile after the final text edit, check undefined refs/citations and `Overfull \\hbox`, then refresh `SAS/Research/_packages/bài bandwidth-scheduling_STAIS_revised_clean_submission.zip`.
