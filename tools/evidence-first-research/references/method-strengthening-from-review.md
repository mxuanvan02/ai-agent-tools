# Strengthening a method in response to reviewer critique (DERIVE-then-verify)

Reusable techniques that emerged while turning a peer-review critique into real
manuscript improvements (bài bandwidth-scheduling/hội nghị C1, greenhouse IoT scheduling). All numbers must
come from real runs on real data — never hardcode, never fabricate.

## 1. Replace a dead heuristic term with a theory-grounded one (VoU ← VoI)

Symptom: an ablation shows a "risk" term in a weighted-sum urgency/utility score is
**useless or harmful** (dropping it improves the objective AND the tail). Do not
force a "every term matters" story — that is dishonest and reviewers see through it.

Root cause pattern: a raw probability term like `w · p_vio` ranks an item highest
exactly when its decision value is LOWEST. When `p→1` the detector already fires, so
an extra measurement cannot CHANGE the decision → its value-of-information ≈ 0. Worse,
`p_vio` often double-counts a detector threshold already inside the loss (e.g. `p≥0.55`).

Fix (leading-order value-of-information for a binary decision):
- Replace `p` with **decision uncertainty** `g(p) = 4·p(1−p)` (scaled to [0,1]) or
  binary entropy `H(p)`. Both peak at the `p≈0.5` boundary and vanish once the outcome
  is certain. This is the Bayes-optimal leading-order VoI — defensible as a truncation
  of a Bayes-optimal object, matching người dùng's Q1 rigor bar (not a "thin heuristic").
- Verify on real data: in this session VoU cut objective −14%, missed-events −42%,
  tail CVaR −30% vs the raw-p heuristic, all at once. That is the signature of a
  correct term, not a tuned one.
- Bonus: a VoU/decision-uncertainty term that already appears in a SIBLING manuscript
  (e.g. bài AoI-greenhouse) is self-overlap risk. Add one sentence in related work distinguishing
  the two uses so both papers survive concurrent review.

## 2. Match the mechanism to the data regime before claiming it helps

A tail-risk mechanism (CVaR / Rockafellar–Uryasev, mean-variance) can ONLY help when
the data actually has a heavy tail. Repeatedly patching a tail mechanism that shows no
benefit is wasted effort — diagnose the DATA first.

- Light-tailed data (rare violations, e.g. a stable greenhouse replay) → CVaR adds only
  noise; it will tie or lose vs the plain expected-risk penalty. This is a real finding,
  not a bug. (Confirmed here across 5 attempts on greenhouse data.)
- Heavy-tailed data (real heat episodes: ERA5 Mekong 2024, >34 °C = 2–4 % of hours,
  peak ~38 °C) → CVaR cuts the loss tail with significance (−14 %/−12 %/−4 % across
  burst/severe/extreme, paired Wilcoxon p<0.05 on n=240). The mean-variance baseline
  does NOT cut the tail (p>0.7) — good evidence the CVaR machinery specifically targets
  the tail.
- Correct CVaR implementation notes (avoid the two bugs hit this session):
  - Estimate the VaR level ξ as the **empirical α-quantile of a trailing window** of the
    realized tail quantity. Do NOT drift ξ by raw subgradient — it collapses to 0 and the
    term degenerates to `loss/(1−α)`, just amplifying the mean.
  - Price only the **exceedance** `max(0, x − ξ)/(1−α)` of the PREDICTED-per-candidate
    quantity, added on top of the expected penalty.
  - A mean-variance term must use variance of the **predicted per-candidate** quantity,
    not variance of realized history (history is constant across candidates in the argmin
    → no effect → MV silently equals the base policy).
- Frame the honest trade-off: CVaR buys tail safety at a small mean-objective/bandwidth
  cost. That is the DEFINITION of CVaR, and a legitimate deployment knob for
  safety-critical systems — say so explicitly.

## 3. Reproducibility recovery: refetch, don't fabricate

If a manuscript reports results whose generating script/data were never committed
(only the final `.tex` table survives), treat it as a reproducibility defect, not a
dead end. Look for a `fetch_*.py` referencing a **public API** (here: Open-Meteo ERA5
archive `archive-api.open-meteo.com/v1/archive`) and refetch the real source by
coordinates/date. Data that is "lost" locally is often reproducible from a public
source. Never substitute fabricated numbers.

## 4. Scaling as a reviewer answer, and its honesty caveat

"N too small / not generalizable" is answerable by a synthetic scalability stress test
(replay real streams with independent circular time offsets + small per-zone biases,
recompute violations). Keep the real streams as anchor zones, label the extra zones
SYNTHETIC explicitly, and frame it as a stress test — never as additional real data.
Watch for the objective mechanically favoring the method as N grows (a per-unit
bandwidth cost makes full-polling scale linearly): report the safety metric (missed %)
alongside the objective so the win is not just an artifact of the cost weighting.

## Workflow discipline reused this session
- Backup manuscript+code to `_backups/<ts>/` before edits.
- One edit point in code (change the urgency form in exactly one branch; leave baselines
  untouched) then regen ALL dependent artifacts (tables, figures, Wilcoxon) from the CSV.
- Scripts that `import` the main simulator inherit the change automatically — verify which
  helper scripts re-implement the scoring vs import it, so the change propagates correctly.
- Report negative/inverted results to người dùng immediately with the numbers; let him choose
  the framing rather than silently picking a flattering story.
