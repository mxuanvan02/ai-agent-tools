# Folding a tail-risk (CVaR) variant into a scheduling/control paper

When người dùng says "thử thêm CVaR / risk-aware", "chạy trên dữ liệu khó/thực tế VN",
or "nâng hàm lượng" for a scheduler whose deployed cost constrains an *expectation*,
the natural Q1-grade lift is a **tail (CVaR) constraint** replacing the mean
constraint. This file is the proven recipe + the pitfalls that actually bit.

## The fold-in math (Rockafellar–Uryasev), derive BEFORE running
- Replace `E[ℓ] ≤ c` by `CVaR_α(ℓ) ≤ c_tail`. Since `CVaR_α ≥ E[ℓ]`, the mean
  constraint is the `α→0` limit ⇒ the deployed policy is a special case (sanity anchor).
- RU identity: `CVaR_α(ℓ)=min_ξ ξ + 1/(1-α)·E[(ℓ-ξ)_+]`, minimizer `ξ*=VaR_α`.
- Two coupled projected-subgradient updates: dual ascent on the constraint slack
  (λ), and a quantile tracker `ξ_{t+1}=ξ_t+β/(1-α)·(1{ℓ_t>ξ_t}-(1-α))` whose
  stationary point gives `P(ℓ>ξ)=1-α` ⇒ ξ→VaR_α (threshold LEARNED, not tuned).
- **Constants must be derivable, not hand-tuned**: coupling `1/(1-α)` is fixed by
  RU; reuse the deployed step (`α_λ=β=α_M`) so the variant "adds no new rate" —
  this makes it a clean ablation. Boundedness of λ reuses the same drift/telescoping
  argument as the existing feasibility proposition (ℓ,ξ∈[0,1]).
- Write `docs/<proj>_cvar_derivation.md` FIRST (math fixed before any expensive run),
  list falsifiable H1 (tracker calibration P(ℓ>ξ)≈1-α), H2 (payoff at matched
  bandwidth), H3 (α→0 degeneracy). Win-or-fold by evidence.

## PITFALL 1 — zero-inflated tail variable makes CVaR degenerate (kills the idea)
First spike constrained CVaR of **per-slot miss-rate**, which is zero-inflated
(most slots = 0, misses are rare bursts). The 90th-percentile of a mostly-zero
series ≈ 0, so CVaR_0.9 collapses to ≈ a mean constraint — CVaR adds NO value and
just buys more bandwidth. Verdict was fold (negative).
**Fix that rescued it:** put the tail constraint on a **continuous** per-slot loss
(control/tracking loss `ℓ_t`, the thing `L̂_t` predicts), which spikes during the
hard episodes and has a genuine heavy tail. Diagnose tail health BEFORE running:
print violation% + burst run-length; "double-digit violation% + nonzero burst
structure ⇒ non-degenerate tail ⇒ CVaR is meaningful". If the candidate tail
variable is zero-inflated, switch variables or fold.

## PITFALL 2 — "wins" may just be "spends more bandwidth" (confound)
A risk-aware variant left free will buy extra budget (e.g. B̄ 1.51→2.03) and "win"
trivially. The honest test is **matched operating point**: bind the bandwidth dual
HARD and IDENTICALLY on all policies (~B_target), then ask whether the variant
allocates a *fixed* budget smarter. Re-run at several bw-dual strengths (e.g.
0.06/0.12/0.20) and show the win survives → not "spending more". Add a fair
risk-sensitive baseline (mean–variance / exponential-utility) that is NOT a straw
man — it should land BETWEEN the deployed policy and CVaR, proving the comparison
is fair and tail-shaping (not generic second-moment shaping) is what helps.

## PITFALL 3 — bold/no-bold for a matched operating-point column
When bandwidth is the *matched control* (not a ranked win metric), do NOT bold the
"lowest bandwidth" cell — bolding it misreads as a win. Caption: "Avg. Bw. is the
realized/matched operating point (reported for context, not marked)". Same family
as the runtime-context-only rule.

## PITFALL 4 — changing DATASET (not N) can flip the main narrative
Switching the eval to harder real data (here VN ERA5 Mekong-delta, violations
18–21%) flipped the headline: high-budget Fixed-B3 now BEATS the proposed policy on
the composite objective (frequent violations ⇒ full polling genuinely pays off).
This is the dataset analogue of the N-scaling regime flip. Response that người dùng
endorsed (do NOT fudge weights to win back):
- STOP and report the flip with verified numbers before writing prose.
- Offer framing choices; he chose **keep the two datasets separate** — original
  dataset for the SoTA/baseline comparison (where the method competes on objective),
  the hard real-data set declared as a **separate hard-regime case study** for the
  new variant. Two datasets, transparently labelled, beats one forced-uniform table.
- The new variant's claim still holds at matched bandwidth and *grows with tail
  severity* (marginal on mild channel p≈0.20, significant on severe p≈0.006, strong
  on extreme p<1e-3) — report the gradient honestly; it's a stronger story than a
  flat "wins everywhere".

## Real VN climate data (verifiable, downloadable)
Open-Meteo Historical Archive (ERA5 reanalysis) gives real hourly temp+RH for any
lat/lon — used Can Tho / Soc Trang / Ca Mau (ĐBSCL), full-year hourly (~8784 pts ×
3 stations). Declare as semi-real: real climate trace driving a simulated control
loop (same spirit as dataset khí hậu VN, but real + longer). Three stations → three
sensors. Always state provenance (source, coords, year) — never call it field-measured.

## Mechanics that recur
- Spike/clone work lives in a separate `<proj>_branchB_clone/` (NOT a git repo,
  NOT the manuscript dir); manuscript stays untouched until win confirmed.
- scipy/numpy live in the project venv (`_repos/<proj>/.venv`), NOT in execute_code's
  sandbox — run stats scripts via that venv in terminal.
- Generate every results table from ONE CSV via a script (`make_*_table.py`) that
  computes mean + paired Wilcoxon; never retype numbers. Bold = best per ranked
  column only.
- Fold into manuscript: derive eq → tie new symbols to existing labelled eqs
  (`\eqref`), add J^variant showing it IS the deployed cost with one term swapped,
  cite the variant back into the algorithm ("Alg. X with J→J^variant in line 5,
  dual→coupled updates in line 8"). Spell out acronym at first use, add to keywords
  + contribution list + abstract (method-name coherence). Verify cites live
  (Crossref/arXiv), build full chain + build-from-bundle, then package.
