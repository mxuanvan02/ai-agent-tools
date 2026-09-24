# Method-enhancement spike: validate a method change BEFORE touching the manuscript

Precedent: bài probe-transmit / bài AoI-greenhouse, session 2026-06-19. Người dùng asked whether the
proposed algorithm had enough scientific depth for Q1, and proposed enhancing the
probe stage. The right move was a throwaway spike, not editing the paper.

## Workflow that worked

1. **Diagnose depth honestly first.** Strip the method to primitives; if it is a
   linear combination of known terms + top-k, say "incremental combination". Find
   the real contribution (here: the two-stage probe-then-transmit *formulation*,
   which the 2024–2026 literature had NOT formalized).
2. **Fan-out literature search** (3 parallel subagents): semantic/AoII scheduling,
   submodular active sensing, multi-action RMAB indexability. Each returns ranked
   papers with arXiv IDs + the specific guarantee proven. This located two proof
   routes (submodular (1-1/e); asymptotic optimality without indexability).
3. **Delegate a deep read** of the 1–2 foundational papers (here arXiv 2409.03541
   Crowley-Esnaola, 2606.10192 Dutta survey) to a background subagent, asking for a
   PROVEN-vs-INFERENCE brief with section/equation citations.
4. **Backup + implement as a new opt-in mode**, never overwrite the deployed path.
   Backup to `_backups/new_algorithm.py.<timestamp>`. Add the new objective behind a
   flag (`credit_mode="submodular_info"`) so the existing smoke tests still pass.
5. **Spike on real data before believing the theory.** Write a throwaway
   `scripts/spike_*.py` comparing variants (debt_only / old-corr / new) across ALL
   datasets, holding everything else identical. Run a 3-window smoke FIRST to catch
   bugs, then decide whether the full 30-window run is even worth it.

## The key scientific lesson (provable ≠ better)

The information-gain objective `J(S)=½logdet(I+Σ_SS/σ²_meta)` IS provably monotone
submodular (greedy 1-1/e), but in the spike it was **16× WORSE** on Intel. Reason:
pure information/variance maximization **discards the safety/threshold term** —
it becomes max-variance probing, which the paper had ALREADY shown is weak
(VoI-greedy). There is a real tension:

- The objective that is *provably submodular* (information gain) does NOT serve the
  safety objective.
- The objective that *serves safety well* (VoU-weighted / summed-variance credit) is
  NOT submodular (it is the trace-of-error-covariance family — non-submodular per
  Dutta survey Table 4).
- Danger-gating/thresholding inside the objective breaks submodularity, so you
  cannot naively bolt safety onto the provable objective. Keep danger as a
  ground-set feasibility filter, not a utility transform — but a near-empty filter
  (most nodes mid-band, p_vio≈0) falls back to the full set and loses the safety focus.

Takeaway: an approximation guarantee is only worth claiming if the guaranteed
objective is the one you actually care about. Verify with a spike; do not assume a
theoretically clean reformulation improves the target metric.

## CRITICAL: 3-window smoke results reverse at full N — never report from the smoke

The 3-window smoke looked dramatic: old corr-credit beat debt-only ×0.31 on Intel,
and a "safety-restricted submodular" variant looked promising. Running the **full
30-window** run with a **paired Wilcoxon** test REVERSED both conclusions:

| Dataset | debt_only (best) | corr_variance | Wilcoxon p |
|---|---|---|---|
| Intel  | 0.00247 | 0.00272 (×1.10 WORSE) | 0.87 |
| Beijing| 0.09379 | 0.09859 (×1.05 WORSE) | 0.56 |
| KETI   | 0.00719 | 0.00739 (×1.03 WORSE) | 0.89 |

So corr_variance did NOT beat debt-only anywhere significantly — it was marginally
worse on average. The 3-window "win" was pure small-sample noise. **Lesson: a 3-window
smoke is for catching bugs, NOT for drawing conclusions. Always run the full N (here
30 windows) AND a paired significance test (Wilcoxon on per-window deltas) before
telling người dùng a component "wins" or "is worth reviving."** Add the Wilcoxon to the
spike script itself so the verdict comes with wins/losses/p, not just a mean ratio.

## Outcome: dropping the component was correct — confirmed with evidence

