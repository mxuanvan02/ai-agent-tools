# AI Agent Tools

A curated monorepo of installable tools and skills for AI agents. Each tool is isolated under `tools/`, documents its routing contract, and owns its tests and license notices.

## Catalog

| Tool | Purpose | Entry point |
|---|---|---|
| [`academic-prose`](tools/academic-prose/) | Bilingual Vietnamese/English academic writing, translation, revision, humanization, and fidelity auditing | `tools/academic-prose/SKILL.md` |
| [`ppt-master-officecli`](tools/ppt-master-officecli/) | Beautiful PowerPoint generation/redesign with PPT Master plus read-only OfficeCLI QA and controlled publication | `tools/ppt-master-officecli/SKILL.md` |
| [`jev-decision-benchmark`](tools/jev-decision-benchmark/) | Evidence-first harness to decide whether TypeSafe Jev should replace an LLM at a harness decision point (guardian, monitor); head-to-head benchmark + verified Jevbridge MCP integration | `tools/jev-decision-benchmark/README.md` |
| [`evidence-first-research`](tools/evidence-first-research/) | Evidence-first applied research workflow: divergent ideation, live literature gap-scan, claim-to-source gates (TypeSafe Jev via Jevbridge MCP), and reviewer-standard manuscript integrity | `tools/evidence-first-research/SKILL.md` |
| [`system-one-work-loop`](tools/system-one-work-loop/) | Autonomous multi-step work loop (plan/build/check/gate) where a System-One model (Jev, laya offline fallback) gates each step: continue silently vs ask/report/stop; role-lens criteria templates by domain | `tools/system-one-work-loop/SKILL.md` |
| [`evidence-verified-auditing`](tools/evidence-verified-auditing/) | Bulk code/data scan discipline: a scan produces candidates, not findings; confirm against an independent oracle, classify before counting, and prove a verifier can fail before trusting a green result |
| [`github-pr-workflow`](tools/github-pr-workflow/) | GitHub PR lifecycle with evidence gates: branch from the real base, conventional commits, open and verify a PR from the remote, monitor CI, and leave merging to the human |

## Validation

```bash
python3 tools/academic-prose/scripts/validate_skill.py
python3 tools/academic-prose/scripts/public_hygiene_check.py
python3 -m unittest discover -s tools/academic-prose/tests -v
python3 -m unittest discover -s tools/ppt-master-officecli/tests -v
python3 -m py_compile tools/ppt-master-officecli/scripts/*.py
bash -n tools/ppt-master-officecli/scripts/install.sh
python3 tools/ppt-master-officecli/scripts/public_hygiene_check.py
python3 tools/evidence-first-research/scripts/public_hygiene_check.py
python3 -m py_compile tools/evidence-first-research/scripts/*.py
python3 tools/system-one-work-loop/scripts/public_hygiene_check.py
python3 -m py_compile tools/system-one-work-loop/scripts/*.py
python3 tools/evidence-verified-auditing/scripts/public_hygiene_check.py
python3 -m py_compile tools/evidence-verified-auditing/scripts/*.py
python3 tools/github-pr-workflow/scripts/public_hygiene_check.py
python3 tools/jev-decision-benchmark/scripts/public_hygiene_check.py
python3 -m py_compile tools/github-pr-workflow/scripts/*.py
```

The PowerPoint integration does not vendor the upstream engines. Its installer fetches pinned upstream versions, applies a narrowly scoped MIT-compatible patch, installs only the pinned core generation dependencies, and excludes optional AGPL `PyMuPDF` by default.

## License

Original integration code is MIT licensed. Each tool retains its own license and third-party notices; see the files within its directory.
