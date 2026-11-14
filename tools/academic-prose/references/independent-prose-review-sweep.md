# Independent prose review sweep

Trigger: the user asks for a prose review of a finished manuscript — "rà soát văn
phong", "independent read", "review the writing" — or asks for more style factors
after an automated pass already came back clean.

This is the orchestration reference. It does not restate what each gate checks;
it states the order, the division of labour between gates and measurement, and the
adjudication contract that turns a pile of candidates into a defensible answer.

## Why the gates are not the sweep

Every scanner in this skill matches a **lexical pattern** and reports one finding
per occurrence. None of them divides. A tell used at a high *rate* is therefore
invisible: measured on a 10-page bilingual manuscript, six gates returned 5
findings while 34 explanatory colons sat in 6,326 words — 5.4× the registry
ceiling of one per 1,000. Not one gate was wrong. They simply never computed a
density, and a density is what makes machine prose feel machine.

So the sweep has two halves that cannot substitute for each other:

| Half | Finds | Blind to |
|---|---|---|
| Candidate gates | local defects: a phrase, a sentence, a label collision | rates, distribution, rhythm |
| Measurement (`style_metrics.py`) | distributional tells: colon density, rhythm uniformity, nominalisation rate | whether any single instance is wrong |

A clean gate report plus an unmeasured manuscript is the failure mode this
reference exists to prevent. Conversely, a metric above threshold is a candidate
for the manual pass, never a verdict: `được` at 10.4/1,000 on a legal manuscript
is normal Vietnamese passive use, well under the 19.2/1,000 measured defect level.

## Order

**1. Freeze the baseline.** Build, record page count, and extract the distinct
set of numeric tokens across all prose files. Every later step is diffed against
this set: word count may move freely, evidence may not. A prose pass that
silently drops a number is a claim-integrity failure wearing a style badge.

**2. Extract prose before scanning.** Raw `.tex` inflates every rate here —
preamble, `tabular` rows, float scaffolding and macro arguments all count as
words. Use `scripts/tex_prose_extract.py`, which also re-appends captions under a
`[caption]` marker so body and captions can be measured separately (they have
different limits).

**3. Run the candidate gates, in this order.** Each takes the extracted prose and
returns candidates; none rewrites.

| Gate | Script | Class of finding |
|---|---|---|
| Internal register | `internal_register_scan.py --genre manuscript` | prose about the manuscript, project, or drafting conversation |
| Academic discourse | `academic_discourse_scan.py` | deficit-centred paragraphs, saturated caveats, clause overload |
| Vietnamese AI patterns | `vi_ai_pattern_scan.py --genre manuscript` | calques, ceremonial vocabulary, self-reference |
| Process logic | `process_logic_scan.py` | compressed chronology, misassigned role |
| Veracity protestation | `veracity_protestation_scan.py` | sentences asserting their own evidence is genuine |
| Consistency | `consistency_audit.py --terms ...` | referent collision, format zone, self count, hardcoded crossrefs |

**4. Measure.** `python3 scripts/style_metrics.py prose.txt`. Ten dimensions; the
four that carry hard thresholds are the colon rate, em dashes in prose, sentence
length CV, and (for captions) colon count. The rest are reported so a reader can
see whether the prose is within a sane band, not to be driven to a target.

**5. Adjudicate into three classes.** Mandatory, and the classes go in the report:

- `author_prose_fix` — a real defect in author-written text.
- `immutable_source_false_positive` — a hit inside a published title, quotation,
  DOI, author name, or official instrument name. Verify against the source, then
  retain verbatim.
- `needs_human_review` — the gate is right that something is odd and wrong about
  what; a semantics call only the author can make.

A release can pass with verified immutable-source false positives. It cannot pass
with unresolved `author_prose_fix` items.

**6. Repair.** One relation per sentence. See the vocabulary below.

**7. Rebuild and re-measure.** Page count against the baseline; numeric-token
invariant empty; the four hard metrics re-read from the new build's text layer.
Report before/after as numbers, not as "improved".

## Colon repair vocabulary

An explanatory colon is not one defect; it stands in for a logical relation the
writer did not name. Replace it with the marker that states the actual relation.
If no single marker fits, the sentence was carrying two propositions — split it.

| Relation the colon was hiding | Vietnamese marker | Shape |
|---|---|---|
| enumeration | `gồm`, `bao gồm` | `Tiêu chí gồm (1)… (2)… (3)…` |
| cause | `vì`, `do` | `… gặp trở ngại vì lỗi OCR …` |
| specification | `cụ thể là`, `trong đó` | `… chuẩn hóa, cụ thể là bỏ ghi chú khung …` |
| partition / membership | `trong đó` | `… giữ 16.158, trong đó 411 trượt …` |
| apposition | `tức là`, `tức` | `… (đpt), tức hiệu số điểm phần trăm …` |
| two independent propositions | split the sentence | `… suy biến. Thân câu không chứa …` |
| list follows | close the sentence, let the list follow | `… ba câu hỏi sau.` |

Verify the repair by the connective distribution, not by the colon count alone: a
correct repair raises `gồm` and `vì` in proportion to the colons removed. In the
measured pass `gồm` moved 13 → 20 and `vì` 13 → 18 while colons went 34 → 0. A
colon count that drops while no connective rises means the relation was deleted
rather than named — check that no proposition went missing.

Do not "repair" a colon that is doing a non-prose job: `Từ khóa:`, `Abstract:`,
ratios (`10:1`), and times are labels and notation. The script excludes these by
pattern; confirm any remaining hit by eye.

## False positives that must survive the sweep

These look like defects and are not. Each was measured on a manuscript that the
corresponding detector flagged:

| Candidate | Why it is correct |
|---|---|
| An opening repeated between the abstract and the first body paragraph | IMRaD convention: the abstract restates the paper's own opening move. A repeated-opening detector must compare within a zone, not across the abstract/body boundary. |
| `được` at ~10/1,000 | Ordinary Vietnamese passive. The defect level is 19.2/1,000; below it, removing `được` produces ungrammatical or evasive prose. |
| An em dash inside a bibliography title | Immutable citation zone. Verify the title against the source, keep it verbatim, record the hit as a verified false positive. |
| An em dash inside an author-written figure label (`Ví dụ 1 — Mức Nhớ`) | This one is **author prose**, not a citation. Fix it to parentheses. The test is authorship of the string, not its position in the document. |
| `và` appearing three or more times in one sentence | If each `và` joins a real item in an enumerated list, it is a list, not a chain. Repair only when it joins clauses rather than items. |
| A long sentence with one subject and parallel objects | Length alone is not clause overload; overload is multiple propositions competing for one main verb. |

## Output contract

Report, in this order:

1. **What the sweep covered** — gates run, dimensions measured, and the explicit
   statement that measurement plus gates is still partial verification.
2. **Defects fixed**, each as location → what was wrong → the measured before/after.
3. **Candidates deliberately preserved**, each with the evidence that licenses it.
   This section is not optional: a reader cannot distinguish "checked and correct"
   from "missed" unless the preserved items are named.
4. **Open items needing the author**, phrased as a decision, not a defect.
5. **Build state** — page count against the frozen baseline, and the numeric-token
   invariant.

Never report the sweep as complete because the gates returned zero. Zero findings
is what a gate says when it is looking for something else.
