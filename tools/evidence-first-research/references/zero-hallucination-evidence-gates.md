# Zero-hallucination gates for hard-to-reach evidence

When a claim rests on a source you could not fully read, the failure mode is rarely
"no evidence". It is **evidence-shaped output**: a keyword table that reads as a
finding, a file that exists but is not the document, a quotation attributed to an
article number from a superseded draft. Every gate below was paid for with a real
false result, and each one has a command that decides it — so a checker can be run,
not trusted.

## The seven gates

| # | Gate | Deciding test | If it fails |
|---|---|---|---|
| 1 | Source integrity before counting | `len(text) > 5000` and diacritic ratio `> 3%` (Vietnamese) and structural markers present | Do not report any count. The source is not text. |
| 2 | Positive control before reporting a zero | Insert one item you **know** is present; the checker must find it | The checker is broken, not the corpus |
| 3 | Enacted text, not draft | Article numbering read from the signed/promulgated version | Retract the recommendation; drafts renumber |
| 4 | Context printed for every relied-on hit | Show ±150 chars around each keyword match | Substring false positives |
| 5 | Full identifier for "missing citation" | Search `56/2026`, `Thông tư 56`, `Thông tư số 56` — not `56` | Number collisions with unrelated data |
| 6 | File is the file type it claims | `file <path>` / magic bytes, not the extension | HTML error pages saved as `.pdf` |
| 7 | Every citation carries a read-status | `READ-IN-FULL` / `METADATA-ONLY` / `ABSTRACT-ONLY` / `UNREADABLE` | Only `READ-IN-FULL` may carry a number or quotation |

## 1. A zero count is not a finding until the source passes integrity

`curl` without `--compressed` on a gzip response writes compressed bytes to disk. The
download still reports `http=200` and a plausible size. Measured: 95 KB, every keyword
count returned **0** — including words certain to appear — and diacritics measured 0.7%
against a 3–6% norm for Vietnamese legal text.

That output is indistinguishable from *"this instrument does not address the topic"*,
which is the most dangerous shape a false result can take, because absence is exactly
what a research-gap claim is built from.

```python
text = open(path, encoding="utf-8", errors="ignore").read()
dia = sum(c for c in text if unicodedata.combining(unicodedata.normalize("NFD", c)[0]))
ratio = dia / max(len(text), 1)
assert len(text) > 5000, "too short to be full text"
assert ratio > 0.03, f"diacritic ratio {ratio:.3f} — you parsed compressed bytes"
assert text.count("Điều") > 5, "no structural markers"
```

Always pass `--compressed`. A scan with no text layer also reads near-zero — see gate 6
and the OCR route below; the distinction is *which* zero you are holding.

## 2. Positive control before you report any zero

A checker that finds nothing cannot tell you whether nothing is there or whether it
looked in the wrong place. Measured failure: a script counted "Vietnamese authors in the
reference list" by matching numbered lines (`^\s*\d+[.)]`). The list was APA, sorted
alphabetically, with no numbers. It returned **0** while the file contained entries in
plain sight. The report would have said "the bibliography has no domestic sources".

Before publishing any zero:

1. Pick one item you already know is present, by direct reading.
2. Run the same checker for it.
3. If it also returns zero, the checker is wrong — fix it before counting anything else.

Same discipline for regex-based verification of your own output: a pattern written as
`a.pdf/.txt` matches a single token and reports a file missing that is present. Check
each name as its own literal.

**Probe the shortest unique substring, never the form you intended to write.** Three
measured false negatives of this one kind:

- Searching an APA reference list for `Đặng Bá Lãm` returned **0** while the entry was
  present as `Lãm, Đ. B. (2003)` — APA inverts the name. Probe `Lãm,` and the year.
- Counting domestic authors by matching numbered lines returned **0** because the list
  was alphabetical with no numbers.
- Checking that a new citation landed by searching `(Chính, 2002)` returned **0** in a
  document that contained it, because the rendered form was the group
  `(Chính, 2002; Lương, 2022)` — the closing parenthesis is not adjacent to the year.
  Probe `Chính, 2002` without punctuation.

