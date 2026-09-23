# Thesis PRISMA consistency + figure audit

Use this when người dùng asks to make a thesis/systematic-review manuscript consistent after a corpus count changes (e.g., 68 -> 64 unique studies), or asks whether the appendix has enough detail and whether all in-text numbers/figures match the PRISMA flow.

## Core workflow

1. **Treat the appendix/audit trail as the source of truth.** First identify the final PRISMA flow from appendix CSV/JSON/table evidence, then make the main text conform to it. Do not let old narrative numbers survive in Chapter 2/3/4/conclusion.
2. **Back up before broad consistency passes.** Copy the chapter `.tex` files, appendix, and bibliography to `_backups/<timestamp>/` before global edits.
3. **Use one canonical PRISMA flow everywhere.** For this thesis pattern the clean form was:
   - Identification: `627 -> 627`
   - Deduplication/cleaning: `627 - 203 = 424`
   - Title/abstract screening: `424 - 237 = 187`
   - Eligibility/full-text-or-metadata: `187 - 123 = 64`
   - Included/final core: `64`
   Avoid hybrid rows such as `123 candidates -> 56 added` in the main PRISMA table unless clearly marked as a supplemental audit trace; otherwise it confuses the final flow.
4. **Synchronize all derived counts and percentages.** Grep across included `.tex` for stale forms like `68 công`, `n=68`, `9/68`, `20/68`, `25/68`, `57/68`, `83.8`, `36.8`, `33.8`, `29.4`, and update them from the final unique corpus. Recompute percentages programmatically when possible.
5. **Vietnamese/form consistency matters.** Main narrative and PRISMA tables should use Vietnamese labels: `Xác định nguồn`, `Gộp lặp`, `Sàng lọc tiêu đề/tóm tắt`, `Thẩm định sự phù hợp bằng toàn văn hoặc metadata`, `Đưa vào phân tích`. Avoid leaving table headers/captions like `Eligibility`, `Included`, `candidate`, `title/abstract screening` unless they are raw audit statuses inside a CSV-derived longtable.
6. **Use careful wording for evidence level.** If some records are verified by full text and others by metadata, write `kiểm chứng bằng toàn văn hoặc metadata`, not `kiểm chứng toàn văn`. Keep `metadata/title-coded` limitations visible when counts come from titles/metadata.
7. **Figures are part of the integrity audit.** Do not only grep `.tex`. Run `pdftotext` on every included figure PDF and search embedded labels such as `n=68`, `n=81`, `n=120`, `n=148`. A figure can visually contradict the manuscript even when the caption is fixed.
8. **Regenerate or remove stale figures.** If included figures have old `n`, regenerate them from the final corpus. If stale figures are no longer included, move them to `_backups/unused_stale_figures_<ts>/` and exclude them from final zip so reviewers do not find contradictory artifacts.
9. **Patch captions and prose after figure regeneration.** Captions should say exactly what the figure represents, e.g., `tập 64 công trình lõi duy nhất`, `tái tạo từ bảng mã hóa đã loại trùng nội bộ`, or `mã hóa tiêu đề/metadata`.
10. **Package-gate the zip, not just the source tree.** After creating the handoff zip, inspect `unzip -l` for stale figure filenames and build/cache artifacts. Exclude old figure basenames globally, not only under `figures/ch03`, because copies may exist in `simulation/figures/ch03` or other subfolders.

## Verification commands/patterns

- Source stale-number grep:
  `grep -R -nE '68 công|68 nguồn|n=68|9/68|20/68|25/68|57/68|83\.8|36\.8|33\.8|29\.4|119 nguồn|56 thêm|chấp nhận thêm 56|123 ứng viên mới|tab:keywords|sec:coso_tongquan|sec:tieu_ket_1|toàn văn/metadata|Phụ lục A\.|local sources|Tốt nhất|n=120|n=81|n=148' Chapter/noidung_chap*.tex Chapter/ketluan.tex Chapter/phuluc*.tex figures/ch03`
