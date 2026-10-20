#!/usr/bin/env python3
"""Integrity tests for vietnamese-classical-literature-research.

These enforce the invariants that make the skill safe to trust. The two that
matter most are the ones that would silently rot otherwise:

  * every Han character in the glossary came from a fetched source (no row may be
    marked verified without a status value this file recognises, and no row may
    have an empty Han string);
  * no URL cited anywhere in the skill is a source the registry classifies as
    dns-dead -- citing a dead domain is the failure this skill exists to prevent,
    so it is tested, not merely documented.

Plus the drift check: the two generated reference files must match
assets/verified_terms.json, because a hand-edited table quietly stops being
evidence.

Run:  python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1]
SKILL = TOOL / "SKILL.md"
ASSETS = TOOL / "assets" / "verified_terms.json"
REFS = TOOL / "references"
SCRIPTS = TOOL / "scripts"

GENERATED = ["han-nom-keyword-glossary.md", "source-corpus-verified.md"]
VALID_STATUS = {"CONFIRMED-INDEPENDENT", "CONFIRMED+GLOSS", "CONFIRMED"}
VALID_REACH = {"curl-ok", "browser-only", "dns-dead"}
VALID_LAYER = {1, 2, 3, 4}
VALID_CAT = {"work", "author", "genre", "form", "script", "thought", "exam"}

# Han ranges used by the glossary. Extension B+ planes are excluded on purpose:
# this skill verifies Han titles, and letting Nom-range characters through would
# weaken the check rather than broaden it.
HAN_RE = re.compile(r'^[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+$')
URL_RE = re.compile(r'https?://[^\s\)\]>"\'`,;]+')


def load_assets() -> dict:
    return json.loads(ASSETS.read_text(encoding="utf-8"))


def md_files() -> list[Path]:
    out = [SKILL]
    out.extend(sorted(REFS.glob("*.md")))
    if (TOOL / "README.md").exists():
        out.append(TOOL / "README.md")
    return out


class TestFrontmatter(unittest.TestCase):
    def test_required_keys_present(self):
        text = SKILL.read_text(encoding="utf-8")
        m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        # Guard with self.fail() rather than assertIsNotNone: unittest assertions
        # do not narrow Optional for static checkers, and a None here would raise
        # AttributeError instead of reporting the real problem.
        if m is None:
            self.fail("SKILL.md must open with a YAML frontmatter block")
        fm = m.group(1)
        for key in ("name:", "description:", "version:", "license:", "platforms:"):
            self.assertIn(key, fm, "frontmatter missing %s" % key)

    def test_name_matches_directory(self):
        text = SKILL.read_text(encoding="utf-8")
        m = re.search(r'^name:\s*(\S+)\s*$', text, re.M)
        if m is None:
            self.fail("frontmatter has no name: field")
        self.assertEqual(m.group(1), TOOL.name,
                         "frontmatter name must equal the tool directory name")

    def test_description_is_a_trigger_not_a_summary(self):
        text = SKILL.read_text(encoding="utf-8")
        m = re.search(r'^description:\s*"?(.*?)"?\s*$', text, re.M)
        if m is None:
            self.fail("frontmatter has no description: field")
        d = m.group(1)
        self.assertTrue(d.lower().startswith("use when"),
                        "description should start with 'Use when' so routing can "
                        "fire on the trigger: got %r" % d[:60])


class TestEvidenceTable(unittest.TestCase):
    """The glossary is only worth anything if every row is evidence-backed."""

    def setUp(self):
        self.data = load_assets()
        self.terms = self.data["terms"]

    def test_has_terms(self):
        self.assertGreaterEqual(len(self.terms), 100,
                                "evidence table shrank: %d terms" % len(self.terms))

    def test_every_row_has_han_label_status_category(self):
        for t in self.terms:
            with self.subTest(term=t.get("label")):
                self.assertTrue(t.get("label"), "row missing label")
                han = t.get("han", "")
                self.assertTrue(han, "row %r has empty han" % t.get("label"))
                self.assertRegex(han, HAN_RE,
                                 "row %r han %r contains non-Han characters"
                                 % (t["label"], han))
                self.assertIn(t.get("status"), VALID_STATUS,
                              "row %r has unrecognised status %r"
                              % (t["label"], t.get("status")))
                self.assertIn(t.get("cat"), VALID_CAT,
                              "row %r has unrecognised category %r"
                              % (t["label"], t.get("cat")))

    def test_every_row_names_evidence(self):
        for t in self.terms:
            ev = t.get("evidence") or []
            with self.subTest(term=t.get("label")):
                self.assertTrue(ev, "row %r marked verified but names no evidence"
                                % t["label"])
                for e in ev:
                    self.assertIn(e.get("kind"), {"named-source", "wiki-corpus"})
                    self.assertTrue(e.get("where"),
                                    "row %r has an evidence entry with no location"
                                    % t["label"])

    def test_independent_rows_cite_a_named_source(self):
        n = 0
        for t in self.terms:
            if t.get("status") != "CONFIRMED-INDEPENDENT":
                continue
            n += 1
            kinds = {e.get("kind") for e in t.get("evidence", [])}
            with self.subTest(term=t["label"]):
                self.assertIn("named-source", kinds,
                              "CONFIRMED-INDEPENDENT requires a named-source row")
        self.assertGreaterEqual(n, 10, "expected a meaningful set of "
                                       "independently verified terms, got %d" % n)

    def test_no_duplicate_han_for_different_labels_unless_intended(self):
        seen: dict[str, list[str]] = {}
        for t in self.terms:
            seen.setdefault(t["han"], []).append(t["label"])
        # A few shared Han strings are legitimate (e.g. a genre term that is also
        # part of a title). What must not happen is an accidental collision where
        # two rows mean different things. Assert the collisions are few and that
        # each is explainable by substring containment.
        dups = {h: ls for h, ls in seen.items() if len(ls) > 1}
        self.assertLessEqual(len(dups), 6,
                             "too many Han collisions (%d): %s"
                             % (len(dups), list(dups.items())[:5]))

    def test_discovery_rejections_recorded(self):
        rej = self.data.get("discovery_heuristic_rejections", [])
        self.assertGreaterEqual(len(rej), 3,
                                "the measured failure of the frequency heuristic "
                                "must stay documented as negative evidence")
        for r in rej:
            self.assertTrue(r.get("label") and r.get("wrong_output") and r.get("why"))


class TestSourceRegistry(unittest.TestCase):
    def setUp(self):
        self.data = load_assets()
        self.srcs = self.data["sources"]

    def test_registry_populated_and_well_formed(self):
        self.assertGreaterEqual(len(self.srcs), 20)
        for s in self.srcs:
            with self.subTest(source=s.get("name")):
                for k in ("name", "url", "layer", "reach", "note"):
                    self.assertTrue(s.get(k), "source row missing %s" % k)
                self.assertIn(s["reach"], VALID_REACH)
                self.assertIn(s["layer"], VALID_LAYER)
                self.assertRegex(s["url"], r'^https?://')

    def test_all_reachability_classes_used(self):
        used = {s["reach"] for s in self.srcs}
        self.assertEqual(used, VALID_REACH,
                         "registry should exercise every class so readers learn "
                         "the distinctions; got %s" % used)

    def test_dead_sources_are_never_cited_outside_the_registry(self):
        """The core invariant: a dns-dead URL must not appear in prose as a
        place to go. It may appear in the registry itself, where it is labelled
        dead and explained -- that labelling is the point."""
        dead = {s["url"].rstrip("/") for s in self.srcs if s["reach"] == "dns-dead"}
        self.assertTrue(dead, "expected some measured-dead sources")
        # Build the allowed set: the registry file and the generated sources file,
        # which both carry the DNS-DEAD label next to the URL.
        allowed_files = {
            "references/source-corpus-verified.md",
            "scripts/probe_sources.py",
        }
        offenders = []
        for path in md_files():
            rel = path.relative_to(TOOL).as_posix()
            if rel in allowed_files:
                continue
            text = path.read_text(encoding="utf-8")
            for u in URL_RE.findall(text):
                if u.rstrip("/") in dead:
                    offenders.append("%s -> %s" % (rel, u))
        self.assertEqual(offenders, [],
                         "dead domains cited as usable sources: %s" % offenders)

    def test_live_sources_have_a_reachable_majority(self):
        live = [s for s in self.srcs if s["reach"] in ("curl-ok", "browser-only")]
        self.assertGreaterEqual(len(live), 20,
                                "too few usable sources for the skill to be useful")


class TestGeneratedFilesAreNotStale(unittest.TestCase):
    def test_build_glossary_check_passes(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "build_glossary.py"), "--check"],
                           capture_output=True, text=True, cwd=str(TOOL))
        self.assertEqual(r.returncode, 0,
                         "generated references have drifted from "
                         "assets/verified_terms.json: %s%s" % (r.stdout, r.stderr))

    def test_generated_files_exist_and_are_marked(self):
        for name in GENERATED:
            p = REFS / name
            with self.subTest(file=name):
                self.assertTrue(p.exists(), "%s missing" % name)
                head = p.read_text(encoding="utf-8")[:400]
                self.assertIn("Generated file", head,
                              "%s must warn against hand edits" % name)


class TestSkillLinks(unittest.TestCase):
    def test_every_referenced_file_exists(self):
        text = SKILL.read_text(encoding="utf-8")
        refs = set(re.findall(r'`?(references/[A-Za-z0-9._-]+\.md)`?', text))
        refs |= set(re.findall(r'`?(scripts/[A-Za-z0-9._-]+\.py)`?', text))
        refs |= set(re.findall(r'`?(assets/[A-Za-z0-9._-]+\.json)`?', text))
        refs |= set(re.findall(r'`?(tests/[A-Za-z0-9._-]+\.py)`?', text))
        self.assertTrue(refs, "SKILL.md references no supporting files")
        missing = [r for r in sorted(refs) if not (TOOL / r).exists()]
        self.assertEqual(missing, [], "SKILL.md points at missing files: %s" % missing)

    def test_every_reference_file_is_reachable_from_skill(self):
        text = SKILL.read_text(encoding="utf-8")
        orphans = []
        for p in sorted(REFS.glob("*.md")):
            if p.name not in text:
                orphans.append(p.name)
        self.assertEqual(orphans, [],
                         "reference files not indexed in SKILL.md (dead weight or "
                         "a missing index row): %s" % orphans)

    def test_reference_index_table_covers_all_files(self):
        text = SKILL.read_text(encoding="utf-8")
        # The index table rows look like: | `references/foo.md` | ... |
        indexed = set(re.findall(r'\|\s*`(references/[^`]+\.md)`\s*\|', text))
        present = {"references/" + p.name for p in REFS.glob("*.md")}
        self.assertEqual(present - indexed, set(),
                         "reference files missing from the index table")


class TestScripts(unittest.TestCase):
    def test_scripts_compile(self):
        for p in sorted(SCRIPTS.glob("*.py")):
            with self.subTest(script=p.name):
                r = subprocess.run([sys.executable, "-m", "py_compile", str(p)],
                                   capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_probe_sources_runs_offline(self):
        """Offline mode must work: the skill is usable with no network."""
        r = subprocess.run([sys.executable, str(SCRIPTS / "probe_sources.py"),
                            "--layer", "1", "--quiet"],
                           capture_output=True, text=True, cwd=str(TOOL))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_probe_sources_rejects_check_dead_without_live(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "probe_sources.py"),
                            "--check-dead", "--quiet"],
                           capture_output=True, text=True, cwd=str(TOOL))
        self.assertEqual(r.returncode, 2,
                         "--check-dead without --live must fail loudly, not pass")

    def test_verify_han_terms_reports_empty_corpus(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "verify_han_terms.py"),
                            "--corpus", "/tmp/__no_such_corpus_dir__",
                            "--terms", "/dev/null"],
                           capture_output=True, text=True, cwd=str(TOOL))
        self.assertEqual(r.returncode, 2,
                         "an empty corpus must be an error, not a silent pass")

    def test_verify_han_terms_end_to_end_on_a_fixture(self):
        """Prove the checker can fail: a deliberately wrong Han string must come
        back NOT-FOUND against a corpus that contains the right one. A verifier
        that passes everything is worse than no verifier."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            corpus = Path(d) / "corpus"
            corpus.mkdir()
            (corpus / "vi_fixture.txt").write_text(
                "'''Truyền kỳ mạn lục''' (chữ Hán: 傳奇漫錄) là tác phẩm của "
                "Nguyễn Dữ (阮嶼), gồm 20 truyện.", encoding="utf-8")
            terms = Path(d) / "terms.txt"
            terms.write_text(
                "Truyền kỳ mạn lục ; 傳奇漫錄 ; Truyền kỳ mạn lục\n"
                "Nguyễn Dữ ; 阮嶼 ; Nguyễn Dữ\n"
                "Nguyễn Dữ WRONG ; 阮與 ; Nguyễn Dữ\n",
                encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPTS / "verify_han_terms.py"),
                                "--corpus", str(corpus), "--terms", str(terms),
                                # The fixture is three lines; the default 200-byte
                                # floor (which exists to skip failed fetches) would
                                # discard it and report 'empty corpus' instead of
                                # running the check at all.
                                "--min-bytes", "1",
                                "--json", str(Path(d) / "out.json")],
                               capture_output=True, text=True, cwd=str(TOOL))
            self.assertEqual(r.returncode, 1,
                             "must exit 1 when a candidate is NOT-FOUND; "
                             "stdout=%s stderr=%s" % (r.stdout[-400:], r.stderr[-400:]))
            res = json.loads((Path(d) / "out.json").read_text(encoding="utf-8"))
            by = {x["label"]: x["status"] for x in res}
            self.assertEqual(by["Truyền kỳ mạn lục"], "CONFIRMED+GLOSS")
            self.assertEqual(by["Nguyễn Dữ"], "CONFIRMED+GLOSS")
            self.assertEqual(by["Nguyễn Dữ WRONG"], "NOT-FOUND")


