# Manuscript results-reproducibility audit (numbers/tables/figures ↔ code)

A different axis from the bibliography audit (`latex-reference-audit`): that one checks *citations*; this one checks whether the **reported numbers, tables, and figures are actually produced by executed code** — not hand-faked placeholders — and whether the prose numbers are internally consistent with the paper's own tables. Built from the "Toward Zero-Touch Smart Agriculture" manuscript audit.

Trigger phrasing (người dùng): "các số liệu/bảng/biểu đã được chạy đúng chuẩn theo những gì trình bày trong bài chưa", "chuẩn cả tham số chưa", "verify số liệu", or any request to confirm a draft's results before submission.

## Core principle: RUN the code, don't read the README
The deliverable is real execution output, never a description. When the user has (or references) a reproduction repo:
1. Clone it (`.git` can be heavy → clone may time out at 600s but the working files usually land first; verify the files exist rather than trusting the exit code).
2. Build an isolated env with `uv venv` + `uv pip install`. **torch is the long pole** — install the **CPU-only** wheel (`--index-url https://download.pytorch.org/whl/cpu`, or the repo's CPU extra) in the **background with `notify_on_complete=true`**; the CUDA wheel is hundreds of MB and will blow the foreground timeout. Sci stack (numpy/scipy/matplotlib) installs fast in foreground.
3. Run the actual simulation/training script in the background with `notify_on_complete=true`. TD3 + FedAvg + multi-experiment runs take minutes.
4. Read the machine-written `results.json` / `REPORT.md` the run emits, and diff THOSE numbers against the manuscript `.tex` — table by table, prose-claim by prose-claim.

## The two killer defects (this is what the user actually wants caught)
1. **Figures/numbers are hand-drawn placeholders, not simulation output.** Tell-tale: a `generate_all_plots.py` (or similar) that builds every figure from closed-form synthetic functions — `np.exp(...)`, hard-coded arrays, `np.random.normal` noise — with **no call into the actual model** (no TD3, no FedAvg, no env). Such a file *looks* like it produces results but is cosmetic. The real repo instead runs the model and writes `results/*.png` + `results.json`. A reviewer who opens the plotting script sees the fakery instantly → highest submission risk. Always open the figure-generating script and check whether it imports/calls the real algorithms or just draws curves.
2. **Orphan / self-contradictory prose numbers** — percentages stated in body text that (a) have no source in the repo output AND/OR (b) contradict the paper's own tables. Recompute every prose percentage from the paper's own table cells before trusting it. Real catches:
   - "sensing energy giảm 27.3% vs FIXED" while the energy table shows 3.4 vs 7.1 → the true figure is 52.1%. Flat wrong.
   - "FL tiết kiệm 12.5% vs IND" while totals 20.5 vs 23.3 → 12.0%.
   - Numbers with no repo provenance at all ("+8.7% belief fusion", "63% accuracy after 50% mission", "72% sparsification overhead", "Prediction Accuracy 89.7%") — the run never emits them. Flag as unsourced; they must be regenerated or cut.
   - Cross-table unit mismatch: one table lists `Hyperspectral 50MB→2.5MB`, another lists `Multispectral 12800KB→640KB` for the "same" payload story. Inconsistent units/values invite reviewer suspicion.

## Reporting shape the user expects
Split findings cleanly into **KHỚP** (magnitudes that match executed code — keep) vs **CÓ VẤN ĐỀ** (placeholder figures, orphan numbers, contradictions — fix before submission), each in a markdown table with `Bài ghi | Repo chạy thật | Khớp?`. Then offer concrete remediation options (e.g. (A) swap in the repo's real figures + consistent results section, (B) just patch the contradictory prose numbers) and let him choose — don't silently rewrite.

## Backfilling author affiliations from prior papers
When a draft has placeholder affiliations (`University of`, `@example.edu`):
- Pull the **real** affiliation/email/ORCID block from the author group's most recent prior paper in `SAS/<author-group>/` (e.g. the ICCSIT/IEEE Access `.tex`). Grep often misses the author block (macro differences) — read the header lines directly around `\author{`.
- Map each author to the correct institution (the group spans **Gia Dinh University** + **the university** sub-units: *Institute of Open Education and IT* and *College of Education*). Use real ORCIDs/emails verbatim.
- For IEEEtran, render with `\IEEEauthorrefmark{n}` superscripts tying names to affiliation lines. Preserve the draft's existing author ORDER and corresponding-author designation unless told otherwise; flag the choice ("I set X as corresponding as in the prior paper — say if you want Y").

## Pre-submission LaTeX hygiene that recurs here
- **Markdown bold leaked into `.tex`**: `**18.2\%**` renders as literal asterisks, not bold. Grep for `\*\*` and replace with `\textbf{...}`. AI-drafted results sections are full of these.
- Always backup to `_backups/<ts>/` before editing (standing rule), then `latexmk -g` and confirm EXIT 0 + page count as real build evidence — never call the manuscript "ready" without a clean build.
- File may live in `~/Downloads/` rather than `SAS/Research/<project>/`; offer to relocate to the convention but don't move without asking.
