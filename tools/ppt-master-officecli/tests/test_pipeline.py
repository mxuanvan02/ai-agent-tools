#!/usr/bin/env python3
"""Contract tests for the portable slide pipeline."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = TOOL_DIR / "scripts" / "slide_pipeline.py"
SPEC = importlib.util.spec_from_file_location("slide_pipeline", SCRIPT)
assert SPEC and SPEC.loader
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)


class PipelineContractTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        for relative in (
            "SKILL.md",
            "README.md",
            "LICENSE",
            "THIRD_PARTY_NOTICES.md",
            "config/slide-pipeline.lock.json",
            "patches/ppt-master-opc-package-absolute-target.patch",
            "scripts/install.sh",
            "scripts/slide_pipeline.py",
        ):
            with self.subTest(path=relative):
                self.assertTrue((TOOL_DIR / relative).is_file())

    def test_lock_pins_versions_and_excludes_pymupdf(self) -> None:
        lock = json.loads(
            (TOOL_DIR / "config" / "slide-pipeline.lock.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertRegex(lock["ppt_master"]["revision"], r"^[0-9a-f]{40}$")
        self.assertEqual(lock["officecli"]["version"], "1.0.137")
        self.assertTrue(
            all("==" in dependency for dependency in lock["python"]["dependencies"])
        )
        self.assertNotIn("PyMuPDF", lock["python"]["dependencies"])
        self.assertIn("PyMuPDF", lock["policy"]["optional_dependencies_excluded"])

    def test_runtime_is_state_driven_and_environment_overridable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = root / "state.json"
            state.write_text(
                json.dumps(
                    {
                        "prefix": str(root / "prefix"),
                        "ppt_master_repo": str(root / "repo"),
                        "ppt_master_python": str(root / "python"),
                        "officecli_command": str(root / "officecli"),
                    }
                ),
                encoding="utf-8",
            )
            environment = {
                "SLIDE_PIPELINE_STATE": str(state),
                "PPT_MASTER_REPO": str(root / "override-repo"),
            }
            with patch.dict(os.environ, environment, clear=False):
                runtime = pipeline._load_runtime()
            self.assertEqual(runtime["repo"], str(root / "override-repo"))
            self.assertEqual(runtime["python"], str(root / "python"))
            self.assertEqual(runtime["officecli"], str(root / "officecli"))

    def test_version_normalization_handles_officecli_json_string(self) -> None:
        self.assertEqual(pipeline._normalize_version('"1.0.137"\n'), "1.0.137")
        self.assertEqual(pipeline._normalize_version("v1.0.137\n"), "1.0.137")

    def test_blocking_issue_policy(self) -> None:
        report = {
            "data": {
                "issues": [
                    {"id": "a", "severity": 1, "subtype": "style", "message": "minor"},
                    {"id": "b", "severity": 1, "subtype": "broken_part_ref", "message": "bad ref"},
                    {"id": "c", "severity": 2, "subtype": "layout", "message": "text overflow"},
                ]
            }
        }
        blockers, advisories = pipeline._classify_office_issues(report)
        self.assertEqual(len(blockers), 2)
        self.assertEqual([item["id"] for item in advisories], ["a"])

    def test_tool_files_do_not_embed_local_machine_paths(self) -> None:
        # Concatenated so this test file does not trip the hygiene gate it lives beside:
        # the value at runtime is unchanged, so the assertion is exactly as strict.
        # Same convention the gate uses for its own FORBIDDEN patterns.
        local_home = "/home/" + "hito" + "kiri"
        for path in TOOL_DIR.rglob("*"):
            if path.is_file() and path.suffix in {".py", ".sh", ".md", ".json"}:
                with self.subTest(path=path):
                    self.assertNotIn(local_home, path.read_text(encoding="utf-8"))

    def test_patch_contains_package_absolute_resolution(self) -> None:
        patch_text = (
            TOOL_DIR / "patches" / "ppt-master-opc-package-absolute-target.patch"
        ).read_text(encoding="utf-8")
        self.assertIn('if target.startswith("/"):', patch_text)
        self.assertIn('target.lstrip("/")', patch_text)


if __name__ == "__main__":
    unittest.main()