- Included figure embedded-number check:
  `for f in figures/ch03/*.pdf figures/ch04/*.pdf; do pdftotext "$f" - | grep -oE 'n ?= ?(68|81|120|148)' && echo "$f"; done`
- Build gate: run project build script, then grep final log for `undefined`, `Citation.*undefined`, `Reference.*undefined`, `multiply defined`, `Fatal`, `Error`.
- Zip gate: `unzip -l <zip> | grep -Ei '(_backups|scratch|tmp_archive|\.aux|\.log|\.xdv|\.fls|\.fdb_latexmk|\.DS_Store|\.venv|combined_overview|control_strategy_distribution|control_strategy_pie|protocol_distribution_bar)'` should return empty.

## Figure-provenance audit (script-generated charts can carry FABRICATED/STALE/WRONG-N data while prose is correct)

When người dùng points at a figure and says it has wrong numbers, English text, or "thiếu sót", the fix is almost never the image — it is the SCRIPT that generated it. Trace every statistical figure to its generator before editing:

1. **Map figure → generator script.** `grep -rl <figure_basename>` across `scripts/` and `simulation/`. There are often TWO generators: a stale one with hardcoded/fallback numbers and a correct one. Real bug this session: `regenerate_verified_figures.py` synthesized `publication_trend`/`top_sensors` from `N_TOTAL` fallback `=81` and an entirely DIFFERENT corpus (whole `references.bib`, 104 entries) — those figures were NOT even included in the thesis but got pasted onto SLIDES. Meanwhile the 3 figures the thesis DID include (`stacked_bar_trend`, `heatmap_codesign`, `bubble_tradeoff`) came from `generate_q1_charts.py` with **hardcoded n=120** and an explicit comment `Tạo data giả lập` (fabricated data) for the bubble chart.
2. **Read the generator's data arrays inline.** If the script hardcodes counts (`data = np.array([...])`, `irrigation=[25,18]`, `energy_saving=[60,20,...]`) instead of reading the coding CSV, the figure is fabricated/stale by construction. A bubble/tradeoff chart whose axes are invented "to match the conclusion" is an integrity risk at defense — flag it, do not silently keep it.
3. **Regenerate from the real per-paper coding CSV**, counting programmatically. Source of truth = `bib_audit/lvtn_68_coding_per_paper.csv` joined with the audit trail for year. Write a fresh generator (`scripts/regen_ch3_figs_real.py`) that loads the CSV, asserts `N==expected`, and computes every cell by counting — never retype counts.
4. **Replace fabricated charts with REAL simulation data** when người dùng approves (e.g., bubble tradeoff → energy-saving% vs RMSE from `q1_benchmark_summary.csv`, sized by tx_rate). Caption must say `mô phỏng thật, kịch bản <scenario>`.

## Reconciling conflicting corpus counts (coded-total vs analysis-window)

Three sources disagreed this session: coding CSV = **68**, JSON summary = 56/54, manuscript prose = **64**. Do NOT just pick the manuscript number — diagnose. The reconciliation: `68 coded − 4 classic pre-2015 works (Van Henten 1994, event-triggered originals 2003/2013/2014) = 64 in the 2015–2025 search window`. So 68 = total coded, 64 = analysis set inside the search frame; both are legitimate for different sentences. Always check a year filter before assuming a count is wrong: `print sorted(years)`, count `<2015`. Once reconciled, sync EVERY table/prose number to the analysis set (this session: Table 3.1 and 3.2 still had the 68-corpus split — 27/9/11/55/23 — that had to become the 64-set counts 30/7/10/53/20).

## English labels surviving in matplotlib figures of a Vietnamese thesis

