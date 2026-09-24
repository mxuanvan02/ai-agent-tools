# IEEE/LaTeX Layout Polish Pass

Use this when a manuscript is scientifically close to submit-ready but the PDF still has LaTeX layout warnings such as `Overfull \\hbox`.

## Workflow

1. Build from the project root after the latest edits:
   ```bash
   latexmk -pdf -interaction=nonstopmode main.tex
   grep -n "Overfull" main.log || true
   grep -n "Warning:.*undefined\\|undefined references\\|Citation.*undefined\\|Reference.*undefined" main.log || true
   pdfinfo <final>.pdf | grep '^Pages'
   ```
2. Map each overfull warning to its source section and inspect the nearby table, figure, or equation.
3. Prefer minimally invasive layout fixes that do not change claims or numeric evidence:
   - Wrap wide single-column TikZ figures as `\\resizebox{\\columnwidth}{!}{\\input{...}}`.
   - Wrap wide single-column tables as `\\resizebox{\\columnwidth}{!}{% ... }`.
   - Wrap wide `table*` content as `\\resizebox{\\textwidth}{!}{% ... }`.
   - Break long equations into `align`/`aligned` instead of shrinking math blindly.
   - For dense IEEE tables, use `\\small` only if needed, and keep captions readable.
4. Rebuild after each batch and re-check `main.log`; do not declare layout clean until `grep -n "Overfull" main.log` is empty.
5. Copy the fresh PDF to the named final artifact and refresh the submission zip/package.

## Orphan `\paragraph{}` label pitfall (IEEEtran)

In IEEEtran, `\paragraph{Title.}` renders as a run-in **labeled list item** that auto-numbers `a)`, `b)`, `c)`. A LONE `\paragraph` in a section therefore prints a dangling `a)` with no `b)` — looks broken, and người dùng WILL catch it. Rules:
- Only use `\paragraph{}` when there are **≥2** of them in the same mechanic/group (so they read as a coherent a)–e) list, e.g. Quality+Cost, or a 5-part complexity breakdown).
- For a SINGLE lead-in, use a run-in italic phrase instead: `\smallskip\noindent\textit{Title---...}\; Body text...` (agent-dash inside, single period, no colon). This gives the emphasis without the orphan label.
- Watch for double punctuation when converting: `\paragraph{X.}` → italic must not become `X.:` etc.
- Audit after any edit that adds a `\paragraph`: `search_files pattern=paragraph path=sections` and confirm every match is part of a ≥2 group; convert the lone ones.

## Pitfalls

- `Overfull` line ranges can refer to an included figure/table rather than nearby prose; inspect the log context and the rendered page.
- Do not use a layout pass to rewrite scientific narrative unless the warning is caused by wording in a caption/header.
- If a previous patch warns that a file changed since last read, re-read the relevant region before continuing to avoid clobbering sibling/user edits.
- Keep the workspace tidy: update the main artifact in place and refresh the existing package; avoid creating `final2` copies.

## Session precedent

In the bài probe-transmit IoTJ polish pass, the remaining overfulls were removed by resizing two TikZ figures, splitting a long payload-index equation into `align`, resizing several IEEE tables, splitting the service-debt equation, rebuilding, confirming 14 pages, and refreshing `bài probe-transmit_IoTJ_clean_submission.zip`.
