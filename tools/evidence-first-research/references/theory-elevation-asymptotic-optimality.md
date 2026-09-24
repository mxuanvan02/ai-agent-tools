# Theory-elevation route: proving a deployed scheduling rule is asymptotically optimal

Precedent: bài probe-transmit / bài AoI-greenhouse, session 2026-06-19 (continuation). After the
empirical spike closed the probe-enhancement lever (see
`method-enhancement-spike.md`), the remaining Q1 lever was THEORY: prove the
*already-deployed* rule `Index_i = p_succ·VoU_i + w_debt·D_i; top-B` is
asymptotically near-optimal, turning a heuristic into a provably-good scheduler.
This file captures how to run that route without overclaiming or accidentally
proposing a new artifact.

## When to use

Người dùng wants to raise scientific content to Q1 and the method is an
incremental-combination scheduler (linear index + top-k) whose empirical lever is
exhausted. The goal is a guarantee tied to the rule that ALREADY RUNS, not a new
algorithm. Typical for RMAB / scheduling / AoI / remote-estimation work.

## Workflow that worked

1. **Frame it as "proof layer", not "new architecture" — and SAY SO.** Người dùng
   asked point-blank "khác hoàn toàn [project] cũ hả?" (is this a totally new
   architecture?). The honest answer is NO: you are not changing the algorithm,
   only proving a property of it. State this explicitly and early, or the user
   reasonably fears you are quietly redesigning their paper. Use the framing:
   "máy chạy tốt sẵn, agent chỉ chứng minh nó tối ưu — máy không đổi."
2. **Map the deployed rule to a standard RMAB formulation.** Arm = sensor; state =
   (belief μ,σ² + age/deficit + any channel mode); action ∈ {0,1}; budget B of N;
   reward = −expected loss. Write the transition kernel from the actual model
   (AR(1)+Kalman predict/update, age reset on success).
3. **Fan-out / delegate a deep read of 2-3 candidate theorem papers** asking for
   PROVEN-vs-INFERENCE briefs with exact theorem/equation/page citations. For
   safety-monitoring scheduling the strong fits found were:
   - arXiv 2507.09833 (Ornee-Shisher-Sun, Remote Safety Monitoring): Maximum-Gain-
     First top-B index policy, asymmetric safety loss, **avoids indexability**,
     asymptotically optimal **under UGAP** (global attractor — ASSUMED not proven).
     Closest structural match to a VoU = tracking-error + violation-prob rule.
   - arXiv 2402.05689 (Hong-Xie-Chen-Wang): focus-set / set-expansion policies are
     **O(1/√N)**-optimal under ONLY aperiodic-unichain (Assumption 1) — NO GAP/UGAP,
     NO indexability, NO non-degeneracy. The only route with a finite-N RATE. BUT
     the guarantee is for focus-set policies, not a raw top-B index rule (a raw
     index rule is LP-priority and still needs GAP).
   - arXiv 2404.16281 (Shisher-Sun-Hou): dummy-bandit + Lagrangian-dual to handle
     budget + a second constraint; but REQUIRES proving indexability (Thm 9) —
     usually intractable for a belief+age arm, so avoid as the primary vehicle.

## CRITICAL: verify each theorem assumption against the ACTUAL SIMULATOR CODE

Do this BEFORE writing the theorem. The math papers assume things your code may
violate. Read the simulator/channel/policy source and check each:

- **Arm independence.** RMAB theory assumes arms are independent given the policy.
  In this precedent, reading `simulator.py` revealed a SINGLE shared channel state
  (`bad` scalar) and a SINGLE shared `pi_bad` belief used by ALL N sensors in a
  slot → arms are NOT independent → the entire theorem collapses. This was invisible
  from the math; only the code showed it. ALWAYS read the delivery/channel loop.
- **Bounded vs unbounded state.** A bounded deficit D_i∈[0,1] keeps the per-arm
  state finite (theorem-friendly). An *accumulating* age-of-service debt grows
  without bound → infinite state → breaks the finite-S premise of all three papers.
  Restrict the theorem to the bounded-deficit variant. Bonus: this gives a clean
  division of labor — an accumulating-debt term powers a separate no-starvation
  bound (service-gap theorem), while the bounded variant powers asymptotic
  optimality. Two regimes, two guarantees, no conflict.
- **Finite vs continuous state.** Continuous Kalman belief (μ,σ²) needs quantization
  to a finite grid to apply finite-S theorems; flag this as a stated step.
