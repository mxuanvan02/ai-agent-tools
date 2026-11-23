"""Unit tests for latex-diff-and-revision-audit scripts."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from build_highlight_diff import sanitize_diff_tex
from verify_prompt_sync import extract_python_constant, extract_verbatim_contents, scan_clipped_vietnamese


class TestSanitizeDiffTex(unittest.TestCase):
    def test_strips_deletions_only_in_body_and_restores_verbatim(self):
        new_main = (
            "\\documentclass{article}\n"
            "\\providecommand{\\DIFdelbegin}{}\n"
            "\\begin{document}\n"
            "Body\n"
            "\\end{document}\n"
        )
        diff_raw = (
            "\\documentclass{article}\n"
            "%DIF PREAMBLE\n"
            "\\providecommand{\\DIFdelbegin}{}\n"
            "\\begin{document}\n"
            "Keep \\DIFdelbegin \\DIFdel{old1\n\nold2} \\DIFdelend \\DIFadd{new}.\n"
            "\\begin{Verbatim}\n"
            "\\DIFadd{{\"answers\":[{\"stt\":1}]}}\n"
            "\\end{Verbatim}\n"
            "\\end{document}\n"
        )
        clean_vb = ['\\begin{Verbatim}\n{"answers":[{"stt":1}]}\n\\end{Verbatim}']
        out = sanitize_diff_tex(diff_raw, new_main, clean_vb)

        self.assertIn(r"\providecommand{\DIFdelbegin}{}", out)
        self.assertIn(r"\usepackage{lua-ul}", out)
        self.assertNotIn("old1", out)
        self.assertNotIn(r"\DIFdelbegin \DIFdel", out)
        self.assertIn('{"answers":[{"stt":1}]}', out)
        self.assertNotIn(r'\DIFadd{{"answers"', out)


class TestPromptSyncAndProseScan(unittest.TestCase):
    def test_ast_prompt_matches_verbatim_and_prose_scanner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            py_file = root / "sample.py"
            py_file.write_text(
                'PROMPT = """\\\nLine one.\n## Output Format\nXML\n"""\n',
                encoding="utf-8",
            )
            tex_file = root / "appendix.tex"
            tex_file.write_text(
                "Văn bản chuẩn tiếng Việt.\n"
                "\\begin{Verbatim}[fontsize=\\scriptsize]\n"
                "Line one.\n"
                "\\end{Verbatim}\n",
                encoding="utf-8",
            )
            extracted = extract_python_constant(py_file, "PROMPT")
            blocks = extract_verbatim_contents(tex_file)
            self.assertEqual(blocks[0], extracted)
            self.assertEqual(scan_clipped_vietnamese([tex_file]), [])

            bad_tex = root / "bad.tex"
            bad_tex.write_text("Kiểm chứng khả phục hồi trên tập 4 chọn.\n", encoding="utf-8")
            self.assertEqual(len(scan_clipped_vietnamese([bad_tex])), 1)


if __name__ == "__main__":
    unittest.main()
