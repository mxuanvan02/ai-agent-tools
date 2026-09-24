# Tail-risk (CVaR) method enhancement + sourcing real Vietnam data

When người dùng says "thử thêm xem", "nâng hàm lượng", or asks to test a risk-aware /
CVaR / tail-risk variant of a scheduling/allocation method on a **harder, real,
Vietnam-first** dataset (như bài bài AoI-greenhouse), this recipe applies. It is a specialization
of `method-enhancement-spike.md` for the *risk-aware* class, and it carries the single
most important lesson learned: **a tail-risk variant only helps if the target signal
has a non-degenerate tail — diagnose that BEFORE running, and pick the data + target
variable accordingly.**

## The core failure mode: zero-inflated target kills CVaR

First spike (bài bandwidth-scheduling-CVaR on per-slot *miss-rate*) was a clean negative result even at
matched bandwidth: tail CVaR did not improve (Δ≈+0.002, p=0.34), the variant just
bought more bandwidth. Root cause was NOT a bug — it was the signal:

- Per-slot miss-rate is **zero-inflated**: most slots are exactly 0, misses occur only
  in rare bursts. So the 90th percentile of the series ≈ 0, and the CVaR-0.9 constraint
  **degenerates into ~an expectation constraint on a rare event**. The mechanism adds
  no value; bài bandwidth-scheduling-PD's expectation constraint was already near-optimal for that signal.

Two principled corrections turned the negative into a real positive — note both are
*reformulations of the science*, not knob-tuning:

1. **Retarget to a continuous loss variable.** Move the tail constraint from the
   zero-inflated miss-rate onto the **per-slot composite control loss** `ℓ_t` (the
   continuous quantity whose predictor is the existing `\widehat{L}_t`). Continuous +
   bursty ⇒ non-degenerate tail ⇒ CVaR has something to bite on.
2. **Find data with a genuinely heavy tail** (next section). Synthetic Gilbert–Elliott
   miss events were too sparse; real diurnal+seasonal climate gave 18–21% threshold
   violations with burst run-lengths ~5–6 slots.

### Go/no-go GATE before any expensive run

Compute and print tail-structure diagnostics on the candidate dataset/target FIRST:
violation %, number of bursts, mean burst run-length. State the verdict explicitly,
e.g. "nonzero burst structure + double-digit violation% ⇒ per-slot risk is NOT
zero-inflated ⇒ CVaR tail constraint is non-degenerate." If the target is zero-inflated,
retarget the loss variable or fold the variant — do not run full N hoping it works.

## Sourcing real Vietnam data: Open-Meteo ERA5 Historical Archive

Zenodo / Mendeley / Kaggle searches for "Vietnam greenhouse/agriculture sensor dataset"
are thin and mostly irrelevant. The reliable, verifiable, downloadable source for
**real Vietnamese climate traces** is the Open-Meteo Historical Archive (ERA5 reanalysis):

- Endpoint: `https://archive-api.open-meteo.com/v1/archive` with `latitude`,
  `longitude`, `start_date`, `end_date`, and `hourly=temperature_2m,relative_humidity_2m`
  (add `,shortwave_radiation` etc. as needed). Returns hourly JSON.
- Pick Mekong-delta stations by coordinate: Cần Thơ (~10.03, 105.78), Sóc Trăng
  (~9.60, 105.97), Cà Mau (~9.18, 105.15). One full year (8784 hourly points) per
  station; treat multiple stations as multiple sensors.
- Provenance is **semi-real and MUST be declared**: control/violation dynamics are
  simulated *on top of* a real ERA5 weather trace (same pattern as dataset khí hậu VN in
  bài AoI-greenhouse). Say "real Vietnamese (ERA5 Mekong-delta) climate replay", never "field-
  measured". This satisfies người dùng's integrity bar and is defensible to reviewers.
- The Open-Meteo / arXiv / Crossref calls are plain-HTTP-ish and may trip the security
  scanner (HTTP-in-execution) — expect an approval prompt, it's fine to proceed.

## Confound control: matched operating point

To claim "smarter allocation" rather than "just spends more", **bind the shared resource
(bandwidth) hard for ALL policies with an identical dual step** so they sit at the same
realized operating point, then compare the tail/quality metrics. Re-run at 2–3 stronger
binding levels (e.g. BW_STEP 0.06/0.12/0.20) to show the win is robust to the operating
point, not an artifact of one setting. A variant that wins only by consuming more of the
shared resource is confounded — surface that honestly and fix the control before claiming.

## Fair risk-sensitive baseline (no straw-man)

Add a classical risk-sensitive reference (mean–variance / exponential-utility penalty),
not just the deployed mean-constraint policy. A good sign of fairness: the MV baseline
also beats the mean-constraint policy but lands **between** it and your CVaR variant —
proves the comparison is fair and your variant is the genuine winner, not a rigged field.

## VaR-tracker (Rockafellar–Uryasev) implementation notes

- CVaR_α(ℓ) = min_ξ [ ξ + 1/(1−α)·E[(ℓ−ξ)_+] ]. Coupling factor 1/(1−α) is FIXED by the
  identity (=10 at α=0.9), derivable not tuned.
- Online: dual ascent on λ over realized RU slack; quantile-tracker on ξ with subgradient
  `ξ_{t+1} = ξ_t + β·(1{ℓ_t>ξ_t} − (1−α))`. **Pitfall:** do NOT also divide the ξ step by
  (1−α) — that double-divides and miscalibrates the tracker. Stationary point gives
  P(ℓ_t>ξ)=1−α (H1 check: measured exceed-rate should ≈ 1−α; if it reads ~0.02 vs target
  0.10 the tracker is mis-stepped).
- Anchor c_tail to the deployed mean target so the comparison is a clean ablation
  (same nominal target, expectation- vs tail-constraint). α→0 recovers the mean
  constraint — state this as the degeneracy sanity anchor.

## Folding into a page-limited manuscript

- Merge the results table and the Wilcoxon p/effect table into ONE table (p/r as a
  trailing column) to save a float — page-limited venues care.
- **Bold-correctness for a matched operating-point column:** the matched-bandwidth
  column is a *control, not a ranked metric* — do NOT bold its min, and say so in the
  caption ("a control, not a ranked metric, and not marked"). Same rule as context-only
  (runtime) columns.
- New equations: tie any reused symbol back to its definition (e.g. `ℓ_t` ⇒ the loss
  whose predictor is `\widehat{L}_t`) to avoid clash with same-letter symbols elsewhere
  (here `ℓ_G,ℓ_B` were G–E channel loss-rates). Spell out CVaR/VaR at first use.
- A large new contribution must NOT be silent in the abstract — add one clause.
- Cite 2–3 recent (2024–2026) risk-sensitive scheduling papers fetched LIVE via Crossref
  and actually `\cite` them (in related work) — bib entries added but never cited are
  dead weight and waste the positioning research. Verify bbl: bibitems == unique cite keys.
- Packaging: exclude `.venv/` (a 15MB python-docx venv leaked into the bundle once) and
  build-from-bundle to confirm source reproduces, not just that a prebuilt PDF opens.