- **Reward continuity.** A hard safety indicator `I(xh safe)` makes the reward
  discontinuous in the belief mean → fine on a discretized state (just a reward
  table) but breaks any continuous-state rate argument. Flag it.
- **UGAP / global attractor.** Both Sun-group theorems ASSUME it; they do not prove
  it, and it can genuinely fail (Weber-Weiss counterexamples), especially with
  bursty/correlated channels. Do not claim it holds — claim conditionally and
  support empirically (show mean-field convergence in the existing simulation).
- **Heuristic index ≠ exact gain index.** The deployed `p_succ·VoU + w_debt·D` is a
  hand-designed linear form, not the exact `Q(s,0)−Q(s,1)`. State the theorem for
  the gain-index policy and validate empirically that the heuristic induces the
  same ordering, OR redeploy the gain index.

## Surface scope changes and re-run cost BEFORE acting

When the assumption check forces a model change, do NOT silently change it.
Example: fixing arm-independence by giving each sensor an independent channel
("hướng A") makes the theorem apply cleanly BUT (a) makes the model LESS realistic
(a real 1-gateway/1-radio system genuinely shares the channel) and (b) forces
re-running EVERY experiment (all datasets × baselines × windows), changing every
number in the manuscript. Present the trade-off as a table and offer the cheaper
alternative: keep the realistic shared-channel experiments, state the theorem for
the independent-channel regime as a sufficient-condition abstraction, and note the
gap honestly ("theorem holds under independent-channel assumption; experiments use
the realistic shared channel and confirm the trend"). Many Q1 papers do exactly
this. Let người dùng choose — it is a positioning decision, not a mechanical one.

## Cleanest claimable theorem shape

- **Primary (conditional, index-free):** under UGAP, the gain-index top-B policy is
  asymptotically optimal as N→∞ with B/N=α fixed, no indexability needed. Flag UGAP
  as an assumption, support it empirically.
- **Stronger corollary (GAP-free, quantitative):** if the LP-optimal single-armed
  policy is an aperiodic unichain on the quantized per-arm state, then deploying the
  focus-set / set-expansion variant gives an **O(1/√N)** gap. Cost: analyze/deploy a
  focus-set variant, not the literal heuristic.

Always separate PROVEN (in the papers, with citations) from INFERENCE (your mapping
to the model), and explicitly list which assumptions are likely to HOLD vs likely to
FAIL for the specific model.

## Gate an expensive re-run on a DECISIVE SPIKE that produces positive evidence

When người dùng approves a model change that forces a full re-run (e.g. per-arm
channel: "hướng A"), do NOT jump straight to the multi-hour full re-run. First run
a cheap decisive spike answering the actual question that motivated the change, and
only commit the full re-run if the spike is positive. In this precedent the
question was "does per-arm channel widen bài AoI-greenhouse's advantage over channel-blind
baselines?" — the spike (Intel, 30 windows, bài AoI-greenhouse vs AoII/MaxWeight variants +
paired Wilcoxon) showed loss ×3–5 better with p<0.025 on every comparison and
missed-violation 3–5× lower. That is hard evidence the model change *improves* the
paper, not just unblocks the theory — exactly what justifies re-running everything.
Reuse the spike discipline from `method-enhancement-spike.md`: 3-window smoke to
catch bugs (it WILL show inflated/noisy ratios — do not trust it), then full N +
Wilcoxon for the verdict. Report the spike numbers to người dùng and let him green-
light the full re-run; do not bundle still-pending design decisions (e.g. a VoU
redesign) into the same re-run without his sign-off — gather them so the expensive
job runs ONCE.

## Refactor recipe: shared scalar state → independent per-arm vector

Fixing arm-independence usually means turning one shared scalar (channel mode,
belief) into an (N,) per-arm vector. This touched 5 files here; the pattern that
worked cleanly:

1. **Grep every call-site first** (`grep -rn "pi_bad\|step_state\|predict_success"
   src scripts policies`). Note: the in-repo `search_files` tool returned 0 hits
   spuriously this session — fall back to `grep -rn` via terminal when a content
   search you KNOW should match comes back empty.
2. **Add `_vec` variants ALONGSIDE the scalar functions, do not delete the scalar.**
   Keeping the scalar path intact means self-contained smoke tests keep passing and
   the diff stays reviewable. Vectorize the channel filter as predict-all (every arm
   advances its latent mode each slot — restless) + Bayesian-update-served-only.