This run confirmed người dùng's earlier decision to drop correlation-credit was RIGHT:
debt-only is the best deployed configuration, and NO probe-stage enhancement (corr,
submodular info, safety-restricted submodular) beat it significantly. The honest
conclusion: the probe-algorithm lever for novelty is closed; the remaining Q1 lever
is theory (asymptotic-optimality / RMAB-style guarantee tied to the deployed rule),
not adding probe machinery. When a spike closes a direction, say so plainly and pivot
to the theory route rather than forcing a marginal empirical gain into the manuscript.

## SECOND CONFIRMED INSTANCE (2026-06-19, same session, predictive VoU)

Người dùng asked to add mathematical depth by turning VoU from *confirming* a current
violation into *predicting* a future one. Implemented two real, citable pieces of
math behind an opt-in flag (`use_first_passage`): (1) a damped local-linear-trend
Kalman forecaster (`LocalLinearTrendModel`) replacing mean-reverting AR(1), and
(2) a closed-form first-passage / boundary-crossing probability (Bachelier-Lévy /
inverse-Gaussian) replacing the point-in-time exit probability. A 4-arm ablation
(AR1/LLT × confirm/first-passage) isolated each ingredient.

Two patterns from above REPEATED, confirming they are rules not flukes:

- **3-window reversal struck again.** Smoke (3 win): `LLT+confirm` looked like a
  huge win (loss ×0.36 vs current). Full 30-window REVERSED it: `LLT+confirm` ×1.86
  WORSE, and the full predictive proposal `LLT+first-passage` ×2.29 WORSE, losing on
  Wilcoxon (12/30, p=0.015) and much worse on missed-violation safety (2/30 safer,
  p=0.004). The 3-window "win" was again pure small-sample noise.
- **Trend/correlation/information features all die on near-stationary fields.** Same
  root cause as the corr-credit and submodular-info failures: Intel/KETI/Beijing are
  slow-moving near-uniform fields with little exploitable drift, so a momentum model
  has nothing to extract. When a benchmark field is near-stationary, be skeptical of
  ANY feature whose value comes from trend/spatial-structure; expect it to add noise,
  not signal. Verify with a 30-window spike before claiming depth.

New specific lesson — **closed-form first-passage is an upper bound, so it
over-triggers.** Because it conservatively counts crossings at ANY step in the
horizon, it raises P_danger across the board → over-probes/over-transmits → wastes
budget → loss UP, and missed-violation did NOT improve. A "safety-favouring" bound
is not free: in a budget-constrained scheduler it manifests as false alarms.

Meta-lesson for "add math for Q1": adding genuinely sophisticated, citable math
(state-space Kalman + analytic hitting-time law) does NOT automatically raise a
paper's quality if it fails to improve the target metric on the available data.
Forcing it in is overclaim — a reviewer who reruns will see it lose to your own
baseline. Keep it as a documented negative result ("we tried trend-aware
first-passage; it did not improve on near-stationary fields") and put the Q1 depth
where the evidence supports it (here: the per-arm-channel win + asymptotic-optimality
theory). Tell người dùng plainly, offer the choice (bank the win / try to salvage /
seek a field where it could work) rather than silently dropping or silently shipping.

Counterweight — the spike-gate discipline also WORKED this session. The per-arm
channel model change was gated by a decisive 30-window spike BEFORE the expensive
full re-run: bài AoI-greenhouse's advantage over channel-blind baselines widened to ×3–5.3 with
every Wilcoxon p<0.025. That positive spike justified the model change with evidence;
the negative predictive-VoU spike prevented a bad change. Same tool, both directions.

## THIRD CONFIRMED INSTANCE (2026-06-20, Autoencoder + AoI vs VoU)

Người dùng proposed his own idea: "thay vì dùng VoU, ta sẽ dùng Autoencoder + AoI thì
sao" — then "thử triển khai cả 2" (try BOTH a replacement branch and a synergy
branch). Workflow that worked and the honest verdict:

