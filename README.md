# AI Agent Tools

A curated monorepo of installable tools and skills for AI agents. Each tool is isolated under `tools/`, documents its routing contract, and owns its tests and license notices.

## Catalog

| Tool | Purpose | Entry point |
|---|---|---|
| [`academic-prose`](tools/academic-prose/) | Bilingual Vietnamese/English academic writing, translation, revision, humanization, and fidelity auditing | `tools/academic-prose/SKILL.md` |
| [`ppt-master-officecli`](tools/ppt-master-officecli/) | Beautiful PowerPoint generation/redesign with PPT Master plus read-only OfficeCLI QA and controlled publication | `tools/ppt-master-officecli/SKILL.md` |
| [`jev-decision-benchmark`](tools/jev-decision-benchmark/) | Evidence-first harness to decide whether TypeSafe Jev should replace an LLM at a harness decision point (guardian, monitor); head-to-head benchmark + verified Jevbridge MCP integration | `tools/jev-decision-benchmark/README.md` |

## Validation

```bash
python3 tools/academic-prose/scripts/validate_skill.py
python3 -m unittest discover -s tools/academic-prose/tests -v
python3 -m unittest discover -s tools/ppt-master-officecli/tests -v
python3 -m py_compile tools/ppt-master-officecli/scripts/*.py
bash -n tools/ppt-master-officecli/scripts/install.sh
```

The PowerPoint integration does not vendor the upstream engines. Its installer fetches pinned upstream versions, applies a narrowly scoped MIT-compatible patch, installs only the pinned core generation dependencies, and excludes optional AGPL `PyMuPDF` by default.

## License

Original integration code is MIT licensed. Each tool retains its own license and third-party notices; see the files within its directory.
