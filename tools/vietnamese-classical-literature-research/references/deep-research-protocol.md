# Giao thức nghiên cứu sâu (deep research protocol)

How to run a multi-round search on a classical Vietnamese literature question and
keep the result auditable. The point is not to search more; it is to know when to
stop and to be able to show why each claim is in the paper.

## Before searching: fix the question type

The four question types need different evidence, and mixing them is the most
common way a search goes nowhere.

| Type | Example | Evidence that settles it |
|---|---|---|
| **Textual** (văn bản học) | Which manuscript is earliest? Is this poem really his? | Shelfmarks, edition collations, prefaces (`序跋`) — layer 1 |
| **Interpretive** | What does the underworld trial in `傘圓祠判事錄` argue? | Close reading of a fixed text + scholarship on the genre — layers 1, 2 |
| **Reception** | How was Nguyễn Trãi read in the 18th century? | Later texts quoting him; commentaries; compilations — layers 1, 2 |
| **Comparative** | Vietnamese `傳奇` against Chinese `傳奇` | Both corpora, in their own languages — layers 1, 2, 4 |

If you cannot say which type you are asking, you cannot tell when you have an
answer.

## The five rounds

Run them in order. Each has a stop condition, because unbounded searching is how
context fills with material that never gets used.

### Round 0 — Orientation (max 3 queries)

Goal: vocabulary, not conclusions. Establish the standard periodisation, the
canonical works, and who the recognised scholars of the sub-field are.

Read `period-and-canon-map.md` first — it replaces most of this round for the
works it covers. Then run at most three queries to fill the gap: one Vietnamese
survey, one Chinese-language framing, one English-language framing.

**Stop when** you can name three scholars whose work defines the sub-field and
you know which century your material belongs to.

### Round 1 — Divergent (parallel, one query per script layer)

Same question phrased in each language, run in parallel where possible:

- **Vietnamese** — `từ khoá tiếng Việt + thể loại/tác giả`. Retrieves domestic
  scholarship, textbook material, văn bản học disputes, journal articles.
  Include spelling variants (`kì`/`kỳ`, `ký`/`kí`, `tùy`/`tuỳ`, `Truyện`/`Chuyện`).
- **Hán / Chinese** — the verified Han title or genre term. Retrieves
  Chinese-language scholarship, digitised full texts, edition images. Use
  `han-nom-keyword-glossary.md`; **never** a recalled character.
- **English / French** — `chuanqi`, `zhiguai`, `Classical Chinese`, `Vietnamese
  literature`, plus the romanised title. Retrieves area-studies journals and
  dissertations.

Keep everything. Do not judge relevance yet — classification now biases the set.

**Stop when** you have at least one hit per language layer, or you have confirmed
a layer genuinely returns nothing (record that; "no English scholarship on X" is
itself a finding).

### Round 2 — Convergent

Extract from round 1 the **recurring coordinates**: names, shelfmarks, edition
dates, and the disputes. These are the field's real reference points.

Concretely, build a table:

```
coordinate | how many sources mention it | which ones | does it change my question?
```

Anything mentioned by three or more independent sources is a coordinate. Anything
mentioned once is a lead. **Do not treat a single source's claim as settled** —
this field has a lot of confident single-source statements.

**Stop when** two consecutive passes add no new coordinate.

### Round 3 — Primary

For each load-bearing claim, go down a layer to the manuscript/edition record.
For every text you rely on, record:

- which witness you read (Hán original / Nôm rendering / phiên âm / translation)
- shelfmark or edition identifier (`R.xxx`, `nlvnpf-xxxx`, `NLVNPF-xxxx`,
  `A.xxx`, `VHv.xxxx`)
- whether it is a facsimile, a transcription, or a modern typeset edition
- what the preface (`序跋`) says about date, compiler and earlier editions

Catalogue records at `hannom.nlv.gov.vn` give shelfmark, page count, dimensions,
print type and a Vietnamese abstract that often quotes the original Han title —
which is also how you verify a Han character. See `source-corpus-verified.md`.

**Stop when** every claim your argument depends on has a layer-1 or layer-2 row
in the ledger.

### Round 4 — Adversarial

Search specifically for the counter-position:

- `tồn nghi`, `tranh luận`, `vấn đề văn bản`, `giả thuyết`, `nghi vấn` + title/author
- `disputed`, `attribution`, `authenticity`, `dating problem` + romanised title
- the author's name + a rival author's name (for the overlap cases)
- the work + `dị bản` (variants)

Read `textual-criticism-caveats.md` first: it lists the disputes already known,
which saves a round.

**Stop when** you can state the strongest objection to your thesis and have
either answered it with evidence or narrowed the thesis so it survives.

A direction that survives round 4 is worth proposing. One that does not is still
worth recording — the objection is usually the next researcher's topic.

## The evidence ledger

Keep it in a file, not in context. One row per claim:

```
id | claim | source (author, year, title) | layer | witness/shelfmark | read-by-me | confidence | note
```

Rules, in order of how much trouble they save:

1. **A claim with no source row is not a finding.** If it is in the draft, it has
   a row.
2. **`read-by-me` means you read it**, not that a summary said it. An abstract, a
   wiki sentence, and a search snippet are all summaries.
3. **Separate work from witness.** "Truyền kỳ mạn lục has 20 stories" is a claim
   about a work. "R.424 is a handwritten copy, 112 pages, 27×16 cm" is a claim
   about a manuscript. Mixing them produces false specifics that look precise.
4. **Separate composition date from edition date.** See
   `period-and-canon-map.md`. This is where most wrong dates enter.
5. **Confidence is calibrated, not decorative.** `high` = layer-1 witness read
   directly. `medium` = layer-2 scholarship, single source. `low` = layer-4 only,
   or a traditional attribution with no documentary basis.
6. **Layer 4 can verify a spelling, never a claim.** A full text at `識典古籍` is
   excellent for confirming that `傘圓祠判事錄` is the title's character string. It
   is not a citable edition.

## Query patterns that work in this field

```
"<Han title>"                             # exact, layer 1 and 4
"<Vietnamese title>" "văn bản" | "dị bản"  # textual criticism
"<author>" "<effect>" | "hiệu"            # catalogues index both names
"<Han genre term>" 越南                     # Chinese scholarship on Vietnamese material
"<romanised title>" chuanqi|zhiguai        # comparative English scholarship
"<title>" "tồn nghi" | "tranh luận"         # the disputes (round 4)
site:lib.nomfoundation.org "<title>"      # catalogue record
site:hannom.nlv.gov.vn "<title>"          # catalogue record
```

Two mechanical notes from this session's measurements:

- **Batch wiki fetches.** One request per title gets rate-limited after ~15 calls
  on a shared IP (measured: 33 of 44 titles came back empty). The MediaWiki API
  accepts up to 50 titles in one request. `scripts/verify_han_terms.py --fetch-vi`
  batches at 40.
- **A curl failure is not a dead source.** Ten of the 29 registered sources return
  000 or 403 to curl but work in a browser. Check the reachability class in
  `source-corpus-verified.md` before concluding anything is unavailable, and run
  `scripts/probe_sources.py --live` to re-measure.

## When to stop searching

Stop when all four hold:

1. Every load-bearing claim has a ledger row at layer 1 or 2.
2. Two consecutive rounds added no new coordinate.
3. The strongest objection is stated and answered, or the thesis is narrowed to
   survive it.
4. You know which witness of each text you are talking about.

More searching after this point adds noise and burns context. Write instead, and
let writing reveal the remaining gaps — they are almost always narrower and more
answerable than the questions you started with.
