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
import importlib.util
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
# Domains, concatenated for the same reason: this file sits inside a scanned tool
# directory, and the gate now has patterns for both of these hostnames.
SCHOOL_DOMAIN = "dhsphue" + ".edu.vn"
VENUE_DOMAIN = "jos." + "hueuni" + ".edu.vn"
VENUE_DOMAIN_BARE = "hueuni" + ".edu.vn"

CITATION_FILE = "references/academic-vietnamese-standard.md"
WORD_LIMIT_FILE = "references/word-budget-and-rendered-artifact-compliance.md"

# THE GATE IS CANONICAL-ONLY INFRASTRUCTURE, AND tests/ IS NOT.
# ---------------------------------------------------------------------------
# Every tool directory of this repository ships a copy of the gate, but the runtime tree
# (~/.hermes/skills/academic-prose/) ships none, and has no sibling tools/ directory either --
# evidence-first-research and system-one-work-loop have no runtime copy at all. The tests/ folder,
# however, IS part of the runtime tree, so this file can legitimately be executed from a place
# where nothing it inspects exists. Measured rather than assumed: copied into a runtime-shaped
# tree it produced 2 failures and 12 errors out of 14, because REPO_ROOT resolved to the tree's
# grandparent and both GATE and TOOLS_DIR were missing.
#
# So skip, with the reason stated, when the gate is not here. A red runtime suite would be a false
# alarm about content that was never supposed to be there, and a failure everyone learns to ignore
# is worse than a skip. Inside the repository HAS_REPO_GATE is true, so all 14 tests really run --
# which CI proves on every push.
HAS_REPO_GATE = GATE.is_file() and TOOLS_DIR.is_dir()
SKIP_REASON = ("the public-hygiene gate is canonical-only infrastructure: no %s and no %s/ here, "
               "so this suite only runs inside the monorepo" % (GATE_NAME, TOOLS_DIR.name))


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


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
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


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
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


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
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


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
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


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
class TestDomainPatternsAreCaught(unittest.TestCase):
    """Hostnames identify an employer or a submission target as precisely as names do.

    A name-only pattern list left the strongest identifier uncovered: six domain
    occurrences shipped across two tools while every gate printed PASS. These tests
    pin both domain patterns, including the bare-journal form and the realistic
    hard-wrap case, plus the one wrap shape that CANNOT be caught -- recorded as a
    known limit so it is documented rather than discovered again as a false alarm.
    """

    def test_school_domain_is_caught(self) -> None:
        tmp = build_tool({"notes.md": "Tra cứu tại " + SCHOOL_DOMAIN + "/huong-dan.\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("institution-7", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_journal_domain_with_subdomain_is_caught(self) -> None:
        tmp = build_tool({"notes.md": "Search " + VENUE_DOMAIN + " for each term.\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("venue-1", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_journal_domain_without_subdomain_is_caught(self) -> None:
        """The optional (?:jos\\.)? group must not narrow the pattern to one host."""
        tmp = build_tool({"notes.md": "Portal cấp trên (" + VENUE_DOMAIN_BARE + ") cho HTML tĩnh.\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("venue-1", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_journal_domain_split_at_the_subdomain_dot_is_caught(self) -> None:
        """Hard-wrapped prose can break a URL at a dot; the pattern must survive it.

        normalise() collapses the newline to one space, so this case passes only
        because the subdomain group is optional: the bare domain still matches on
        the second line. Measured, and the reason that group exists.
        """
        tmp = build_tool({"notes.md": "Search jos.\n" + VENUE_DOMAIN_BARE + " for terms.\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("venue-1", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_domain_split_mid_token_is_a_known_limit(self) -> None:
        """Pinned as a limit, NOT as a pass: do not "fix" this by relaxing normalise.

        normalise() collapses whitespace to a single space; it never deletes it. A
        domain has no internal space, so a break inside the hostname leaves
        "dhsph ue.edu.vn" in the normalised text and a spaceless pattern cannot match.
        No wrapping convention produces this shape -- markdown and hand wrapping break
        at whitespace -- so the gate stays correct and the expectation would be
        impossible. A mutation suite that asserted a catch here reported a false
        failure; the assertion is inverted on purpose so that anyone who later
        deletes whitespace in normalise() sees this test change meaning.
        """
        split = SCHOOL_DOMAIN[:5] + "\n" + SCHOOL_DOMAIN[5:]
        tmp = build_tool({"notes.md": "Tra cứu tại " + split + "/mau.\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
            self.assertIn("PASS", out)
            self.assertNotIn("institution-7", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_a_generic_descriptor_is_not_caught(self) -> None:
        """The sanitised replacement used in the references must stay legal."""
        tmp = build_tool({"notes.md": "<venue-site> search \"thực nghiệm\" -> 20 articles\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
            self.assertIn("PASS", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
class TestSeparatorVariantsAndDescriptorCollisions(unittest.TestCase):
    """Two properties that pull in opposite directions, both measured on real content.

    A token whose canonical form carries a hyphen also ships with an en dash, an
    underscore or no separator at all -- 15 of 69 identifier occurrences in one tool
    used U+2013 and were invisible to every hyphen-built pattern. So separator
    flexibility is required.

    But it cannot be applied uniformly. One project's codename and its APPROVED
    descriptor differ only by case and separator, so a separator-flexible pattern for
    that token flagged 37 occurrences of legitimate prose. The other three projects
    have codenames and descriptors that are entirely different strings, so they are
    safe. This suite pins both halves: the variants must be caught, and the
    descriptors must not be.
    """

    # Concatenated for the reason given in the module docstring.
    CODENAME_A = "CAW" + "-" + "VoU"
    CODENAME_B = "RA" + "BS"
    CODENAME_C_GLUED = "Probe" + "Transmit"
    CODENAME_C_DESCRIPTOR = "probe" + "-transmit"
    CODENAME_D = "ECM" + "-" + "TQAG"
    CODENAME_E = "ST" + "AIS"
    ABBREV_FUNDER = "DH" + "H"
    ABBREV_INSTITUTE = "HO" + "EIT"

    EN_DASH = "\u2013"
    EM_DASH = "\u2014"

    def test_every_separator_variant_of_a_hyphenated_codename_is_caught(self) -> None:
        left, right = self.CODENAME_D.split("-")
        for sep_name, sep in [("hyphen", "-"), ("en dash", self.EN_DASH),
                              ("em dash", self.EM_DASH), ("underscore", "_"),
                              ("space", " "), ("none", "")]:
            with self.subTest(separator=sep_name):
                tmp = build_tool({"notes.md": f"the {left}{sep}{right} protocol\n"})
                try:
                    rc, out = run_gate(Path(tmp))
                    self.assertEqual(rc, 1, f"{sep_name} variant not caught: {out}")
                    self.assertIn("codename-4", out)
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)

    def test_underscore_joined_path_forms_are_caught(self) -> None:
        """`\\b` does not bound an underscore, which is why these used to pass."""
        cases = {
            "codename-2": [f"{self.CODENAME_B}_summary.csv",
                           f"run_{self.CODENAME_B}_adaptive_bandwidth.py",
                           f"/tmp/{self.CODENAME_B.lower()}_venv"],
            "codename-5": [f"bài bandwidth-scheduling_{self.CODENAME_E}_clean/"],
            "codename-1": [f"{self.CODENAME_A.replace('-', '_')}_main.pdf"],
        }
        for label, texts in cases.items():
            for t in texts:
                with self.subTest(label=label, text=t):
                    tmp = build_tool({"notes.md": f"path {t}\n"})
                    try:
                        rc, out = run_gate(Path(tmp))
                        self.assertEqual(rc, 1, out)
                        self.assertIn(label, out)
                    finally:
                        shutil.rmtree(tmp, ignore_errors=True)

    def test_lowercase_and_compound_forms_of_an_abbreviation_are_caught(self) -> None:
        """A boundary assertion cannot see these, which is why they are substrings."""
        for text in (f"project code {self.ABBREV_FUNDER}2026",
                     f"TM{self.ABBREV_FUNDER}",
                     f"\\logo{self.ABBREV_FUNDER}" + "{0.6cm}",
                     f"\\definecolor{{{self.ABBREV_INSTITUTE}Blue}}"):
            with self.subTest(text=text):
                tmp = build_tool({"notes.md": text + "\n"})
                try:
                    rc, out = run_gate(Path(tmp))
                    self.assertEqual(rc, 1, out)
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)

    def test_ordinary_words_containing_a_codename_are_not_caught(self) -> None:
        """A plain substring pattern would flag all of these forever."""
        clean = ["He grabs the cable", "the crabs were boiled", "drabs of paint",
                 "arabs and arabic text", "The subrabs module",
                 "the dhh gene in zebrafish", "cdhh protocol variant"]
        tmp = build_tool({f"n{i}.md": s + "\n" for i, s in enumerate(clean)})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
            self.assertIn("PASS", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_colliding_descriptor_is_not_caught_but_its_codename_is(self) -> None:
        """The one token where descriptor and codename differ only by case+separator.

        Strengthening codename-3 to be separator-flexible makes this test fail on the
        descriptor line, which is the intended signal: the fix is to rename the
        project's descriptor, not to accept 37 false positives in approved prose.
        """
        # the approved descriptor, used 33 times in that tool, must stay legal
        tmp = build_tool({"notes.md": f"dùng lại venv của bài {self.CODENAME_C_DESCRIPTOR}\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
            self.assertIn("PASS", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        # the glued codename must still be caught
        tmp = build_tool({"notes.md": f"pipeline {self.CODENAME_C_GLUED}\n"})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 1, out)
            self.assertIn("codename-3", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_three_non_colliding_descriptors_are_not_caught(self) -> None:
        """These projects' descriptors are different strings from their codenames,
        so separator flexibility is safe for them and must not regress."""
        clean = ["bài bandwidth-scheduling", "bài AoI-greenhouse", "bài TQA-generation",
                 "<project>_summary.csv", "https://<conf>.vn",
                 "\\logo<inst>{0.6cm}", "<funder>2025-19-07", "<inst>Blue"]
        tmp = build_tool({f"d{i}.md": s + "\n" for i, s in enumerate(clean)})
        try:
            rc, out = run_gate(Path(tmp))
            self.assertEqual(rc, 0, out)
            self.assertIn("PASS", out)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def load_gate_module():
    """Import the gate in-process to inspect FORBIDDEN itself, not just its verdict."""
    spec = importlib.util.spec_from_file_location("phc_under_test", GATE)
    assert spec is not None and spec.loader is not None, "gate did not load"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(HAS_REPO_GATE, SKIP_REASON)
class TestEveryPatternIsAlive(unittest.TestCase):
    """A dead pattern prints PASS on the exact leak it exists to catch.

    Measured defect: five FORBIDDEN entries concatenated a NON-raw string half
    ("BS\\b" is backspace 0x08, not a word boundary), so the compiled pattern
    could never match anything -- including two codenames and an institution
    pattern whose real leaks were sitting in shipped files while the gate
    reported PASS. The wrapped-token suite proved a line break cannot defeat a
    LIVE pattern; this suite proves every pattern is live in the first place.
    One probe per label makes the whole inventory self-checking: a pattern that
    stops matching its canonical token fails here instead of failing silently.
    """

    def setUp(self) -> None:
        self.patterns = dict(load_gate_module().FORBIDDEN)

    def test_no_compiled_pattern_contains_a_backspace(self) -> None:
        for label, pat in self.patterns.items():
            with self.subTest(label=label):
                self.assertNotIn(
                    chr(8), pat.pattern,
                    "compiled pattern contains literal backspace 0x08: a non-raw "
                    "string half turned \\b into a control character, so this "
                    "pattern can never match and its gate verdict is worthless",
                )

    def test_every_pattern_matches_its_canonical_probe(self) -> None:
        # Probes are concatenated for the reason given in the module docstring:
        # this file lives inside the scanned tool directory.
        probes = {
            "personal-name": "đã nhờ " + PERSONAL_NAME + " soát lại",
            "host-username": "clone vào /home/" + HOST_USERNAME + "/repos",
            "old-skill-name": "xem skill anh-van-" + "research-workflow",
            "internal-path": "dữ liệu nằm ở /media/" + "SAS/Research",
            "codename-1": "bản " + "CAW-" + "VoU chưa công bố",
            "codename-2": "trong phiên " + "RA" + "BS trước",
            "codename-3": "pipeline " + "Probe" + "Transmit",
            "codename-4": "bài " + CODENAME,
            "codename-5": "thư mục " + "ST" + "AIS đang chạy",
            "codename-6": "dự án " + "Mekong-" + "Trace",
            "codename-7": "bộ dữ liệu " + "HO" + "EIT-" + "LegalQA",
            "institution-1": "trường " + INSTITUTION_1,
            "institution-2": "Đại học " + "Huế thông báo",
            "institution-3": INSTITUTION_3 + " press",
            "institution-4": "mã tài trợ DH" + "H",
            "institution-5": "viện " + "HO" + "EIT",
            "institution-6": "campus " + "Thu " + "Dau Mot",
            # domain probes are split the same way the gate splits its patterns:
            # this file sits inside a scanned tool directory.
            "institution-7": "tệp hướng dẫn ở " + "dhsphue" + ".edu.vn",
            "venue-1": "tra cứu tại " + "jos." + "hueuni" + ".edu.vn",
            "secret-token": "token " + "ghp_" + "A1b2C3d4E5f6G7h8I9j0",
            "secret-key": SECRET_KEY,
            "placeholder": "kết quả\x00cũ",
        }
        self.assertEqual(
            set(probes), set(self.patterns),
            "probe inventory and FORBIDDEN diverged: every label needs a probe, "
            "and a probe without a label tests nothing",
        )
        for label, probe in probes.items():
            with self.subTest(label=label):
                self.assertIsNotNone(
                    self.patterns[label].search(probe),
                    f"{label} does not match its canonical probe -- the pattern is "
                    "dead and the gate would print PASS over this leak",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
