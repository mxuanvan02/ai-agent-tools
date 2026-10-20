---
name: vietnamese-classical-literature-research
description: "Use when researching Vietnamese classical literature (văn học trung đại), its Confucian/Buddhist/Taoist thought background, or Hán-Nôm primary sources — builds verified Vietnamese↔漢↔English keyword bridges, probes which archives are actually reachable, and turns a vague topic into a defensible research direction with an evidence ledger."
version: 1.0.0
author: Mai Xuan Van
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    # Field classification. This tool belongs to the humanities/literature field,
    # not to the engineering tools it sits beside in the repository, and the
    # classification travels with the skill so an installer that honours it can
    # group it accordingly.
    category: van-hoc
    tags: [Literature, Van-Hoc, Han-Nom, Vietnamese, Classical-Chinese, Research, Humanities, Deep-Research, Medieval-Literature]
    related_skills: [academic-prose, deep-research, evidence-first-research, grounded-citations, literature-gap-recon]
---

# Nghiên cứu văn học trung đại Việt Nam (Vietnamese Classical Literature Research)

Domain: văn học trung đại Việt Nam (10th–19th century) and the thought systems it sits
inside — Nho giáo, Phật giáo, Đạo giáo, lý học/tâm học, khoa cử. Covers source discovery,
deep research, research-direction design, and the Hán–Nôm keyword discipline that decides
whether a search returns scholarship or nothing.

## Why this skill exists

Three failure modes are near-certain without it:

1. **Searching in the wrong script.** The literature is bilingual by construction: works
   written in chữ Hán (Classical Chinese), works written in chữ Nôm, and scholarship about
   both in Vietnamese, Chinese, English, French. A Vietnamese-only query misses the entire
   Chinese-language scholarship on the same corpus; a Chinese-only query misses Vietnamese
   textual scholarship (văn bản học), which is where authorship and dating disputes live.
2. **Inventing Hán characters.** Model memory of 漢字 for Vietnamese titles is unreliable in
   a specific, dangerous way: it produces *plausible* characters. Wrong variants
   (異體字), wrong component, wrong title form. A wrong character silently returns zero
   results, and the agent concludes "no sources exist". **Every character in a query must be
   verified against a fetched page or a named bibliography.** See
   `references/han-nom-keyword-glossary.md` for the verified set and
   `scripts/verify_han_terms.py` for the checker.
3. **Citing dead or bot-walled archives.** Several well-known domains in this field are
   unreachable. Some resolve in DNS but return HTTP 000 or 403 to plain `curl`; others have
   dead DNS entirely. A source list built from memory will contain links that do not work,
   and the researcher will lose hours. **Probe before citing** — `scripts/probe_sources.py`.

## The five workflows

Pick the one that matches the request. They compose; run them in this order when starting a
new topic from nothing.

### 1. Keyword bridge (do this first, always)

Input: a Vietnamese topic, title, author, genre, or concept.
Output: a query set across scripts, each term marked verified/unverified.

Build three rows per concept:

| Layer | Example | Where it pays off |
|---|---|---|
| Vietnamese | `Truyền kỳ mạn lục`, `truyện truyền kì`, `yếu tố kì ảo` | Domestic scholarship, SGK, giáo án, văn bản học disputes |
| Hán / Nôm | `傳奇漫錄`, `傳奇`, `志怪`, `文言` | Chinese-language scholarship, primary-source catalogues, digitised manuscripts |
| English / French | `chuanqi`, `zhiguai`, `Classical Chinese`, `strange tales`, `Vietnamese literature` | International journals (JVS, JSEAS), dissertations, library guides |

Rules:
- Expand the **genre term separately from the title**. `傳奇` as a genre label retrieves
  comparative studies; `傳奇漫錄` retrieves only that book. Both are needed, they answer
  different questions.
- Include the **variant spelling** for Vietnamese: `kí`/`ký`, `tùy`/`tuỳ`, `kỳ`/`kì`,
  `Truyện`/`Chuyện`. Domestic sources are inconsistent and a single form loses hits.
  Measured on the corpus in `references/han-nom-keyword-glossary.md`: both
  `Thượng kinh ký sự` and `Thượng kinh kí sự` occur in reputable sources.
- For an author, add the **courtesy name / hiệu**: Nguyễn Trãi → `Ức Trai` `抑齋`;
  Nguyễn Bỉnh Khiêm → `Bạch Vân am` `白雲庵`, `Trình quốc công` `程國公`;
  Huyền Quang → `玄光`. Catalogues index by both.
