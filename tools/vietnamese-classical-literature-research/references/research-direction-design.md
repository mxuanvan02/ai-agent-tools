# Thiết kế hướng nghiên cứu (research direction design)

How to turn "I want to work on X" into a direction that can actually be
completed, and how to say honestly when it cannot.

## The four tests

A direction is worth proposing only if all four hold. Score each honestly —
the value of this file is in the **no**s it lets you give early.

### 1. Có vấn đề — there is a real problem

Not "study X" but "X is contested / unexplained / unexamined in dimension Y".

The test: **can you name the source that reveals the gap?** If the gap is
something you noticed while reading, name the passage. If it is something the
scholarship argues about, name the two positions and who holds them. If you can
name neither, you have a topic, not a problem.

Gap typology, ordered from most to least feasible for a first project:

| Gap type | Shape | Where to find it |
|---|---|---|
| **Disputed fact** | Two scholars say incompatible things | `textual-criticism-caveats.md`; round-4 searches for `tồn nghi`, `tranh luận` |
| **Unexamined witness** | A manuscript exists and nobody has collated it against the printed edition | Catalogue records at `hannom.nlv.gov.vn`; compare `R.xxx` against the standard edition |
| **Missing comparison** | X is studied domestically, never against its Chinese counterpart Y | Round-1 divergent search: a term that returns hits in Vietnamese but none in Chinese, or vice versa |
| **Untextualised theme** | A theme is discussed without attention to form | Read a work formally (`genre-and-poetics.md`) where scholarship reads it thematically |
| **Reception gap** | How a later period read an earlier author | Compilations and prefaces: `皇越文選`, `全越詩錄`, `歷朝憲章類誌` |
| **Framework mismatch** | A text is read through the wrong doctrine | `thought-frameworks.md`: which framework is actually arguing |

The first two are the most tractable because the evidence is finite and locatable.
The last two are the most interesting and the most likely to fail on evidence
availability.

### 2. Có tư liệu — the material exists and is reachable

Name the primary sources **by shelfmark or edition**. This is not a formality;
it is where most ambitious directions die.

Checks to run, in order:

1. Is there a catalogue record? (`hannom.nlv.gov.vn`, `lib.nomfoundation.org`)
2. Is there a digitised image, or only a description? A description supports
   bibliographic claims; only an image or a transcription supports textual ones.
3. Is the holding institution's site reachable? Run
   `scripts/probe_sources.py --layer 1`. Five registered sources in this field are
   **DNS-dead** — a direction resting on one of them is not feasible until the
   material is found elsewhere.
4. Is it among the **lost** material? `全越詩錄` is recorded as among 25 volumes
   lost from the Hán Nôm Institute. See `textual-criticism-caveats.md`.
5. For the Chinese side of a comparison: is `ctext.org` or `kanripo.org` reachable
   for you? Both are **browser-only** from this network (curl 000 / 403), which is
   workable but not scriptable — plan accordingly.

Verdict wording, because vagueness here is what wastes months:
- **feasible** — witnesses named and reachable
- **feasible with a limitation** — reachable but only as a description, or only
  one witness survives; state what the limitation prevents you from claiming
- **not feasible now** — material unreachable or lost; say what would change that

### 3. Có phương pháp — the method fits the material

Match the question type to the method. A mismatch is detectable early and is the
most common reason a well-sourced direction still fails.

| Question | Method | What it needs |
|---|---|---|
| Which witness is earlier? Whose poem is this? | **Văn bản học** (textual criticism) | At least two witnesses; prefaces; collation |
| How does this form produce meaning? | **Thi pháp học** (poetics) | A fixed text you can read formally; tone/rhyme/parallelism analysis |
| How does Vietnamese X relate to Chinese Y? | **So sánh** (comparative) | Both corpora in their own languages; a real tertium comparationis |
| How was this read later? | **Tiếp nhận** (reception) | Later texts quoting it; commentaries; compilations |
| What思想 does this text argue from? | **Liên ngành** (interdisciplinary, with思想史) | The framework vocabulary; the author's examination record and offices |
| What does this text mean in its own terms? | **Close reading** | One witness, read carefully, with allusions resolved |

Rule: **state the method before the thesis.** If the method cannot produce
evidence for the thesis, change one of them.

### 4. Có đóng góp — statable in one sentence

If the contribution cannot be written in one sentence, it is not a contribution
yet. Templates that force specificity:

- "Establishes that ___ by collating ___ against ___."
- "Shows that ___'s use of ___ is not ___ as previously read, but ___."
- "Provides the first Vietnamese-language account of ___ based on ___."
- "Argues that the dispute over ___ rests on conflating ___ with ___."

The last template is disproportionately productive in this field, because
`textual-criticism-caveats.md` shows how many disputes are actually category
confusions — composition date vs edition date, work vs witness, genre vs function.

## Scoring

Score each candidate 0–2 on the four tests, then rank by total. But apply two
overrides, because a raw total misleads:

- **Test 2 = 0 vetoes the direction** regardless of total. Unreachable material
  cannot be argued around.
- **Test 1 = 0 with test 3 = 2 is a methods exercise, not research.** A well-formed
  method applied to no problem produces a competent summary. Fine for coursework;
  not a thesis.

Report the scores and the reasoning. A direction you reject with a stated reason
is more useful than one you silently drop — the reason often becomes someone
else's feasible version.

## Scaling by level

The four tests do not change; the acceptable scope does.