3. **The broadcast trick:** most call-sites are `p_succ * vou` where `vou` is already
   (N,). Once `p_succ` becomes (N,), the elementwise product Just Works — only change
   the assignment line, not the arithmetic. Drop the `float(...)` wrapper.
4. **In-loop indexing is the exception:** inside a greedy `for j in remaining:` loop
   the scalar was used as `p_succ * delta_j`; with a vector it must become
   `float(p_succ[j])`. Search for loop bodies specifically.
5. **Vectorize the BASELINES too, for a fair comparison.** Baselines often live in a
   separate `policies/` dir and also read the shared state; if you only vectorize the
   proposed method, baselines silently break (TypeError: only 0-d arrays can be
   converted to scalars) or — worse — see a different channel model. They must all
   see the same per-arm `p_succ_i`.
6. **Watch for dead code.** A file may define a class that is actually re-defined and
   imported from elsewhere (here `whittle_vou_shield.py` was never imported; the live
   class was in `policies.py`). Confirm with `grep -rn ClassName` before spending time
   patching the dead copy.
7. **Verify end-to-end before the spike:** unit smoke (`python new_algorithm.py`) →
   one real `run_window` call (catches simulator-loop bugs the unit smoke misses) →
   then the comparison spike.

## Numerically VALIDATE the asymptotic theorem (don't just cite it)

Precedent continuation 2026-06-19: after writing the O(1/√N) theorem, người dùng
said "có chứng minh toán học trước khi chạy thì hay hơn" and "làm thêm" — i.e. the
theorem must come with its OWN numerical certificate, not just an external
citation. This is the derive-then-verify contract applied to theory. Recipe that
ran clean and produced Q1-grade evidence:

1. **Build the finite per-arm MDP from the FITTED parameters, not toy numbers.**
   Fit AR(1) α and innovation σ on the real trace; pull the channel kernel
   (P_gg, P_bb, p_ok) from the actual `channel.py`. State = (quantized
   distance-to-threshold bin, channel mode). The belief summary that matters is
   the standardized distance z=(u−μ)/s_pred — bin THAT, not raw (μ,σ²), because
   the danger term only depends on z.
2. **Solve the relaxed single-arm LP with `scipy.optimize.linprog(method="highs")`.**
   Variables y(s,a); constraints = balance (per state: inflow−outflow=0), budget
   (Σ_s y(s,1)=α), normalization (Σ=1). Recover π*(a|s)=y(s,a)/Σ_a y(s,a). Report
   R_rel (the per-arm upper bound).
3. **Emit an Assumption-1 CERTIFICATE, computed on P^{π*}:**
   - Unichain: reachability closure of (P^{π*}>0), then count recurrent classes
     (a state is recurrent iff every reachable state communicates back). Must = 1.
   - Aperiodicity: a self-loop (diag(P^{π*})>0) inside the recurrent class ⇒
     period 1. Both are cheap decidable matrix checks.
   - Bonus signal: fraction of states where π* is deterministic (≈96% here) — high
     determinism empirically justifies the deployed top-B LP-priority rule.
4. **Simulate the true N-arm constrained system over a SWEEP of N** (e.g.
   10..500), exactly B=⌊αN⌋ served per slot, and measure: (b) mean-field
   convergence ‖empirical state dist − μ*‖₁→0; (c) the index↔set-expansion BRIDGE;
   (d) optimality gap R_rel−R_N regressed on 1/√N (report slope + R²).
5. **AVERAGE OVER MULTIPLE SEEDS (≥8) with paired noise.** A single-seed N-sweep
   is too noisy — here it gave a non-monotone curve (N=50 bumped up) and R²=0.65.
   Re-running 8 seeds with the SAME rng reseed for both policies (paired) cleaned
   the curve to R²≈0.87 (set-expansion) / 0.77 (index). Do not present a single-seed
   rate fit.
6. **\"Nâng độ khó\" → more seeds + wider N may LOWER R², and that is the honest
   result to report.** Continuation 2026-06-20: người dùng asked to raise rigor, so
   seeds 8→32 and N extended to 1000. R² DROPPED (0.87→0.83 set-exp, 0.77→0.73
   index) because 8 seeds gave a flatteringly clean fit; 32 seeds reflect the true
   dispersion. Report the lower number truthfully — frame it as \"more honest\", and
   highlight the gains that DID strengthen: convergence ‖·‖₁ became MONOTONE all the
   way to N=1000 (0.39→0.015) and the reward bridge tightened (≤1e-4 for N≥200).
   Never keep the prettier low-seed number once you've run the higher-seed version.
   When you change SEEDS or N in the script, every dependent number in the
   manuscript paragraph must be re-synced from the new run output (don't leave the
   old 0.87/0.02/N=500 phrasing); and disambiguate \"8 seeds\" in text (it is theory-
   validation seeds, NOT the experiment's 30 windows — người dùng explicitly mistook a
   bare \"(8 seeds)\" for a window count, so write \"32 seeds per N, N∈{...}\").