The tell is the same every time: a "missing" result that contradicts another check that
passed (here, the orphan-citation gate reported zero orphans while the probe reported the
citation absent). When two checks disagree, one of them is wrong — resolve it before
reporting either.

Two more traps in the same family, both measured:

- **A positive control may only contain items you have confirmed are present.** A control
  set built from the *expected* contents of a document is not a control: it asserted
  `Đặng` was in a paper that never mentions that author, so it printed FAIL and cast doubt
  on a reading that was correct. Build the control from strings you have already seen in
  the source.
- **A DOCX-built PDF splits diacritics away from their base letters.** `page.get_text()`
  returned `"Li u, N. T., B o, L. Đ."` for `Liễu, N. T., Bảo, L. Đ.` — tone marks arrive
  as separate code points, often at the end of the line. So no accent-stripping fold will
  ever match a heading searched from the PDF text layer. Search headings in the *markdown
  or DOCX source*, and use the PDF only for page counts and layout. Detect it first: if a
  probe for a 5-letter heading fails but a 4-letter accent-free fragment (`"THAM KH"`)
  matches, the text layer is mark-split.

Six more from the same session, each one a check that reported a defect which did not
exist — or missed one that did:

- **Compare like with like before calling a difference a defect.** A drift check of a blank
  data-collection FORM against a research PAPER flagged five numeric strings (163, 2.371,
  8,6 %, 79,1 %, 95,1 %) as "mismatched". The form is meant to be empty of results, so
  every one was a false positive. State what each artefact is *for* before diffing them.
- **Search every place the text can live.** A sentinel phrase lived inside table cells
  (twice), while the haystack was built from paragraphs only, so the gate reported
  `article=False` for text that was present. A sentinel that can appear in a table must be
  searched in table text.
- **Case and surface form, again.** Probing `Hoãn` / `Dùng được` against a form that prints
  `HOÃN` / `DÙNG ĐƯỢC` reads as absent. Fold case for content probes; keep case sensitivity
  only where it is the thing under test.
- **Know your units before you tune a number.** Word cell padding is in `dxa` = 1/20 point,
  so a "padding 8" change is 0.14 mm — visually nothing. It read as a real fix and bought
  none. Convert to mm and say the mm out loud.
- **A verification script that crashes verifies nothing.** A backslash inside an f-string
  expression (`f"...{len(re.findall(r'\S+',seg))}..."`) is a SyntaxError in Python, and it
  killed three separate check runs in one session, each time silently shortening what got
  checked. Hoist regexes to module constants (`WS = re.compile(r"\S+")`).
- **Patch by verified anchor or by index, never by memory.** One edit used a hard-coded
  anchor for text the previous edit had already changed, and another spliced at
  `s.index("gate_all()", start)` which matched the substring inside `def gate_all():`
  itself, leaving a duplicate block and a SyntaxError. `assert s.count(old) == 1`, prefer
  regex or line indices, and `ast.parse()` **before** writing the file.

## Gates for layout claims, not just content claims

A prose claim about an artefact's *shape* is as checkable as a claim about its content, and
it breaks silently. Two measured cases:

- **The article claimed a one-page review sheet three times.** The sheet shipped at two
  pages; page 2 held eight border drawings and no text at all — only the blank signature row
  had spilled. Measure the page count of the promised artefact in the same audit that checks
  the manuscript, and include the artefact's own sentinel phrases so drift is caught. Here
  the sheet had drifted for five days because the manuscript pipeline never invoked its
  builder: the source carried a reviewer-mandated fix the shipped PDF did not.
- **Four figures were printed at 14.60 × 8.91 cm against a written 7 × 14 cm limit**, and
  every earlier audit pass said nothing, because the PNGs were fine and the oversize came
  from a `width=` attribute in the markdown. Measure figure extents from the built DOCX
  (`wp:extent` cx/cy ÷ 360000 EMU-per-cm), never from the image file.

