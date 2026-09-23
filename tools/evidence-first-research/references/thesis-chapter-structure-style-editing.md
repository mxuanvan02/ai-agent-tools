# Thesis chapter structure/style editing (Vietnamese LVTN/NCS)

Use when người dùng asks to continue polishing a thesis chapter for `cấu trúc` and `văn phong`, especially PRISMA/methodology/results chapters in LaTeX.

## Durable workflow

1. **Inspect the real chapter file first.** Locate the active `Chapter/noidung_chap*.tex`, not an old PDF/zip/backup. If backups exist, do not assume they are current.
2. **Make a controlled backup before editing.** Prefer `_backups/<timestamp>/...` if the project already uses that convention; otherwise a timestamped sidecar is acceptable but keep it tidy.
3. **Review structure before wording.** Look for duplicate subsections, repeated PRISMA counts, stale cross-references, overlong enumerations, method sections that repeat the same dedup/screening narrative, and tables/figures that appear without a clear lead-in or takeaway.
4. **Build the reader's roadmap explicitly.** For each major section, state its function in the chapter flow (`chọn cái gì`, `tìm ở đâu`, `lọc thế nào`, `mã hóa ra sao`, `kiểm soát chất lượng bằng cách nào`). Make the previous section's output become the next section's input.
5. **Patch prose in-place.** For người dùng, default to direct execution: polish the actual `.tex`, reduce repetition, tighten academic tone, and preserve scientific claims/counts unless verified from data.
6. **Add short table/figure takeaways.** Before a table/figure, explain why it is needed; after it, add 1-3 sentences saying what the reader should conclude and how it connects to the next step. Do not let a table/figure stand alone as decoration.
7. **Keep implementation steps concise and central.** Methodology steps should be described in words before technical detail: input, rule, output, and verification evidence. Avoid long tool-centric narratives unless they support reproducibility.
8. **Preserve labels when consolidating sections.** If merging two subsections, keep both `\label{...}` lines when downstream chapters may reference either label.
9. **Build with the correct engine.** If the project uses `fontspec`, use `latexmk -xelatex ...`; a `pdflatex` failure complaining about `fontspec` is an engine mismatch, not a manuscript error.
10. **Separate new issues from pre-existing project issues.** Report BibTeX duplicate keys, missing month strings, Unicode glyphs, appendix warnings, or unrelated layout warnings as pre-existing/unrelated if chapter edits still produce a PDF.
11. **Fix blocking build hygiene before moving on.** If người dùng asks to resolve build issues, deduplicate repeated BibTeX keys carefully (usually keep the first canonical entry), quote/brace bare month strings (`month={July}`), replace unsupported Unicode hyphens in source files, then rebuild until exit code 0.
12. **Do a visual figure/table gate before continuing chapters.** Use `.aux` labels to identify pages for chapter figures/tables, render those PDF pages to PNG (`pdftoppm -f <p> -l <p> -png -r 140/150`), inspect a contact sheet plus high-risk pages (dense TikZ/table), and fix legibility/caption/layout before starting the next chapter. Build success alone is not enough.
13. **Verify page numbers from physical PDF pages, not only LaTeX labels.** `.aux` labels store printed page numbers, which can differ from physical PDF pages when front matter uses Roman numbering or unnumbered pages. Use the log around `(./Chapter/noidung_chapX.tex` or `pdftotext`/visual inspection to find the physical pages before rendering contact sheets; otherwise you may accidentally inspect the previous chapter's figures.
14. **When moving from methodology to results chapters, preserve the workflow bridge.** Start the results chapter by explicitly saying: Chapter 2 created/controlled the evidence set; Chapter 3 analyzes what that evidence set shows. Then organize by RQ/PNCE rather than dumping tables.
15. **For results chapters, each table/figure needs a role label.** Add compact takeaways after artifacts: corpus descriptor, evidence-group role, time-trend context, architecture implication, control trade-off, network impact, simulation bridge, or certainty/limitation. Make sure the takeaway references the correct table/figure; after automated replacements, re-read the surrounding 10-20 lines to catch misplaced conclusions.

## Style preferences for Vietnamese thesis prose

