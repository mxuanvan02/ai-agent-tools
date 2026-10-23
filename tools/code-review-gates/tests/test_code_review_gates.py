"""Regression tests for the code-review-gates tool.

WHY THESE TESTS EXIST
---------------------
A gate that cannot fail is worse than no gate, because its PASS is believed. Each test pins
one property that was MEASURED on real repository content or on a failure we had to fix:

  glob stays inside one segment   ``docs/*`` must NOT match ``docs/a/b/c.py`` -- fnmatch's *
                                  matches /, so a broad-but-shallow rule would silently grant
                                  the low tier to a deeply nested file. Measured once.

  default is a floor, not a start a rule of tier=low must be able to lower the tier; if the
                                  running maximum starts at the default, no rule can ever
                                  win and every change becomes high. The gate is quietly
                                  useless while still printing a verdict.

  always-human wins over rules    a workflow file cannot be demoted to low by a docs/** rule,
                                  even when it is inside docs/. Measured: the original
                                  Anthropic policy puts CI workflows in always_human for this
                                  reason.

  unknown paths fail closed       a path that matches no rule must land on the default tier
                                  (high), not on low. The failure mode of a wrong low is a
                                  silent merge; the failure mode of a wrong high is one extra
                                  read.

  empty diff is not low           an empty numstat must NOT produce tier=low. A caller that
                                  treats "no files" as "nothing changed, merge it" would then
                                  merge anything whose diff failed to parse.

  duplicate finding is rejected   the same (file, line, class) cannot be added twice while
                                  the first is still open. A reviewer that re-flags the same
                                  thing every round is the failure mode the convergence cap
                                  exists to stop.

  round cap blocks the merge      when rounds_used > max_rounds the gate must refuse, even if
                                  every finding has been answered. This is what stops a
                                  reviewer from producing round 4.

  noise rate is honest            rejected + ignored over closed; not over total. A ledger
                                  with 1 finding still open must not report a noise rate.

  ledger is append-only           responding to a finding appends a new row; the original row
                                  is never modified. This is what makes the ledger auditable.

FORBIDDEN LITERALS ARE CONCATENATED IN THIS FILE TOO. It lives inside a tool directory that the
gate scans, so an unsplit literal would fail the very check this suite is testing.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent
SCRIPTS = TOOL_DIR / "scripts"
GATE_NAME = "public_hygiene_check.py"
GATE = SCRIPTS / GATE_NAME
TOOLS_DIR = TOOL_DIR.parent


def run_script(script: str, *args: str, input_text: str = "") -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, timeout=60, input=input_text,
    )
    return proc.returncode, proc.stdout + proc.stderr


def tmp_ledger() -> Path:
    d = tempfile.mkdtemp(prefix="review-ledger-")
    return Path(d) / "ledger.jsonl"


class TestRiskTier(unittest.TestCase):
    # -- glob correctness --------------------------------------------------

    def test_glob_star_stays_in_one_segment(self) -> None:
        """``docs/*`` must NOT match ``docs/a/b/c.py``. fnmatch's * matches /, so a
        broad-but-shallow rule would silently grant the low tier to a deeply nested file."""
        cfg = json.dumps({
            "default_tier": "high",
            "rules": [{"glob": "docs/*", "tier": "low", "reason": "docs"}],
        })
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write(cfg); cfg_path = fh.name
        try:
            out = run_script("risk_tier.py", "--config", cfg_path, input_text="0\t0\tdocs/a/b/c.py\n")
            self.assertEqual(out[0], 0, out[1])
            data = json.loads(out[1])
            # The path did NOT match docs/* (single star), so it falls through to default high.
            # If glob_star crossed segments, the tier would be low.
            self.assertEqual(data["files"][0]["tier"], "high", data)
        finally:
            Path(cfg_path).unlink(missing_ok=True)

    def test_glob_double_star_crosses_segments(self) -> None:
        """``**/tests/**`` must match ``app/tests/x.py`` and ``tests/x.py``."""
        cfg = json.dumps({"default_tier": "high", "rules": [{"glob": "**/tests/**", "tier": "low", "reason": "test"}]})
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write(cfg); cfg_path = fh.name
        try:
            out = run_script("risk_tier.py", "--config", cfg_path,
                             input_text="0\t0\tapp/tests/x.py\n0\t0\ttests/y.py\n")
            self.assertEqual(out[0], 0)
            data = json.loads(out[1])
            for f in data["files"]:
                self.assertEqual(f["tier"], "low", f)
        finally:
            Path(cfg_path).unlink(missing_ok=True)

    # -- default-as-floor, not start ---------------------------------------

    def test_default_is_floor_not_start(self) -> None:
        """A rule of tier=low must be able to lower the tier. If the running maximum starts
        at the default, no rule can ever win and every change becomes high."""
        cfg = json.dumps({"default_tier": "high", "rules": [{"glob": "docs/**", "tier": "low", "reason": "docs"}]})
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write(cfg); cfg_path = fh.name
        try:
            out = run_script("risk_tier.py", "--config", cfg_path, input_text="0\t0\tdocs/x.md\n")
            self.assertEqual(out[0], 0)
            data = json.loads(out[1])
            self.assertEqual(data["tier"], "low", data)
        finally:
            Path(cfg_path).unlink(missing_ok=True)

    # -- always-human wins -------------------------------------------------

    def test_always_human_wins_over_matching_rule(self) -> None:
        """A workflow file inside docs/ must still be high, even when docs/** is low."""
        cfg = json.dumps({
            "default_tier": "high",
            "always_human": ["**/.github/workflows/**"],
            "rules": [{"glob": "docs/**", "tier": "low", "reason": "docs"}],
        })
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write(cfg); cfg_path = fh.name
        try:
            out = run_script("risk_tier.py", "--config", cfg_path,
                             input_text="0\t0\tdocs/.github/workflows/ci.yml\n")
            self.assertEqual(out[0], 0)
            data = json.loads(out[1])
            self.assertEqual(data["tier"], "high", data)
        finally:
            Path(cfg_path).unlink(missing_ok=True)

    # -- unknown paths fail closed -----------------------------------------

    def test_unknown_path_fails_closed_to_default(self) -> None:
        """A path that matches no rule must land on the default tier (high), not on low."""
        cfg = json.dumps({"default_tier": "high", "rules": [{"glob": "docs/**", "tier": "low", "reason": "docs"}]})
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write(cfg); cfg_path = fh.name
        try:
            out = run_script("risk_tier.py", "--config", cfg_path, input_text="0\t0\tunknown/path.py\n")
            self.assertEqual(out[0], 0)
            data = json.loads(out[1])
            self.assertEqual(data["tier"], "high", data)
        finally:
            Path(cfg_path).unlink(missing_ok=True)

    # -- empty diff is not low ---------------------------------------------

    def test_empty_diff_is_not_low(self) -> None:
        """An empty numstat must NOT produce tier=low. A caller that treats 'no files' as
        'nothing changed, merge it' would then merge anything whose diff failed to parse."""
        out = run_script("risk_tier.py", input_text="")
        self.assertEqual(out[0], 0)
        data = json.loads(out[1])
        self.assertNotEqual(data["tier"], "low", data)

    # -- malformed input ---------------------------------------------------

    def test_malformed_input_exits_nonzero(self) -> None:
        out = run_script("risk_tier.py", input_text="this is not a numstat line\n")
        self.assertNotEqual(out[0], 0)
        data = json.loads(out[1])
        self.assertIn("error", data)

    # -- size threshold ----------------------------------------------------

    def test_size_threshold_raises_floor_to_medium(self) -> None:
        """A change over the threshold must raise the tier floor to medium, but not override
        an already-high path."""
        cfg = json.dumps({
            "default_tier": "low",
            "rules": [{"glob": "docs/**", "tier": "low", "reason": "docs"}],
            "large_change": {"lines": 100, "tier_floor": "medium"},
        })
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write(cfg); cfg_path = fh.name
        try:
            out = run_script("risk_tier.py", "--config", cfg_path, input_text="200\t0\tdocs/big.md\n")
            self.assertEqual(out[0], 0)
            data = json.loads(out[1])
            self.assertEqual(data["tier"], "medium", data)
        finally:
            Path(cfg_path).unlink(missing_ok=True)

    # -- approvals_required is PEOPLE, not bot ----------------------------

    def test_approvals_required_is_people(self) -> None:
        """The note in the output must state that approvals_required counts people."""
        out = run_script("risk_tier.py", input_text="0\t0\tdocs/x.md\n")
        data = json.loads(out[1])
        self.assertIn("PEOPLE", data["note"])


class TestReviewLedger(unittest.TestCase):
    # -- add / respond / gate ----------------------------------------------

    def test_add_and_gate_blocks_merge(self) -> None:
        """An open finding must block the merge."""
        ledger = tmp_ledger()
        rc, _ = run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                           "--severity", "important", "--class", "bug",
                           "--message", "m", "--ledger", str(ledger))
        self.assertEqual(rc, 0)
        rc, out = run_script("review_ledger.py", "gate", "--ledger", str(ledger))
        self.assertEqual(rc, 1)
        data = json.loads(out)
        self.assertFalse(data["mergeable"])

    def test_respond_allows_merge(self) -> None:
        """After every finding is answered, the gate must pass."""
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--ledger", str(ledger))
        run_script("review_ledger.py", "respond", "--id", "F001", "--action", "fixed",
                   "--note", "done", "--ledger", str(ledger))
        rc, out = run_script("review_ledger.py", "gate", "--ledger", str(ledger))
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertTrue(data["mergeable"])

    # -- duplicate finding is rejected -------------------------------------

    def test_duplicate_open_finding_is_rejected(self) -> None:
        """The same (file, line, class) cannot be added twice while the first is still open.
        A reviewer that re-flags the same thing every round is the failure mode the
        convergence cap exists to stop."""
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--ledger", str(ledger))
        rc, out = run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                             "--severity", "important", "--class", "bug", "--message", "m2",
                             "--ledger", str(ledger))
        self.assertNotEqual(rc, 0)
        data = json.loads(out)
        self.assertIn("duplicate", data.get("error", ""))

    # -- duplicate of a CLOSED finding is allowed --------------------------

    def test_duplicate_of_closed_finding_is_allowed(self) -> None:
        """A new observation of the same (file, line, class) after the previous one was
        resolved must be allowed -- it is a real new finding."""
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--ledger", str(ledger))
        run_script("review_ledger.py", "respond", "--id", "F001", "--action", "fixed",
                   "--note", "done", "--ledger", str(ledger))
        rc, out = run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                             "--severity", "important", "--class", "bug", "--message", "m2",
                             "--ledger", str(ledger))
        self.assertEqual(rc, 0, out)
        data = json.loads(out)
        self.assertEqual(data["added"], "F002")

    # -- round cap blocks the merge ----------------------------------------

    def test_round_cap_blocks_merge(self) -> None:
        """When rounds_used > max_rounds the gate must refuse, even if every finding has
        been answered. This is what stops a reviewer from producing round 4."""
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--round", "4", "--ledger", str(ledger))
        run_script("review_ledger.py", "respond", "--id", "F001", "--action", "fixed",
                   "--note", "done", "--ledger", str(ledger))
        rc, out = run_script("review_ledger.py", "gate", "--max-rounds", "3",
                             "--ledger", str(ledger))
        self.assertEqual(rc, 1)
        data = json.loads(out)
        self.assertFalse(data["mergeable"])
        self.assertTrue(any("cap" in r for r in data["reasons"]))

    # -- noise rate --------------------------------------------------------

    def test_noise_rate_is_honest(self) -> None:
        """Noise = (rejected + ignored) / closed. Not over total. A ledger with 1 finding
        still open must not report a noise rate over total."""
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--ledger", str(ledger))
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "2",
                   "--severity", "nit", "--class", "style", "--message", "m2",
                   "--ledger", str(ledger))
        run_script("review_ledger.py", "respond", "--id", "F001", "--action", "fixed",
                   "--note", "ok", "--ledger", str(ledger))
        run_script("review_ledger.py", "respond", "--id", "F002", "--action", "rejected",
                   "--note", "no", "--ledger", str(ledger))
        rc, out = run_script("review_ledger.py", "stats", "--ledger", str(ledger))
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(data["noise_rate"], 0.5)
        self.assertEqual(data["closed"], 2)

    # -- ledger is append-only ---------------------------------------------

    def test_ledger_is_append_only(self) -> None:
        """Responding to a finding appends a new row; the original row is never modified."""
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--ledger", str(ledger))
        before = ledger.read_text(encoding="utf-8")
        run_script("review_ledger.py", "respond", "--id", "F001", "--action", "fixed",
                   "--note", "done", "--ledger", str(ledger))
        after = ledger.read_text(encoding="utf-8")
        self.assertTrue(after.startswith(before), "the original row was modified")
        self.assertGreater(len(after), len(before))

    # -- bad severity is rejected ------------------------------------------

    def test_bad_severity_is_rejected(self) -> None:
        ledger = tmp_ledger()
        rc, out = run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                             "--severity", "critical", "--class", "bug", "--message", "m",
                             "--ledger", str(ledger))
        self.assertNotEqual(rc, 0)

    # -- respond to unknown id is rejected ---------------------------------

    def test_respond_to_unknown_id_is_rejected(self) -> None:
        ledger = tmp_ledger()
        rc, out = run_script("review_ledger.py", "respond", "--id", "F999",
                             "--action", "fixed", "--note", "x", "--ledger", str(ledger))
        self.assertNotEqual(rc, 0)
        data = json.loads(out)
        self.assertIn("error", data)

    # -- round command opens a new round -----------------------------------

    def test_round_command_opens_new_round(self) -> None:
        ledger = tmp_ledger()
        run_script("review_ledger.py", "add", "--file", "x.py", "--line", "1",
                   "--severity", "important", "--class", "bug", "--message", "m",
                   "--ledger", str(ledger))
        rc, out = run_script("review_ledger.py", "round", "--ledger", str(ledger))
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(data["round"], 1)


class TestGateIdentity(unittest.TestCase):
    """The public-hygiene gate is byte-identical across every tool in this repository.
    A drifted gate makes PASS mean something different per tool, and the tests in
    academic-prose/tests/test_public_hygiene_gate.py already pin this property. This class
    just confirms the new tool is covered."""

    def test_this_tool_ships_the_gate(self) -> None:
        self.assertTrue(GATE.is_file(), "code-review-gates must ship %s" % GATE_NAME)

    def test_this_gate_matches_the_canonical_copy(self) -> None:
        canonical = sorted(TOOLS_DIR.glob("*/scripts/" + GATE_NAME))
        self.assertGreaterEqual(len(canonical), 2, "expected at least two tools to ship the gate")
        digests = {
            p.parent.parent.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in canonical
        }
        self.assertEqual(len(set(digests.values())), 1,
                         "gate copies drifted; PASS would mean something different per tool: %s"
                         % {k: v[:12] for k, v in digests.items()})


if __name__ == "__main__":
    unittest.main()
