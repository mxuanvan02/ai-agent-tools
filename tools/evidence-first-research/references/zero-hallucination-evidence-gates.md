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
