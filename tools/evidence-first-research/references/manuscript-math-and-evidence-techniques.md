# Manuscript math design + evidence-synthesis techniques

Durable techniques that emerged strengthening a Q1/conference manuscript
(replacing a thin heuristic with theory, running new experiments, syncing
code+tables, honest negative results). Applies to người dùng's DERIVE-then-verify
and "theory-grounded VoU/cost over thin heuristics" contract.

## 1. Replace a redundant probability term with decision-uncertainty (VoU)

Signal: an ablation shows a "risk"/`p_vio` term in a scoring/urgency function
is neutral or HARMFUL (dropping it improves every metric). Do NOT just delete it
and do NOT grid-search for pretty numbers. DERIVE the correct form first.

Root cause pattern: ranking by raw violation probability `p` is sub-optimal
because polling/measuring only has value when a fresh reading can CHANGE the
decision. When `p→1` the detector already fires, so extra information is
worthless — yet raw-`p` ranks it highest, and often DOUBLE-COUNTS a detector
threshold already used elsewhere (e.g. `p>=0.55` inside the loss/eval).

Correct closed form: the **value of uncertainty / leading-order value of
information** for a binary safety decision is the decision uncertainty
`g(p) = 4·p·(1-p)` (scaled to [0,1]), equivalently binary entropy `H(p)`
(second-order expansion `H(p) ≈ (1/2ln2)·4p(1-p)`). It peaks at the band edge
`p=0.5` (max ambiguity) and vanishes when the outcome is certain either way.
Defensible per người dùng's rule: a closed-form term is defensible when shown to be
the leading-order truncation of a Bayes-optimal object with an explicit regime.

Result in this session: swapping `w·p` → `w·4p(1-p)` in the urgency score
turned "Pareto trade-off, loses to a baseline" into "lowest composite objective
among all practical baselines" (obj −14%, missed-violations −42%), with only a
one-line code change. Verify by re-running the FULL pipeline, not just the headline.

NOTE ON SELF-OVERLAP: if VoU/VoI is already the core of another of the user's
manuscripts (e.g. CAW), add a related-work sentence distinguishing THIS use
(e.g. decision-uncertainty channel coupled to an adaptive *budget*) from the
other (e.g. per-link VoI gating), so the two papers don't read as self-plagiarism
in overlapping review rounds.

## 2. Paired-difference SIGN pitfall (nearly shipped a backwards claim)

When reporting paired Wilcoxon / mean-difference `Δ = A - B`:
- SIGNIFICANCE (small p) says the difference is real; it says NOTHING about
  direction. A `p≈1e-6` result can mean your "Proposed" method is significantly
  WORSE.
- Always print BOTH the signed mean delta AND an explicit "-> A better / B better"
  verdict, and confirm every `\best{}`/bold cell lands on the intended method
  before writing prose. In this session a significant-but-wrong-direction result
  (`Δ=PD-CVaR<0` = CVaR worse) was briefly mis-narrated as a CVaR win.
- Cross-check: if your "Proposed" row has no bold/best cell in any column, the
  claim is probably backwards.

## 3. Honest negative-result discipline (when to CUT a contribution)

If a mechanism fails to beat baseline after repeated honest attempts across
MULTIPLE real datasets — even after fixing implementation bugs and fetching the
favorable-regime data the user asked for — stop patching. Distinguish:
- implementation bug (e.g. a variant computed identically to baseline because a
  variance/penalty term was constant across the argmin candidates; or a CVaR VaR
  level `ξ` that drifts to 0 instead of tracking the empirical α-quantile), vs
- genuine negative result (the regime's tail is too light for tail-pricing to help).
Fix bugs first; if it still loses, report it as a controlled negative result OR
cut it to Future Work. Default to the user's call, but never label a method
"Proposed" when it loses its own target metric with significance. Cutting a weak
third contribution and concentrating on two strong, fully-reproducible ones makes
a stronger paper. (This session: CVaR cut after ~6 attempts on 2 real datasets.)

## 4. LaTeX review-markup that survives math mode

Requirement: highlight agent-added NEW manuscript text (yellow-markup rule) so
người dùng can review, strippable in one line before submit.
- `soul`'s `\hl{}` FATALLY breaks inside math mode (`$...$`, equations) → build fails.
- Use a color macro instead, which works in both text and math:
  ```latex
  \definecolor{reviewnew}{rgb}{0.00,0.00,0.75}
  \newcommand{\hlnew}[1]{{\color{reviewnew}#1}}
  % strip before submit:  \renewcommand{\hlnew}[1]{#1}
  ```
- Do NOT wrap whole equations/`\subsection{}` awkwardly; wrap the prose and the
  inline symbols. Rebuild and grep the log for undefined refs after adding.

## 5. Regenerate manuscript tables from CSV via a generator script

Manuscripts often carry hand-formatted `.tex` tables whose numbers must match
freshly-computed CSVs exactly. Write ONE `make_manuscript_tables.py` that reads
the result CSVs and emits each table in the manuscript's exact format (column
order, `\best{}` bolding, p-value column). This guarantees numbers are
reproducible and stay in sync when you re-run experiments. Note mapping: script
output names often differ from manuscript `\input{}` names — map them explicitly.

## 6. Reproducibility gap: manuscript ships but code/data were never saved

Recurring failure: the `.tex` result tables exist but the generating script and
source data were never committed anywhere (not in repo, not in any git commit,
not in backups). Before trusting "just regenerate", search repo + all backups +
git history. If the data was fetched from a public API (e.g. ERA5 via
Open-Meteo archive API by lat/lon), the fetch script itself is the recovery
path — re-fetch rather than declare data lost. Then commit code+data so it is
reproducible next time. Companion repo ships CODE + SOURCE DATA only (per user
convention); push only the scripts that match the FINAL paper (don't push code
for cut contributions), verify on the remote (don't trust the push log), and
scrub any tokenized push URL from git config afterward.
