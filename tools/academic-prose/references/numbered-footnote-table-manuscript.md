# Editing a Numbered-Footnote / Numbered-Table Manuscript

Applies to markdown manuscripts compiled to DOCX via Pandoc with numbered
footnote definitions (`[^n12]:`) and manually numbered tables/captions.
Every failure below actually happened; each cost a full rebuild cycle.

## 1. A new criterion needs a NEW citation, or Pandoc silently drops it

When adding a criterion/row that rests on literature, cite it in the body text
in the same edit. A footnote definition never cited in body text is DROPPED by
Pandoc: the compiled definition count falls below what the markdown shows, and
the reference never appears in the DOCX. Symptom: audit reports `defs=N-1`
while markdown grep reports `N`.

Rule: add marker AND definition AND bibliography entry in one pass.

## 2. Count citations from body text only, never from the whole file

`re.findall(r'\[\^(n\d+)\]', s)` matches definition lines too, so a definition
alone makes an orphaned footnote look cited. Filter first:

```python
body  = '\n'.join(l for l in s.split('\n') if not l.startswith('[^'))
cited = set(re.findall(r'\[\^(n\d+)\]', body))
defs  = set(re.findall(r'^\[\^(n\d+)\]:', s, flags=re.M))
assert not (defs - cited), f"orphans: {sorted(defs-cited)}"   # cited nowhere
assert not (cited - defs), f"dangling: {sorted(cited-defs)}"  # marker, no def
```

Orphans = a citation deleted while trimming. Dangling = a new marker with no
definition. Both break the build or produce a missing note.

## 3. Re-citing an existing footnote needs its OWN short-form definition

Chicago short form is a separate footnote, not a second marker on the same id.
Reusing `[^n15]` twice makes Pandoc emit 2 references for 1 definition, which
breaks any count-based check. Correct: create `[^n65]: Author, "Short Title,"
pages.` and cite that at the second location.

## 4. Renumber every table after an insertion, prose references included

Inserting a new `**Bảng 2.**` duplicates a number further down. Fix all
captions AND in-text mentions (`Bảng 2 dùng cả hai chiều...`):

```bash
grep -nE '\*\*Bảng [0-9]' file.md                 # captions: 1..N unique
grep -noE 'Bảng [0-9]' file.md | sort | uniq -c   # every mention
```

## 5. Headings that encode a count must be updated

`### 3.3.3. Năm nhóm tiêu chí` became wrong the moment a sixth criterion was
added — as did `Năm nhóm tiêu chí` in the conclusion and `Bốn dạng căn cứ` when
a fifth basis type was added. Grep the counting words:

```bash
grep -nE '(hai|ba|bốn|năm|sáu|bảy) (nhóm|dạng|loại|mức|tiêu chí|giai đoạn)' file.md
```

## 6. Verify in the DOCX, not in the markdown

Markdown being right proves nothing about the compiled file. Unzip and assert
the new content is actually present:

```python
import zipfile, re
z   = zipfile.ZipFile(docx)
rx  = lambda x: re.sub(r'\s+',' ',''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', x)))
doc = rx(z.read('word/document.xml').decode('utf8'))
fn  = rx(z.read('word/footnotes.xml').decode('utf8'))
assert 'new criterion text' in doc
assert 'New Author' in fn
```

For tables use python-docx: print `len(table.rows)` and the first cell of each
row. This catches a header/row column-count mismatch that markdown hides — a
5-column header over 4-column rows still renders while silently dropping data.

## 7. Word-budget arithmetic when the cap counts footnotes and bibliography

If the venue counts footnotes + reference list toward the body limit:

- A footnote definition costs its full word count; a bibliography entry ~20-30.
- Vietnamese legal instruments (nghị quyết, thông tư, bộ luật) are cited
  footnote-only per Chicago — do NOT add them to the bibliography. Saves words
  and avoids alphabetical-order breakage.
- Prose compression plateaus fast: after two passes each yields only tens of
  words. Stop micro-editing and cut whole redundant passages instead —
  typically a paragraph restating a point already made in the conclusion,
  contribution statement, or abstract.
- Tables are a good target: cell prose halves with zero content loss.

## 8. Never delete a citation marker just to save words

Trimming a sentence carrying `[^n47]` orphans that definition and breaks the
count. If a cut removes a marker, re-attach it to a surviving sentence or
delete the definition (renumbering if numbered sequentially).

## 9. Let an audit script be the gate

An `audit_spec.py` checking word count, footnote integrity, bibliography order,
spacing, anonymity, and caption placement catches every error above
automatically. Run it after EVERY rebuild, for each layout variant. Update the
script when the manuscript legitimately changes (footnote count 60 -> 65 -> 68)
— but never hard-code a count not verified by unzipping the DOCX.

## 10. Back matter counts toward the body word budget

Word counters typically start at the first numbered section (`1. Đặt vấn đề`)
and run to end of document. Anything placed AFTER the conclusion —
Acknowledgements, Funding, AI-use declaration, Data availability — is therefore
COUNTED, while the abstract and keywords are excluded. Read the counter's start
index instead of assuming; budget roughly 80-120 words before adding a funding
block, and cut an equal amount elsewhere in the same pass.

## 11. An author block is front matter: centre it by POSITION, not content

Author / affiliation / corresponding-author lines sit between the native-language
title and the abstract. They are neither all-caps nor numbered headings, so they
fall through to the body branch and get JUSTIFIED — stretching a three-word line
across the full measure. Detect them by position (first non-empty paragraph after
the all-caps title) plus a positive test (leading superscript digit, or contains
the contact email). Position alone is fragile: once a house-layout build moves
the abstract into a two-column table, there is no `Tóm tắt` body paragraph left
to stop the scan.

## 12. Never copy an acknowledgement from a sibling paper

Grant codes and AI-use declarations are normally reusable across papers by the
same team. The ACKNOWLEDGEMENT is not: it names a specific contribution (for
example "provided 48 textbook PDFs as research data"). Copying that into a paper
which used no such data is a false data-credit claim. Keep the funding line and
the AI declaration verbatim, rewrite the acknowledgement to match what was
actually provided, and ask the author to confirm before submitting.

## 13. Flipping an anonymity gate

If a build script or audit asserts anonymity and the author then asks for names
in the manuscript, first verify that the venue really requires blind review —
read the venue's own submission instructions. A comment in your own build script
is NOT policy; it may be an unverified assumption from an earlier session. Once
identity is confirmed wanted, REPLACE the anonymity check with a completeness
check (every author, every affiliation, corresponding email, grant code) rather
than deleting it, so the gate still catches a half-filled author block.

## 14. If the paper claims a usable artefact, BUILD the artefact

A contribution statement like "the framework is immediately usable in the
department" plus references to "a one-page review form" creates a deliverable
obligation. Ship the actual form (a separate DOCX generated from the same
criteria tables), and verify content parity programmatically: every criterion,
every outcome level, every verdict row must appear in BOTH the manuscript
tables and the form, or the form silently drifts from the framework. Also
verify the form's physical promise (page count via pdfinfo) — "one page" is a
falsifiable claim.

A decision-rule table (condition -> verdict -> action, scanned in order, stop at
first match) is what turns a criteria list into a usable instrument: without it
the framework says what to look at but never how to conclude. When reviewers or
supervisors ask "is this a real contribution?", the decision rule plus the
printable form are the answer.
