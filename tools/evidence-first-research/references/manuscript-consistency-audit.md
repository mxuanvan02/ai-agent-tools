# Manuscript cross-consistency audit — what "xong" (done) MUST mean

## Why this file exists
Người dùng's recurring, sharpest complaint: the agent declares a manuscript "xong/ready"
after a **mechanical** check (LaTeX build passes, numbers match the repo, page count fits),
then when he asks "dò lại" (re-check) the agent *finally* reads the prose and finds real
errors. His words: "khi nhắc dò lại thì agent mới dò và phát hiện lỗi sai, thì làm sao agent bảo
xong mà người dùng yên tâm được?" — i.e. a "done" that only holds until someone reads it is a
FAKE done, and it destroys his trust in every result.

**Root cause:** the agent conflated two different meanings of "done":
- mechanical done = build compiles, 0 undefined refs, 0 overfull, numbers == source CSV/repo
- semantic done = every claim read, every cross-reference reconciled, math self-consistent

A LaTeX compiler does NOT read meaning. It happily typesets a wrong objective function or
a "half" that contradicts a "one third" three pages later. So mechanical pass ≠ correct paper.

## Rule
NEVER report a manuscript as "xong/ready/clean" on mechanical evidence alone. "Done" for a
manuscript = a completed cross-consistency audit whose result is shown to người dùng as a
pass/fail table, not a prose assurance. If the audit hasn't run, say "build passed, semantic
audit chưa chạy" — do not imply completeness.

## The audit (run BEFORE claiming done, not after he asks)

1. **Numeric traceability.** Extract every number stated in prose (abstract, intro,
   narrative paragraphs, conclusion). For each, trace it to its source table cell / CSV /
   script output. Flag any number with no source, or that disagrees with its source.
   - Classic catch this session: bài bandwidth-scheduling-PD "1.37 vs 3.00" = 0.457 → "about half" is right,
     "little more than one third" is WRONG. Same ratio described two contradictory ways in
     abstract vs conclusion.

2. **Cross-section term/claim reconciliation.** The same quantity must be described the same
   way everywhere. Build a small map: what does the System Model say the objective is? What
   does the Method selector actually minimize? What does the code minimize? All three MUST
   agree.
   - Classic catch this session: System Model wrote min $\widehat M_t$ (unpolled risk), but the
     deployed selector (eq. 15) and the code minimize $\widehat L_t$ (tracking loss) with
     $\widehat M_t$ only a penalty term. The Lagrangian derivation inherited the wrong objective.
     This is the kind of error that makes a reviewer reject on "the formulation doesn't match
     the algorithm."

3. **Math ↔ code agreement.** Every constant, weight, target, step size quoted in the paper
   must equal the value in the released script. Every derived object (Lagrangian, update rule,
   selector) must be the code's actual operation, not an idealized version.

4. **Claim ↔ evidence direction.** Check the paper doesn't claim a win the data doesn't support.
   - This session: bài bandwidth-scheduling-PD does NOT beat full polling on missed-rate (Wilcoxon p=0.36, effect
     favours Fixed-B3). The honest claim is "bandwidth–safety trade-off," not "safer." Verify
     every "outperforms/best/lowest" against the actual table + significance test.

5. **Leftover-framing sweep.** grep the body for terms from abandoned framings/methods
   (here: "greenhouse", "measured" for reanalysis data, "synthetic/stress test", a dropped
   method name). Confirm each remaining hit is legitimate (e.g. inside a cited paper title, or
   a negation like "no synthetic traces") — not a stale leftover.

## Deliverable shape
Present the audit as a table the user can scan: claim/number | source | pass/fail | note.
That is the artifact that earns "yên tâm" (peace of mind). A paragraph saying "I checked
everything" does the opposite — it's exactly the fake-done he called out.

## Tie-ins
- Numbers-from-data-not-hardcoded and regen-on-mismatch discipline: see the manuscript LaTeX
  revision reference in this same skill.
- Bibliography/citation integrity is a separate, complementary audit: `latex-reference-audit` skill.
