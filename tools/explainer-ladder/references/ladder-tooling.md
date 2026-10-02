# Ladder tooling: concrete commands per rung

Generic commands only. Adapt paths to the machine in use; never hard-code one
operator's home directory into a deliverable.

## Rung 2 - diagrams

Graphviz (deterministic pipelines, good label control):

```bash
dot -Tpng -Gdpi=150 flow.dot -o flow.png
dot -Tsvg flow.dot -o flow.svg
```

Vietnamese diacritics require a Unicode-capable font on the renderer host.
Always inspect the PNG after rendering:

1. Tofu boxes = missing glyphs in the chosen font.
2. Overlapping edge labels = switch layout engine (`dot` vs `neato`) or shorten
   labels.
3. `dashdot` edge style is unsupported by some renderers and silently degrades
   to a solid line; use `dashed` plus colour to distinguish routes.

Mermaid renders natively in GitHub/GitLab Markdown; prefer it when the diagram
lives inside a README or issue.

## Rung 3 - interactive page

- One self-contained `.html` file: inline CSS and JS, no mandatory CDN.
- Text summary of the whole explanation at the top of the page.
- Test by opening the file directly (`file://`) with the network disabled.

## Rung 4 - video

- Math/algorithm animation: Manim community edition.
- Slide-based video: render slides to images, add narration, concatenate with
  FFmpeg.
- Narration: any available TTS voice in the target language; keep one voice per
  video.
- Workflow: script (rung-1 text) -> approval -> render. Never the reverse.

## Delivery

- Keep every artifact of one explainer in one dated topic folder.
- Verify files exist and open before reporting done (`ls`, plus a render/parse
  check per format).
- Send the actual files through the chat channel in use; a description is not a
  delivery.
