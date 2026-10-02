---
name: explainer-ladder
description: "Four-rung explainer ladder for learners: text, diagram, page, video."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Education, Explainers, ASD-STE100, Diagrams, Teaching, Communication]
    related_skills: [academic-content-development, excalidraw, manim-video]
---

# Explainer Ladder

Build explanations for learners as a four-rung ladder: controlled text, then
diagram, then interactive page, then video. Each higher rung ADDS to the lower
one; it never replaces it. Every deliverable ships with the rung-1 text so the
content stays verifiable without the visual layer.

Inspired by Andrej Karpathy's 2026-10-02 post on understanding LLM output
(x.com/karpathy/status/2105819303471976479): ask for ASD-STE100-style writing,
then diagrams, then HTML pages, then bespoke explainer videos.

## When to activate

Activate only on an explicit request, for example:

- "Explain X for my students / for undergraduates / for a study group."
- "Build an explainer about X."
- "I need to teach X to non-specialists."

Do NOT activate for ordinary chat questions. The ladder is expensive; a direct
answer is the right default for everything else.

## Before building (at most 2 questions)

1. Audience: school students, undergraduates, or research colleagues?
2. Highest rung needed: text, diagram, interactive page, or video?

Skip both when the request already answers them. State the assumption instead
of asking when the choice is minor and reversible.

## Rung 1 — Controlled text (always produced)

Apply the spirit of ASD-STE100 (a controlled language written for aerospace
maintenance manuals) to the target language. Rules:

- Short sentences: under 20 words. One idea per sentence.
- Active voice: "Do X", never "X should be done".
- One term per concept, used consistently across the whole document.
- Paragraphs of at most 6 sentences; one topic per paragraph.
- Procedures as numbered steps, one bounded action per step.
- If the topic is highly specialised and the strict register reads too stiff,
  use "80% ASD-STE100": keep short sentences and consistent terminology, allow
  moderate clause combination.

For Vietnamese teaching material, prefer native terminology over borrowed
English (thang danh gia, cau lenh, bang dieu khien). See
`references/asd-ste100-vietnamese.md`.

## Rung 2 — Diagram

Activate when the content has structure, process flow, or causal chains that
prose carries poorly.

- Tools: Graphviz `dot` (deterministic, good for pipelines), Mermaid (fastest,
  renders in Markdown), hand-drawn SVG styles for friendly audiences.
- Every diagram ships with 3-5 caption lines written in rung-1 style.
- Export a raster (PNG) and a vector (SVG) copy into the deliverable folder.
- Verify the render visually: fonts (diacritics!), overlaps, unreadable labels.
  A diagram nobody can read is worse than none.

## Rung 3 — Interactive page

Activate when learners must manipulate the material: simulations, drag-and-drop,
self-check questions with feedback.

- Single self-contained HTML file; runs offline; no mandatory CDN.
- A plain-text summary of the whole explanation sits at the top of the page, so
  the content survives even when the interactive layer is skipped or broken.

## Rung 4 — Explainer video

Only on explicit request. Highest cost (tens of minutes of build time); confirm
scope before rendering.

- Tools: Manim-style math animation, or slide-video pipelines; narration via any
  available text-to-speech voice in the target language.
- The script IS the rung-1 text. Write the script first, get it approved, then
  render. Never render first and fix the script after.

## Hard rules

1. Higher rungs add to rung 1; they never replace it. Every deliverable
   includes the controlled text.
2. A beautiful artifact does not make the content correct. Before shipping,
   check every technical claim against a verified source (textbook, paper,
   domain reference). Never invent figures, citations, or examples. Mark any
   unverified claim explicitly as unverified.
3. For deep research topics, load the relevant domain or academic-writing skill
   BEFORE writing, so the content meets field standards.
4. Deliver real files. Sending a description of a diagram is not sending a
   diagram. Verify each file exists and opens before reporting done.

## Acceptance checklist (run before reporting done)

- [ ] Rung-1 text passes the short-sentence and consistent-terminology rules.
- [ ] Every technical claim has a source, or is labelled unverified.
- [ ] Each artifact file exists on disk (list it) and opens/renders.
- [ ] Diagrams were visually checked: no font tofu, no overlaps, labels legible.
- [ ] Video: script was approved before rendering began.
- [ ] The actual files were delivered, not just described.
