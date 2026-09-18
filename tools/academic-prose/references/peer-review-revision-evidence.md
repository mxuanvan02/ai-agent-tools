# Author-side peer-review revision for computational papers

Playbook for revising a manuscript in response to received peer-review reports
when the paper ships a public code/data artifact. Core rule: **every answer to
a reviewer must be grounded in re-executed evidence, never in recall of what
the numbers "probably" were.** This is the author side; for refereeing someone
else's paper use the peer-review/refereeing skills instead.

## 0. Match the review to the manuscript first

Before planning anything, verify submission ID and title inside the review
against the manuscript being revised. Machines that host several paper projects
accumulate review files for *other* submissions (a real near-miss: two
`STAIS2026_128_review_*` files for a LegalQA-RAG paper sat in the document
cache while the task was revising RABS, submission 40). A mismatched review
produces a confidently wrong revision plan. If no review file for the target
paper exists anywhere, ask the author for it — do not substitute an older
internal feedback report without explicit confirmation.

## 1. Reproduce before responding

1. Clone the **public artifact repo** referenced in the manuscript's Data/Code
   statement (not whatever local experiment clone is handy — local branch
   clones may be stale variants whose constants do not match the submitted
   numbers; verify constants like safety band, seeds, window length, n/cell
   against the manuscript text before trusting a pipeline).
2. Run the pipeline (`reproduce.sh` or the individual experiment scripts).
3. Byte-diff every regenerated `.tex` table against the submitted ones.
   - Identical → your evidence base is confirmed; you can quote numbers and
     CIs freely.
   - Caption-only diffs → keep the submitted caption (it was usually improved
     deliberately); keep regenerated numbers.
   - Number diffs → STOP; resolve which pipeline produced the submission
     before writing a single response word.
4. Regenerate figures from the fresh CSVs so figure/table/manuscript cannot
   drift apart.

## 2. Read the code behind each reviewer claim

Reviewers routinely collapse two same-named components that live in different
code paths. Located example (RABS, Reviewer 2 Q4): the submitted ablation
table removed the risk term from the *ranking score* (`choose_sensors`) only,
while the namesake mechanism — the risk relaxation `-c_R·R·B` in the *budget
rule* (`choose_B`) — was never ablated. The reviewer read "the risk term does
not help" as covering both. Grep the exact functions the reviewer's claim
touches, and establish what was and was not actually varied, before conceding
or rebutting.

## 3. Answer "why keep component X?" with a fresh targeted ablation

When a reviewer shows your component is neutral or counterproductive on the
reported metrics:

1. Write a minimal script reusing the published primitives (import or
   copy the exact functions; stdlib-only, deterministic, same seeds/windows
   as the submitted runs) that toggles exactly the constant under question.
2. Report mean ± 95% CI for every metric, and check the reviewer-quoted delta
   against CI overlap (e.g. Δobj = 0.0017 vs half-widths ±0.0024/±0.0021 →
   within noise; the honest statement is "neutral knob", not a defense).
3. If the component is neutral in the evaluated regime but plausibly matters
   in a harsher one, offer the author two options with measured fallback:
   **(A)** reframe honestly — demote the component to a conservative design
   knob, report the new ablation, state the neutrality as a limitation;
   **(B)** run the harsher regime (e.g. an `extreme_burst` channel already
   parameterized in the codebase) and report both regimes truthfully, falling
   back to (A) if the mechanism still shows no effect. Never fabricate a
   defense and never hide the unfavorable measurement; a headline claim that
   the evidence weakens must be re-scoped, and the author decides how.

## 4. Non-monotonic trends: report the whole sequence

When a reviewer extrapolates a trend ("safety gap widens with N — will it
worsen beyond N=20?"), pull the per-point values with CIs. Real data often
shows a non-monotonic sequence (measured missed-event gap: +1.29 pp at N=3,
−0.04 at N=8, 0.00 at N=12, +1.86 at N=20, with overlapping CIs at N=20).
State the sequence, the CI overlap, and explicitly mark beyond-range behavior
as unknown → limitation, not reassurance.

## 5. Figure label-overlap check without vision

When a reviewer reports overlapping symbols/annotations and the vision tool is
unavailable, detect collisions programmatically: open the figure PDF with
PyMuPDF, extract text spans with bboxes (`page.get_text("dict")`), sort by
(y, x), and test pairwise intersection. This caught four data labels colliding
in a tight low-bandwidth cluster — including two policies at *identical*
coordinates, which no amount of dx/dy nudging can fix (needs leader lines or
offset stacking) — plus an annotation ("low-bandwidth region") overlapping an
unrelated label. After fixing the plot script, re-run the bbox check and
require zero intersections before delivery.

## 6. Page budget and author-approval discipline

- Build a review-point → evidence-type table first (text-only verified /
  needs new experiment / figure fix), with the measured evidence attached to
  each row, and let the author approve the plan **before** editing.
- If the manuscript sits at the venue's hard page cap, every addition must be
  offset by tightening elsewhere; if it still overflows, ask the author —
  never silently cut content to fit (overflow → appendix or author decision).
- Keep new reviewer-facing text inside the manuscript's existing markup
  convention when one exists (e.g. `\rev{}`/`revblock` environments that
  render highlighted in the review copy and neutral in the clean copy).

## 7. Response-letter hygiene

Each response: quote the reviewer point → state what was measured or changed
→ cite the exact table/figure/line where the change lives. Distinguish
verified-from-code statements from inferred ones. If an answer is "we could
not measure this", say so and route it to limitations/future work.
