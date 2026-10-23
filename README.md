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
| [`jev-routing-relay-ops`](tools/jev-routing-relay-ops/) | Jev model/effort routing behind a local relay (one endpoint fronting many upstream accounts): verify the wire instead of the config, price pools from measured per-request cost, and gate the guards that catalog-unknown refs silently disable | `tools/jev-routing-relay-ops/SKILL.md` |
| [`explainer-ladder`](tools/explainer-ladder/) | Four-rung explainer ladder for learners: controlled text (ASD-STE100 spirit), diagram, interactive HTML page, video; each rung adds to the one below, every deliverable keeps a verifiable text layer | `tools/explainer-ladder/SKILL.md` |
| [`google-sheets-formatting`](tools/google-sheets-formatting/) | Google Sheets via API, professional from the first write: born-formatted workbooks, real data types and formulas, dropdown validation, status colors, and two-layer read-back (API properties plus rendered screenshots); includes the batchUpdate schema traps that cause HTTP 400 | `tools/google-sheets-formatting/SKILL.md` |
| [`vietnamese-classroom-slide-production`](tools/vietnamese-classroom-slide-production/) | Vietnamese high-school lesson decks end to end: real hands-on screenshots (xterm/Inkscape on Xvfb) verified by OCR against ground truth, projected-font-size math, geometry gates that import house thresholds, mandatory independent peer review before release, and checksum-verified publication | `tools/vietnamese-classroom-slide-production/SKILL.md` |
| [`ui-ux-pro-max`](tools/ui-ux-pro-max/) | UI/UX design intelligence with cognitive psychology, calm 60-30-10 color strategy, extreme minimalism, and multi-stack best practices | `tools/ui-ux-pro-max/SKILL.md` |
| [`web-toolkit`](tools/web-toolkit/) | Three dependency-free browser-automation modules: proxy pool with leases/cooldown/health probes, human-like timing for test stability, and a declarative page-state machine for multi-step forms | `tools/web-toolkit/SKILL.md` |
| [`jev-form-driver`](tools/jev-form-driver/) | Form automation with a measured code/model split: code orchestrates (checklist, values, arithmetic, termination, verification), a System-One decision model selects each field in one parallel request; library + CLI + MCP tool, 4/5 graded fixtures passed at ~$0.00003/run | `tools/jev-form-driver/SKILL.md` |
| [`vietnamese-classical-literature-research`](tools/vietnamese-classical-literature-research/) | **Field: văn học.** Vietnamese classical literature (10th–19th c.) and its Hán-Nôm / Confucian-Buddhist-Taoist context: 155 verified Vietnamese↔漢 keyword bridges, 29 sources classified by measured reachability, five bounded research rounds with an evidence ledger, and four feasibility tests for proposing a direction. Encodes seven measured failures (recalled Han characters, frequency-heuristic guessing, dead domains cited as live, witness dates read as composition dates) | `tools/vietnamese-classical-literature-research/SKILL.md` |
| [`code-review-gates`](tools/code-review-gates/) | Review machinery for changes produced faster than a human can read them: risk tier from the change (not the author), findings need evidence and a response, review rounds are capped, and noise is measured from what authors actually do. Four mechanisms, each with a script and tests that prove the gate can fail | `tools/code-review-gates/SKILL.md` |
| [`product-application-slide-deck`](tools/product-application-slide-deck/) | Build applied-product presentation decks for education competitions: 15-slide structure with real screenshots, speaker notes with video scripts, and highlight animations for demo videos. Validates slide count, element bounds, aspect ratios, and speaker notes | `tools/product-application-slide-deck/SKILL.md` |

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
python3 tools/vietnamese-classroom-slide-production/scripts/public_hygiene_check.py
python3 -m py_compile tools/vietnamese-classroom-slide-production/scripts/*.py
python3 tools/evidence-verified-auditing/scripts/public_hygiene_check.py
python3 -m py_compile tools/evidence-verified-auditing/scripts/*.py
python3 tools/github-pr-workflow/scripts/public_hygiene_check.py
python3 tools/jev-decision-benchmark/scripts/public_hygiene_check.py
python3 -m py_compile tools/github-pr-workflow/scripts/*.py
python3 tools/jev-routing-relay-ops/scripts/public_hygiene_check.py
python3 tools/explainer-ladder/scripts/public_hygiene_check.py
python3 tools/ui-ux-pro-max/scripts/validate_data.py
python3 tools/ui-ux-pro-max/scripts/public_hygiene_check.py
python3 tools/google-sheets-formatting/scripts/public_hygiene_check.py
python3 -m py_compile tools/google-sheets-formatting/scripts/*.py
python3 -m py_compile tools/jev-routing-relay-ops/scripts/*.py
# literature research skill: generated references must match the evidence table,
# 25 integrity tests, hygiene gate, and a compile check
python3 tools/vietnamese-classical-literature-research/scripts/build_glossary.py --check
python3 -m unittest discover -s tools/vietnamese-classical-literature-research/tests -v
python3 tools/vietnamese-classical-literature-research/scripts/public_hygiene_check.py
python3 -m py_compile tools/vietnamese-classical-literature-research/scripts/*.py tools/vietnamese-classical-literature-research/tests/*.py
# code-review-gates: risk tier from the change, findings need evidence, rounds capped, noise measured
python3 tools/code-review-gates/scripts/public_hygiene_check.py
python3 -m py_compile tools/code-review-gates/scripts/*.py
python3 tools/product-application-slide-deck/scripts/public_hygiene_check.py
python3 -m py_compile tools/product-application-slide-deck/scripts/*.py
python3 -m unittest discover -s tools/product-application-slide-deck/tests -v
python3 -m unittest discover -s tools/code-review-gates/tests -v
# offline gate: reads the live routing config, makes no network call, needs no key
python3 tools/jev-routing-relay-ops/scripts/probe_routing_pool.py --self-check --prefix <relay-prefix>
```

The PowerPoint integration does not vendor the upstream engines. Its installer fetches pinned upstream versions, applies a narrowly scoped MIT-compatible patch, installs only the pinned core generation dependencies, and excludes optional AGPL `PyMuPDF` by default.

## License

Original integration code is MIT licensed. Each tool retains its own license and third-party notices; see the files within its directory.
