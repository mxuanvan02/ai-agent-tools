---
name: ppt-master-officecli
description: "Create, redesign, inspect, and publish beautiful .pptx presentations with PPT Master and OfficeCLI."
license: MIT
platforms: [linux, macos]
---

# PPT Master + OfficeCLI

Use this tool when an AI agent must create, redesign, beautify, inspect, or publish a PowerPoint deck.

## Required routing

Select exactly one authoring engine per mutation pass:

- New deck, visual redesign, or beautification → PPT Master.
- Preserve native design, slide identity, notes, or motion → PPT Master round-trip.
- Small deterministic native edit to an existing PPTX → OfficeCLI.
- Read/extract/analyze only → read-only tools; do not initialize authoring.

The exported `.pptx` is the integration boundary. Never let both engines rebuild the same deck in one pass. Every created or mutated deck must pass `scripts/slide_pipeline.py inspect`; use `finalize` for the delivered copy. The shared post-generation OfficeCLI gate is read-only and performs no automatic fixes.

## Setup and use

Read [`README.md`](README.md), then install the pinned toolchain:

```bash
bash scripts/install.sh
python3 scripts/slide_pipeline.py generate my-deck --dir /absolute/workspace --format ppt169
python3 scripts/slide_pipeline.py inspect /absolute/path/draft.pptx
python3 scripts/slide_pipeline.py finalize /absolute/path/draft.pptx /absolute/path/final.pptx
```

A successful finalization writes a byte-identical delivered PPTX plus `manifest.json`, component reports, and `preview.png`. A machine pass does not replace human review of glyphs, spacing, hierarchy, visual correctness, and factual accuracy.