**Pre-analysis BEFORE coding (predict the outcome from existing evidence).** Before
writing anything, I told người dùng plainly that AE+AoI is the "freshness +
novelty/uncertainty" family with NO safety-threshold term, so it would likely lose —
and pointed at the paper's own §4 where VoI-greedy (posterior-variance reduction ≈ AE
novelty) already trails ×33. This sets honest expectations and frames the spike as
hypothesis-testing, not a fishing trip. Người dùng values this: lead with the predicted
answer, then prove it.

**Branch 1 (AE+AoI REPLACES VoU).** Built `AEAoIProbe` policy (sklearn MLP autoencoder
recon-error + AoI, channel-weighted, NO threshold term) through the SAME `run_window`
harness, 8-window Intel + KETI, vs bài AoI-greenhouse. Result:

| Policy | Intel ×VoU | KETI ×VoU |
|---|---|---|
| bài AoI-greenhouse (ours) | 1.00× | 1.00× |
| AE+AoI (replace) | 3.88× WORSE | 0.94× (tie) |
| AE-only (recon) | 22.1× WORSE | 1.56× WORSE |
| AoI-only | 2.85× WORSE | 0.94× (tie) |

**Branch 2 (AE multivariate forecaster FEEDS VoU).** MLP predicting x(t+h) from the
full panel vector (exploit spatial correlation) vs per-arm AR(1), 4-step RMSE:

| Dataset | AR(1) | AE-MLP | ratio | AE wins |
|---|---|---|---|---|
| Intel | 0.178 | 1.692 | 9.5× WORSE | 0/30 sensors |
| KETI | 0.161 | 0.690 | 4.3× WORSE | 0/40 sensors |

**New specific lessons (AE family):**
- **Reconstruction error ≠ safety value.** AE-only was catastrophic (22× on Intel)
  because recon-error captures *statistical anomaly*, not *proximity to a safety
  threshold*. A node can be perfectly "normal" to the AE yet sitting at the boundary.
  This is the precise mechanism behind why novelty/uncertainty objectives fail the
  safety metric — same root cause as submodular-info and max-variance probing.
- **Decompose a tied/near-tie win to find who actually contributed.** On KETI, AE+AoI
  "won" 0.94× — but AoI-only ALSO scored 0.94×, proving the AE component added
  NOTHING; the entire effect was AoI. Always run the single-component ablations
  (AE-only, AoI-only) alongside the combined policy so a tie isn't misread as the new
  component working. On a near-uniform field (KETI band 21–26°C, high eff-rank),
  round-robin-by-age is already near-optimal and VoU has no spread to exploit — so
  freshness-only ≈ VoU. Report this as a REGIME boundary, not a win.
- **Spatial/multivariate forecasters die on near-stationary fields too** — the SAME
  killer as trend (LLT), correlation-credit, and submodular-info. With α≈0.9998 the
  per-arm dynamics dominate and cross-sensor structure is too weak to beat AR(1); the
  MLP just overfits and adds noise (0/N sensors improved on BOTH datasets). This is
  now the FOURTH feature family (trend, correlation, information-gain, AE/spatial) to
  fail for the identical reason. Default expectation on these near-stationary
  benchmark fields: ANY feature whose value comes from trend or spatial structure or
  reconstruction-novelty will add noise, not signal. Predict it, then confirm with a
  spike.

**Outcome / how to bank it.** Both branches are honest negative results that
STRENGTHEN the paper: propose adding AE+AoI and AE-only as new §4 baselines (run full
30-window for the table) plus a one-paragraph "why reconstruction error ≠ safety
value" discussion, and state the KETI regime boundary explicitly (freshness ≈ VoU on
near-uniform fields; VoU wins when the field has exploitable danger structure).
Reviewers like a paper that pre-empts the obvious "did you try an autoencoder?"
question with measured evidence. Offer người dùng the choice (promote to baselines vs
keep as internal spike) rather than silently doing either.

## FOURTH CONFIRMED INSTANCE (2026-06-26, bài bandwidth-scheduling CVaR / tail-risk constraint)