## Metric-design pitfalls when validating (both bit me this session)

- **A policy-INDEPENDENT metric ties trivially across all policies — useless.**
  First tail metric measured raw true-overshoot (x_true beyond the band). But
  x_true is the same trace regardless of policy ⇒ every policy got identical
  P90/P99 and p=nan. The FIX: condition the metric on what the policy controls —
  here "severity of UNDETECTED violations" = overshoot of x_true ONLY where the
  held estimate xh still reports inside the band (the system failed to see it).
  That is policy-dependent and meaningful. Before trusting any per-policy metric,
  ask: "does this quantity actually change when the policy changes?"
- **Exact-set-match "agreement" decays combinatorially → not a real bridge.**
  Measuring the fraction of slots where two policies pick the identical B-arm
  subset goes →0 as N grows for purely combinatorial reasons (many ties, tiny
  differences in tie-breaking), even when the policies are effectively equivalent.
  It LOOKS like divergence but isn't. The substantive bridge is the REWARD GAP
  |R_index − R_setexp| (→0, ≤4e-4 for N≥100 here). When you need to show "the
  cheap deployed rule ≈ the theoretically-optimal variant," compare achieved
  reward/loss, never exact action-set identity.

## When người dùng says "X made the results better" — MEASURE, don't agree

Continuation 2026-06-20: người dùng observed "from when we switched to per-arm the
results seem better, right?" The reflexive move is to agree; the correct move is to
run the A/B and report what it actually shows. Here the honest answer was nuanced
and worth the check:
- The deployed simulator only wired the per-arm path; the scalar/shared functions
  still existed in `channel.py` but weren't called. To run a FAIR A/B (same
  bài AoI-greenhouse, same seeds, same everything, only the channel regime differs),
  **monkeypatch the three simulator channel hooks** (`sim.step_state_vec`,
  `sim.update_bad_belief_vec`, `sim.stationary_bad_belief_vec`) with shared-mode
  closures (one latent G-E mode + one scalar belief broadcast to all N), run, then
  restore the originals. This keeps ALL metric machinery byte-identical across
  regimes — the only thing that changes is the channel. Far cleaner than forking
  `run_window`.
- Result: per-arm beat shared on MEAN loss (ratio 1.24×) but **paired Wilcoxon
  p=0.46, wins 14/30 windows** — NOT statistically significant. Reporting "per-arm
  improves results" as an empirical win would have been an overclaim người dùng would
  later get burned by in review.
- The defensible framing (which người dùng accepted): per-arm's real value is
  STRUCTURAL/THEORETICAL — independent arms are the premise that makes the O(1/√N)
  theorem apply at all (a shared channel couples all arms and breaks it), plus it
  enables genuine per-link opportunistic scheduling. The ~24% mean improvement is a
  bonus, not the selling point. And người dùng's directive on this: keep it IMPLICIT in
  the paper (one sentence in §2 that independence decouples the arms), do NOT add an
  A/B table or spell it out — "chữ ít thôi, tập trung chữ cho nội dung chính."
- General rule: a structural/architectural change is justified by the guarantee it
  unlocks, not necessarily by a significant metric delta. Don't conflate the two,
  and don't let a flattering mean hide an insignificant p-value.

## Integrating the theorem into the manuscript

Same build-gated workflow as the VoU math (see SKILL.md Stage 6 subsection): backup
→ add the `\newtheorem{assumption}{Assumption}` env to preamble if missing → fetch
the anchor paper's metadata LIVE from arXiv for the bib → put the verified certificate
numbers (α, σ, P_gg/P_bb, ‖·‖₁ endpoints, R² values, bridge bound) into a
"Numerical validation" paragraph → full pdflatex→bibtex→pdflatex×2 → grep last pass
for 0 undefined citations / 0 `??` → confirm via pdftotext the theorem is in the PDF.
Frame honestly: the set-expansion variant carries the UNCONDITIONAL O(1/√N) bound;
the deployed top-B index is optimal only under a mean-field attractor, which you
VERIFY empirically (the bridge) rather than assume.
