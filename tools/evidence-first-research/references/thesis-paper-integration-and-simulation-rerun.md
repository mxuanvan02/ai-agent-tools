# Thesis integration of derivative papers + simulation rerun

Use this when người dùng says derivative papers (e.g. bài bandwidth-scheduling, bài AoI-greenhouse/bài probe-transmit) are part of a thesis and asks to adjust the thesis, especially to rerun the thesis simulation.

## Core workflow

1. **Classify as EXECUTE, not advice.** Observable success is: thesis text updated, derivative papers positioned as thesis branches, simulation pipeline rerun, numbers synchronized, and PDF built.
2. **Inspect the thesis structure first.** Find `main.tex`, included chapters, appendix files, publication/product sections, simulation directory, and existing generated figures/CSVs.
3. **Respect thesis front-matter / proposal boundaries.** If người dùng says the **Mở đầu / đề cương** must not be touched, do not add derivative-paper names or new framing there. Restore it to the original state if needed. Put linkage only in body chapters, conclusion, and included appendices.
4. **Backup before edits.** Copy chapters being changed (usually discussion/simulation chapter, conclusion, appendix/publication files) and relevant simulation scripts to `_backups/<ts>/`. If Mở đầu is off-limits, back it up only for comparison/revert, not for new content.
5. **Fix reproducibility blockers, not just prose.** If a simulation script writes to an absolute stale path (e.g. `/home/node/...`), patch it to use a path relative to the script/project so the pipeline is portable. Treat this as a code fix and rerun tests/pipeline.
6. **Rerun the actual simulation pipeline.** Prefer the project master script (`run_all.sh`) after installing deps in a local venv. Do not keep old illustrative numbers if the rerun produces different metrics.
7. **Programmatically derive headline numbers from fresh CSV.** Compute means/percent changes directly from the rerun output (e.g. `q1_benchmark_summary.csv`), then patch tables/prose/conclusion. Avoid retyping from terminal logs.
8. **Copy fresh generated artifacts into the thesis tree.** Put PDFs/CSVs under the figures or appendix paths used by LaTeX, then update `\includegraphics`/tables accordingly.
9. **Position derivative papers neutrally and hierarchically.** Phrase them as specialized branches of the same Plant--Network--Control--Evaluation / control--communication co-design problem, not as unrelated papers and not as the thesis objective:
   - **bài AoI-greenhouse / bài probe-transmit:** if it is the direct simulation continuation, say it extends the simulation from “when to transmit” to “which sensor update has the highest control value under channel/budget constraints.”
   - **bài bandwidth-scheduling:** if not the simulation backbone, keep it as a related/broader product branch on risk-aware bandwidth/resource allocation for greenhouse NCS.
10. **Add papers where the built thesis actually includes them.** A `publication.tex` file may exist but not be included by `main.tex`; if so, add the PDFs to an included appendix (e.g. `phuluc.tex`) or update `main.tex` deliberately.
11. **Build with the project's intended engine.** If `fontspec` is used, `pdflatex`/`latexmk -pdf` will fail; use the project `build.sh`/`xelatex` path. If stale `.toc/.aux` causes `\xpg@aux` errors after switching engines, clean generated build files and rebuild.
12. **Verify the PDF, not only build exit.** Use `pdftotext`/grep or equivalent to confirm new terms and numbers appear: `bài bandwidth-scheduling`, `bài AoI-greenhouse`, fresh percent reductions, and appendix entries. Report remaining old undefined refs/citations separately.
13. **Package cleanly only after build.** Create a clean ZIP excluding `_backups`, `scratch`, `tmp_archive*`, build outputs, aux/log/xdv/fls/fdb files, `.venv`, `.DS_Store`; test the zip and provide the current PDF separately.

## RLM final-readiness review pattern for thesis chapters

When người dùng asks to “rà soát lại nội dung” and mentions **RLM phân rã**, run read-only parallel reviews before editing:

1. **RLM-A — Chapter 2 / methodology:** PRISMA flow, search strings, inclusion/exclusion, extraction/coding, RoB, reproducibility, labels/cites.
2. **RLM-B — Chapter 3 / quantitative corpus:** verify `n`, duplicates, percentages, figure/table source trace, claims based on title/metadata vs full text.
3. **RLM-C — narrative coherence:** Chapter 3 gaps → Chapter 4 simulation → conclusion and derivative-paper linkage; catch stale narrative like “irrigation” when current simulation is greenhouse.
4. Subagents are **READ ONLY**. Parent verifies findings, then patches serially. Do not let agents write concurrently in thesis repositories.

## Pitfalls and fixes from thesis integration sessions

- **Do not preserve old narrative numbers.** If old text says ETC/STC reduces packets 77.8--80.6% but fresh CSV says ET-MPC reduces energy 65.3% and transmissions 75.1%, rewrite the narrative around the fresh result.
- **Avoid absolute-path simulation outputs.** A script that saves to a previous workstation path can pass code review but fail on rerun; patch to `Path(__file__).parent` or project-relative paths.
- **Publication file may be dead code.** Before adding papers to `Chapter/publication.tex`, check whether `main.tex` includes it. If not, add the PDFs to an included appendix or explicitly include the publication chapter.
- **Corpus `n` must be unique, not just line count.** If an appendix says “68 công trình lõi” but 4 titles/DOIs are duplicated, either replace the duplicates with valid sources or revise the corpus to `n=64` and update every table, percentage, caption, conclusion, appendix, and audit note. Use the unique corpus as the source of truth.
- **Figures can silently use the wrong corpus.** If Chapter 3 figures show `n=120` or another exploratory corpus while captions say `n=64/68`, either regenerate figures from the final corpus or explicitly label them as exploratory/trend illustrations and make tables the source for final percentages.
- **Title/metadata coding is weaker than full-text coding.** If protocol/control counts are based on titles/metadata, say so and avoid claims like “verified full text” for every coded variable unless the full-text audit actually exists.
- **Stale object narrative breaks coherence.** If the current simulation is greenhouse temperature, remove old “irrigation/soil-moisture slow plant” framing in Chapter 4; present LoRa/LPWAN-like channel as a stress-test if it is not a deployment recommendation for greenhouse.
- **Build success is not enough.** Grep log for undefined refs/citations and PDF text for stale counts (`68`, `9/68`, `tab:keywords`, etc.). Fix labels (`tab:keywords` → actual label), missing bib entries, and chapter refs before packaging.

## Suggested wording pattern

- Body chapter: “Trong phạm vi mô phỏng của luận văn, hướng liên hệ trực tiếp là **bài AoI-greenhouse**... bài bandwidth-scheduling được đặt ở vai trò bổ trợ trong mạch nội dung...”
- Conclusion: “bài AoI-greenhouse là phần phát triển trực tiếp từ mô phỏng kiểm chứng; bài bandwidth-scheduling là nhánh sản phẩm khoa học liên quan, mở rộng cùng trục đồng thiết kế sang phân bổ tài nguyên theo rủi ro.”

## Do not do

- Do not add bài bandwidth-scheduling/bài AoI-greenhouse to **Mở đầu / đề cương** if người dùng says not to touch it.
- Do not call the thesis “final-ready” solely because PDF builds. Final-ready requires: clean refs/cites, corpus consistency, figure/table source consistency, and narrative coherence.
