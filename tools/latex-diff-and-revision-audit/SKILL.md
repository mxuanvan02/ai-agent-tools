---
name: latex-diff-and-revision-audit
description: >-
  Workflow for polishing revised LaTeX manuscripts, generating clean additions-only
  yellow-highlighted diff PDFs (latexdiff + lualatex + lua-ul without broken
  Verbatim blocks or mid-sentence line breaks), AST-verifying prompts against
  public source code, and keeping public GitHub research repositories clean.
---

# LaTeX Revision, Highlight Diff & Source Audit

Use this skill when preparing revised scientific manuscripts, response letters, and public companion repositories for journal resubmission.

## 1. Additions-Only Yellow Highlight PDF (`latexdiff` + `lualatex`)
Run [build_highlight_diff.py](./scripts/build_highlight_diff.py) or apply these invariants:
1. Run `latexdiff --flatten --encoding=utf8 --exclude-safecmd=needspace,texttt,emph --append-safecmd=highLight old_main.tex new_main.tex`.
2. **Keep clean preamble:** Replace `latexdiff`'s generated preamble with the clean `main.tex` preamble plus `\usepackage{luacolor}`, `\usepackage{lua-ul}`, `\definecolor{diffhl}{HTML}{FFF3A8}`, `\DIFadd[1]{{\highLight[diffhl]{#1}}}`, `\DIFdel[1]{}`, and `\pdfstringdefDisableCommands{\def\highLight#1{#1}\def\DIFadd#1{#1}\def\DIFaddFL#1{#1}}`.
3. **Strip deletions in body only:** Split at `\begin{document}` and strip `\DIFdelbegin(?:FL)?\b.*?\DIFdelend(?:FL)?\b\s*` **only inside the document body** (never in the preamble) to prevent blank lines inside deleted blocks from causing mid-sentence paragraph breaks.
4. **Protect `Verbatim` blocks:** Do **not** add `Verbatim` to `VERBATIMLINEENV` (it triggers `listings` `alsolanguage undefined` keyval errors). Instead, restore every `\begin{Verbatim}...\end{Verbatim}` block 1-for-1 from the clean `.tex` sources after `latexdiff`.
5. Compile with `lualatex -> bibtex -> lualatex -> lualatex`, verify `0` errors / `0` `Overfull \hbox`, and visually inspect rendered PNGs.

## 2. AST Prompt Sync & Vietnamese Prose Sweep
Run [verify_prompt_sync.py](./scripts/verify_prompt_sync.py):
- Extract prompt string constants from public `.py` files with `ast.parse` + `ast.literal_eval` and assert exact equality with every `Verbatim` prompt block in LaTeX appendices.
- Sweep `.tex`, `.docx`, and `.md` deliverables for clipped/telegraphic Vietnamese phrasing and shorthand slashes (`A/B`) in prose before final compilation.

## 3. Public Research Repo Hygiene
- Keep only pipeline and research/test code (`0% TeX`), read API base/keys from `OPENAI_API_BASE` / `OPENAI_API_KEY` env vars, and verify `gh api repos/<owner>/<repo>/contributors` and `languages` after pushing.