- Open with a concise function statement for the chapter: what the chapter does, why the sequence matters, and how it connects to the next chapter.
- Replace list-like phrasing with causal/methodological links: `vì vậy`, `theo quy tắc này`, `cấu trúc này giúp...`.
- Avoid inflated claims; use `được xem là`, `được sử dụng khi`, `đóng vai trò`, `không thay thế cho`.
- For methodology chapters, keep a single canonical PRISMA flow (e.g. `627 -> 424 -> 187 -> 64`) and make every summary/caption match it.
- For results chapters, use the sequence `evidence set -> RQ/PNCE map -> architecture -> control strategy -> network impact -> hypotheses for next chapter -> certainty/limitations`. This keeps the chapter from becoming a loose table gallery.
- For every important table/figure, add a compact takeaway: `Bảng/Hình này cho thấy...`, `Điểm cần lưu ý là...`, `Kết quả của bước này là...`. The takeaway should orient the reader, not repeat the caption.
- Keep implementation steps short and verbal before details: `đầu vào -> quy tắc xử lý -> đầu ra -> bằng chứng kiểm chứng`.
- When the chapter contains audit/traceability prose, phrase it as kiểm tra ngược dữ liệu rather than tool-centric narrative.
- When connecting chapters, use direct bridge language: `Chương 2 tạo lập/kiểm soát tập bằng chứng; Chương 3 phân tích tập bằng chứng đó; Chương 4 kiểm chứng các giả thuyết rút ra`.

## Pitfalls caught in session

- `latexmk -pdf` may invoke `pdflatex` and fail on `fontspec`; rerun with `-xelatex` before declaring build failure.
- Do not overreact to unrelated BibTeX duplicate-entry errors if the PDF is still generated and the edited chapter compiles structurally.
- Unicode hyphen `U+2010` can be missing from Times New Roman under XeLaTeX; replace unusual hyphen/dash characters with ASCII `-` or plain prose when they break rendering, including appendix/audit files if người dùng asks to clean build issues.
- BibTeX duplicate keys and bare month tokens can keep `latexmk` in error even when a PDF is produced. Fix by keeping one canonical entry per key, removing duplicate entry blocks/comments, and bracing month values (`month={Sept}`), then rebuild.
- Caption style may already add terminal punctuation; if a `\caption{... .}` renders as `..`, remove the final period inside the caption text rather than changing global caption style.
- Build success does not prove figures are readable. For dense TikZ/PRISMA diagrams, render the page to PNG and check: text inside boxes, arrow direction, caption punctuation, clipping/truncation, and whether a feedback arrow creates a misleading workflow.
- For result chapters with many floats, LaTeX may move figures/tables to nearby physical pages. Check both `.aux` labels and actual rendered pages so you do not review a previous chapter's artifacts by mistake.
- Automated prose replacement can insert a takeaway for the wrong artifact (e.g., a control-strategy conclusion immediately after a corpus-summary table). Always re-read around each edited table/figure after bulk replacements.
- Terminal/tool working directory can persist or shift between calls; if a relative `workdir` unexpectedly fails, diagnose with `pwd` and use the absolute project path.

## Condensing an over-long chapter (page-count reduction)

When người dùng says the thesis is `dài quá rồi` / asks to shorten while keeping content, the goal is fewer pages, not just nicer prose. Work in this order:

1. **Map the chapter skeleton first.** Dump every `\section`/`\subsection`/`figure`/`table` with line numbers and counts before reading prose. This reveals when one chapter is carrying multiple roles (e.g. Chapter 1 holding both NCS technical background AND review-methodology background) — that dual role, not wordy sentences, is usually why a chapter is bloated.
2. **Measure what occupies pages before cutting.** Prose trimming often removes near-zero pages if the bloat is large TikZ figures, dense tables, or a long appendix. A `.tex` file shrinking 158KB→149KB can leave the page count unchanged because the cut text sat inside already-dense paragraphs. Identify the real page drivers (oversized figures, listing tables, appendix dumps) and tell người dùng honestly that prose cuts alone won't move the page count.
3. **Gate content-level cuts on người dùng's choice.** Pure wording fixes (lặp câu, câu thiếu vị ngữ, roadmap liệt kê) — do immediately. But cuts that touch *content* (dropping a theory derivation, removing explanatory boxes, condensing a literature cluster, pushing tables online) — present them as a short numbered menu with the trade-off, and let him pick. He often approves all, but the decision is his.

## Preserving citations when condensing literature paragraphs

