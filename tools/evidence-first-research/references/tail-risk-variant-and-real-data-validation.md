# Folding a tail-risk (CVaR) variant + validating on real regional data

Triggers: người dùng says "thử thêm xem", "chạy trên tập dữ liệu khó/thực tế như bài AoI-greenhouse",
"ưu tiên dữ liệu Việt Nam sát thực tiễn", "đề xuất phương án bổ sung nếu method chưa đủ tốt",
or asks to fold a risk-aware / CVaR / tail-risk extension into a scheduling/control paper and
prove the formulas link together. End-to-end recipe proven on bài bandwidth-scheduling (branch B).

## 1. Real regional data sourcing (when Zenodo/Kaggle/OpenAlex come up empty)

Open-Meteo **Historical Archive** (ERA5 reanalysis) is the reliable fallback for REAL,
verifiable, downloadable regional climate data — no auth, lat/lon + full-year hourly:
```
https://archive-api.open-meteo.com/v1/archive?latitude=<lat>&longitude=<lon>
  &start_date=2024-01-01&end_date=2024-12-31
  &hourly=temperature_2m,relative_humidity_2m&timezone=Asia/Bangkok
```
- Pick real stations as sensors (e.g. Mekong-delta: Can Tho, Soc Trang, Ca Mau → 3 sensors).
- 8784 hourly points/station/year. Declare provenance honestly as **semi-real**: real climate
  trace driving the simulated control/channel layer (same spirit as bài AoI-greenhouse dataset khí hậu VN, but
  real and longer). NEVER call it field-measured packet logs.
- Zenodo `query` returns can blow the 20000-char JSON cap (`Invalid control character at ...`)
  and are mostly irrelevant — don't burn turns there; go straight to Open-Meteo for climate.
- The on-disk `vietnam_mekong_weather.csv` from prior papers is ~480 synthetic points, single
  column, unclear provenance — not "hard" and not verifiable. Check the README: prior repos
  often state the trace is `weather-conditioned synthetic`, so don't reuse it as real data.

## 2. CVaR / tail-risk constraint can DEGENERATE on a zero-inflated signal

The most important methodological lesson. A `CVaR_α` constraint adds nothing if the per-slot
signal is **zero-inflated** (mostly 0, rare bursts): the α-quantile ≈ 0, so the tail constraint
collapses to ~the mean constraint and the variant just spends more resource. First bài bandwidth-scheduling spike
folded for exactly this (miss-rate is zero-inflated). Fixes that produced a real positive:
- **Switch the tail variable to a continuous, non-zero-inflated loss** (per-slot control loss
  whose predictor already exists, e.g. `L̂_t`) — it spikes during the dangerous episodes, so
  its tail is non-degenerate.
- **Find a data regime with a real tail.** Print tail-structure diagnostics BEFORE claiming
  non-degeneracy: violation %, burst count, mean run-length. VN ERA5 gave 18–21% violations +
  burst runs ~5–6 slots → non-degenerate (vs. the old zero-inflated miss-rate).

## 3. Matched-operating-point control — kill the "smarter vs. just spends more" confound

When a risk-aware variant beats the baseline but also uses MORE of a resource (bandwidth), the
comparison is confounded. Make it airtight:
- **Bind the resource constraint hard on BOTH policies** (shared dual, identical step) so they
  sit at the same operating point; differences then reflect *allocation*, not *spending more*.
- **Sweep the binding strength** (e.g. BW_STEP 0.06/0.12/0.20) and show the win persists at all
  matched levels (p, win-count stable) → not an artifact of one matching.
- **Include a fair classical risk-sensitive baseline** (mean–variance / exponential-utility).
  If it lands BETWEEN the deployed baseline and your method, that *proves* it's not a straw-man
  and your method is the genuine winner. Report it.
- Pair by `(network, seed, window_start)`, full N, paired Wilcoxon + effect r. Run both channels
  (burst + severe_burst), not just one.

## 4. DERIVE-then-spike, win-or-fold by evidence

- Write `docs/<method>_derivation.md` (the math, RU identity, coupled λ/ξ updates, derived
  constants) BEFORE any expensive run. Then spike on a clone (`<repo>_branchB_clone/`), never
  touching the manuscript until H2 holds with a real effect.
- Reuse simulator primitives via `importlib.util.spec_from_file_location` + repoint `M.SRC` at
  the new calibration CSV — don't reimplement the channel/eval/selector.
- Report the honest negative (first spike folded) before the positive — người dùng trusts the
  evidence trail, not hope.

## 5. Equation-coherence audit WHEN FOLDING A VARIANT (extends the §Stage-6 notation audit)

người dùng: "Các công thức đã liên kết với nhau chưa? ... dùng các phép biến đổi suy ra, tương
đương ... ít chữ nhưng toán học rõ ràng." This is a DERIVE-chain audit, not prose polish:
- **The variant objective must be DERIVED from the deployed objective by explicit term
  substitution, shown as an equation** — not a free-standing formula. bài bandwidth-scheduling: write
  `J^CVaR = J_t` with the expected-risk term `(c_M+λ^M)M̂` *replaced by* the predicted tail
  penalty. Add the chain: constraint `CVaR_α(ℓ)≤c_tail` → Rockafellar–Uryasev identity
  `CVaR_α=min_ξ ξ+1/(1-α)E[(ℓ-ξ)_+]` → `J^CVaR` → coupled subgradient updates (λ dual ascent on
  slack, ξ = VaR tracker from `∂φ/∂ξ`). Reader must see "tương đương/suy ra" at each step.
- **Every symbol in an objective or Algorithm needs a defining equation.** Bug caught: `p_t^bad`
  was used in the system-risk eq AND in the Algorithm REQUIRE line but had NO equation (only
  prose). Add it, matching code 1-1 (EWMA: `p_{t+1}=Π_[ε,1-ε](ρ p_t + κ_l·1_loss − κ_s·1_succ)`,
  ρ=0.85, gains 0.15/0.05, clip [0.01,0.99]).
- **Anchor every new constant** as derivable, not hand-tuned: coupling `1/(1-α)` fixed by the RU
  identity; reuse deployed steps (`α_λ=β=α_M`) so the variant "adds no new rate."
- **Orphan-label check**: diff the set of `\label{eq:}` against `\eqref{}` usages. Range refs
  `\eqref{eq:a}--\eqref{eq:b}` make the in-between labels look "unused" — FALSE POSITIVE, verify
  before deleting. Genuinely-unreferenced new eqs → tie them into prose/Algorithm.
- **Tie the variant to the Algorithm explicitly**: "bài bandwidth-scheduling-CVaR is Algorithm 1 with `J_t→J^CVaR`
  in line 5 and the missed-risk dual replaced by the coupled updates in line 8; all else
  unchanged." Closes the method↔algorithm loop.
- **Method-name coherence**: a folded contribution must appear in abstract AND intro
  contribution list AND keywords — not silently in one place. (CVaR was added to abstract first,
  missing from the contribution itemize + keywords until audited.)

## 6. Page-budget reality for conference variants

Adding a real contribution (here +4 equations, +1 table) pushes 8→9→10 pages. người dùng's call
this session: "không nén được thì kệ ... chỉ phình tài liệu tham khảo thì chắc không sao" — i.e.
keep the math, don't sacrifice scientific content to hit the page limit; ask before pushing
proofs/aux tables to an appendix. Bandwidth-as-matched-operating-point column in a results table
is a CONTROL, not a ranked metric — do NOT bold it; say so in the caption (bold-correctness).