- Never emit an unverified 漢字 into a query without labelling it. An unverified character
  is a hypothesis, not a search term.

Detail and the verified table: `references/han-nom-keyword-glossary.md`.

### 2. Source discovery

Input: what you need (primary text, manuscript image, secondary scholarship, dissertation).
Output: a ranked, reachability-tested source list.

Order of preference, because it tracks how citable the result is:

1. **Primary / manuscript layer** — national-library digitised Hán-Nôm holdings, manuscript
   shelfmarks, woodblock and stele records. This is the only layer that settles a textual
   question.
2. **Peer-reviewed scholarship** — Hán-Nôm studies journals, national literature journals,
   university working papers, international area-studies journals.
3. **Reference layer** — bibliographies and dictionaries of Hán-Nôm texts, the standard
   author catalogues.
4. **Open corpora** — multilingual wikisource/wiki projects. Fast and useful for
   *confirming a character or a title form*, but **not** citable as scholarship.
   Use them to verify spelling, then go to layer 1–2 for the claim.
5. **Aggregators / personal sites** — last resort, verify anything load-bearing.

Reachability classes recorded in `references/source-corpus-verified.md`:
- `curl OK` — plain HTTP fetch works, scriptable.
- `curl 403/000` — reachable but blocks non-browser clients; needs a real browser session,
  and may still work for a human. **Do not conclude the source is dead.**
- `DNS-FAIL` — domain does not resolve. Do not cite; if a claim depends on it, find the
  same content in a surviving mirror or a print edition.

Probe command: `python3 scripts/probe_sources.py` (offline-safe: prints the recorded
registry; add `--live` to re-probe with curl).

### 3. Deep research protocol

Input: a research question. Output: an evidence ledger where every claim carries a source.

Run as bounded rounds, not as one big search:

- **Round 0 — orientation (max 3 queries).** Establish the standard periodisation, the
  canonical works, and who the recognised scholars of the sub-field are. Goal: enough
  vocabulary to search well, not conclusions.
- **Round 1 — divergent (parallel, one query per script layer).** Same question phrased in
  Vietnamese, Hán/Chinese, English. Keep everything, classify later.
- **Round 2 — convergent.** From round 1, extract the *recurring* names, shelfmarks, edition
  dates and disputes. These are the field's real coordinates.
- **Round 3 — primary.** For each load-bearing claim, go to the manuscript/edition layer.
  Record shelfmark, edition year, and whether the text you read is a transcription
  (phiên âm), a facsimile, or a modern typeset edition.
- **Round 4 — adversarial.** Actively search for the counter-position: disputed authorship,
  alternative datings, "tồn nghi" (doubtful attribution). This field has many. A direction
  that survives round 4 is worth proposing.

Ledger format (one row per claim, keep in a file — do not hold it in context):

```
claim | source (author, year, title) | layer (1-5) | verified? | confidence | note
```

Hard rules:
- A claim with no source row is not a finding.
- `verified?` means *you read it*, not *a summary said it*.
- Distinguish **work** from **edition**: "Truyền kỳ mạn lục, 20 truyện" is a claim about a
  work; "bản chép tay R.424, 112 trang, 27×16 cm" is a claim about a manuscript. Mixing
  them is how false specifics enter a paper.
- Stop when two consecutive rounds add no new coordinate. More rounds then only add noise.

Full protocol with query templates: `references/deep-research-protocol.md`.

### 4. Research-direction proposal

Input: a topic area + the researcher's constraints (level: coursework / MA / PhD / journal
article; available time; accessible sources).
Output: 3–5 candidate directions, each with a feasibility verdict.

A direction is worth proposing only if all four hold:

1. **Có vấn đề (there is a real problem).** Not "study X" but "X is contested / unexplained /
   unexamined in dimension Y". Point at the specific gap, with the source that reveals it.
2. **Có tư liệu (the material exists and is reachable).** Name the primary sources by
   shelfmark or edition. If the material is only in a DNS-dead archive, the direction is
   not feasible now — say so.
3. **Có phương pháp (the method fits the material).** Văn bản học for manuscript variants;
   thi pháp học for genre/poetics; so sánh for cross-cultural (Việt–Trung, truyền kì vs
   chí quái); tiếp nhận for reception history; liên ngành for the thought-system questions.