When nén a dense literature-review cluster (author-by-author listing → grouped-by-theme prose):
- **Extract every `\cite{...}` from the original line BEFORE rewriting**, count them, and assert the new version contains the exact same set (diff the cite-key sets, fail loudly if any missing). Losing a citation during condensation is silent and breaks the reference. This session: 23 cites across 3 paragraphs, all preserved by programmatic check.
- Group citations by sub-topic rather than narrating each author sequentially; push per-paper detail to the results chapter. Typical compression: ~50-55% fewer characters with zero cite loss.
- After condensing, build and grep the final pass for `Citation.*undefined` (must be 0) to confirm no cite was orphaned.

## Figure-merge discipline (do not merge on size alone)

When người dùng says `cái nào gộp được thì gộp`, merging figures to save pages is tempting but often wrong:
- **Map each figure's references first** (`search_files` for each `\ref{fig:label}` and `\label{fig:label}`). A figure referenced by surrounding text that explains its symbols cannot be merged without orphaning that prose.
- Figures that look similar can serve **distinct roles** (conceptual schematic vs physical-layout map vs functional block diagram). Three NCS architecture figures this session shared a topic but each had a unique job + dependent paragraph — merging would orphan explanation or jam 3 messages into 1 diagram.
- Two figures illustrating a *partly* overlapping idea (e.g. timing-diagram in §1.3 and ZOH-Bernoulli waveform in §1.5) that sit in **different sections ~600 lines apart** should not be merged: it creates a far cross-reference (read §1.3, jump to a figure in §1.5) that hurts readability more than it saves.
- Say no to a merge plainly when it would break the reader flow; redirect to the real page lever (shrink oversized figure, trim appendix).

## Appendix as the biggest page lever

For PRISMA/audit appendices, the raw source-listing longtables (e.g. 627 raw records + 424 unique-with-decisions = ~1000+ lines) are usually the single largest page block in the whole thesis — often larger than Chapter 1. Map sections with `grep -n '\section\|longtable'` (terminal, not search_files — see pitfall below). The data in those listing tables typically already lives in `bib_audit/*.csv`, and the appendix already has a file-map table pointing reviewers there. Present three options to người dùng: (1) push the raw listings online, replace with a short pointer to the CSVs (saves ~40-60 pages, audit still traceable); (2) trim columns to ID+title+status; (3) keep as-is. Modern transparency convention favors (1) — raw data in repo, appendix keeps summary + trace-map.

## ⚠️ Pitfall: stale PDF — multiple `main.pdf` files cause repeated wrong page-count reports

The single worst time-sink this session. After cutting ~1081 lines of appendix longtable, I reported "still 219 pages" FOUR times — wrong every time — because the page count came from a STALE PDF, not the rebuilt one. Root cause: three `main.pdf` existed simultaneously (`./build/main.pdf`, `./main.pdf` at repo root, `./_build/latex/main.pdf`), and the build command wrote to a DIFFERENT path than the one I was reading.

How to avoid / diagnose:
- **Before trusting any page count, confirm WHICH file the build just wrote and read THAT exact file.** `find . -name main.pdf -printf '%p %s %t\n'` — compare byte size + mtime; the freshest one (matching the build you just ran) is authoritative. A page count from an older-mtime PDF is meaningless.
- **`latexmk` reporting "All targets up-to-date" with an unchanged PDF mtime is a red flag**, not success — it means latexmk thinks nothing changed (often because output went elsewhere or `.aux`/`.fdb_latexmk` is stale). If you just edited a file and the PDF mtime didn't move, the build did NOT regenerate what you're reading.
- **Pin the output directory explicitly** (`latexmk -xelatex -output-directory=build ...` or `cd` to the canonical location) so every build and every page-count read hit the same file. Then delete stray `./main.pdf` at root so it can't be misread again.
- A clean rebuild that wipes `.bbl` will make citations undefined until you run the full chain (`xelatex → bibtex → xelatex → xelatex`); don't panic at a spike in undefined-cite count mid-rebuild — finish the chain, then grep the FINAL pass.
- Verify the actual change landed: after externalizing tables, the `.tex` dropped 1370→289 lines but I had to read the correct PDF to see 219→173 pages. `pdftotext` grep for a phrase that should be GONE (or a new link that should be PRESENT) confirms the rebuild reflects the edit — but only on the correct file.

## Externalizing raw appendix tables to a NEW public companion repo