| Level | Scope that works | Scope that fails |
|---|---|---|
| **Coursework / seminar paper** | One passage or one story, read formally, with allusions resolved and one scholarly position engaged | A whole work, a whole genre, "the thought of X" |
| **Journal article** | One argument about one text or a small group, with a witness identified | A survey, or a comparison of two traditions |
| **MA thesis** | One work or one author, with textual questions addressed and a comparative or reception dimension | A period, a genre, a思想 |
| **PhD** | A corpus with a genuine methodological contribution, or a reception history across a boundary | Anything that could be finished by reading one book |

Say the level out loud when proposing. Most infeasible directions are feasible at
one level down.

## Worked examples

Each is built from material verified in this skill's own corpus, so the sources
named are real and checkable.

**A — feasible, narrow, high-confidence (coursework to article)**

*Problem:* The lời bình (`評`) at the end of each story in `傳奇漫錄` states a moral
judgement, but Vietnamese textbook treatment of `傘圓祠判事錄` typically summarises
the plot and the "chính nghĩa thắng gian tà" theme without analysing how the lời
bình relates to the narrative that precedes it.
*Material:* Full text at `識典古籍` (verified this session — 卷之二 opens with
`傘圓祠判事錄`); catalogue records at `hannom.nlv.gov.vn` (R.424, R.1565, R.1624
all recorded, with differing titles and page counts).
*Method:* Close reading + paratext analysis; the lời bình as a claim about the
narrative, not a summary of it.
*Contribution:* "Shows that the lời bình in `傘圓祠判事錄` does not restate the
story's moral but reframes its juridical cosmology."
*Scores:* 2 / 2 / 2 / 2. Note the bonus: three recorded manuscripts with
**different titles and page counts** means a textual dimension is available if
wanted.

**B — feasible with a limitation (article)**

*Problem:* Whether `傳奇漫錄` is a compilation or a creation is explicitly argued
in Vietnamese scholarship (Bùi Duy Tân's position is recorded in the corpus), but
the argument is usually made from the stories' character, not from the prefaces.
*Material:* Hà Thiện Hán's 1547 preface and Nguyễn Lập Phu's preface are recorded
as opening the work; the manuscript R.1624 records Nguyễn Bỉnh Khiêm as
`hiệu chính` and gives a **different title** (`傳奇傳錄`).
*Limitation:* reading the prefaces requires the manuscript images, not the
typeset text. If images are unreachable, the direction narrows to what the
catalogue abstracts support.
*Method:* Văn bản học + reception.
*Contribution:* "Argues that the compilation-vs-creation dispute turns on how the
paratexts position Nguyễn Dữ relative to his sources."
*Scores:* 2 / 1 / 2 / 2.

**C — not feasible now (record and revisit)**

*Problem:* The relationship between the Nôm poems attributed to Nguyễn Trãi and
those attributed to Nguyễn Bỉnh Khiêm, given the ~30 overlapping poems.
*Why it fails test 2:* both collections survive in later copies; `全越詩錄`, which
would help date the transmission, is among the **25 volumes recorded lost** from
the Hán Nôm Institute.
*What would change it:* access to a collated edition of both collections with
variant apparatus, or a newly catalogued witness.
*Scores:* 2 / 0 / 2 / 2. **Vetoed by test 2** despite a strong problem.
*Still useful:* the overlap is documented, so a *review* of the dispute is
feasible at article level even though resolving it is not.

**D — a category-confusion contribution (article, low cost)**

*Problem:* Dates for `上京記事` circulate as 1885; for `雨中隨筆` as 1906; for
`金雲翹新傳` as 1902/1906. All are **witness** dates (print or copy years), not
composition dates (1782–83; late Lê–early Nguyễn; and the Chinese source
respectively).
*Material:* all verified in `period-and-canon-map.md` and
`textual-criticism-caveats.md`, from catalogue records and the works' own pages.
*Method:* bibliographic; no manuscript work needed.
*Contribution:* "Shows that widely circulated dates for three canonical works are
witness dates misread as composition dates, and proposes a dating notation that
distinguishes the four date kinds."
*Scores:* 2 / 2 / 2 / 2 — and it needs no archive access at all. This is the
cheapest real contribution available in the field, which is why the date discipline
is in this skill rather than left implicit.

## Anti-patterns

- **"Study the humanitarian value of X."** No problem, no method, no end. Every
  work has been read this way already.
- **"Compare Vietnamese and Chinese literature."** Without a tertium comparationis
  and a named pair of texts, this is a reading programme.
- **"The thought of Nguyễn Trãi."** A PhD-shaped topic proposed at article scale.
- **"Prove that X is by Y."** Test 2 decides this before you start: if only one
  witness survives and it is a late copy, attribution cannot be proved, only
  argued probabilistically. Say which you are doing.
- **Resting a claim on a single source.** Recorded explicitly in
  `deep-research-protocol.md`: this field has many confident single-source
  statements. Three independent sources make a coordinate.
- **Quoting a shelfmark you did not open.** Cite the record, and say you cite the
  record.

## Output format

For each candidate direction, produce:

```
Direction:      <one sentence>
Problem:        <the gap, and the source that reveals it>
Material:       <works/witnesses with shelfmarks or edition IDs; reachability class>
Method:         <from the table above>
Contribution:   <one sentence, from the templates>
Level:          <coursework / article / MA / PhD>
Scores:         problem _/2  material _/2  method _/2  contribution _/2
Verdict:        feasible | feasible with a limitation (state it) | not feasible now (state what would change it)
Strongest objection: <from round 4>
```

Present three to five candidates ranked, with the rejected ones and their reasons.
A shortlist with honest vetoes is more useful than a list of five directions that
all look equally promising and cannot all be done.
