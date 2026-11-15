#!/usr/bin/env python3
"""Integrity tests for van-hoc-de-cuong-luan-van.

The invariants this skill must not silently lose:

  * the frontmatter carries the required keys so an installer classifying by
    field (van-hoc) can route it correctly;
  * the frontmatter `name` equals the directory name, so skill discovery cannot
    load a mismatched pair;
  * every reference file named in SKILL.md exists on disk, and every reference
    file on disk is named somewhere in SKILL.md -- a drift either way is a dead
    pointer for the reader;
  * the proposal skeleton lists all nine numbered sections, because the "nine
    sections in committee order" claim is this skill's core promise.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1]
SKILL = TOOL / "SKILL.md"
REFS = TOOL / "references"

NINE_SECTIONS = [
    "Lý do chọn đề tài",
    "Lịch sử nghiên cứu vấn đề",
    "Đối tượng nghiên cứu",
    "Phạm vi nghiên cứu",
    "Mục đích và nhiệm vụ",
    "Phương pháp nghiên cứu",
    "Đóng góp mới",
    "Cấu trúc",
    "Tài liệu tham khảo",
]


def md_files() -> list[Path]:
    out = [SKILL, TOOL / "README.md"]
    out.extend(sorted(REFS.glob("*.md")))
    return [p for p in out if p.exists()]


class TestFrontmatter(unittest.TestCase):
    def test_required_keys_present(self):
        text = SKILL.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if m is None:
            self.fail("SKILL.md must open with a YAML frontmatter block")
        fm = m.group(1)
        for key in ("name:", "description:", "version:", "license:", "platforms:"):
            self.assertIn(key, fm, "frontmatter missing %s" % key)

    def test_name_matches_directory(self):
        text = SKILL.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(\S+)\s*$", text, re.M)
        if m is None:
            self.fail("frontmatter has no name: field")
        self.assertEqual(m.group(1), TOOL.name,
                         "frontmatter name must equal the tool directory name")

    def test_field_category_is_van_hoc(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("van-hoc", text,
                      "SKILL.md must carry the van-hoc field classification")


class TestReferences(unittest.TestCase):
    def test_reference_links_are_not_dead(self):
        """Every references/*.md named in SKILL.md must exist on disk."""
        body = SKILL.read_text(encoding="utf-8")
        named = set(re.findall(r"`references/([\w-]+\.md)`", body))
        on_disk = {p.name for p in REFS.glob("*.md")}
        for name in sorted(named):
            self.assertIn(name, on_disk, "SKILL.md names missing file references/%s" % name)

    def test_no_orphan_reference_files(self):
        """Every references/*.md on disk must be named in SKILL.md."""
        body = SKILL.read_text(encoding="utf-8")
        on_disk = {p.name for p in REFS.glob("*.md")}
        for name in sorted(on_disk):
            self.assertIn("references/%s" % name, body,
                          "orphan reference file %s is never linked from SKILL.md" % name)

    def test_reference_files_have_content(self):
        for p in sorted(REFS.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            self.assertGreater(len(text.strip()), 200,
                               "reference %s looks empty/stub" % p.name)


class TestSkeleton(unittest.TestCase):
    def test_nine_sections_listed(self):
        text = SKILL.read_text(encoding="utf-8")
        for section in NINE_SECTIONS:
            self.assertIn(section, text,
                          "SKILL.md must name section: %s" % section)

    def test_six_failures_documented(self):
        text = SKILL.read_text(encoding="utf-8")
        # the six numbered failure mode has at least six numbered items
        m = re.search(r"## Sáu lỗi làm hỏng đề cương\n(.*?)\n## ", text, re.S)
        if m is None:
            self.fail("SKILL.md must have a 'Sáu lỗi làm hỏng đề cương' section")
        items = re.findall(r"^\d+\.\s", m.group(1), re.M)
        self.assertGreaterEqual(len(items), 6, "failure list must keep all six items")


if __name__ == "__main__":
    unittest.main()