Người dùng asked to raise scientific depth on bài bandwidth-scheduling by replacing the **expected**
miss-rate constraint of bài bandwidth-scheduling-PD with a **CVaR (tail-risk)** constraint
(Rockafellar–Uryasev), constant `1/(1-α)=10` derived not tuned, on a clone
(`bài bandwidth-scheduling_branchB_clone`, code+data only, never the manuscript). Derivation written to
`docs/rabs_cvar_derivation.md` BEFORE coding (người dùng's DERIVE-then-verify). Verdict:
**fold** — the tail constraint did not beat the mean constraint, confirmed by 640
paired runs + Wilcoxon. Two new, reusable techniques emerged:

**TECHNIQUE 1 — matched-resource control: never let a candidate "win" by spending
more.** First spike ran CVaR with *free* bandwidth: it scored worse on the composite
objective AND used more budget (B̄=2.03 vs PD 1.51, p≈1e-106). That comparison is
CONFOUNDED — you cannot tell whether CVaR allocates smarter or just buys more
resource. The scientifically honest test is to **bind the shared resource equally for
both arms** (here: a strong, identical bandwidth dual step `BW_STEP` driving both
policies to the same B̄≈B_TARGET), THEN compare the tail metric at matched cost. Only
a matched-resource comparison isolates "smarter allocation" from "spend more". Even
after matching, CVaR still drifted to B̄=1.66 vs 1.51 and gained only Δ=−0.003 on the
tail (p=0.007, negligible) while losing the composite (r=−0.82). Rule: whenever a
candidate method touches the resource/budget knob, equalize that knob across arms
before believing any quality delta — apply the SAME dual/penalty machinery to both,
not a handicap on one.

**TECHNIQUE 2 — zero-inflated signals make CVaR/tail constraints DEGENERATE to the
mean.** Root-cause diagnosis (not another patch): the per-slot miss-rate signal is
**zero-inflated** — most slots are exactly 0, misses occur only in rare bursts. So
the 90th percentile of the series is ≈0, and a CVaR-0.9 constraint collapses onto
roughly an expectation constraint over the rare tail. The H1 quantile-tracker
confirmed it: P(Z>ξ)=0.027 ≠ target 0.10, ξ→0.007. The CVaR mechanism adds no value
when the constrained quantity is sparse/zero-inflated — there is no dense tail to
shape. General rule: before proposing CVaR / VaR / tail-risk / quantile constraints,
CHECK the signal's sparsity. If P(signal>0) ≪ (1−α), the tail sits in the zero mass
and the tail constraint ≈ the mean constraint → no novelty, only extra cost. The
honest conclusion ("bài bandwidth-scheduling-PD's expectation constraint is already near-optimal for this
sparse safety signal") is itself a Q1-worthy finding. Note a candidate fix worth one
last spike before fully folding: redefine the tail on a CONTINUOUS, non-zero-inflated
per-slot quantity (e.g. control-tracking loss, which spikes exactly during loss
bursts) instead of the binary/sparse miss-rate — that changes the OBJECTIVE VARIABLE
(principled), not a knob (tuning). Offer người dùng the (a) ship-A-fold-B vs (b)
one-more-spike-on-continuous-tail choice rather than deciding unilaterally.

**Tracker calibration pitfall.** The Rockafellar–Uryasev quantile-tracker subgradient
step is `ξ ← ξ + β·[1{Z>ξ} − (1−α)]`. Do NOT also divide the step by `(1−α)` — that
double-counts the level and miscalibrates the tracker (symptom: exceed-rate far below
target). The `1/(1−α)` factor belongs in the CVaR *penalty* `ξ + 1/(1−α)·[Z−ξ]₊`, not
in the tracker step.

## Environment note (AE/forecaster specifics)

No `torch` in the bài probe-transmit venv — use `sklearn.neural_network.MLPRegressor`
for autoencoders/forecasters (bottleneck hidden layer for an AE; denoising = fit on
noise-added inputs to clean targets). `ConvergenceWarning` at max_iter is benign for
a spike. Pyright flags numpy/sklearn imports as unresolved in this venv — false
positive, ignore.


bài probe-transmit repo needs its own venv (the active python lacked numpy):
`uv venv .venv --python 3.11 && .venv/bin/python -m ensurepip && .venv/bin/python -m pip install -q numpy scipy pandas matplotlib`.
Data panels: `data/raw/intel_berkeley/*.npy`, `data/raw/_candidates/{beijing_prsa,keti_smartbuilding}/*.npy`.
Beijing/KETI use a data-driven [2.5,97.5] percentile safe band; Intel uses fixed [18,32].
