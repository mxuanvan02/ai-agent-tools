# Manuscript Reproducibility & Honest-Claims Discipline

Session-hardened rules for revising người dùng's manuscripts when numbers, framing,
or "proposed methods" are in doubt. Load when the user says results feel
untrustworthy, when there are multiple .tex/.zip copies, or when a method was
tried and lost.

## 1. One canonical source of truth (fixes "không tin được kết quả nào là thật")

Symptom: many parallel `.tex` dirs + scattered `.zip` builds, numbers disagree
between the PDF being submitted and the code repo.

Procedure:
- Find the repo that **regenerates numbers from data** (script → CSV → LaTeX
  tables). That repo — not any `.tex`/`.zip` — is the ONLY canonical source.
- **Prove reproducibility, don't assume it:** delete the committed generated
  tables into a temp dir, re-run the whole pipeline, and `diff` regenerated
  tables/CSVs against what's committed. Exact match = numbers are deterministic
  and trustworthy. Mismatch = you've found the "ảo" numbers.
- The submit-ready PDF often carries **orphan numbers** (from an older pipeline
  that no longer exists). If the PDF and the reproducible repo tell opposite
  stories, the PDF loses. Never submit numbers a reviewer can't regenerate.
- After establishing canonical, every table/figure/sentence must trace to it.
  Regenerate figures from the same pipeline (env-overridable CSV path), don't
  reuse stale PDFs/SVGs.

## 2. Tested-and-lost method: NOT Future Work (workflow correction)

người dùng's rule extended. Three distinct fates for a candidate method:
- **Untested but promising** → Future Work is legitimate.
- **Tested and lost** → does NOT go to Future Work (self-contradictory: "we
  tried it, it failed, so future work will try it"). It belongs as an
  **ablation / comparison row** documenting "we considered X, it lost on this
  regime, so we use Y" — this is an honesty *strength*, not a weakness. Or drop
  it entirely.
- **Tested and won** → it's the Proposed method.

Concrete example this session: bài bandwidth-scheduling-CVaR / VoU urgency channel was tested and
lost on the heavy-tailed regime. Wrong: list it as a Future Work "tail-risk
variant". Right: keep it only as an ablation row (raw-p 0.1000 beats VoU 0.1006)
+ a Related-Work citation to *others'* CVaR work. Never "Proposed", never
"Future Work".

## 3. Honest claims: win-story must match the table

- State exactly what the method wins and where it does NOT. If it wins composite
  objective + bandwidth but NOT missed-rate, the contribution is a
  "bandwidth–safety trade-off", not "safer". Claiming a win the paper's own
  Wilcoxon table contradicts (p=0.36, effect size favours baseline) is an
  instant reviewer kill.
- Beware self-referential metrics: if the method optimizes a composite objective
  the authors defined, "best on that objective" is near-tautological — lean the
  claim on the independent evidence (bandwidth saving + paired significance).

## 4. Synthetic → real data upgrade (kills "stress test / not measured")

- Reanalysis climate data (ERA5 via Open-Meteo archive-api, free, no key) is
  **real climate** but NOT "in-field sensor / measured" data — never call it
  "measured". Describe as "real ERA5 reanalysis", keep in-field validation as a
  Limitation.
- When scaling N is faked by replicating a few real stations (circular time
  offset + thermal-bias noise), that's a synthetic "stress test" a reviewer will
  attack. ERA5 is a **global grid**: replace replicated zones with N *distinct
  real* lat/lon locations (e.g. 20 real Mekong-delta towns). Refetch, drop the
  `make_zone_steps` synthesis, read N real stations directly. Numbers often
  improve AND the "synthetic" caveat disappears. Update caption/README/abstract
  wording in lockstep — grep for "synthetic", "stress test", "measured" and fix
  every site (a synthetic *channel* like Gilbert–Elliott is fine; synthetic
  *data* is the problem).

## 5. LaTeX review-markup for agent-added text (soul vs mdframed)

Agent-added manuscript text must be YELLOW review markup, stripped before submit.

- **soul `\hl{...}` is fragile**: it breaks on `\cite`, `\ref`, and display math
  inside the highlighted span (garbage `\citation{\hbox{}}` in the .aux →
  undefined citations). `\soulregister{\ref}{1}` causes **infinite recursion**
  (TeX capacity exceeded) — do NOT register `\ref`.
- **Fix**: for any highlighted paragraph containing `\cite`/`\ref`/math, use a
  block-level `mdframed` environment instead of inline `\hl`:
  ```latex
  \usepackage{soul}\sethlcolor{yellow}\newcommand{\rev}[1]{\hl{#1}} % plain text only
  \usepackage{mdframed}
  \newmdenv[backgroundcolor=yellow!30,linecolor=yellow!55!black,linewidth=0.4pt,
    innertopmargin=3pt,innerbottommargin=3pt,skipabove=3pt,skipbelow=3pt,
    leftmargin=0pt,rightmargin=0pt,innerleftmargin=4pt,innerrightmargin=4pt,
    splittopskip=0pt,splitbottomskip=0pt]{revblock}
  ```
  Keep `\rev{}` only for short plain-text inline highlights. Wrap whole
  reframed paragraphs (with citations/refs/theorem envs) in
  `\begin{revblock}...\end{revblock}`. `splittopskip`/`splitbottomskip` let it
  break across pages.

## 6. Build + verify gates (never call a manuscript "ready" without these)

- Full latexmk cycle: `pdflatex → bibtex → pdflatex → pdflatex`. A single-pass
  build shows false "undefined citations".
- Check: page count within limit, **0 undefined citations**, **0 bibtex
  errors**, **0 overfull >5pt**.
- Prune orphan `.bib` entries (cited-set vs bib-set diff) and unused
  `outputs/tables/*.tex` into `_backups/<ts>/` — don't delete.
- Vision-check rendered pages: tables show canonical numbers, math not broken,
  review markup renders. pdftotext "missing" hits are often hyphenation, not
  real clipping — verify with an overfull-vbox check before believing loss.

## Theory-derivation note (rigor vs novelty)

When asked to "add math derivation" to justify hand-tuned constants: deriving a
primal–dual/Lagrangian update as online dual ascent (drift-plus-penalty, Neely
2010) turns bare constants into shadow prices + step sizes and yields a
bounded-multiplier Lemma + O(1/T) feasibility Proposition. Be honest that this
is **rigor, not novelty** — the framework is textbook (Lyapunov/dual ascent);
it makes the paper defensible, it is not a new theoretical contribution. Pitch
at conference tier accordingly; don't oversell as novel.
