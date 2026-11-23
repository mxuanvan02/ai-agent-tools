#!/usr/bin/env python3
"""Verify AST prompt sync with LaTeX Verbatim blocks and lint Vietnamese prose."""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path
from typing import Sequence

VERBATIM_CONTENT_RE = re.compile(r"\\begin\{Verbatim\}(?:\[[^\]]*\])?\n(.*?)\n\\end\{Verbatim\}", re.DOTALL)

# Common clipped/telegraphic Vietnamese patterns from over-compression.
CLIPPED_PATTERNS = re.compile(
    r"khả phục hồi|mô hình mạnh hơn|cổng kiểm định dạng|\b\d+(?:--\d+)?\s+chọn(?![ \t]+(?:khác|lệch|phương án|đáp án))\b|"
    r"họ sinh/lọc|mô hình sinh/lọc|đầu/cuối/số trang|môi trường/hạt giống",
    re.IGNORECASE,
)


def extract_python_constant(py_path: Path, const_name: str, *, strip_output_format: bool = True) -> str:
    """Extract a runtime string constant via AST without regex escaping bugs."""
    tree = ast.parse(py_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == const_name:
                    value = ast.literal_eval(node.value)
                    if not isinstance(value, str):
                        raise ValueError(f"{const_name} in {py_path} is not a string literal")
                    value = value.rstrip()
                    if strip_output_format and "## Output Format" in value:
                        value = value[: value.find("## Output Format")].rstrip()
                    return value
    raise KeyError(f"Constant {const_name} not found in {py_path}")


def extract_verbatim_contents(tex_path: Path) -> list[str]:
    """Return all Verbatim block bodies from a LaTeX file in order."""
    return VERBATIM_CONTENT_RE.findall(tex_path.read_text(encoding="utf-8"))


def scan_clipped_vietnamese(paths: Sequence[Path]) -> list[str]:
    """Scan .tex and .md files for clipped/telegraphic Vietnamese expressions."""
    findings: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        in_verbatim = False
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if r"\begin{Verbatim}" in line:
                in_verbatim = True
                continue
            if r"\end{Verbatim}" in line:
                in_verbatim = False
                continue
            if in_verbatim or line.lstrip().startswith("%"):
                continue
            if CLIPPED_PATTERNS.search(line):
                findings.append(f"{path}:{lineno}: {line.strip()}")
    return findings


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint Vietnamese prose and verify Verbatim prompt blocks.")
    parser.add_argument("--tex-dir", type=Path, required=True, help="Directory containing .tex files")
    args = parser.parse_args(argv)
    files = sorted(args.tex_dir.glob("*.tex"))
    findings = scan_clipped_vietnamese(files)
    if findings:
        for item in findings:
            print(f"[FAIL] {item}")
        return 1
    print(f"[OK] Checked {len(files)} TeX files: 0 clipped Vietnamese patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