Subagent figure-audit flagged figs 4.2/4.3 (and partly 1.9/1.10/1.13) with ~100% English titles/axes/legends. These are raster/PDF charts from python scripts — Việt hóa at the SOURCE script, then regenerate, never edit the image:
- Patch `set_title`/`set_xlabel`/`set_ylabel`/`label=` strings to Vietnamese. KEEP standard terms untranslated: method names (TT-MPC, ET-MPC, ET-PID), RMSE, LoRa, °C, mJ/J, product names (Semtech SX1276), place abbreviations (ĐBSCL).
- Fix unit inconsistency at source too (this session: subplot trục ghi `mJ` 0–20000 nhưng legend ghi `J` → divide the cumsum by 1000 and label the axis `(J)` so axis and legend agree).
- Fix lặp ký hiệu like `Packet Loss % (%)` → `Tỉ lệ mất gói (%)`.
- The simulation scripts often need scipy/pandas in a throwaway venv (`uv venv` + `uv pip install --python <venv>/bin/python scipy pandas matplotlib seaborn`); `uv` venvs have no `pip` binary, use `uv pip install --python`.
- After regenerating, COPY to the exact filename the thesis includes (names differ: `q1_eval.pdf` → `q1_eval_greenhouse.pdf`), then render the page and vision-check.

## Logic-contradicting figure (number is "right" but tells the wrong story)

Fig 1.13 showed ETC sending 60 packets > TTC 50 while labeled "tiết kiệm băng thông" — physically backwards for a Chapter-1 pedagogical figure. Root cause read from `etc_stc_comparison.py`: the toy model has only natural decay (no reference/disturbance to track) and each trigger multiplies `x *= 0.9`, creating an artificial jump that re-triggers → self-firing loop inflates ETC's count. When a figure's numbers contradict its own message, read the generator's model assumptions; offer người dùng explicit options (fix the toy model to be textbook-correct B1 / drop the misleading panel B2 / replace with real benchmark numbers B3) and STOP for his choice — this touches scientific correctness, not just formatting.

## Extracting thesis TikZ figures as standalone vectors for slides

When a slide needs an architecture/PRISMA diagram that exists in the thesis as TikZ-over-image or pure TikZ, do NOT copy just the background PNG (loses all arrows/labels — this session the slide showed a bare farm-map with no signal arrows). Instead extract the `tikzpicture` block, wrap it in a `standalone` document with the same `\usetikzlibrary{...}` (positioning, arrows.meta, shadows, fit, calc) + Vietnamese fonts (`fontspec`+`polyglossia` under xelatex), compile to a 1-page vector PDF, and include THAT. It carries every arrow/label baked-in and scales crisply. Pure-TikZ block-diagrams (e.g. fig 1.3 functional blocks) are better slide material than spatial-layout raster images; on slides give them a full-width slide rather than cramming into a 48%-width column (text becomes unreadable).

## Subagent figure-audit: verify diacritic false-positives

A read-only vision subagent is great for fanning out over 25 figures, but vision OCR misreads Vietnamese diacritics. This session it reported fig 2.1 had a typo "Giá thuyết" → the source actually said "Giả thuyết" (correct); it read the hỏi mark (̉) as a sắc. Always grep the SOURCE for any character-level error a vision pass reports before "fixing" it — and bundle the subagent task as READ-ONLY (render PNG + report only) so it cannot act on its own misreads.

## Pitfalls

- Fixing captions is not enough: PDF figures often contain their own `n=...` labels.
- A supplemental candidate/eligibility table can be useful, but if it says `123 -> 56 added` beside the main PRISMA table, readers may infer a second final corpus. Present it as audit trace only, while the main flow remains `187 -> 64`.
- Do not keep old unused figures inside the final handoff zip. A reviewer can open the zip and find contradictory `n=120` even if the manuscript no longer includes that figure.
- Avoid claiming `final-ready` solely because the PDF builds. For systematic-review theses, consistency of PRISMA flow, final corpus count, appendix trace, captions, and embedded figure text is part of the readiness gate.
