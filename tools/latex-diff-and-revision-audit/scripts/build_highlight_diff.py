#!/usr/bin/env python3
"""Build an additions-only yellow-highlighted PDF diff with latexdiff + lualatex.

Key invariants:
1. Replace latexdiff's generated preamble with the clean target preamble + luacolor/lua-ul.
2. Strip \\DIFdelbegin...\\DIFdelend blocks ONLY in the document body (never in preamble)
   so blank lines inside deletions cannot inject spurious mid-sentence paragraph breaks.
3. Restore \\begin{Verbatim}...\\end{Verbatim} blocks 1-for-1 from clean .tex sources
   so literal \\DIFadd{} markup never leaks inside Verbatim environments.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence

VERBATIM_RE = re.compile(r"\\begin\{Verbatim\}.*?\\end\{Verbatim\}", re.DOTALL)
DEL_BLOCK_RE = re.compile(r"\\DIFdelbegin(?:FL)?\b.*?\\DIFdelend(?:FL)?\b\s*", re.DOTALL)

DIFF_PREAMBLE = r"""
\usepackage{luacolor}
\usepackage{lua-ul}
\definecolor{diffhl}{HTML}{FFF3A8}
\providecommand{\DIFaddbegin}{}
\providecommand{\DIFaddend}{}
\providecommand{\DIFdelbegin}{}
\providecommand{\DIFdelend}{}
\providecommand{\DIFmodbegin}{}
\providecommand{\DIFmodend}{}
\providecommand{\DIFaddbeginFL}{}
\providecommand{\DIFaddendFL}{}
\providecommand{\DIFdelbeginFL}{}
\providecommand{\DIFdelendFL}{}
\providecommand{\DIFadd}[1]{{\highLight[diffhl]{#1}}}
\providecommand{\DIFdel}[1]{}
\providecommand{\DIFaddFL}[1]{{\highLight[diffhl]{#1}}}
\providecommand{\DIFdelFL}[1]{}
\pdfstringdefDisableCommands{\def\highLight#1{#1}\def\DIFadd#1{#1}\def\DIFaddFL#1{#1}}
"""


def collect_verbatim_blocks(tex_dir: Path, tex_files: Sequence[Path] | None = None) -> list[str]:
    """Collect all Verbatim blocks in input order from clean .tex sources."""
    if tex_files is None:
        main_txt = (tex_dir / "main.tex").read_text(encoding="utf-8")
        included = [tex_dir / f"{name if name.endswith('.tex') else name + '.tex'}"
                    for name in re.findall(r"\\input\{([^}]+)\}", main_txt)]
        tex_files = [tex_dir / "main.tex", *[p for p in included if p.exists()]]

    blocks: list[str] = []
    for path in tex_files:
        blocks.extend(VERBATIM_RE.findall(path.read_text(encoding="utf-8")))
    return blocks


def sanitize_diff_tex(diff_raw: str, new_main_tex: str, clean_verbatim_blocks: Sequence[str]) -> str:
    """Apply clean preamble, body-only deletion stripping, and Verbatim restoration."""
    begin_doc = r"\begin{document}"
    new_idx = new_main_tex.find(begin_doc)
    diff_idx = diff_raw.find(begin_doc)
    if new_idx == -1 or diff_idx == -1:
        raise ValueError("Missing \\begin{document} marker in TeX source")

    preamble = new_main_tex[:new_idx] + DIFF_PREAMBLE
    body = diff_raw[diff_idx:]
    body = DEL_BLOCK_RE.sub("", body)
    body = re.sub(r"\n{3,}", "\n\n", body)

    if clean_verbatim_blocks:
        diff_blocks = VERBATIM_RE.findall(body)
        if len(diff_blocks) != len(clean_verbatim_blocks):
            raise ValueError(
                f"Verbatim count mismatch: {len(diff_blocks)} in diff vs {len(clean_verbatim_blocks)} in source"
            )
        it = iter(clean_verbatim_blocks)
        body = VERBATIM_RE.sub(lambda _m: next(it), body)

    return preamble + body


def build_diff_pdf(old_main: Path, new_dir: Path, out_pdf: Path) -> Path:
    """Flatten, diff, sanitize, and compile to PDF with lualatex + bibtex."""
    with tempfile.TemporaryDirectory(prefix="latex_diff_") as tmp:
        work = Path(tmp)
        shutil.copytree(new_dir, work, dirs_exist_ok=True)
        old_copy = work / "_old_main.tex"
        shutil.copy2(old_main, old_copy)

        cmd = [
            "latexdiff",
            "--flatten",
            "--encoding=utf8",
            "--exclude-safecmd=needspace,texttt,emph",
            "--append-safecmd=highLight",
            str(old_copy),
            str(work / "main.tex"),
        ]
        res = subprocess.run(cmd, cwd=work, capture_output=True, text=True, check=True)

        new_main_txt = (work / "main.tex").read_text(encoding="utf-8")
        verbatim_blocks = collect_verbatim_blocks(work)
        diff_tex = sanitize_diff_tex(res.stdout, new_main_txt, verbatim_blocks)
        (work / "diff.tex").write_text(diff_tex, encoding="utf-8")

        for step in (
            ["lualatex", "-interaction=nonstopmode", "diff.tex"],
            ["bibtex", "diff"],
            ["lualatex", "-interaction=nonstopmode", "diff.tex"],
            ["lualatex", "-interaction=nonstopmode", "diff.tex"],
        ):
            proc = subprocess.run(step, cwd=work, capture_output=True, text=True)
            if proc.returncode != 0:
                raise RuntimeError(f"Step {step} failed:\n{proc.stdout[-1500:]}")

        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(work / "diff.pdf", out_pdf)
    return out_pdf


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build additions-only yellow highlight PDF diff.")
    parser.add_argument("--old-main", type=Path, required=True, help="Path to original main.tex")
    parser.add_argument("--new-dir", type=Path, required=True, help="Directory with revised main.tex")
    parser.add_argument("--out-pdf", type=Path, required=True, help="Output highlighted PDF path")
    args = parser.parse_args(argv)
    build_diff_pdf(args.old_main, args.new_dir, args.out_pdf)
    print(f"[OK] Wrote {args.out_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
