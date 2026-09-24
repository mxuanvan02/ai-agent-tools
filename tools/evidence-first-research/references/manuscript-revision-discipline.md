# Manuscript revision discipline (LaTeX, data-backed papers)

Session-derived lessons for revising người dùng's papers when a review demands new
experiments + text changes. Numbers must be regenerated from code, never
hardcoded; agent-added text = review markup he can strip.

## Review markup that survives a LaTeX build (IMPORTANT PITFALL)

người dùng wants agent-added NEW manuscript text visually flagged so he can review
then strip it. The obvious choice — `soul`'s `\hl{}` (yellow highlight) — **breaks
the build**: `soul` cannot operate in math mode, so any `\hlnew{...}` wrapping an
equation, inline `$...$`, or a macro like `$4p(1-p)$` throws
`! Fatal error ... no output PDF`.

Use a COLOR macro instead — works in both text and math mode:

```latex
% in main.tex preamble (xcolor already loaded)
% REVIEW MARKUP: agent-added text in review-blue; works in text AND math.
% Strip before submit by making it identity: \renewcommand{\hlnew}[1]{#1}
\definecolor{reviewnew}{rgb}{0.00,0.00,0.75}
\newcommand{\hlnew}[1]{{\color{reviewnew}#1}}
```

Then wrap new prose AND new equations with `\hlnew{...}` freely. To produce the
clean submission copy, redefine as identity (one line) — no need to hunt down
every occurrence.

Note: người dùng's stated convention says "yellow highlight". Color-blue is the
build-safe substitute; mention the swap when handing over. If he insists on
yellow, `\hl` only works on pure-text spans — never wrap math.

## Regenerate ALL dependent artifacts; delete stale outputs first

When changing a core method (e.g. urgency score), numbers propagate to many
tables/figures. Discipline that avoided silent stale-number bugs:

1. `rm -rf outputs/` (or move to _backups) BEFORE rerunning — stale CSV/TeX left
   in place get silently reused and mismatch the new run.
2. Run scripts in dependency order: main experiment → sensitivity → nonstationary
   → wilcoxon (needs raw.csv) → pairwise → ablation → scaling.
3. Scripts that `import` the main module inherit the change automatically; only
   scripts that RE-DEFINE the scoring function need editing too. Grep for the
   duplicated formula (e.g. `0.55*` weight) across all scripts before assuming
   one edit is enough.
4. Manuscript tables are often hand-formatted (different column set / language)
   from what scripts emit — there is no auto-bridge. Write a single
   `make_manuscript_tables.py` that reads the fresh CSVs and emits the EXACT
   manuscript-format .tex, so numbers are reproducible and match byte-for-byte.
5. Build cycle: pdflatex → bibtex → pdflatex → pdflatex; then grep the log for
   `undefined`/`Fatal`. A `\ref` to a table you added is undefined until the
   table's `\input{...}` is actually placed in the body (not just referenced).

## Don't force a failing method into the paper — even when asked

người dùng may ask to keep a component (e.g. bài bandwidth-scheduling-CVaR) and "make it help". Honor
the intent by testing hard, but do NOT ship a "Proposed" method that loses on
its own metric. Sequence that worked:
- DERIVE the theoretical reason a form should work BEFORE expensive runs
  (e.g. VoU `4p(1-p)` = leading-order value-of-information for a binary safety
  decision; raw `p_vio` double-counts the detector threshold).
- Verify with real data + paired Wilcoxon (scipy in a uv venv). Read the SIGN of
  the delta carefully: a tiny p-value can mean significantly WORSE. Do not report
  "improvement" without confirming direction.
- After ~fair attempts fail on real data (here 6×, across 2 datasets), state the
  negative result plainly and recommend dropping. When he says "if it fails, drop
  it", cut it cleanly: remove the subsection, its table, related-work/abstract/
  intro/conclusion mentions, and the data-availability line — then grep for
  leftover mentions (`grep -n CVaR|tail|ERA5|Mekong`) before building.
- A controlled negative result ("we tried tail-pricing, proved it doesn't help on
  this regime → gain comes from X") is Q1-respectable; a forced win is a liability
  since the repo ships runnable code reviewers will execute.

## Recovering "lost" Vietnam climate data

ERA5 station data (Can Tho / Soc Trang / Ca Mau) is NOT lost when only the .tex
result remains — it is re-fetchable from Open-Meteo archive API. Look for a
`fetch_real_vn_data.py` that calls
`https://archive-api.open-meteo.com/v1/archive?latitude=..&longitude=..&start_date=..&end_date=..&hourly=temperature_2m`.
Refetch is reproducible; prefer it over synthesizing.
