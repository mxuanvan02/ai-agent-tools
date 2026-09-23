# Conference submission: verify the REAL format, then hit the page limit

Trigger: người dùng says "nộp cho đúng", "bám sát thông tin hội nghị", gives an
EasyChair/conference link, or asks to finalize a paper for a named venue. Do NOT
guess the template from internal metadata (MATERIAL_PASSPORT "hội nghị C1 conference
style" is a self-note, not a spec). A generic `\documentclass{article}` is a
draft placeholder, not a venue template — flag it and verify before packaging.

## Step 1 — find the authoritative format

1. EasyChair management links (`easychair.org/my/conference?conf=X`) need login and
   carry NO format info. The public **CFP** does: try `easychair.org/cfp/<CONF>`
   (the conf code is often lowercase, e.g. `stais2026`). The CFP page lists the
   conference web page, submission link, deadline, and frequently a **"Link
   Template"** anchor.
2. Web search engines are frequently blocked in-browser (Google `/sorry`,
   DuckDuckGo HTML returns an empty form, Bing throws a Cloudflare challenge). Do
   not burn turns retrying them — go straight to the EasyChair CFP or the
   conference web page (`https://stais.vn` type).
3. If the template is a **Google Doc**, the in-browser view is an iframe you cannot
   scroll/scrape reliably. Grab the doc id from `window.location.href`
   (`docs.google.com/document/d/<ID>/edit`) and download the real file:
   `curl -sL "https://docs.google.com/document/d/<ID>/export?format=docx" -o tpl.docx`
   then `read_file tpl.docx` (read_file auto-extracts .docx text). Save the
   template into the project's `_templates/` for provenance.

## Step 2 — extract the format spec into a checklist

Read the template top-to-bottom and pull the hard constraints. hội nghị C1 (2026) example
(một trường ĐH, Trans-Tech/Elsevier-style Word template) — a typical regional
Word-template venue:
- A4, margins top 2.5 / bottom 1.5 / left=right 2 cm; single column.
- Title Arial 14 bold; body Times New Roman 12.
- **Section headings boldface, NOT numbered** (`\setcounter{secnumdepth}{0}`).
- Do not number pages (`\pagestyle{empty}`).
- Abstract standalone, opens with "Abstract.", <=200 words, no eq/fig/table/ref.
- References numeric `[1]`, cited in order.
- **Page limit 6--8 pages** (verify this number — it is the binding constraint).

Build a table: requirement | venue spec | manuscript status. Tick what already
matches (margins often do) so you only work the deltas.

## Step 3 — convert LaTeX to match (cheap deltas first)

- Title font: `\fontsize{14}{17}\selectfont` + Helvetica (`\usepackage[scaled]{helvet}`).
- Un-number headings: `\setcounter{secnumdepth}{0}`; drop any `\sffamily` from
  `\titleformat*` if body headings should be serif-bold.
- **Bug after un-numbering:** every `Section~\ref{sec:...}` now renders `??`. grep
  `\ref{sec:` and replace each with the section's prose name, or re-add labels via
  a different mechanism. Always grep cross-refs after changing `secnumdepth`.

## Step 4 — hit the page limit (the slow part)

Over-length is usually NOT prose — measure first. `pdftotext -f N -l N main.pdf -`
per page to see what occupies each page; tables/figures/float-spacing dominate.
Levers, in order of yield, that drop pages WITHOUT cutting scientific content:
1. **Float + display spacing** in preamble:
   `\setlength{\textfloatsep}{4pt}` `\intextsep` `\abovedisplayskip{3pt}`
   `\belowdisplayskip{3pt}` `\setlength{\parskip}{0pt}`, `enumitem` `\setlist{nosep}`.
2. **Shrink figures** (`width=0.66\linewidth`, or `\resizebox{0.66\linewidth}`).
3. **Compact bibliography**: `\renewcommand{\thebibliography}` wrapper that appends
   `\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}\footnotesize`.
   Stronger: `\scriptsize` + 2-column via `multicol`:
   `{\begin{multicols}{2}\renewcommand{\section}[2]{}\bibliography{refs}\end{multicols}}`
   (the `\section` redef silences the auto-generated "References" heading inside
   the multicol so it doesn't break across columns).
4. **Fold a symbols/glossary table** into one inline parenthetical sentence.
5. **Merge adjacent propositions** sharing a proof into one statement + one
   proof-sketch (watch: a `Propositions~\ref{a}--\ref{b}` elsewhere now reads
   "1--1" — change to singular `Proposition~\ref{a}`).
6. **Dedup prose**: a figure paragraph that repeats its own caption; an intro
   contribution list echoed in related-work's last paragraph.
7. **Last-resort `\linespread{0.96}\selectfont`** in preamble after `\pagestyle`.
   At Times-12 the visual change is imperceptible but reclaims ~1 page across
   8 pages of body. Do NOT go below 0.94 — it becomes legible to copy editors.
Re-run the full chain after each cluster and re-count pages; the last reference
spilling onto an extra page is common — one more spacing/`\footnotesize` pass
usually claws it back. Verify 0 undefined / 0 `??` / 0 overfull>60pt at the end.

### Pitfall: cutting a `\input{table}` while keeping the prose that cites it

When tightening to hit page limit, do NOT just delete a `\input{outputs/tables/X.tex}`
to save space if any paragraph still says "Table~\ref{tab:X} shows...". The
build still succeeds (with warnings), but the PDF prints "Table ??". Either:
(a) keep the `\input` and shrink with `\scriptsize`/2-col, or
(b) delete the prose-with-citation along with the `\input`.
After cutting tables, always: `pdftotext main.pdf - | grep -c "??"` must be 0
AND `grep "Reference.*undefined" main.log` must be empty.

## Step 4b — fidelity audit: page-limit hacks can DEVIATE from the template

After you hit the page limit, the compaction levers may have pushed you away from
the template's actual layout. Người dùng audits this ("template gốc của hội nghị đó là
thế này hả?") — be the one to flag deviations first, don't wait to be caught. Two
that recur and are easy to miss because the build is clean and the page count is
right:
- **References STYLE vs the template's.** The template usually ships a worked
  reference list — read it. hội nghị C1/Trans-Tech/Elsevier-style venues format refs
  **Elsevier** ("J. van der Geer, ..., J. Sci. Commun. 163 (2000) 51-59", title
  NOT in quotes, initials-before-surname) while `\bibliographystyle{IEEEtran}`
  produces "..." around titles and a different author order. This is a real,
  reviewer-visible delta. If exact fidelity matters, switch to `elsarticle-num`.
- **References COLUMN count.** Single-column template + your `multicol{2}` + 
  `\scriptsize` bib to fit the page limit = a layout deviation from the 1-column
  original. Name it.
Present the trade-off explicitly: "đúng mẫu 100%" (1-col, Elsevier refs) usually
costs a page → forces cutting an experiment, vs "vừa page-limit" (2-col compact)
which deviates on style only. Offer the dual-fidelity middle option (correct ref
STYLE but keep 2-col to stay within pages) and let người dùng choose — don't silently
keep either. Verify alignment of title/author block against the template too
(hội nghị C1 title block is CENTER, not IEEE-left): render page 1 to PNG and vision-check.

### "Direction 3" recipe — Elsevier ref STYLE + keep 2-col compaction (executed)

When người dùng picks the middle option ("đi hướng 3"), the switch is one line plus a
clean rebuild — no content cut, stays at the page limit:
- `elsarticle-num.bst` ships with TeX Live (`kpsewhich elsarticle-num.bst` to confirm;
  also at `.../bibtex/bst/elsarticle/`). It does NOT need the elsarticle class — it
  self-defines `\url`/`\href`/`\path` fallbacks in the generated `.bbl`, so it works
  fine inside an `article`/IEEEtran doc.
- Change `\bibliographystyle{IEEEtran}` → `\bibliographystyle{elsarticle-num}`, keep
  the `multicol{2}` + `\scriptsize` bib wrapper untouched. `rm main.bbl`, run full
  chain (`pdflatex → bibtex → pdflatex → pdflatex`). Output is Elsevier format:
  initials-before-surname, title NOT in quotes, `journal vol (year) pages`, with a
  trailing `\href{doi}` newblock.
- Verify by `pdftotext` grepping a ref line — confirm no quotes around titles and the
  `vol (year) pages` shape. Re-count pages (Elsevier entries are often a touch shorter
  → may even gain margin).
- **Sync the .docx too.** If a Word version exists, re-parse the NEW `.bbl` into the
  `\begin{enumerate}` list (per `latex-to-docx-pandoc-conversion.md`), stripping the
  `\href`/`\newblock` tail so pandoc renders clean Elsevier-style numbered refs.

### Co-first / equal-contribution when the template has no slot for it

Người dùng asks "hội nghị X có co-first author không?" — verify against the template's
author line, don't assume. Many regional Word templates (hội nghị C1/Trans-Tech style)
define ONLY three author marks: superscript number = affiliation, superscript
letter = email, and `*` = corresponding author. There is **no** "equal
contribution / co-first" convention in the template.

- Answer honestly: the template has no equal-contribution slot. Then offer the two
  clean options rather than silently keeping a hack: (1) keep co-first but use a
  **dedicated symbol** (`†` / "These authors contributed equally") that does NOT
  reuse the affiliation-number slot — borrowing the address number `¹` to mean
  "equal contribution" is the common mistake and is ambiguous; (2) drop co-first
  to match the minimal template (only `*` for corresponding).
- This is legitimate and widely accepted even when the template doesn't show it, so
  recommend option (1) if the equal contribution is real — just isolate the symbol.

## Step 5 — LaTeX-vs-Word caveat (ask, don't assume)

If the official template is `.docx`, a LaTeX build only matches the *format spec*,
not the file type. Before declaring done, ask người dùng whether the venue accepts a
PDF compiled from LaTeX (matching the spec) or **mandates a .docx upload**. If
.docx is mandatory, OR người dùng says "kèm bản DOCX" / "song song với đó cho thêm
bản docx luôn", run the conversion pipeline — see
`latex-to-docx-pandoc-conversion.md` for the full recipe (strip `\resizebox`,
render TikZ→PNG, parse `.bbl` to `\begin{enumerate}`, use template as
`--reference-doc` for style inheritance, verify via XML count of
`<w:tbl>`/`<w:drawing>`/`<m:oMath>`).

Do not silently ship a LaTeX PDF when the venue wants Word.

## Packaging note

Once the venue is verified, drop the "template pending" caveat from any
SUBMISSION_NOTE; record the verified venue + page limit + deadline instead.
