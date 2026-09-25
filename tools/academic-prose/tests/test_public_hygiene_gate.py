#!/usr/bin/env python3
"""Regression tests for the public-hygiene gate that every tool in this repository ships.

WHY THESE TESTS EXIST
---------------------
The gate had none, and that is how a real defect stayed invisible: institution-3 is
"Hue " + "University", and references/academic-vietnamese-standard.md contains that name split
across a line break, so the pattern never matched and the gate printed PASS on the exact text it
exists to catch. A gate that a line wrap can beat is worse than no gate, because its PASS is
believed -- and without a test, any future edit could reopen that hole silently.

Each test pins one property that was MEASURED on real repository content, not assumed:

  wrapped tokens are caught    a mention split by a newline is found (the original defect), and so
                               is a secret key split the same way
  the allowlist is narrow      the two scholarly citations pass only in their own files and only
                               while the citation framing sits on the same line
  the allowlist is per-line    an unframed mention appended to an allowed file still fails, so the
                               allowance never degraded into "anything in this file"
  the counts are hand-checked  one fixture trips two patterns; asserting one finding there would
                               have made a correct gate look broken
  byte-code litter is ignored  a test suite run before the gate cannot fail it
  the copies are identical     a drifted gate makes PASS mean something different per tool
  every tool is covered        a tool with no gate is a tool CI never inspects

FORBIDDEN LITERALS ARE CONCATENATED IN THIS FILE TOO. It lives inside a tool directory that the
gate scans, exactly like the gate itself, so an unsplit literal here would fail the very check this
suite is testing. Runtime values are unchanged by the splits.
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
TOOL_DIR = TESTS_DIR.parent
REPO_ROOT = TOOL_DIR.parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
GATE_NAME = "public_hygiene_check.py"
GATE = TOOL_DIR / "scripts" / GATE_NAME

# Concatenated for the reason given in the module docstring.
INSTITUTION_1 = "ĐH" + "SP"
INSTITUTION_3 = "Hue " + "University"
PERSONAL_NAME = "anh " + "Văn"
HOST_USERNAME = "hito" + "kiri"
CODENAME = "ECM-" + "TQAG"
SECRET_KEY = "BEGIN " + "RSA PRIVATE KEY"
FRAMING = "Decision 1418"

CITATION_FILE = "references/academic-vietnamese-standard.md"
WORD_LIMIT_FILE = "references/word-budget-and-rendered-artifact-compliance.md"


def run_gate(tool_dir: Path) -> tuple[int, str]:
    """Run the tool's own copy of the gate as a subprocess, the way CI does."""
    proc = subprocess.run(
        [sys.executable, str(tool_dir / "scripts" / GATE_NAME)],
        capture_output=True,
        text=True,
        timeout=600,
    )
    return proc.returncode, proc.stdout + proc.stderr


def finding_count(output: str) -> int:
    match = re.search(r"FAIL: (\d+) finding", output)
    return int(match.group(1)) if match else 0


def build_tool(files: dict[str, str]) -> str:
    """Create a throwaway tool directory holding a copy of the gate plus the given files.

    Returns the directory path; the caller is inside a TemporaryDirectory context, so nothing is
    left in the repository. Writing fixtures into the repo instead would make the gate scan its own
    test input and the result would depend on file ordering.
    """
    tmp = tempfile.mkdtemp(prefix="hygiene_gate_test_")
    root = Path(tmp)
    (root / "scripts").mkdir()
    shutil.copy2(GATE, root / "scripts" / GATE_NAME)
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tmp


