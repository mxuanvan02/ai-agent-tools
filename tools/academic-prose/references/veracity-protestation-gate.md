# Veracity-protestation gate

A generated artifact that asserts its own evidence is real is padding. This file
defines the failure class, the licensing rules, and how the gate is wired into
every content-producing skill.

## The failure

Generated slides, demo pages, reports and manuscripts recurrently spend words
proving the artifact is genuine:

- `THAO TÁC THẬT TRÊN GOOGLE DRIVE` (title)
- `ảnh chụp thật terminal đang chạy rclone` (caption)
- `nằm trên Drive thật, không phải ảnh vẽ` (callout)
- `dung lượng đo được, không ước lượng` (callout)
- EN: `real output, not simulated` / `actual screenshot` / `live terminal run`

Three reasons this is always a defect:

1. **The claim carries no information the reader can use.** "Real Drive" does
   not tell the reader the drive account, the date, or how to reproduce — a
   path, URL, hash or command line does. The adjective competes with, and
   usually displaces, the pointer.
2. **Protestation is the signature of fakery.** Real artifacts present
   evidence; fabricated ones insist. Teaching the model to insist trains the
   exact rhetorical move a reader associates with staged demos.
3. **It costs the thing it protects.** Slide real estate, sentence budget, and
   reader attention spent on self-authentication are not spent on content.

The rule generalizes beyond slides: any sentence whose communicative function
is "trust me, this artifact is genuine" rather than describing the subject
matter is protestation, in every genre and language.

## Evidence presents itself

When authenticity genuinely matters (a demo lesson on real cloud storage, a
reproducibility claim in a paper), replace the adjective with a checkable
pointer:

| instead of | write |
| --- | --- |
| ảnh chụp thật terminal | the terminal block itself, captioned with the command and date |
| dữ liệu đo được, không ước lượng | `rclone size` returned `Total objects: 4, Total size: 217 B` on 2026-10-12 |
| chạy trên Drive thật | path `gdrive:00_THPT_THUAN_HOA/...` + share link |
| real execution, not simulated | the exit code, the log path, the reproducing command |

A pointer is verifiable by the reader; an adjective is not.

## Classes and verdicts

| class | catches | verdict |
| --- | --- | --- |
| `veracity_protestation` | authenticity assertions and fakery denials (`thật`-stacks, `không phải ảnh vẽ`, `not simulated`) | `delete` |
| `authenticity_claim_without_pointer` | a provenance claim with no checkable handle (`chụp trực tiếp từ máy`, `captured directly from the system`) | `replace_with_pointer` |

`delete` means remove the protest, keep the evidence sentence around it.
`replace_with_pointer` means substitute a URL, hash, path, date, or command.
Neither verdict ever deletes the evidence itself — a figure, table, terminal
block, or number stays; only the self-authenticating words go.

## Licensed constructions (suppressed by the scanner)

- **Mathematics.** `số thực`, `phần thực`, `real analysis`, `real part` — `thực`
  here is terminology, not protestation.
- **Stated contrast.** One sentence that explicitly contrasts real against
  synthetic data (`dữ liệu thật, khác với bộ tổng hợp`, `real logs vs synthetic
  ones`) is a methods statement when the contrast is the point. License applies
  per sentence and only when the hit word is the contrastive one.
- **Quotations.** Text inside quotes, `\enquote{}`, or code fences is not
  scanned — quoting someone else's protestation is not making one.
- **Negated meta-discussion.** A sentence discussing the rule itself (this
  file, a lesson teaching students to spot fake screenshots) is licensed by
  context: comments are stripped before scanning, and markdown/HTML comments
  are removed.

## Wiring — where the gate runs

The scanner is genre-independent, so it plugs into every content-producing
surface:

1. `scripts/veracity_protestation_scan.py <file-or-dir>` — accepts `.tex .md
   .txt .html .rst .docx .pptx`, reads office files via `ooxml_text`, exits 0
   pass / 2 candidates / 3 input error.
2. **Slide decks** (`vietnamese-classroom-slide-production`,
   `ppt-master-officecli`, `powerpoint`): run on the built `.pptx` as part of
   the design-gate suite, before the visual gate. A deck fails review with any
   `veracity_protestation` hit in slide text or speaker notes.
3. **Manuscripts / academic prose**: run alongside `vi_ai_pattern_scan.py`;
   protestation in a paper is a `writing_failure_taxonomy` addition, verdict
   `delete`.
4. **Demo pages / dashboards** (any HTML generator): run on the rendered text.
5. **This scanner's own docstring and fixtures** are written to pass themselves
   — comments and fences are stripped, so the rule can be documented without
   tripping the rule.

A hit is a candidate, never a verdict (same discipline as every sibling gate):
read the sentence, apply the licensing rules, then delete or replace. Absence
of hits is partial verification only — paraphrased protestation ("bằng chứng
này đến thẳng từ hệ thống đang chạy") has no lexical signature and needs the
manual pass over captions and titles.

## Why this lives in academic-prose, not in each slide skill

The pattern is one linguistic failure with many artifact surfaces. Duplicating
the pattern list per skill guarantees drift (one skill updates `thật`, another
keeps the stale list). One registry + one scanner, referenced by every
production skill's gate checklist, keeps the rule single-sourced. Slide skills
add one line: *run the veracity-protestation scan; zero candidates or each hit
explicitly licensed.*