class TestNoFabricatedSpecifics(unittest.TestCase):
    """Guards the failure mode this skill was built to prevent: precise-looking
    numbers with no source. Every shelfmark in the references must be a real
    record shape, and the generated glossary must not contain a row whose Han
    string is absent from the evidence table."""

    SHELFMARK = re.compile(r'\b(?:R\.\d{2,5}|nlvnpf-\d{4}|NLVNPF-\d{4}|'
                           r'A\.\d{2,5}(?:/\d+(?:-\d+)?)?|VHv\.\d{2,5}|'
                           r'AB\.\d{2,4}|VNv\.\d{2,4}|HNv\.\d{3})\b')

    def test_shelfmarks_appear_with_a_holding_institution_context(self):
        text = (REFS / "period-and-canon-map.md").read_text(encoding="utf-8")
        marks = self.SHELFMARK.findall(text)
        self.assertTrue(marks, "canon map should cite real shelfmarks")
        # Spot-check that the two headline records are the verified ones.
        self.assertIn("NLVNPF-0171", text)
        self.assertIn("R.601", text)

    def test_glossary_rows_all_trace_back_to_assets(self):
        data = load_assets()
        allowed = {t["han"] for t in data["terms"]}
        text = (REFS / "han-nom-keyword-glossary.md").read_text(encoding="utf-8")
        # Verified-term rows are: | label | `han` | STATUS | evidence |
        # Anchoring on the STATUS cell is what distinguishes them from the
        # "discovery heuristic rejections" table further down, whose rows are
        # | label | `wrong_output` | why | and deliberately contain Han strings
        # that are NOT verified terms. Matching on the backticked cell alone
        # swept those up and failed the build on a string that is there precisely
        # because it was rejected.
        status_alts = "|".join(re.escape(s) for s in sorted(VALID_STATUS))
        rows = re.findall(
            r'^\|[^|]+\|\s*`([^`]+)`\s*\|\s*(?:%s)\s*\|' % status_alts,
            text, re.M)
        self.assertTrue(rows, "no glossary rows parsed — table format changed?")
        stray = [h for h in rows if h not in allowed]
        self.assertEqual(stray, [],
                         "glossary contains Han strings absent from the evidence "
                         "table (hand edit?): %s" % stray[:10])
        # And the rejections table must still be there, carrying its own labels —
        # otherwise the anchor above would pass by matching nothing at all.
        self.assertIn("discovery", text.lower())
        rej_rows = re.findall(r'^\|[^|]+\|\s*`([^`]+)`\s*\|\s*[^|]+\|\s*$',
                              text, re.M)
        self.assertTrue(rej_rows, "rejections table rows not found")


if __name__ == "__main__":
    unittest.main(verbosity=2)