When fitting something to a size limit, sweep and measure instead of guessing: 35
combinations of (font scale × cell padding × page margins) were rendered and page-counted to
find the one that kept both the one-page claim and a usable 1.6 cm signature row. Guessing
took three failed attempts first.

Two mechanical traps that make figure work fail invisibly:

- **Shrinking a canvas does not shrink its labels' collisions when the axes are
  aspect-locked.** `imshow()` forces `aspect='equal'`, so cutting the canvas height hands the
  surplus back to the cells and the tick-label overlap stays *identical*: measured, labels
  17.4 % narrower and the overlap still exactly 4.9 px. For an `imshow` figure the only safe
  lever is uniform scaling at print size, which cannot change overlap at all. Shrink the
  canvas for bar charts; never for one.
- **Gate label overlap on bounding boxes, and negative-control the gate.** Vision readings of
  the same figure disagreed three times in one session (not overlapping / nearly touching /
  overlapping). `get_window_extent()` on the live axes settled it in one run. Then prove the
  gate can fail: pumping `fontsize=16.0` made it exit 1 with `43.3 px / 52.3 px`. A gate that
  has never been shown to fail is decoration — and the first version of this one silently
  measured nothing, because the drawing functions `plt.close()` their own figure before the
  gate could read it.

## 3. Never cite an article number from a draft

Drafts and enacted texts differ in **content and numbering**, and the numbering shift is
silent. Measured on one Vietnamese circular:

| keyword | draft | enacted |
|---|---|---|
| digital technology application | 4 | 0 |
| `công nghệ số` | 6 | 0 |
| artificial intelligence | 11 | 1 (in the fraud clause) |
| risk control | 1 | 0 |

The draft's `Điều 13` became `Điều 12` on enactment, and its substantive rule changed
(two score components → three, with a minimum 50% final-exam weight). A whole section on
applying AI in training existed in the draft and was deleted.

Rules:

- Cite article numbers only from the promulgated text (the signed PDF, the official
  gazette, or the government legal-document portal).
- When both versions exist, diff them by keyword count and show the table.
- A provision that exists only in the draft is a **recommendation to retract**, never a
  finding. If you already advised citing it, say so explicitly and withdraw it — the
  retraction is the deliverable.
