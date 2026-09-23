# bài bandwidth-scheduling code-vs-manuscript integrity and N-scaling pitfall

Use this when working on bài bandwidth-scheduling / adaptive bandwidth scheduling manuscripts or slides, especially if the text, algorithm box, or setup disagrees with the code outputs.

## Core lesson

For bài bandwidth-scheduling, the **code + CSV outputs are the source of truth** for any reported result. Do not trust the manuscript text, algorithm box, or slide numbers if they diverge from the simulator. In the session that produced this note, the manuscript had drifted from code in several high-impact ways:

- Manuscript claimed `N=30`; code/data used **3 measured zones** (`loop ∈ {0,1,2}`, `range(3)`).
- Manuscript claimed safety band `18–28°C`; code and labels used **`22–30°C`**.
- Manuscript Algorithm 1 showed a **single-dual benefit-minus-eta** rule; code used a **3-dual deployed variant** with bandwidth/AoI/missed-risk feedback and `argmin` of predicted candidate cost.
- Manuscript said `T=999`; code windows were **1000 slots**.

The fix was not to make the code fit stale prose. The user explicitly asked to keep the newest/best variant as the main one; the evidence was that all reported tables/figures were reproduced from the code, so the code was canonical.

## Algorithm reconciliation checklist

When auditing bài bandwidth-scheduling Algorithm 1 against code:

1. Read `run_rabs_adaptive_bandwidth.py`, especially:
   - `choose_B_rabs_family`
   - `predict_candidate`
   - `run_fixed` dual updates
   - `SAFE_MIN, SAFE_MAX`, `NETWORKS`, `SEEDS`, window length.
2. Verify the manuscript algorithm matches the deployed variant:
   - Candidate budgets: `{1,2,3}` for the N=3 replay.
   - Cost form:
     `J_t(b)=Lhat_t(b)+(c_B+λ_B)b+(c_A+λ_A)Ahat_t(b)+(c_M+λ_M)Mhat_t(b)-c_R R_t b`.
   - Selection is `argmin_b J_t(b)`, not `argmax benefit`.
   - Updates:
     - `λ_B ← [λ_B + 0.010(B_t-1.55)]_+`
     - `λ_A ← [λ_A + 0.006(mean_aoi-1.60)]_+`
     - `λ_M ← [λ_M + 0.020(miss_rate-0.008)]_+`
3. Frame theory carefully: the clean telescoping proof applies to the **bandwidth-dual component**, not to a full global optimality guarantee for the 3-dual heuristic.

## N=30 scaling pitfall

Do not silently inflate the dataset from 3 measured zones to `N=30` just because the manuscript says N=30. The underlying data only has 3 measured traces. If the user asks to try N=30:

1. State clearly that N=30 must be **semi-synthetic/virtualized** unless a real 30-zone dataset exists.
2. If simulating N=30, run a smoke only for bug detection, then run the **full paired design** before changing the paper narrative. Smoke results are not evidence.
3. In the observed full N=30 run (`n=320`), the bài bandwidth-scheduling-PD thesis failed: Max-AoI and Fixed-B3 dominated bài bandwidth-scheduling-PD with extremely significant Wilcoxon deltas. The cause was a regime shift: under heavy under-observation, tracking/AoI dominated and the risk signal was saturated.
4. The final user decision was to revert to the honest N=3 framing (C3 in the session): **three measured greenhouse zones**, no dense-field `B_t << N` claim.

## Manuscript/setup patch pattern

When reverting to honest bài bandwidth-scheduling framing:

- Write `N=3 measured temperature zones`, not `N=30 sensors`.
- Remove `B_t << N`; say budgets `{1,2,3}` are operational modes from minimum bandwidth to polling all measured zones.
- Use safety band `[22,30]°C`.
- Use `16 windows × 20 seeds = n=320`, `1000 slots/window`.
- Include grouped simulation table: Dataset / Safety / Scheduler / Channel.
- Channel params from code:
  - Burst G–E `(ℓ_G,p_gb,ℓ_B,p_bg)=(0.06,0.035,0.65,0.22)`
  - Severe burst `(0.08,0.055,0.82,0.15)`

## Slide-specific lessons

- bài bandwidth-scheduling had no existing slide deck; creating a class-consistent Beamer deck was appropriate, but it must carry the honest N=3 limitation prominently.
- bài AoI-greenhouse slide decks can retain stale manuscript numbers even after the paper is fixed. Audit slide sources with grep for stale numeric anchors (`0.0024`, `0.0128`, `96%`, `78%`, `corr`, `Value of Urgency`) and regenerate figures from the fresh CSV.
- Build success is not enough for slides. Render the key slide pages and vision-check:
  - numbers are readable,
  - figures are not clipped,
  - labels do not overlap,
  - a plot shrunk into a slide still has legible axes/values.
- If a multi-panel figure is too small, prefer horizontal bars with direct labels over cramped subplots.