class TestWrappedTokensAreCaught(unittest.TestCase):
    """The defect that motivated this suite: a line break used to defeat every literal pattern."""

    def test_institution_name_split_by_newline_is_caught(self) -> None:
        tmp = build_tool({"notes.md": "Written at " + INSTITUTION_3.replace(" ", "\n") + " by us.\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("institution-3", out)
            self.assertGreaterEqual(finding_count(out), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_secret_key_split_by_newline_is_caught(self) -> None:
        tmp = build_tool({"notes.md": SECRET_KEY.replace(" ", "\n", 1) + "\nabc\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("secret-key", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unwrapped_tokens_are_still_caught(self) -> None:
        """Normalisation must not weaken the ordinary case."""
        tmp = build_tool({
            "a.md": "gửi " + PERSONAL_NAME + " nhé\n",
            "b.md": "path /home/" + HOST_USERNAME + "/x\n",
            "c.md": "repo " + CODENAME + "\n",
        })
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            for label in ("personal-name", "host-username", "codename-4"):
                self.assertIn(label, out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_clean_content_still_passes(self) -> None:
        tmp = build_tool({"a.md": "mọi thứ sạch sẽ, không có gì riêng tư\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
            self.assertIn("PASS", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestAllowlistIsNarrow(unittest.TestCase):
    """The two scholarly citations are kept as evidence; the allowance must not grow beyond them."""

    def setUp(self) -> None:
        self.real = (TOOL_DIR / CITATION_FILE).read_text(encoding="utf-8")
        # Guard against the suite going vacuous: if the reference is ever reworded so the citation
        # disappears, these tests would pass while asserting nothing. Fail loudly instead.
        self.assertIn(FRAMING, self.real,
                      "citation framing gone from %s -- update this suite" % CITATION_FILE)
        self.assertIn(INSTITUTION_1, self.real)

    def test_real_tool_directory_passes_with_both_citations_present(self) -> None:
        rc, out = run_gate(TOOL_DIR)
        self.assertEqual(rc, 0, out)
        word_limit = (TOOL_DIR / WORD_LIMIT_FILE).read_text(encoding="utf-8")
        self.assertIn("Đại học " + "Huế", word_limit,
                      "second citation gone from %s -- update this suite" % WORD_LIMIT_FILE)

    def test_removing_the_citation_framing_makes_the_real_file_fail(self) -> None:
        mutated = self.real.replace(FRAMING + "/", "Decision /", 1)
        self.assertNotIn(FRAMING, mutated)
        tmp = build_tool({CITATION_FILE: mutated})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("institution-1", out)
            # Both institution patterns sit in that one sentence, so both must fire: counted by
            # hand. Asserting 1 here would make a correct gate look broken.
            self.assertGreaterEqual(finding_count(out), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unframed_mention_appended_to_an_allowed_file_still_fails(self) -> None:
        """Proves the context check is per LINE, not per file."""
        mutated = self.real.rstrip("\n") + (
            "\n\nA separate note: the " + INSTITUTION_1 + " committee reviewed this draft.\n"
        )
        tmp = build_tool({CITATION_FILE: mutated})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("institution-1", out)
            self.assertIn("committee reviewed this draft", out)
            # The framed citation on its own line is still allowed, so exactly the appended one
            # is reported.
            self.assertEqual(finding_count(out), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_same_text_in_a_different_file_fails(self) -> None:
        """The allowance is bound to the file the citation actually lives in."""
        content = FRAMING + "/QĐ-" + INSTITUTION_1 + " at " + INSTITUTION_3 + ".\n"
        tmp = build_tool({"references/other.md": content})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("institution-1", out)
            self.assertIn("institution-3", out)
            self.assertEqual(finding_count(out), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestByteCodeLitterIsIgnored(unittest.TestCase):
    """README's validation block runs test suites before the gate; their caches must not fail it."""

    def test_pycache_and_pyc_are_skipped(self) -> None:
        tmp = build_tool({"a.md": "sạch\n"})
        try:
            root = Path(tmp)
            cache = root / "scripts" / "__pycache__"
            cache.mkdir(parents=True, exist_ok=True)
            (cache / "mod.cpython-312.pyc").write_bytes(b"\x00\x01\x02\x03undecodable")
            (root / "loose.cpython-312.pyc").write_bytes(b"\x00\xffundecodable")
            rc, out = run_gate(root)
            self.assertEqual(rc, 0, out)
            self.assertNotIn("binary-file", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_a_real_binary_is_still_reported(self) -> None:
        """Skipping caches must not disable the binary check for anything else."""
        tmp = build_tool({"a.md": "sạch\n"})
        try:
            root = Path(tmp)
            (root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x01")
            rc, out = run_gate(root)
            self.assertEqual(rc, 1, out)
            self.assertIn("binary-file", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestGateCoverageAcrossTheRepository(unittest.TestCase):
    def test_every_tool_ships_a_gate(self) -> None:
        tools = sorted(p.name for p in TOOLS_DIR.iterdir() if p.is_dir())
        self.assertTrue(tools, "no tool directories found at %s" % TOOLS_DIR)
        missing = [t for t in tools if not (TOOLS_DIR / t / "scripts" / GATE_NAME).is_file()]
        self.assertEqual(missing, [],
                         "a tool with no gate is a tool CI never inspects: %s" % missing)

    def test_all_copies_are_byte_identical(self) -> None:
        digests = {
            p.parent.parent.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(TOOLS_DIR.glob("*/scripts/" + GATE_NAME))
        }
        self.assertGreaterEqual(len(digests), 2)
        self.assertEqual(len(set(digests.values())), 1,
                         "gate copies drifted; PASS would mean something different per tool: %s"
                         % {k: v[:12] for k, v in digests.items()})

    def test_gate_does_not_flag_itself(self) -> None:
        tmp = build_tool({})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_gate_leaves_no_litter_in_the_repository(self) -> None:
        """Running the whole suite must not dirty the tree it is testing."""
        before = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "-uall"],
            capture_output=True, text=True, check=True,
        ).stdout
        run_gate(TOOL_DIR)
        after = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "-uall"],
            capture_output=True, text=True, check=True,
        ).stdout
        self.assertEqual(before, after, "running the gate changed the working tree")


if __name__ == "__main__":
    unittest.main(verbosity=2)
