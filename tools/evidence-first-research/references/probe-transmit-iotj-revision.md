# bài probe-transmit IoTJ revision notes (session 2026-06-17)

Use this as a compact precedent when revising người dùng's LaTeX manuscripts for IEEE IoTJ or similar venues.

## Workspace convention learned

- Research manuscripts belong under `SAS/Research/<project-name>/`, not directly under `SAS/`.
- Repo/code used for verification can live under `SAS/Research/_repos/<repo>/`.
- Keep review/diff artifacts inside project-private folders such as `_review_artifacts/` or `_review_artifacts_final/`; only copy final PDFs to the project root.

## bài probe-transmit-specific correction pattern

Problem discovered: manuscript narrative mixed a weak/optional correlation branch with the real contribution.

Correction chosen by người dùng:
- Remove `corr`, `correlation credit`, `debt+corr`, and `debt-only` entirely from the main story.
- Present bài AoI-greenhouse as: threshold-aware urgency + service debt.
- If the opposing branch is removed, do not keep labels like `debt-only`; just call it `debt`.
- Search broadly: title, abstract, contributions, system model, related work, methodology, evaluation, discussion, conclusion, figure comments/styles, and generated/artifact text.

## Result verification pattern

When a manuscript has public code/results:
1. Clone/pull the canonical repo the user specifies.
2. Identify result files (`docs/*.csv`, `docs/*.json`, reports).
3. Compute means/CIs from the correct branch/variant, not from the best-looking table.
4. Update Data and Code Availability with the canonical repo link.

For bài probe-transmit, canonical repo was:
`https://github.com/OWNER/bài probe-transmit`

Relevant result source:
- `docs/ablation_results_30windows.csv`, variant `+debt -corr`, for the final no-correlation claim.

Checked values:
- loss mean `0.002662`, CI95 `0.001126` -> manuscript `0.0027 ± 0.0011`.
- missed violation mean `0.041376%`, CI95 `0.018278%` -> manuscript `0.041 ± 0.018%`.
- probe Jain `0.959`, payload Jain `0.952`, max age `41.23`.

## Math clarity preference

Người dùng explicitly prefers math to be very clear and step-by-step. For theorem/proof edits:
- Define helper constants explicitly, e.g. `K = ceil(Vmax/w)`.
- Start from score comparison, then algebraically transform line by line.
- State boundedness assumptions before using them.
- Explain the mechanism after each inequality: what blocks, what resets, what cannot block again.
- Avoid `it is clear`; use numbered or named steps.
- If a claim is stronger than the proof, weaken the theorem rather than patching with handwaving.

## Highlighted PDF workflow note

For multi-file LaTeX:
- Use `latexpand main.tex` on both baseline and revised sources before `latexdiff`.
- `soul`/`\hl` can fail inside math/align. Prefer `latexdiff --type=UNDERLINE` or `--type=CFONT --math-markup=off`; if yellow is required, override `\DIFadd` to use `\colorbox{revYellow}{...}` and keep math markup off.
- A diff PDF may retain undefined references to deleted labels; still verify that the PDF exists and clean PDF builds separately.
