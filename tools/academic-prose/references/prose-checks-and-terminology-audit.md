# Reviewer-phrased prose checks and terminology consistency

Two bundles a methods reviewer phrases as "writing" problems. Neither is a
style preference: both are repeatable checks, and both must be verified on the
built PDF's text layer, because a stale build hides every prose fix.

## Reviewer demand → owning reference

Eight checks that a methods reviewer phrases as "writing" problems. Each is
already owned by a reference — follow the pointer instead of restating it:

| Reviewer demand | Owner |
|---|---|
| Rename terms with the wrong professional connotation (`kiểm toán` → `rà soát`) | `references/terminology-localization.md` |
| Gloss every borrowed English term at first use | `references/academic-vietnamese-standard.md` |
| Never invent an expansion for an identifier you did not coin | `references/terminology-adjudication.md` |
| Disambiguate the task family at first use (`hỏi–đáp` vs `trắc nghiệm bốn lựa chọn`) | `references/terminology-localization.md` |
| Keywords must be field-standard, searchable terms | `references/contribution-statement-design.md` |
| Downgrade an unsupported claim in *every* section, not one | `references/veracity-protestation-gate.md` |
| One claim, one owning section — cut duplicates, do not reword them | `references/manuscript-structural-revision.md` |
| Do not let a negation drift into an opposite assertion when compressing | `references/process-logic-gate.md` |

Two things the pointers do **not** cover, and this is where the checks earn
their place: a renamed term must be swept through its whole family (`kiểm toán
viên` survives a bare `kiểm toán` replace), and every fix above must be verified
on the **built PDF's text layer** — a stale build hides all of them.

## Comparative-literature and contribution genres

Two references sit outside the manuscript pipeline and are easy to miss:

- **Literary and comparative prose** — `references/vietnamese-literary-prose.md`
  owns Vietnamese prose *about* literature: calques from English literary
  criticism, `và` chains, stating the *tertium comparationis*, hedge discipline
  in literary claims, evidence of institutional acts, and the false positives
  specific to this genre (e.g. the colon scan must be judged against a density,
  not against zero). It is not a variant of the manuscript rules — load it
  whenever the object of study is a literary work rather than a dataset.
- **Contribution statements** — `references/contribution-statement-design.md`
  owns the "ba đóng góp" paragraph: one or two sentences per contribution, a
  number plus the price paid, never claiming impossibility for the layer the
  paper then fixes, and stating where the result does *not* reach.

## Terminology consistency audit

Use after writing or revising a Vietnamese scientific manuscript when the user
asks for term consistency ("đồng nhất thuật ngữ, các cụm từ"), or when a
reviewer flags wording drift.

### Four directions of drift

Variant-pair counting sees one direction. Three others survive every prose
scanner, every clean build, and a clean citation check, and they are the ones a
reviewer notices first.

| Direction | Shape | Detection |
|---|---|---|
| `variant_pair` | many names, one concept | count both sides, fix toward the majority |
| `referent_collision` | one name, several referents | co-occurring quantities under one label |
| `format_zone` | one quantity, two surface conventions across language zones | separator character vs zone language |
| `self_count` | a claim about the manuscript's own contents the artifact contradicts | number word vs the table it introduces |

`REFERENT_COLLISION` is the dangerous one because both occurrences look correct
and every count of the label is internally consistent. Measured in a legal-QA
revision: one label named a 14.210-record intermediate pool in Methods and the
688-item scored test set in Results. A reader following the term concludes the
scored set contains 14.210 items — a false statement produced by no single wrong
sentence. Repair by renaming the intermediate pool (`tập ứng viên đánh giá`
alongside `tập ứng viên phát hành`), not by rewording either mention.

`FORMAT_ZONE` is not a typo in either language: Vietnamese writes `54,5` and
English writes `54.5`, and the defect is only ever a convention applied to the
wrong zone. Detect by classifying each zone from its own diacritic density rather
than from a declaration, because a bilingual manuscript often declares one
language globally and inherits it for both abstracts.

`SELF_COUNT` is where an off-by-one hides: prose introducing "seven checks" above
a six-row table. The count is fluent and the sentence is grammatical, so nothing
in a prose scan reacts.

### Automated pass

```bash
python3 scripts/consistency_audit.py manuscript.tex \
  --terms "tập đánh giá,tập kiểm tra" --report audit.md
```

Reports the four directions plus `CROSSREF_HARDCODE`, `ABBREV_LATE`,
`KEYWORD_PARITY`, and `CAPTION_TERMINAL`. Each finding is a candidate for human
adjudication; `REFERENT_COLLISION` in particular prints the co-occurring
quantities so a reader decides whether they name one population.

Two calibration guards decide whether the gate is usable, and both came from
measuring the gate itself rather than the manuscript:

- **A count claim belongs to a table only when the counted noun appears in that
  table's caption or header row.** Comparing against the nearest table regardless
  produced 23 findings on a clean manuscript — `bốn mô hình` matched against an
  unrelated eight-row results table — while the real defect was a table whose
  caption did name the noun.
- **An abbreviation is only late if the document defines it somewhere.** Inferring
  the expansion from initials missed the real case and invented one for a unit
  (`GB` from an accidental two-word match). Require the document's own
  `full form (ACR)` pattern; names and units then fall out of scope by
  construction.

A check is not implemented until a dirty fixture produces the finding **and** a
clean fixture stays silent:
`python3 scripts/test_consistency_audit.py`. A gate that fires on clean prose is
worse than no gate, because it trains the author to skip the report.

### Manual variant-pair sweep

Real failing case (a legal-QA revision round):
`thí nghiệm` vs `thực nghiệm`, `không có ngữ cảnh` vs `không ngữ cảnh`,
`mức độ nhận thức` vs `mức nhận thức`, `bản phát hành cuối cùng` vs
`bản phát hành cuối` — each appeared 1–4 times against a 6–21 count majority.

**Procedure:**
1. Enumerate candidate variant pairs from the domain glossary and from problem
   phrasing (reviewers' own words). Do not rely on a spell dictionary — the
   variants are all spelled correctly.
2. Count every variant **across the whole .tex with a script**, not by
   eyeballing. Report counts where one side is ≥2 and the other side is
   visible (≥1), and where the intended meaning is identical.
3. Fix in one direction: the majority form wins; the minority is replaced.
   Reserve exceptions for *defined* terms whose meaning is genuinely
   different (e.g. `câu trả lời đúng` inside a formula definition vs
   `đáp án đúng` as dataset field — check context before a global replace).
4. Re-scan after the fix: target = 0 for every minority form, and verify the
   majority count went UP by the removed minority count (a replace that
   silently regressed means the term was embedded in another token, e.g.
   `kiểm toán` inside `kiểm toán viên`).
5. Build the PDF and confirm the page count did not move (term-only edits
   must not change pagination; if it did, a sentence was rewritten, not a
   term swapped).

**Term pairs with known drift in Vietnamese legal/NLP manuscripts:**
`thí nghiệm / thực nghiệm` (choose thực nghiệm for evaluation-settings),
`không có ngữ cảnh / không ngữ cảnh` (choose không ngữ cảnh as the condition
label), `mức độ nhận thức / mức nhận thức` (choose mức nhận thức, Bloom's
revised taxonomy term), `bản phát hành cuối cùng / bản phát hành cuối`
(choose ngắn), `kiểm toán / rà soát` (reviewer flagged financial-audit
connotation → rà soát), `tỷ lệ / tỉ lệ`, `tự động / tư động`, `đọan / đoạn`,
truy hồi / truy hôi. Always re-measure after each pass — an edit can introduce
a NEW minority form while fixing an old one.