4. **Có đóng góp (the contribution is statable in one sentence).** If it cannot be stated,
   it is a topic, not a direction.

Score each candidate honestly on the four, then rank. Prefer a narrow direction with solid
layer-1 sources over a grand one resting on open corpora.

Worked examples and the gap-typology: `references/research-direction-design.md`.

### 5. Writing the result

Input: findings. Output: prose that a humanities reader accepts.

Non-negotiables:
- **First mention of a work**: Vietnamese title, then Hán title in parentheses, then
  author with Hán form where relevant — `Truyền kỳ mạn lục (傳奇漫錄) của Nguyễn Dữ (阮嶼)`.
  Later mentions: Vietnamese only.
- **Phiên âm discipline**: state which transcription you follow when variants exist, and
  do not silently normalise. `kì`/`kỳ`, `tùy`/`tuỳ`, `Truyện`/`Chuyện` are real variants
  across editions.
- **Attribution caution**: mark doubtful attributions explicitly (`tương truyền`, `tồn nghi`,
  `được cho là`). This corpus has famous cases — see
  `references/textual-criticism-caveats.md`.
- **No invented specifics.** Shelfmarks, page counts, dimensions, edition years, and
  statistics about a work must come from a source you read. If unknown, write unknown.
- **Cite the layer.** A claim sourced only to an open wiki is flagged as such or upgraded
  before publication.

Vietnamese academic prose conventions, de-AI-ing, and the calque audit live in the
`academic-prose` skill — use it for the actual writing pass. This skill governs the
domain content and the evidence, not the sentence style.

## Reference index

| File | Use when |
|---|---|
| `references/han-nom-keyword-glossary.md` | Building any query; verifying a 漢字; looking up a title/author/genre/concept |
| `references/source-corpus-verified.md` | Choosing where to search; checking reachability; recording a new source |
| `references/genre-and-poetics.md` | Classifying a work by thể loại; analysing form (luật, biền ngẫu, vần, điển cố) |
| `references/thought-frameworks.md` | The work raises Nho/Phật/Đạo, lý học, tâm học, khoa cử, or "văn dĩ tải đạo" questions |
| `references/deep-research-protocol.md` | Running a multi-round search; keeping the evidence ledger |
| `references/research-direction-design.md` | Turning a topic into a defensible direction; scoring feasibility |
| `references/textual-criticism-caveats.md` | Authorship, dating, edition and attribution are in play |
| `references/period-and-canon-map.md` | Orienting a topic in time; finding the canonical works of a period |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/verify_han_terms.py` | Check candidate 漢字 for a term list against fetched pages; reports CONFIRMED / NOT-FOUND with context, and discovers the correct characters near the Vietnamese gloss |
| `scripts/probe_sources.py` | Print the recorded source registry with reachability class; `--live` re-probes with curl (DNS + HTTP code) |
| `scripts/public_hygiene_check.py` | Repository publication gate (byte-identical across tools) |

Both research scripts are dependency-free (stdlib + `curl`). Neither writes outside the
working directory you pass.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 scripts/public_hygiene_check.py
python3 -m py_compile scripts/*.py
```

`tests/test_skill_integrity.py` enforces the invariants that make this skill safe to trust:
every glossary row carries a Hán string and an evidence marker, every cited URL appears in
the source registry with a reachability class, every reference file linked from SKILL.md
exists, and no glossary row is marked verified without a source page named.

## Boundaries

**In scope:** Vietnamese literature from the 10th to the 19th century; the Hán-Nôm textual
tradition; the Confucian/Buddhist/Taoist and examination-system context that the texts
presuppose; comparative Việt–Trung genre study; finding, verifying and citing sources;
designing a research direction.

**Out of scope:** modern and contemporary Vietnamese literature (post-1900, chữ quốc ngữ
literature) except as reception history of a classical work; pure Chinese literature with no
Vietnamese connection; linguistics of chữ Nôm as a writing system beyond what keyword work
needs; teaching-method and curriculum design (that belongs to the education skills).

**Adjacent skills:** `academic-prose` (Vietnamese academic writing, translation, de-AI-ing,
calque audit), `grounded-citations` (citation grounding discipline), `deep-research`
(general multi-source protocol), `evidence-first-research` (claim-to-source gates),
`literature-gap-recon` (novelty claims), `vietnamese-law-rag` (a working example of a
domain RAG if you need local retrieval over a corpus).
