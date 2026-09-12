# PPT Master + OfficeCLI for AI Agents

A portable, policy-enforced PowerPoint pipeline:

```text
request → one authoring engine → draft.pptx → read-only quality gate → final.pptx
```

PPT Master provides content/layout/SVG-to-native-DrawingML generation and native-preserving round trips. OfficeCLI validates OpenXML, inventories issues and statistics, and renders a contact-sheet preview. The two engines communicate only through `.pptx` artifacts.

## Install

Requirements: Python 3.11+, Git, Node.js/npm, and Linux or macOS.

```bash
bash scripts/install.sh
```

The default prefix is `${XDG_DATA_HOME:-$HOME/.local/share}/ai-agent-tools/ppt-master-officecli`. Override it with `--prefix PATH`. The installer:

1. clones PPT Master at the pinned revision;
2. applies and verifies the package-absolute OPC relationship patch;
3. creates a virtual environment and installs exact core dependency versions;
4. installs exact OfficeCLI `1.0.137` under the prefix;
5. writes `.state/toolchain.json` beside this tool.

It intentionally does not install optional AGPL `PyMuPDF`.

## Commands

```bash
PIPELINE=./scripts/slide_pipeline.py
python3 "$PIPELINE" generate project-name --dir /workspace --format ppt169 --quick
python3 "$PIPELINE" inspect draft.pptx --report-dir qa
python3 "$PIPELINE" finalize draft.pptx final.pptx --report-dir qa
```

Runtime locations can be overridden without editing the lockfile:

- `PPT_MASTER_REPO`
- `PPT_MASTER_PYTHON`
- `OFFICECLI_COMMAND`
- `SLIDE_PIPELINE_STATE`
- `SLIDE_PIPELINE_LOCK`

## Blocking policy

Publication is blocked by toolchain drift, PPT Master delivery failure, OfficeCLI validation/stats/issues/render failure, severity-0 findings, broken references, unresolved note relationships, text overflow, overlap, outside-slide geometry, or undeclared relationships. Other findings remain advisories. No auto-fix is performed.

## Update procedure

Test a candidate in a temporary clone. Reapply the compatibility patch only if upstream still needs it. Run unit tests, two structurally different no-edit round trips, a clean inspect/finalize, an overflow rejection, and a referenced-part deletion rejection. Update the lock only after XML/stat/issue/render parity passes.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for licensing and attribution.