- Beware substring traps in the diff: `chuyển đổi số` ("digital transformation") matched
  twice in the enacted text, both inside `chuyển đổi số **lượng** chứng chỉ` ("convert the
  *quantity* of certificates"). Gate 4 catches this.

## 4. Print the context of every hit you intend to rely on

A count is a candidate, not a result. For each keyword you will quote a number for, print
±150 characters. Two minutes of output prevents a claim about a provision that does not
exist.

## 5. Verify a "missing citation" with the full identifier

Splitting `Thông tư 56/2026` into `56` and searching the manuscript matched `dài nhất 56`
— a word-count datum from the body — and reported the document as already cited. Require
the full forms and treat the citation as present only if one matches.

## 6. Confirm the file is what its extension says

Measured: three files saved as `.pdf` at 1.2 KB, 2.1 KB and 4.0 KB were all HTML — one a
`403 Forbidden` page, two article **landing pages** (navigation plus `<title>`). They had
survived several review rounds as "downloaded sources".

```bash
for f in *.pdf; do printf "%-34s %8s  %s\n" "$f" "$(stat -c%s "$f")" "$(file -b "$f" | cut -c1-60)"; done
```

Any file under ~40 KB claimed to be a paper, or reporting `HTML document`, is not a
source. Re-download or downgrade the citation's read-status.

A citation whose only file is a landing page may support **metadata** (title, journal,
issue, pages) and nothing else. If the manuscript attributes a substantive claim — a
trend, a number, a recommendation — to that article, either obtain the full text or remove
the specific hook and let the sentence stand as a general statement.

**Scanned PDFs are the opposite case:** a genuine 11 MB signed document extracted 164
characters over 24 pages, because it is an image scan with no text layer. Do not conclude
it is empty.

```python
import fitz
d = fitz.open(pdf)                      # page_count == 24, text ~164 chars -> scan
for i, page in enumerate(d, 1):         # render, then OCR page by page
    page.get_pixmap(dpi=170).save(f"pages/p{i:02d}.png")
```

Locate the right page before OCR-ing all of them: map each article's character offset in
a full-text copy (from a readable secondary source) to a fraction of the document,
multiply by the page count, and OCR only that window. This found the target clause in
three OCR calls instead of twenty-four. OCR also truncates at the page break — re-prompt
for "only the lower half, starting at clause 5 or 6" to recover a tail.

## 7. Read-status is part of the citation record

Every source gets one label, recorded next to it:

- **READ-IN-FULL** — may carry a quotation, an article/clause number, or a statistic.
- **METADATA-ONLY** — title, authors, venue, year confirmed; no content claim permitted.
- **ABSTRACT-ONLY** — the abstract was read; claims must be attributed to the abstract.
- **UNREADABLE** — retrieval failed. Cite only if the fact is corroborated by a source in
  one of the three states above, and record the retrieval failure in the audit notes.

A manuscript that mixes these silently is where hallucinated citations are born: the
reference list looks complete, and no gate distinguishes an entry you read from one you
inferred.

## Retrieval routes when official portals refuse

Ordered by what actually worked:

1. **Guess the government asset path from a citation that already resolves.** A sibling
   document cited `…/vbpq/2026/7/54-bgddt.pdf`. The same pattern with `.pdf` 404'd, but
   **`.signed.pdf` returned 200 `application/pdf`, 11.5 MB** — the signed original. Probe
   suffix variants (`.pdf`, `.signed.pdf`, zero-padded month) before concluding.
2. **Commercial legal aggregators** are far less defended than official-looking portals
   and often serve full text to a plain `curl -sL --compressed` with a browser UA
   (74,915 characters, all 27 articles contiguous). Use them to read; cite the government
   copy.
3. **Cross-check two independent sources.** When both agree on article numbering and every
   keyword count, the reading is safe to quote.
4. Hard-blocked portals: a real browser sitting on a challenge page for 72 s with an
   unchanged 266-byte body will not pass. Stop waiting; change source. Archive services
   may have zero snapshots of recent legal documents — check CDX before relying on them.

Keep the evidence: both texts, the rendered scan pages, and their SHA-256, in an
`evidence/` folder, so any quotation can be re-checked later.

## Provenance notes must match reality

A comment claiming "verified against the signed PDF, saved at `evidence/…`" is itself a
claim. Measured failure: the saving script crashed on an empty list (`max()` over a scan
with no text layer) before copying anything, while the comment — written afterwards from
the plan, not the outcome — described files that did not exist. Run the save, then list
the directory and check each name.

## Gate the evidence, then the claim

Prose rules decay; commands do not. `scripts/zero_hallucination_gates.py` implements the
seven gates as functions that return a verdict plus the measurements behind it:

```bash
python3 scripts/zero_hallucination_gates.py --self-test   # prove each gate can FAIL
python3 scripts/zero_hallucination_gates.py EVIDENCE...   # gates 1 + 6 over real files
```

The self-test is mutation discipline, not decoration: each fixture is a failure shape
from a session where the gate was needed (compressed bytes, a name printed in capitals,
a clause number taken from a draft, an HTML error page saved as `.pdf`). Run it on the
evidence folder before writing any absence finding — measured on one project it marked
3 of 7 files unusable, including two that had survived several review rounds as
"downloaded sources".

## Reporting shape

For each finding:

```
CLAIM:      <the sentence in the manuscript>
SOURCE:     <document, version, article/clause>
READ-STATUS: READ-IN-FULL | METADATA-ONLY | ABSTRACT-ONLY | UNREADABLE
EVIDENCE:   <file, sha256, page/offset>
GATES RUN:  1 integrity ✓ · 2 positive control ✓ · 3 enacted ✓ · 4 context ✓ …
VERDICT:    supported | unsupported | must-downgrade
```

A finding without `READ-STATUS` and at least gates 1–2 is a hypothesis, and must be
labelled as one in the manuscript.

## The measuring instrument also fabricates findings

Every trap above was a probe that mis-searched real data. This family is worse: the
measurement function itself manufactures a defect that does not exist in the artefact, so
there is nothing to re-read to catch it. Four measured cases from one manuscript pass.

- **Joining lines before splitting sentences invents sentences.** A word-count audit did
  `" ".join(all_lines)` and then split on `(?<=[.!?])\s+`. A title line has no terminal
  period, so it fused with the author line and four affiliation lines into a single
  "143-word sentence", and a build sentinel (`<<<ENGLISH_BLOCK>>>`) fused with the English
  title into a "124-word sentence". The report said 7 sentences exceeded 60 words; the real
  count was 5, and the two worst offenders were not text at all. Split sentences *within
  each line*, and exclude front matter by an explicit pattern rather than by assuming every
  line is prose.
- **A fixed-character context window bleeds across sentence boundaries.** An epistemic-upgrade
  check looked at ±62 characters around each hit to apply its whitelist. An affirmative
  `Nó chứng minh một điều yếu hơn` was acquitted because the *preceding* sentence contained
  `không chứng minh` — which is precisely the self-contradiction the rule exists to catch.
  Scope a whitelist to the enclosing sentence (`s.rfind('.', 0, pos)` … next `.`), never to a
  character window.
- **Counting a table column as flattened text.** A numbered column was probed as the literal
  `"Hàng 1."` and reported absent, because the number `1` sits in its own cell apart from the
  header word `Hàng`. No such concatenated string exists in the file. Iterate
  `doc.tables[i].rows[j].cells[k]` when the field under test is a table.
- **A rule that judges a list by its lead-in.** A "compressed argument" check counted
  semicolons in the whole sentence, so `khung năm thành phần: a; b; c; d` — a genuine
  colon-led enumeration — was reported as a defect because the lead-in counted as the first
  item. Partition at the colon and judge only the items after it.

The general discipline: **when a metric produces a number, print the items behind it.** Every
one of these four was caught by printing the offending text rather than by trusting the count.
A count that cannot be traced to its members is not evidence.

### Negative fixtures are part of a self-test

A check that has only ever been shown to catch defects can still over-fire, and over-firing
is what sends an author to rewrite correct prose. Measured on this manuscript, an un-triaged
style audit reported 64 defects of which **46 were false positives**: `8.192` and `2.371`
flagged as decimal points when Vietnamese uses the dot as the thousands separator (25 of 30
hits); 12 of 15 "epistemic upgrades" that were negations (`không chứng minh`), mathematical
senses (`tính kín đã chứng minh`), or schema requirements (`trường bắt buộc`); two
`semicolon chains` that were APA citation separators; and a keyword "missing" from the
reference list because the search ran against 76 titles instead of an external index.

So each rule needs both directions in its self-test:

```python
positive = [("H.md", 1, 'Một là hai nhãn không suy ra nhau. Hai là hồ sơ thiếu nhãn.', 'prose')]
negative = [("G.md", 1, 'Không gian gồm 8.192 trạng thái trên 2.371 câu ở mục 3.6.', 'prose'),
            ("G.md", 2, 'Cập nhật (Haladyna & Downing, 1989; Towns, 2014; Haladyna, 2022).', 'prose')]
```

And a fixture set is only as good as its strictest threshold: a check configured `>= 0`
passes on every possible input. The title-and-keyword check passed its first self-test by
matching nothing; adding a title that repeats its own noun and a one-item keyword list, then
raising the threshold to `>= 3`, is what made it a gate.

### Cross-checking an independent reviewer is a two-way audit

Dispatching reviewers over the same text found three defects the tool had missed (an
enumerative pair with no colon, an upgrade acquitted by the previous sentence, three surface
forms for one concept). Reviewing the reviewers back rejected three of their proposals:

| Reviewer proposal | Verdict | Evidence |
|---|---|---|
| Expand a legal term, claiming another section "already uses this form" | **reject** | `grep` for that exact form: **0 occurrences** anywhere. False premise. |
| Replace `ánh xạ` as an untranslated borrowing | **reject** | It is standard Vietnamese mathematical terminology, and it is pinned. |
| Reorder two sections to put Limitations before Future Work | **reject** | The section number is pinned in both abstracts, five body references, and a verifier gate. Reordering means renumbering. |

Accept a reviewer's finding only after re-measuring it against the artefact, the same
discipline as any other claim.

## A rendered image can be perfect while the artefact is broken

The opposite failure to the family above: the measurement said something was wrong, the
author looked at the output, it looked flawless, so the measurement got discarded as a bad
probe. Here the measurement was right and the eye was the thing that could not see.

Measured case. A Vietnamese manuscript's DOCX→PDF step produced a 31-page PDF whose pages
rendered **perfectly** — vision review confirmed diacritics complete and correctly placed,
no tofu boxes, no clipping. But its text layer was unusable:

| Measurement | Broken PDF | Fixed PDF |
|---|---|---|
| Vietnamese phrases findable (top 40) | **7/40 = 18 %** | 40/40 = 100 % |
| Table captions `Bảng 1..8` findable | **0/8** | 8/8 |
| Lines holding a single orphaned diacritic | **6,372 of 10,863 = 58.66 %** | 0 |
| Copy-paste of one sentence | `Phân tích khái ni m  m c 3.2 phân bi t ba c p` | correct |
| Page count | 31 (inflated) | 27 |

Root cause, traced rather than guessed: the venue mandated `Palatino Linotype`, which was
not installed; fontconfig substituted **P052**, whose Type1 build covers **194/282** of the
Vietnamese codepoints (`texgyrepagella` covers 278/282 — the same typeface in OpenType).
LibreOffice therefore painted each diacritic as a separate text object. Fix: a local
`fonts.conf` passed via `FONTCONFIG_FILE` for that one conversion only, mapping the mandated
name onto TeX Gyre Pagella, with a dedicated `UserInstallation` profile so LibreOffice's own
font cache cannot reintroduce the substitution. The DOCX keeps declaring the mandated font,
so the venue's own font gate still passes.

Two rules follow:

1. **Rendering quality and text-layer integrity are separate properties.** A gate must read
   the text layer directly. Looking at the PDF — by a human or by a vision model — cannot
   detect this class of defect, and the defect survived several review rounds for exactly
   that reason. An earlier round had already reached a *wrong* conclusion from it ("the
   review sheet is missing from the PDF") and worked around it by measuring the DOCX
   instead; the workaround preserved the finding's absence but not its cause.
2. **Prove the absence of content before trusting a page-count drop.** The fix removed 4
   pages, which looks like data loss until measured: comparing the normalised character
   stream (NFC, whitespace stripped) of DOCX vs old PDF vs new PDF gave **70,966 = 70,966 =
   70,966**, an exact multiset match. The old PDF was longer because 6,372 lines contained a
   single mark each, not because it held more text.

### When a gate's own threshold disagrees with reality, suspect the gate first

The first version of the new text-layer gate reported `37/40 = 92 %` on the *fixed* PDF and
passed only barely. The three misses were `bộ giáo dục và đào tạo`, `giáo dục và đào tạo` and
`và đào tạo` — all present in the PDF, but capitalised as a proper noun, so a lowercase needle
can never match. Comparing case-insensitively: **40/40 = 100 %** fixed, **7/40 = 18 %** broken,
so the threshold could be tightened to 95 % instead of 90 %.

Same for the orphan-line rule: the first discriminator was `len(line) <= 2 and every char is
a diacritic`, which over-fired on the real words `đề` (from `Nhận diện vấn đề`) and `độ` (from
`trình độ đại học`) whenever a table cell wrapped them alone. Restricting it to *exactly one*
character, and gating the **ratio** rather than the count, separated 58.66 % from 0.00 %.

A gate must be calibrated on both a known-broken and a known-good artefact before its
threshold means anything. Measured on only the fixed one, 92 % looked like a healthy margin;
measured on both, it was revealed as a bias, and the true margin was 100 % vs 18 %.

## Companion artefacts drift, and the main document's gates cannot see it

A submission is usually *more than one file*: a manuscript plus a form, worksheet, codebook,
supplementary table or appendix that a **different script** builds. The main pipeline never
calls that script, so the companion silently diverges while every gate on the main artefact
stays green. Observed: the companion was five days stale, and a second time its terminology
had drifted after the article's own wording pass.

Measured case. A one-page review form claimed to operationalise the article's Table 2 and was
published so departments could "use it immediately". Its axis-2 checkbox labels were
`Rule-recall`, `Rule-explanation`, `Issue/Application` — English terms appearing **0 times** in
the article, whose Table 2 axis reads `Nhắc lại quy phạm hoặc thuật ngữ`, `Giải nghĩa điều kiện
áp dụng của quy phạm`, … A reviewer holding the form could not map it onto the article. It had
also kept `thao tác pháp lý` after the article standardised on `thao tác chuyên môn` (19× vs 0×).
**All nine existing checks on the form passed** — they tested page count, one wording sentinel
and six row numbers. A form can satisfy every one of those and still be unusable.

Gates that actually catch this class, each calibrated on the broken and the fixed artefact:

| Gate | Broken | Fixed |
|---|---|---|
| no term the article has retired | FAIL (`thao tác pháp lý` ×2) | ok |
| every label traces to the article (≥4 labels, ≥70 % of its tokens present) | FAIL (2 labels, worst 50 %) | ok (8 labels, worst 100 %) |
| punctuation rule already enforced in the article | FAIL (8 em dashes) | ok (0) |
| checkbox bound to its label with a non-breaking space | n/a | ok (0 separable / 44 joined / 86 boxes) |

The traceability gate is the general one: for each label or field the companion prints, require
that most of its content words occur in the main artefact. It catches renamed concepts,
leftover foreign-language jargon, and stale terminology without hard-coding any specific string.

Two traps inside the gate itself:

- **A whitespace-flattened variable cannot delimit labels.** The audit already had
  `_ft = re.sub(r'\s+', ' ', raw)`; splitting labels on `r'\s{2,}'` then recovered 1 of 4 and
  the fragment `gian`. Parse raw text with newlines intact.
- **`grep` for a lowercase term misses the capitalised occurrence.** The stale term appeared at
  line 245 lowercase and line 252 as `Thao tác pháp lý…`, so a case-sensitive sweep found one of
  two and would have left a drifted header in place.

### Coordinates prove nothing about a line break inside a cell

The form's text bounding box measured **identical** before and after the change (bottom edge
754.3 pt, 3.09 cm of slack), so no coordinate check could flag it — yet the fourth checkbox sat
alone at the end of line 1 with its label pushed to line 2, reading as **five items where there
are four**. Joining each box to its label with U+00A0 (14/14 sites) fixed it; the separator
*between* items stays a normal space so wrapping still happens at the right place.

Only looking at the rendered cell revealed this. Rule: for forms and checklists, geometry
proves the box does not overflow the page, never that a marker stayed attached to its label.

### Verify the companion with the same instrument as the main artefact

After fixing the article's text layer, run the *identical* phrase probe on the companion: it
returned 40/40 = 100 % and 0 orphan lines because it uses Times New Roman (TrueType, 282/282
Vietnamese codepoints), while the article used the substituted P052. Same probe, different
verdicts — a fix applied to one file says nothing about the other, in either direction.

### A cached reference document may be an error page wearing a `.pdf` extension

`hujos_assets/author_guidelines.pdf` was 1,789 bytes of HTML — Google Drive's
*"Sorry, the owner hasn't given you permission to download this file."* The real guideline was
sitting beside it as `1hVqkAGK4_...bin`, a genuine 4-page PDF. Any constraint justified by
pointing at the first file is unfounded. This is the same trap already recorded for the
reference corpus (three `.pdf` files that were 403 pages); it applies equally to **project
assets and specification documents**, not just to cited sources. Run `file -b` over every
cached evidence file, not only over downloaded references.