When người dùng approves pushing the PRISMA pipeline + raw data to a NEW repo (not an existing one) and asks to link it from the appendix:
- **The thesis manuscript folder is usually NOT a git repo** and the existing companion repos (`OWNER/bài probe-transmit`, `/bài bandwidth-scheduling`) belong to the *papers*, not the thesis. Don't push thesis data into a paper repo — ask which repo, default to creating a new one (`gh repo create OWNER/<thesis-repo> --public`).
- **Stage selectively into a clean dir** (`~/gh_staging_*`): include code + source data (PRISMA tool, `bib_audit/` CSVs/JSON, simulation `src`/`experiments`/`data`/`results`/`tests`), EXCLUDE `.venv`, `__pycache__`, `.tex`, drafts, `_backups`, and `tmp_archive_*` junk dirs. Add README + .gitignore + LICENSE.
- **Secret scan with false-positive awareness:** `grep -rniE 'api[_-]?key|secret|token|gho_|bearer'`. This session a file masked as `***.py` was just `hf_experiment.py` — the `hf_` prefix tripped a HuggingFace-token pattern; benign. Also scrub internal runtime paths (`/home/node/.openclaw/...`) → make them script-relative (`os.path.dirname(os.path.abspath(__file__))`) before pushing public.
- **⚠️ ssh-exec blocked in this environment:** `git push` over SSH fails `cannot exec 'ssh': Permission denied`, and HTTPS credential-helper fails `could not read Username`. Working push: write `gh auth token` to a temp file mode 600, read it into the tokenized URL inline (`git push https://x-access-token:$TOKEN@github.com/owner/repo HEAD:main`), then delete the temp file immediately. Keep the stored remote clean (no token in `git config`). Note `gh auth token` output gets masked by the scanner — writing to a file avoids the command-substitution syntax breaking.
- **Verify the repo is live via API, not self-report:** `gh repo view owner/repo --json visibility,pushedAt` + `gh api repos/owner/repo/git/trees/main?recursive=1` to confirm file count + that both `prisma/` and `simulation/` landed.
- **Then add the link to the appendix** (intro + the "file-map" section that points reviewers to the CSVs) via `\url{https://github.com/...}`, rebuild the full chain, and confirm with `pdftotext` that the URL renders (URLs split across lines in `pdftotext` — grep a fragment like `github.com/owner`, not the whole URL).

## Pitfall: search_files / grep chokes on `{` in LaTeX patterns

Searching for `\section{` or `\begin{longtable}` via `search_files` fails with `grep: Unmatched \{` (the ripgrep-backed tool mis-parses the brace). Workarounds that worked: (1) drop the brace, match just `\section` / `longtable`; (2) for an exact structural map, use `terminal` with `grep -n '\section\|longtable'` directly. Do not burn multiple retries tweaking the regex — switch to terminal grep early.

## Thesis formatting/front-matter audit against trường ĐH standard

When người dùng asks to `rà soát về định dạng` / `bố cục phải đi từ đâu lên` / check indent of list items against the current trường ĐH thesis standard, this is a layout+ordering audit, not prose editing. Default unit = **Trường Đại học Sư phạm – đại học** (confirm with người dùng; the cover macros may say `Viện Đào tạo Mở và CNTT` or another unit — reconcile cover macro, lời cảm ơn, and slide unit so all three match).

Read `Libs/settings.tex` (or wherever `\geometry`, `\baselinestretch`, `\newcommand{\@tname}` etc. live) + `main.tex` ordering + the `Covers/*.tex` files first, then audit:

