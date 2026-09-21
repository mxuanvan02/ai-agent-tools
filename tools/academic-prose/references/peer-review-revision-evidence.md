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

Length register: mirror the reviewers' own brevity. Each point should be one
or two sentences stating what was done plus the numbers; the mechanism belongs
in the manuscript, not the letter. A letter that re-argues the analysis reads
as defensive.

Glyph pitfall when building the letter with `pandoc` + `xelatex` and Latin
Modern: Greek and math glyphs (ρ, δ, ≈, ≥, −, →) are **silently dropped** — the
build still exits 0 and prints only a `Missing character` warning. ASCII-fy the
Markdown before building, then grep the build log for `Missing character`.

## 8. Public-artifact confidentiality: the review never reaches the repo

A reproducibility repo is publication-facing, so reviewer identities,
reviewer question numbers, and revision-round framing are prohibited internal
register there exactly as in the manuscript. The leak channels are wider than
prose:

- **commit messages** naming review rounds and question numbers — these also
  expose the author's name and email through the `.patch` endpoint;
- **filenames and output names** tagged with question numbers (a `q4`/`q5` tag
  maps a public file onto a confidential comment);
- **README structure**: a "revision-round experiments" section, and per-table
  reproduction steps, reveal which table answers which reviewer;
- **script docstrings** ("fixes the Reviewer-1 issue", "regime X (submitted)",
  "from branch-B").

Write the repo as if no review existed: descriptive file names, and a README
describing contributions, the algorithm, the application, and a one-command
quick start. The reviewer-by-reviewer mapping lives only in the letter sent to
the editor.

**Force-push does not remove this material.** GitHub keeps serving the
orphaned commits after history is rewritten:

- `/commit/<old-sha>` and `/commit/<old-sha>.patch` still return HTTP 200 with
  the full message, anonymously;
- `GET /repos/{owner}/{repo}/events` publicly lists every PushEvent with its
  `before`/`head` SHAs, so a stranger needs no prior knowledge to recover the
  entire orphaned chain;
- `GET /search/commits` and the commit-list UI expose only reachable commits.

The last point is the trap: a fresh `git clone` followed by
`git grep $(git rev-list --all)` therefore reports **zero matches** and gives
false assurance. Verify a sanitization three ways before calling it clean —
fresh clone (reachable history), each old SHA fetched by URL, and the Events
API. Only **deleting the repository** (GitHub then garbage-collects the
orphaned objects) or **making it private** removes the content; ask the author
before either, and back up the full history first (`git bundle create --all`).
Never report "force-pushed, therefore clean", and never characterize residual
exposure as low-risk without measuring it.

## 9. A claim-strength change is a whole-document sweep, including generated text

When the author asks to soften a claim, the same claim usually survives in
several artifacts under different wording, and the copy already fixed is the
worst place to search from. Observed failure: softening the Results prose left
two stronger copies behind — a table caption asserting the components were
"mutually redundant", and a Conclusion sentence calling them "redundant". Both
survived two review rounds because each search reused the exact phrase from the
spot that had already been edited.

Sweep procedure:

1. Search the **semantic claim across its variants**, never the last-edited
   phrase (`redundant`, `mutually redundant`, `adds nothing`, `no measured
   gain`, `carries N× less information`).
2. Search **every `.tex` file**, not just the section inputs — conclusions,
   acknowledgments, and declaration blocks often sit inline in `main.tex`.
3. Search the **generator scripts in the repo**. Caption and table text emitted
   by a script is regenerated on every pipeline run, so patching only the
   emitted `.tex` is silently reverted; patch the generator and re-emit.
4. Rebuild and probe the **rendered PDF**, which is what a referee reads.
5. Re-pack and re-verify any delivery bundle (§11).

A claim softened in prose but not in the caption still reads as an overclaim in
the compiled paper.

## 10. Verification probe hygiene: the probe is often the broken part

Every defect in §9 was found by a probe, and several probes first reported the
wrong answer. When a probe disagrees with what an edit should have produced,
debug the probe before believing either side.

- **LaTeX hyphenation defeats substring probes.** Text extracted from a PDF can
  contain a word split at its own hyphen. Normalize by stripping whitespace
  *and* hyphens from needle and haystack before comparing.
- **Case-fold both sides or neither.** Lower-casing the haystack while the
  needle keeps internal capitals (`AoI`) yields a false negative.
- **Probe the artifact that actually contains the target.** Scanning a composite
  paper PDF for figure labels also matches prose mentions and undercounts; open
  the standalone figure PDF and read its text layer.
- **Never let a pipe consume an exit code.** `scanner --quiet | sed …` prints
  nothing and `$?` reports the last stage's status, so a "clean" gate proves
  nothing. Redirect to a file, then read the code.
- **A clean scan over too little input is a false pass.** Extracting prose from
  a root `.tex` that only `\input`s its body yields a few hundred words; extract
  every input file, concatenate, and confirm the word count is plausible for the
  paper before trusting `gate: scan_clean`.

## 11. Re-verify the shipped bundle after the last edit

Pack the delivery archive from the current build, then extract it into a clean
directory and compile **there**. An archive packed before a later edit silently
ships stale text — observed when the submission bundle still carried the
pre-softening caption while the working copy was already fixed.

Compare extracted versus working artifacts at the **text level** (normalized
page-text digest), not by file hash: PDFs embed timestamps and document IDs, so
byte-level comparison reports a difference for identical content and invites a
wrong conclusion either way.
