"""Regression tests for pr_review_gate.py -- the command a PR workflow calls before merging.

WHY THESE TESTS EXIST
---------------------
Every rule below is a way an approval can LOOK satisfied while the change is not reviewed:

  bot approval is not a person   an agent approving its own PR must never fill a human slot.
                                 Measured: GitHub renders bots as `login[bot]` with
                                 type=Bot, and both signals must be rejected.

  stale approval is not approval  "an approval covers one specific commit" -- an approval
                                 given before the last push is about code that no longer
                                 exists. The head sha must match.

  latest review wins              approve-then-request-changes is a reviewer who changed their
                                 mind. Replaying reviews in order and keeping the last one
                                 per login is what stops the earlier APPROVED from counting.

  draft is not mergeable          a draft PR is explicitly not ready; merging it because the
                                 checks are green defeats the point of the draft.

  open findings block             an unanswered finding is the case the ledger exists for.

  round cap blocks                a fourth round means the approach is wrong, not that the
                                 reviewer needs a fifth pass.

  cannot-evaluate is exit 2       THE most important property: if gh is missing, the PR is
                                 unreadable, or the fixture is broken, the answer is "I do not
                                 know" -- never "mergeable". A caller that maps 2 to 0 merges
                                 anything whose check crashed. Verified by pointing the tool
                                 at a missing binary and a malformed fixture.

  empty diff is not low           a PR that reports zero changed files must not be classified
                                 low; that would make an unreadable diff the cheapest merge.

Fixture PRs are built in-test so the expected verdict is visible next to the reviews that
produce it, rather than hidden in a JSON blob someone has to decode.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL_DIR = HERE.parent
SCRIPTS = TOOL_DIR / "scripts"
HEAD = "aaaa1111bbbb2222"


def make_pr(**over) -> dict:
    pr = {
        "number": 42,
        "state": "OPEN",
        "isDraft": False,
        "mergeable": "MERGEABLE",
        "headRefOid": HEAD,
        "headRefName": "feat/x",
        "baseRefName": "main",
        "author": {"login": "author", "type": "User"},
        "reviews": [],
        "files": [],
    }
    pr.update(over)
    return pr


def review(login: str, state: str, sha: str = HEAD, user_type: str = "User") -> dict:
    return {"author": {"login": login, "type": user_type}, "state": state,
            "commit": {"oid": sha}}


class GateCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="pr-gate-"))
        self.ledger = self.tmp / "ledger.jsonl"
        self.files = self.tmp / "files.tsv"
        self.pr_json = self.tmp / "pr.json"
        # A change that classifies HIGH (unmatched path), so approvals_required == 2.
        self.files.write_text("20\t3\tapp/server.py\n", encoding="utf-8")

    def run_gate(self, pr: dict, *extra: str, env: dict | None = None) -> tuple[int, dict]:
        self.pr_json.write_text(json.dumps(pr), encoding="utf-8")
        cmd = [sys.executable, str(SCRIPTS / "pr_review_gate.py"),
               "--offline", "--pr-json", str(self.pr_json),
               "--pr-files", str(self.files), "--ledger", str(self.ledger), *extra]
        full_env = {**os.environ, **(env or {})}
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=full_env)
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail("gate printed non-JSON: stdout=%r stderr=%r" % (proc.stdout, proc.stderr))
        return proc.returncode, data

    # -- the happy path -----------------------------------------------------

    def test_two_human_approvals_on_head_allow_merge(self) -> None:
        rc, data = self.run_gate(make_pr(reviews=[review("alice", "APPROVED"),
                                                  review("bob", "APPROVED")]))
        self.assertEqual(rc, 0, data)
        self.assertTrue(data["mergeable"])
        self.assertEqual(data["approvals_counted"], ["alice", "bob"])
        self.assertEqual(data["approvals_required"], 2)

    # -- bot approval never fills a human slot ------------------------------

    def test_bot_approval_does_not_count(self) -> None:
        """An agent approving its own PR must never fill a human slot. Both signals rejected:
        login ending in [bot] and type=Bot."""
        rc, data = self.run_gate(make_pr(reviews=[
            review("alice", "APPROVED"),
            review("dependabot[bot]", "APPROVED"),
            review("claude-agent", "APPROVED", user_type="Bot"),
        ]))
        self.assertEqual(rc, 1, data)
        self.assertEqual(data["approvals_counted"], ["alice"])
        self.assertEqual(data["approvals_needed_more"], 1)

    def test_bot_approval_alone_blocks_a_low_tier_change(self) -> None:
        """Even a tier that needs ONE person is not cleared by a bot."""
        self.files.write_text("5\t0\tdocs/readme.md\n", encoding="utf-8")
        rc, data = self.run_gate(make_pr(reviews=[review("claude[bot]", "APPROVED")]))
        # docs-only => low => 0 approvals required => mergeable. That is the policy, not the bot.
        self.assertEqual(rc, 0, data)
        self.assertEqual(data["approvals_required"], 0)
        self.assertEqual(data["approvals_counted"], [])

    # -- stale approval -----------------------------------------------------

    def test_approval_on_older_commit_does_not_count(self) -> None:
        """An approval given before the last push is about code that no longer exists."""
        rc, data = self.run_gate(make_pr(reviews=[
            review("alice", "APPROVED"),
            review("bob", "APPROVED", sha="oldoldsha0000"),
        ]))
        self.assertEqual(rc, 1, data)
        self.assertEqual(data["approvals_counted"], ["alice"])
        self.assertTrue(any("approval" in r for r in data["reasons"]))

    # -- latest review wins -------------------------------------------------

    def test_approve_then_request_changes_does_not_count(self) -> None:
        """Approve-then-request-changes is a reviewer who changed their mind."""
        rc, data = self.run_gate(make_pr(reviews=[
            review("alice", "APPROVED"),
            review("bob", "APPROVED"),
            review("bob", "CHANGES_REQUESTED"),
        ]))
        self.assertEqual(rc, 1, data)
        self.assertEqual(data["approvals_counted"], ["alice"])

    def test_changes_requested_then_approved_does_count(self) -> None:
        """The mirror case: a reviewer satisfied after changes must count."""
        rc, data = self.run_gate(make_pr(reviews=[
            review("alice", "APPROVED"),
            review("bob", "CHANGES_REQUESTED"),
            review("bob", "APPROVED"),
        ]))
        self.assertEqual(rc, 0, data)
        self.assertEqual(sorted(data["approvals_counted"]), ["alice", "bob"])

    # -- draft / conflicts --------------------------------------------------

    def test_draft_blocks(self) -> None:
        rc, data = self.run_gate(make_pr(isDraft=True, reviews=[review("alice", "APPROVED"),
                                                               review("bob", "APPROVED")]))
        self.assertEqual(rc, 1, data)
        self.assertTrue(any("draft" in r.lower() for r in data["reasons"]))

    def test_conflicting_blocks(self) -> None:
        rc, data = self.run_gate(make_pr(mergeable="CONFLICTING",
                                         reviews=[review("alice", "APPROVED"),
                                                  review("bob", "APPROVED")]))
        self.assertEqual(rc, 1, data)
        self.assertTrue(any("conflict" in r.lower() for r in data["reasons"]))

    # -- ledger integration -------------------------------------------------

    def test_open_finding_blocks_even_with_approvals(self) -> None:
        """An unanswered finding is the case the ledger exists for."""
        subprocess.run([sys.executable, str(SCRIPTS / "review_ledger.py"), "add",
                        "--file", "app/server.py", "--line", "9", "--severity", "important",
                        "--class", "null-deref", "--message", "m", "--ledger", str(self.ledger)],
                       check=True, capture_output=True, text=True)
        rc, data = self.run_gate(make_pr(reviews=[review("alice", "APPROVED"),
                                                  review("bob", "APPROVED")]))
        self.assertEqual(rc, 1, data)
        self.assertEqual(data["open_findings"], 1)

    def test_answered_finding_does_not_block(self) -> None:
        subprocess.run([sys.executable, str(SCRIPTS / "review_ledger.py"), "add",
                        "--file", "app/server.py", "--line", "9", "--severity", "important",
                        "--class", "null-deref", "--message", "m", "--ledger", str(self.ledger)],
                       check=True, capture_output=True, text=True)
        subprocess.run([sys.executable, str(SCRIPTS / "review_ledger.py"), "respond",
                        "--id", "F001", "--action", "fixed", "--note", "guard added",
                        "--ledger", str(self.ledger)], check=True, capture_output=True, text=True)
        rc, data = self.run_gate(make_pr(reviews=[review("alice", "APPROVED"),
                                                  review("bob", "APPROVED")]))
        self.assertEqual(rc, 0, data)
        self.assertEqual(data["open_findings"], 0)

    def test_round_cap_blocks(self) -> None:
        subprocess.run([sys.executable, str(SCRIPTS / "review_ledger.py"), "add",
                        "--file", "app/server.py", "--line", "9", "--severity", "important",
                        "--class", "null-deref", "--message", "m", "--round", "4",
                        "--ledger", str(self.ledger)], check=True, capture_output=True, text=True)
        subprocess.run([sys.executable, str(SCRIPTS / "review_ledger.py"), "respond",
                        "--id", "F001", "--action", "fixed", "--note", "ok",
                        "--ledger", str(self.ledger)], check=True, capture_output=True, text=True)
        rc, data = self.run_gate(make_pr(reviews=[review("alice", "APPROVED"),
                                                  review("bob", "APPROVED")]),
                                 "--max-rounds", "3")
        self.assertEqual(rc, 1, data)
        self.assertTrue(any("cap" in r for r in data["reasons"]))

    # -- fail closed: the most important property --------------------------

    def test_cannot_evaluate_exits_2_not_0(self) -> None:
        """If the inputs are broken the answer must be 'I do not know' (2), never 0.
        A caller that maps 2 to 0 merges anything whose check crashed."""
        # Missing --pr-files
        self.pr_json.write_text(json.dumps(make_pr()), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "pr_review_gate.py"), "--offline",
             "--pr-json", str(self.pr_json), "--ledger", str(self.ledger)],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIsNone(data["mergeable"])

    def test_malformed_fixture_exits_2(self) -> None:
        self.pr_json.write_text("{not json", encoding="utf-8")
        self.files.write_text("20\t3\tapp/server.py\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "pr_review_gate.py"), "--offline",
             "--pr-json", str(self.pr_json), "--pr-files", str(self.files),
             "--ledger", str(self.ledger)],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)

    def test_empty_diff_exits_2_not_low(self) -> None:
        """A PR reporting zero changed files must not be classified low."""
        self.files.write_text("", encoding="utf-8")
        rc, data = self.run_gate(make_pr())
        self.assertEqual(rc, 2, data)
        self.assertIsNone(data["mergeable"])

    def test_without_gh_it_refuses_instead_of_guessing(self) -> None:
        """With gh unavailable and no fixtures, the tool must exit 2 rather than assume."""
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "pr_review_gate.py"), "--pr", "42"],
            capture_output=True, text=True, timeout=60,
            env={**os.environ, "PATH": "/nonexistent"})
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIsNone(data["mergeable"])

    # -- tier drives the number, and the number is people ------------------

    def test_tier_low_needs_no_approvals(self) -> None:
        self.files.write_text("5\t0\tdocs/readme.md\n", encoding="utf-8")
        rc, data = self.run_gate(make_pr())
        self.assertEqual(rc, 0, data)
        self.assertEqual(data["approvals_required"], 0)

    def test_tier_high_needs_two(self) -> None:
        rc, data = self.run_gate(make_pr(reviews=[review("alice", "APPROVED")]))
        self.assertEqual(rc, 1, data)
        self.assertEqual(data["approvals_required"], 2)
        self.assertEqual(data["approvals_needed_more"], 1)

    def test_ci_workflow_file_forces_two_approvals(self) -> None:
        self.files.write_text("3\t1\t.github/workflows/ci.yml\n", encoding="utf-8")
        rc, data = self.run_gate(make_pr(reviews=[review("alice", "APPROVED")]))
        self.assertEqual(rc, 1, data)
        self.assertEqual(data["tier"], "high")
        self.assertEqual(data["approvals_required"], 2)


if __name__ == "__main__":
    unittest.main()
