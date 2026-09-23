# Prism/Overleaf LaTeX Packaging and Clean-Build Checks

Use this when the user reports that a manuscript compiles locally but fails on Prism/Overleaf-like systems, especially with vague delimiter messages such as a `$` error.

## Durable workflow

1. Reproduce from a clean upload-like artifact, not the warm local build:
   ```bash
   rm -rf /tmp/<paper>_zip_test
   mkdir -p /tmp/<paper>_zip_test
   cd /tmp/<paper>_zip_test
   unzip -q /path/to/submission.zip
   cd <project-or-manuscript-dir>
   rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.pdf
   latexmk -pdf -interaction=nonstopmode main.tex
   ```
2. Scan all `.tex` files for non-printing control characters before assuming math delimiters are unmatched. A corrupted backslash sequence can surface as a misleading `$`/math-mode error:
   ```python
   from pathlib import Path
   for p in Path('.').rglob('*.tex'):
       s = p.read_text(errors='replace')
       bad = [(s.count('\n',0,i)+1, ord(ch)) for i,ch in enumerate(s)
              if ord(ch) < 32 and ch not in '\n\r\t']
       print(p, 'dollars=', s.count('$'), 'control_chars=', bad[:5])
   ```
3. Prefer Prism-safe LaTeX when repairing math:
   - Replace fragile `aligned` blocks with simple `equation` blocks if alignment is not essential.
   - Re-type suspicious commands such as `\frac` manually; corrupted `\f` can become form-feed (`^^L`) plus `rac`.
   - Keep URLs in `\texttt{}` or `\url{}` and escape `%`, `_`, `&`, `#` in text mode.
4. Make the package self-contained from the selected main-file directory:
   - If Prism compiles `manuscript/main.tex`, included tables/figures should live under `manuscript/...` and be referenced as `outputs/...`, not `../outputs/...`.
   - Copy generated tables/figures into the manuscript tree before zipping.
5. After fixing, rebuild from the refreshed zip in `/tmp`, then check the log for zero counts of `LaTeX Error`, `Emergency stop`, `Undefined references`, `Citation \``, `undefined`, and `Overfull \\hbox` before saying ready.

## Bundle the official class/bst so the package is self-contained against ANY compiler

When the user says "tải template về, đưa nội dung qua, không thiếu file nào trong bộ
template" (download the official template, move content in, don't leave any template
file out), path self-containment is NOT enough — the package must also carry the
journal `.cls` and `.bst` so it builds even if the upload system's TeX install lacks
them or ships a different version. Workflow (ran clean for bài AoI-greenhouse IoT-J):

1. **Download the official bundle from CTAN** (the source IEEE itself distributes),
   not a random copy:
   ```bash
   curl -sL -o ieeetran.zip "https://mirrors.ctan.org/macros/latex/contrib/IEEEtran.zip"
   unzip -q ieeetran.zip
   ```
   IEEEtran ships `IEEEtran.cls`, `bibtex/IEEEtran.bst`, plus HOWTO PDFs and bare
   templates. You only need the `.cls` and `.bst` for the package.
2. **Diff CTAN vs the system version before swapping** — confirm the local build was
   already using the canonical class, so the page count the user saw is standards-correct:
   ```bash
   diff -q IEEEtran.cls /usr/share/texlive/texmf-dist/tex/latex/ieeetran/IEEEtran.cls
   diff -q bibtex/IEEEtran.bst /usr/share/texlive/texmf-dist/bibtex/bst/ieeetran/IEEEtran.bst
   ```
   (For bài AoI-greenhouse both were IDENTICAL: V1.8b 2015/08/26.)
3. **Copy `IEEEtran.cls` + `IEEEtran.bst` into the repo root** alongside `main.tex`.
4. **Build-from-scratch in a BLANK dir** and confirm the log shows `(./IEEEtran.cls`
   (the LOCAL file), not the system path — this proves the package is self-contained:
   ```bash
   mkdir /tmp/clean && cp -r main.tex IEEEtran.cls IEEEtran.bst references.bib sections figures /tmp/clean/
   cd /tmp/clean && pdflatex -interaction=nonstopmode -halt-on-error main.tex \
     && bibtex main && pdflatex main && pdflatex main
   grep -o "IEEEtran\.cls" *.log; grep "(./IEEEtran.cls" *.log   # must be the local one
   ```

## Prune orphan figures before zipping (clean package, no rifraff)

A `figures/` dir often carries PNGs no longer referenced after trimming. Shipping
them bloats the package and confuses reviewers. Find what is actually used vs present:
```bash
# figures included via \includegraphics
grep -rho "includegraphics\[[^]]*\]{[^}]*}\|includegraphics{[^}]*}" sections/ main.tex \
  | grep -o "{[^}]*}" | tr -d '{}' | sed 's|figures/||;s|\.png||' | sort -u
# TikZ figures pulled via \input
grep -rho "input{figures/[^}]*}" sections/ main.tex | sort -u
# everything present
ls figures/*.png
```
Delete the set difference (orphans), then rebuild from the blank dir again to confirm
nothing broke. Also strip stray backup subdirs (`figures/_backups_*`) before zipping —
`rsync --exclude` without a trailing `/` may not exclude dirs as expected; verify the
final zip contents with `unzip -l submission.zip`.

## Session precedents

- bài probe-transmit Sensors/MDPI: Prism reported a `$` issue, but the root cause was a corrupted `\frac` that appeared as a form-feed `^^L` plus `rac{...}` inside Appendix math. Rewriting the derivation as simple `equation` blocks fixed the clean zip build.
- bài bandwidth-scheduling/STAI(S): the local warm build passed, but a clean upload-like build exposed path fragility when `sections/04_method_and_eval.tex` used `../outputs/...`. Copying outputs under `manuscript/outputs/` and changing references to `outputs/...` made the zip self-contained for Prism/Overleaf.
