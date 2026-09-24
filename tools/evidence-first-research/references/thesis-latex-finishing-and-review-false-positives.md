# Thesis LaTeX finishing pitfalls + review-subagent false-positive classes

Captured from a long LVTN finishing pass (figure audit → number-consistency →
RLM multi-lens review → ready-submit polish). Two durable lessons.

## 1. longtable conversion can desync table NUMBER from PRINT ORDER

Symptom: after converting a `table` float to `longtable` to fix a
`Float too large for page by NNNpt` warning, the List of Tables (`.lot`) shows
numbers out of order — e.g. table **2.4** printed on page 66 BEFORE tables
2.1/2.2/2.3 on pages 79–81.

Root cause: a `longtable` is NOT a float — it pins at its source position and
takes its number where it sits. Sibling `[ht]/[!htbp]` floats defined earlier in
the source can drift far DOWN the document, so they receive smaller numbers
(assigned at definition order) but print LATER than the pinned longtable. Number
order (source) and print order (page) diverge.

Fix that worked: put `\clearpage` immediately before the `\begin{longtable}`.
This flushes all pending floats (the earlier 2.1–2.3) out to print FIRST, so
print order matches numbering. After the fix the `.lot` read 2.1→p66, 2.2→p67,
2.3→p68, 2.4→p69 — contiguous.

Diagnostic recipe (don't guess — read the aux/lot):
- `build/Chapter/<chap>.aux` → `\newlabel{tab:...}{{2.4}{...}}` gives the NUMBER.
- `build/main.lot` `\contentsline{table}{\numberline{2.4}...}{66}` gives the PAGE.
- If number order ≠ page order, you have float drift. `\clearpage` before the
  pinned element (or converting the drifting floats to `[H]`) realigns them.

When to convert table→longtable at all: only when the table genuinely exceeds
one page height (the 889pt-class warning). A small 5-row table that warns
`Float too large` is usually just kept-at-bottom-of-page; longtable fixes the
overflow but introduces the ordering issue above, so always re-check the `.lot`
order after converting.

## 2. logic page number ≠ physical PDF page when rendering to verify

`.aux`/`.lot` page numbers are the PRINTED page (logical, e.g. roman front
matter then arabic body). `pdftoppm -f N -l N` wants the PHYSICAL PDF page,
which is offset by the front-matter pages. Rendering the logical number renders
the WRONG page and vision-check reports "this isn't the table you described".
Resolve the physical page first (grep the caption text across rendered pages, or
add the known front-matter offset) before `pdftoppm` + vision.

## 3. Review-subagent false-positive classes — VERIFY before fixing

The READ-ONLY multi-lens review pattern (3 subagents, parent verifies, fixes
serially) is in the main SKILL.md. These specific false positives recurred and
each was correctly REJECTED after parent verification — do not blindly apply
subagent "errors":

- **cite-key ≠ author name is NORMAL.** A language/content lens flagged
  "Sangetha et al. ~\cite{nawaz2024aiot}" and "Shi and Nekouei ~\cite{zhao2023encrypted}"
  as author mismatches. Cite keys are internal labels; verify the `.bib` `author`
  field actually matches the prose name (it did — Sangeetha, Shi/Nekouei). Not a bug.
- **Vision misreads Vietnamese diacritics on raster figures.** A figure-audit
  subagent reported "Giá thuyết" (wrong) where the TikZ source said "Giả thuyết"
  (correct) — vision read dấu hỏi ̉ as dấu sắc. Always confirm against the `.tex`
  source before "fixing" a diacritic the source already has right.
- **Locked sections override neutral-tone rules.** Content lens flagged
  "ưu việt"/"ưu thế vượt trội" in Mở đầu as non-neutral. But Mở đầu was locked to
  the đề cương gốc by the user, and both phrases were verbatim in that source →
  GHI NHẬN, do not edit. A hard user constraint (locked section) outranks the
  general neutral-baseline preference.

## 4. "Float too large" residual is graded, not binary

After fixing the big offender, a small residual (e.g. `Float too large by 12.3pt`)
is cosmetic and does NOT chặn nộp. Only the page-scale overflow (hundreds of pt,
real risk of clipped content) is worth a structural fix. Report the small one as
low-severity, don't chase it.
