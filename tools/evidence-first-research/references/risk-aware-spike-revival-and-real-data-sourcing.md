# Reviving a closed spike on a harder/realistic dataset + sourcing real VN data

When a method-enhancement spike CLOSES (no variant beats the deployed one), the
lever is not always dead — the **data regime** may be what killed it. This
reference captures a session where bài bandwidth-scheduling-CVaR (tail-risk constraint) first looked
useless, then won decisively once the dataset regime was right. Use it whenever
người dùng says "thử thêm xem", "chạy trên dữ liệu khó/thực tế hơn", or asks to
fold a risk-aware / CVaR / tail-aware variant into a paper.

## 1. Diagnose WHY a risk-aware spike failed before declaring it dead

A tail-risk (CVaR) constraint adds NO value when the risk signal is
**zero-inflated** — most slots are exactly 0, exceedances are rare bursts, so the
α-quantile (e.g. 90th pct) sits at ~0 and CVaR_α degenerates to ~the mean
constraint. Symptom in the spike: H1 tracker P(Z>ξ) far from target 1−α, ξ→~0,
H2 tail improvement Δ≈0 / not significant, and the variant only "wins" by
spending more bandwidth.

Two independent fixes, BOTH applied:
- **Reformulate the tail VARIABLE** to a continuous, non-zero-inflated quantity.
  Miss-rate (fn/(tp+fn)) is zero-inflated; per-slot CONTROL LOSS is continuous and
  spikes exactly during the burst episodes you care about. Constrain the tail of
  the continuous loss, not the sparse event indicator.
- **Find a HARDER, realistic dataset** whose tail is genuinely non-degenerate.
  Print a go/no-go tail diagnostic on the new data BEFORE running the full spike:
  violation %, burst count, mean run-length. Double-digit violation % + burst
  structure ⇒ tail is non-degenerate ⇒ CVaR is meaningful. State this explicitly.

Lesson: "spike closed" is conditional on the regime tested. A negative result on
zero-inflated synthetic data does NOT generalize to a heavy-tailed real regime.
Re-test on the right regime before folding OR before writing it off.

## 2. Matched-resource airtight comparison (kill the confound)

If a risk-aware variant wins but ALSO uses more of the constrained resource
(bandwidth, energy, budget), the win is confounded ("just spent more"). Force the
binding constraint EQUAL for all policies via the SAME dual machinery, then
compare. Then SWEEP the binding step-size at 2–3 strengths (e.g. BW_STEP
0.06/0.12/0.20) and confirm the win survives at matched operating point. Only
then is it "smarter allocation", not "more resource". Report the matched-bandwidth
deltas, not the free-bandwidth ones.

Include a FAIR risk-sensitive baseline (mean–variance / exponential-utility), not
just the deployed policy — if it lands BETWEEN deployed and your variant, that
proves the comparison isn't a straw-man and your variant is the genuine winner.

## 3. Sourcing real, verifiable Vietnam data (Open-Meteo ERA5)

When người dùng wants real VN data "sát thực tiễn" as evidence: Zenodo/Kaggle are
usually thin for VN agriculture. Open-Meteo Historical Archive (ERA5 reanalysis)
gives hourly temperature/humidity/radiation for arbitrary lat/lon over full years,
free, with explicit provenance you can declare. Pick real ĐBSCL stations (Cần Thơ,
Sóc Trăng, Cà Mau) → multiple stations act as multiple sensors. Declare honestly:
"semi-real" = control/comms simulated over a real climate trace (same shape as the
dataset khí hậu VN in bài AoI-greenhouse but real + longer). Verify n, min/max ranges after download.

## 4. Folding the variant in: equation-linkage discipline (người dùng's core ask)

When folding the variant into the manuscript, người dùng wants every formula LINKED by
explicit derivation, not dropped in as a standalone block. Checklist that passed:
- Show the new objective is the OLD one with one term SUBSTITUTED. Here
  J_t^CVaR = J_t with the expected-risk term (c_M+λ^M)M̂_t replaced by the predicted
  tail penalty. Write that equation (`eq:Jcvar`) explicitly and `\eqref` it.
- Chain the derivation: constraint (CVaR≤c) → Rockafellar–Uryasev identity
  (min_ξ φ(ξ)) → substitute into J_t → two coupled projected-subgradient updates
  (dual ascent on slack + ξ = VaR-tracker subgradient ∂φ/∂ξ). Each step "suy ra"
  from the previous, with ⩾/= shown (CVaR_α ≥ E[ℓ] ⇒ α→0 recovers the mean
  constraint = the deployed policy is a special case).
- Anchor every constant as derivable: 1/(1−α) fixed by the RU identity; reuse the
  deployed step (α_λ=β=α_M) so "no new tuned rate".
- **Every symbol in an Algorithm/objective MUST have a defining equation.** Audit
  caught p_t^bad used in the risk score + Algorithm but never defined — added its
  EWMA update eq (matching code: 0.85·p + 0.15·1_loss − 0.05·1_succ, clip
  [0.01,0.99]) and cited it from the algorithm line.
- Tie the variant back to the Algorithm in words: "bài bandwidth-scheduling-CVaR is Algorithm 1 with
  J_t→J_t^CVaR in line 5 and the miss dual replaced by the coupled updates in line
  8; all other steps unchanged."
- Orphan-label audit: grep all `\label{eq:` vs all `\eqref` — every new equation
  must be referenced somewhere (caption, prose, or algorithm). Note: labels inside
  a range ref `\eqref{eq:A}--\eqref{eq:C}` show as "unused" in a naive grep but are
  fine; only truly-unreferenced labels need a pointer added.
- Sync coherence across the whole paper: contribution list in Intro, keywords,
  abstract must all mention the new variant (method-name coherence). Adding it to
  the method/eval but leaving it out of contributions/keywords is the classic gap.

## 5. Page-limit reality when math is the addition

Adding genuine equations (4 here) pushes page count and prose-condensation +
table-merging won't claw it back — that's content, not whitespace. Surface the
trade-off and let người dùng decide (he chose "kệ, phình refs thì không sao"). Don't
silently cram layout (linespread/bib-spacing) past professional density to hide
real new content.
