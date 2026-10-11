# Batch lesson decks from structured JSON — motif generator + fail-closed gates

When a course has many lessons with the SAME pedagogical shape (warm-up → problem
statement → knowledge units → practice → application → wrap-up), hand-authoring one
slide spec per lesson is slow and drifts off standard. The proven alternative: keep
ONE lesson-content JSON schema and ONE generator that emits per-lesson slide specs,
then push every lesson through the same fail-closed gates. One course of 20+ lessons
was shipped this way; every lesson passed the same three gates with zero manual
slide surgery after the generator stabilized.

## Why the generator wins

- Content lives in JSON extracted from the authoritative source (textbook/curriculum).
  The generator only re-presents content; it never invents knowledge. Fix content in
  JSON, regenerate — never patch generated specs by hand (they get overwritten).
- Every systemic defect found while building one lesson (a scaffolding phrase, a
  person-pronoun, a minute count colliding with the real time window) is fixed ONCE in
  the generator or its neutralization table, then all lessons regenerate clean.
  In practice ~10 generator-level fixes cleaned the whole remaining batch.
- The gate set is shared, so "passed" means the same thing for every lesson.

## Lesson JSON schema (18 keys, uniform across lessons)

Metadata: `lesson_number`, `title`, `slug`, `file_name`, `period`, `week`, optional
`theme`. Content: `warmup` (title, cards, guiding question), `objectives` (cards),
`deliverables` (what learners submit), `thread_question` (asked at the start, answered
by the knowledge sections), `sections` (each: title, sub, icon, cross-subject link,
`copy_to_notebook` lines, cards, optional table, `connections`), `practice` (each
task: title, steps, expected results, method), `application` (situations), `summary`,
`common_mistakes`, `notebook_page`, `takeaways`, `closing`, `homework`.

## Generator pipeline

1. **Timeline scheduler.** Each slide has a role (cover, objectives, agenda, warmup,
   problem, unit_divider, unit_copy, unit_apply, practice_task, practice_answer,
   application, review, mistakes, bridge, notebook, takeaways, closing) with
   (default, min, max) minutes. Roles are laid out, then minutes are grown/shrunk
   within bounds in priority order until the total equals the lesson length exactly
   (e.g. 90). Windows are contiguous `[a–b]` and written into BOTH the on-slide
   subtitle and the speaker notes, so the timeline auditor can cross-check them.
2. **Neutralization table.** Ordered regex substitutions applied to every on-slide
   string: learner-facing person pronouns ("you/we/I", "your group") removed or
   rewritten to neutral task statements; scaffolding phrases that talk about the
   teaching process instead of content ("as we just learned", "to get into theory")
   rewritten to content-bearing wording. Longest phrases first, single words last.
   Ambiguous domain nouns (a "class/layer" that is a graphics layer, a "group" that
   is a parameter category) are rewritten at the JSON source, not whitelisted —
   widening the scanner's allowlist to hide a real hit is forbidden.
3. **Self-tested scanner.** The scanner library ships controls proving the
   neutralization table does not blind it: for every allowlisted term, a paired
   control string that MUST still be caught. Any allowlist entry without a control is
   a bug. The generated spec runs `self_test()` before its own content check.
4. **Icon map + sync.** JSON icons are mapped to icons that actually exist in the
   icon library (never emit a missing icon); the generator copies exactly the used
   set into the project and fails closed if any mapped icon is absent from the
   library.
5. **Emit specs** as importable Python modules (part 1 + part 2 to keep files
   medium-sized), with color constants and the logo path emitted as bare names, not
   strings — the renderer rejects string color values.
6. **Quarantine, don't delete.** Before regenerating SVG/notes, move old files into a
   timestamped quarantine dir inside the project so stale slides cannot mix in and
   nothing is lost.

## Fail-closed pre-flight (runs before any rendering)

1. Slide file stems sort alphabetically == teaching order (the exporter orders slides
   by filename).
2. Zero person-pronoun hits and zero scaffolding hits on slide faces, with the
   scanner self-test passing first.
3. Minute windows tile the full lesson (each window starts where the previous ends;
   total equals the lesson length).
4. Builder report with `raise_on_error=True` — the builder only buffers overflow
   errors, so skipping this turns "built OK" into a lie.

## Per-lesson build script (6 steps, parameterized by lesson number)

icon-sync check → build SVG+notes → embed icons (fail if any `data-icon` remains) →
timeline audit (subtitle minutes vs note windows vs total) → slide-face scan (no
administrative/invisible text, no unembedded icons) → geometry/quality checker →
export PPTX with notes. One script serves the whole batch; a failing lesson does not
stop the batch (per-lesson logs, summary at the end).

## Post-build verification and publishing

- **Read-back the PPTX itself** (not the SVGs): extract text per slide in document
  order and re-run the same scanner library — the exporter can reflow text, so a
  clean SVG set does not prove a clean PPTX.
- **Worksheets from the same JSON.** Practice/application worksheets are generated
  from the identical JSON, so slide and worksheet can never disagree. Every worksheet
  promised on a slide must exist as a real file; verify by reading the generated
  document back and checking for a set of "golden" strings taken verbatim from it.
- **Publish with checksums.** Copy PPTX/PDF/worksheet to the delivery folder under
  canonical names; move superseded versions into an archive subfolder (never delete);
  verify by comparing sha256 of source and delivered copy.

## Known pitfalls (all hit in production)

- A neutralization rule can CREATE a new violation ("the class of learners" → still a
  pronoun phrase). Re-run gates after every table change; fix wording at the source.
- Sub-strings carried from JSON may contain their own minute counts ("12 min") that
  contradict the scheduled window — strip leading minute prefixes from JSON-supplied
  subtitles.
- Overflow errors concentrate where a slide stacks an image row plus 3+ note lines;
  the fix budget is: shrink padding/size stepwise, shorten lines to ≤ ~100 chars so
  they stay one line, and never drop body text below the readable floor.
- `repr()` of Python dicts emits single quotes; color constants must be de-quoted to
  bare identifiers when emitting spec source.
