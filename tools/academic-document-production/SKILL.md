---
name: academic-document-production
description: Use for page/word budgets, DOCX, LaTeX, journal templates.
license: MIT
metadata:
  version: "1.0.0"
---

# Academic Document Production

This skill owns the **artifact**: how many words and pages fit, which template is real,
how a DOCX is structured and revised, what must be verified before submission, how a
bibliography is rebuilt, and how a translation tool hands text back.

It does **not** own prose. Claim integrity, stance, terminology, calque removal, AI-pattern
scrubbing, rhetorical moves, and section function belong to `academic-prose`. When both
apply, the split is: `academic-prose` decides what the sentence claims; this skill decides
whether the file that carries it is compliant, complete, and verifiable.

The two fail independently. A manuscript can be beautifully argued and 400 words over the
cap; it can be inside every cap and cite `[1]–[22]` with no reference list. Neither skill
detects the other's defect, which is why they are separate.

## Scope routing

Load this skill for any of these:

- a venue states a page limit, word limit, or "including footnotes and references" clause;
- a journal template must be obtained, verified, or refused;
- a thesis or dissertation needs its format rules established (font, margins, spacing, pagination, front matter) — see [Thesis format authority](references/thesis-format-authority.md); prose architecture for the same document is `academic-prose`;
- a manuscript is delivered as `.docx`, especially with tracked changes;
- a LaTeX source must pass pre-submission checks (citations resolve, floats anchored,
  bibliography renders, no overfull boxes);
- citations exist but the reference list is missing, partial, or unverifiable;
- a PDF translation tool must hand text back into the manuscript.

Do not load it to fix a sentence. Send that to `academic-prose`.

## The three budgets

A "word limit" and a "page limit" behave differently, and the instinct that works for one
fails on the other.

**Words: allocate before drafting, never trim afterwards.** Read what the limit includes
first. A cap written as *including footnotes and the reference list* is three budgets, and
in a footnote-citation style the apparatus can consume a quarter of it before the argument
starts. Compute `apparatus ≈ sources × (full note + short notes + bibliography entry)`,
subtract it from the ceiling, and draft against the remainder.

**Pages: measured in points, not words.** Shortening prose in a document whose pages are
full to the last line produces reflow, not relief. Lock the numeric invariant first (the
distinct set of numeric tokens across all prose files), then pull levers in yield order:
captions, cross-section duplication, typography that changes no content (`microtype`
protrusion/expansion only), prose last. `\looseness=-1` and nibbling already-full pages
both failed in measurement.

**Never close a budget gap by deleting evidence.** A limitation, denominator, hedge, or
verified citation cut to save words is a claim-integrity failure, not a formatting decision.
If the content cannot fit, say so and ask.

Details: [Word budget and rendered-artifact compliance](references/word-budget-and-rendered-artifact-compliance.md),
[Word-cap budget compliance](references/word-cap-budget-compliance.md),
[Venue constraint budget](references/venue-constraint-budget.md),
[Page-budget compression](references/page-budget-compression.md).

## Templates: verify or refuse, never improvise

1. Identify the exact target journal **and section**. A university-wide, legacy, or sibling
   section's template is not equivalent.
2. Retrieve only from a journal-controlled source; record URL, filename, retrieval date,
   SHA-256.
3. Compare against a recent published article from that section: page size, columns,
   margins, body font, front matter, abstracts, reference presentation.
4. If the section publishes rules but no downloadable template, do **not** fill another
   section's template or recreate one. Deliver verified source plus a concrete blocker.
5. A derived notes file is not template authority. Every numeric limit must be quoted from
   the template text or a measured published article. A limit that appears only in your own
   summary file is a `fabricated_constraint` until re-derived.
6. A recommended page range is not a submission ceiling. Read what over-length actually
   costs — page charges, demotion to a short track, or rejection — and report that, never
   assume content must be cut.
7. A same-folder `template.docx` can be a decoy. Decide by page size, margins, style set,
   and `word/footnotes.xml` presence, not by filename.

Measured decoy case and the caption/figure fixes:
[HUL template decoy and caption orphan fix](references/hul-template-caption-fix.md).

## DOCX mechanics

Treat DOCX structure as evidence, not appearance. Recover logical headings from OOXML; read
back the **accepted view** with a script rather than through `Paragraph.text`, which omits
runs inside `w:ins` and skips table cells entirely — a correct tracked copy then fails
assertions its clean twin passes, and numbers in tables vanish from word counts.

Bulk replacements need three guards: scope by language and zone, prevent a second pass from
re-translating its own output, and reconcile any split total against the section prose.

Revision gate: [DOCX manuscript revision and delivery gate](references/docx-manuscript-revision-gate.md).
Bulk-replace failures: [DOCX bulk-replace guard](references/docx-bulk-replace-guard.md).
Numbered footnotes and tables: [Numbered footnote and table manuscript](references/numbered-footnote-table-manuscript.md).

## LaTeX pre-submission

Before delivering a `.tex` manuscript: extract prose before any paragraph-level scan (raw
markup manufactures false hits), verify the bibliography heading actually renders, verify
every float is anchored by an in-text `\ref`, confirm every citation resolves, and check
for overfull boxes and missing characters. A manuscript with in-text citations and no
bibliography is a submission blocker even when every prose scan is clean.

Recipes: [LaTeX pre-submission verification](references/latex-pre-submission-verification.md).

## Bibliography rebuild

When a manuscript cites a range but ships no reference list, rebuild it rather than
inventing entries: extract every citation anchor, resolve each against a real record,
separate `verified` from `inferred`, and emit a placeholder for anything unresolved.

Procedure: [Bibliography reconstruction](references/bibliography-reconstruction.md).

## PDF translation handoff

A PDF translation tool owns extraction and reconstruction; this skill owns the handoff
contract. Language decisions stay in `academic-prose`.

Bridge: [PDF Translate integration](references/pdf-translate-integration.md).

## Delivery gate

A document is not delivered until, in this order:

1. the rendered artifact exists and its page count is read from the file, not from memory;
2. every declared constraint is measured on the rendered artifact and reported with its
   scope (body / tables / footnotes / references separately);
3. citations resolve and the bibliography is present and covers the cited range;
4. every float is referenced in running text;
5. the archive is rebuilt from the frozen source and rebuilt again from a clean extraction;
6. any post-packaging prose edit invalidates the archive — refreeze and rebuild.

Never deliver an older archive beside a newer PDF.

## Prose defects are not this skill's job

If the complaint is about wording, rhythm, calque, register, stance, terminology, or AI
patterns, route to `academic-prose`. Fixing those here would fork the rules and let two
skills disagree about the same sentence.