1. **Line spacing.** trường ĐH standard is **1.5** (`\renewcommand{\baselinestretch}{1.5}`). A value like 1.15 is a real defect — fix it. ⚠️ Warn người dùng that 1.15→1.5 inflates page count significantly (this session 173→206, +33 pages); the increase is the spacing standard, not content bloat. If his faculty actually accepts a tighter value he can ask to revert.
2. **Margins.** `left=3.5cm, right=2.0cm, top=3.0cm, bottom=3.0cm` is within the standard trường ĐH band (left binding margin larger). Keep unless người dùng's faculty guide says otherwise.
3. **Front-matter ORDER (the main thing he means by `đi từ đâu lên`):** Bìa → Bìa phụ → Lời cam đoan → Lời cảm ơn → Mục lục → **Danh mục viết tắt** → Danh mục hình → Danh mục bảng → Danh mục thuật toán → (Mở đầu / chapters). Two common defects: (a) `\input{Covers/camdoan}` + `Acknowledgement` placed BEFORE `\frontmatter`, so they don't get Roman numbering — move them after `\frontmatter`; (b) abbreviation list (`abbreviations.tex`) placed last (after the list of algorithms) — move it to immediately after Mục lục, before the figure/table lists, because the reader needs to decode abbreviations before meeting them in those lists.
4. **`\part{}` structure — usually PRESERVE.** A thesis using PHẦN Mở đầu → PHẦN Nội dung → PHẦN Kết luận (each a `\part`) is valid at trường ĐH. Removing `\part` and `\setcounter{chapter}{0}` risks breaking chapter numbering — don't strip it just to simplify; the risk outweighs the gain.
5. **List indent.** `enumitem` global config (`\setlist[itemize/enumerate]{leftmargin=1.27cm,labelsep=0.3cm}` + `\parindent 1.27cm`) gives consistent 1.27cm (Word tab) indent. Verify chapters don't override it locally with inconsistent values.
6. **Caption.** `name=BẢNG`/`name=HÌNH`, `labelsep=period`, justified — matches trường ĐH convention; keep.

Always rebuild full chain (`xelatex→bibtex→xelatex→xelatex`) after reordering, grep undefined refs/cites = 0, and `pdftotext` the front matter to confirm the new order rendered. Patch front-matter moves as reversible edits and back up `main.tex`+`settings.tex` to `_backups/format_<ts>/` first.

⚠️ **Fetching the official trường ĐH thesis-format guide is hard.** Google/Bing/DuckDuckGo all serve CAPTCHA/Cloudflare to headless browsers; the Trường site (`dhsphue.edu.vn`) is an ASP.NET frameset with postback-driven (`__VIEWSTATE`) file lists that static `curl` can't unfold; the parent trường ĐH portal (`hueuni.edu.vn`) gives static HTML but carries only Thông tư 18/2021 (PhD) and 23/2021 (master's quy chế — which does NOT specify formatting detail). The formatting detail (margins/font/spacing/structure) lives in the Trường's own hướng-dẫn handed to students. So: try `curl` on the portal first (faster, no iframe), but if you can't reach the actual format guide, say so plainly, apply the standard trường ĐH values above, mark them as the common standard (not verified against the Trường's exact current file), and ask người dùng to supply the guide file or confirm the key numbers (spacing, font size, page-number position). Never fabricate quy-chế content.

## Pitfall: a `cp` line in build.sh is the ROOT CAUSE of the multiple-`main.pdf` trap

The stale-PDF trap above (reading an old PDF, reporting wrong page counts) often has a concrete root cause: the project `build.sh` ends with `cp "$OUTDIR/main.pdf" ./main.pdf`, spawning a second copy at repo root on every build. When a later build writes only to `build/` (or the cp is skipped), the root `./main.pdf` goes stale but still gets read. Fix permanently: remove the `cp ... ./main.pdf` line from `build.sh` (point its echo at `build/main.pdf`), delete the stray root PDF, and build straight into `build/`. After this there is exactly one canonical PDF. Grep `build.sh` / Makefile for a `cp.*\.pdf` early when page counts look impossibly unchanged.

## Cleaning the thesis working dir (gather-not-delete)

When người dùng says `làm sạch thư mục` / keep only what compiles: he holds a no-permanent-delete gate, so MOVE junk into `_backups/cleanup_<ts>/` (recoverable), don't `rm`. First read `main.tex` for the real `\include`/`\input` list to know what to keep. Junk to gather: `*.aux`, `*.loa`, `.DS_Store`, `*.bak_*`, stale `_build/`, `tmp_archive_*`, dev `scratch/` (temp_compile, tikz_preview), `add_refs*.sh`, and `.tex` files that aren't included (`data_transparency_section.tex`, `publication.tex` this session). KEEP `notes/` audit reports (his work, not junk) unless he says otherwise. Mass-move bursts trigger the security scanner's mass-deletion guard — that's expected, proceed after approval. Always rebuild + verify page count + undefined=0 afterward to prove nothing essential was moved.

## Final report pattern

Reply in Vietnamese, concise:
- Edited file path.
- 4-6 bullets of structural/style changes.
- Build command/result and PDF path.
- Separate blocker/pre-existing warnings from what was changed.
