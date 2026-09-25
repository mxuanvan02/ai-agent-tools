# Auditing a derived dataset: provenance survival and substring false positives

Failures and procedures from characterising released and staged datasets built from
a restricted textbook corpus. The first sections record confident wrong statements
that had to be retracted to the user; the later ones are the procedures that prevent
them — locating a bundle that is not where the paper says it is, copying only the
channel you measure, and auditing a release that is staged but not yet public.

---

## 1. A released export may have flattened the field you want to filter on

The plan was "filter the 2,371-sample release down to the civil-law subset."
Every provenance field needed for that had been collapsed at export time:

```
document_title : 2367/2371 == "qa_eligible_contexts"        <- placeholder, not a title
legal_domain   : 2371/2371 == "unspecified"                 <- never populated
source_asset   : 2367/2371 == "source_asset::qa_eligible_contexts_jsonl"
```

Only 4 samples retained a real textbook name. The subset filter was impossible
on the release artifact — not because the data lacked the property, but because
the export lost it.

**Rule: before promising a filter, count distinct values of the filter key.** A
single dominant value, a placeholder-looking string, or an all-`unspecified`
column means provenance did not survive. One `collections.Counter` on the field
answers this in one call and costs nothing.

```python
from collections import Counter
c = Counter(json.loads(l).get("legal_domain") for l in open(p))
print(len(c), c.most_common(5))    # 1 distinct value == no filtering possible
```

Symptoms that a field is a placeholder rather than a value: it names the *file or
stage that produced it* (`qa_eligible_contexts_jsonl`) rather than the thing it
describes; it is identical across ~100% of rows; it repeats a pipeline directory
name.

### Go upstream to the inventory, not sideways to another release

The upstream corpus inventory carried what the release had dropped — one row per
source document with the real filename, page count, license, and a text-layer
probe:

```
corpus_48_inventory.jsonl  ->  filename, page_count, sha256, local_pdf_path,
                               license_status, redistribution_scope,
                               text_layer_probe
```

Search for the inventory by *content* rather than by expected filename. Grepping
for a domain term across the pipeline tree found it when a filename guess would
not have. Also: the field holding the human-readable name differed from the one
in the release (`filename`, not `document_title`) — print the field list before
selecting keys, or you get 48 blank lines and misread it as an empty file.

### Two properties to read off the inventory before planning any work

- **`text_layer_probe: false` means OCR is required.** Two of three target
  documents (719 of 1,183 pages) were image-only scans. Sequence the work to
  start with the document that has a text layer, and treat OCR as a separate
  stage rather than a precondition for everything.
- **`license_status` / `redistribution_scope` bound what may be published.**
  `INTERNAL_RESEARCH_SOURCE_UNVERIFIED` + `INTERNAL_ONLY_UNTIL_REVIEW` permits
  internal derivation but not reproducing source passages in a public artifact.
  Check this *before* extracting quotable text, and report the constraint to the
  user with the plan rather than after drafting.

### Which pipeline stage holds the signal you need

A released QA dataset is the pipeline's **output**: generated items, and often redacted
records carrying booleans and hashes instead of text. The **input** bundle — page text
plus the OCR/derived channel — sits further upstream, and it is what measuring the corpus
itself requires. Name the stage that holds your signal before planning any regeneration
work; measuring corpus properties on a redacted release reports what the release kept, not
what the corpus contains.

Two consequences to state rather than discover late: numbers from different stages of one
pipeline are **not interchangeable** (different corpus, different item definitions, a
differently-defined `question` field), so a release can calibrate a threshold but cannot
stand in for a census — scope every figure to the stage it came from; and a released
artifact's own stats file is the cheapest oracle for your loader, so when your
recomputation disagrees with it, suspect the loader before the data.

### Scan your own artifacts before publishing them

Restricted source text must not ride out inside the reports, specs, and scripts generated
from it. Scan every artifact you intend to commit, and report the hit count *and the
method* — a bare "clean" is not evidence.

- Compare **values**, not raw file substrings. Testing whole-file text against tokens
drawn from the corpus flags ordinary English words (`from`, `this`, `with`, `have`) that
occur in your own explanatory prose; each such hit is a false positive costing a
retraction. Parse the artifact (JSON/markdown) and test the field values you actually
emit.
- A shingle index works better than a word list: build n-grams (≈6) of accent-folded,
punctuation-stripped tokens from the restricted fields, then test each artifact against
it. This catches copied passages while ignoring incidental single-word overlap.
- Keep the restricted raw data **outside** the repository tree and say where it lives;
the committed artifact should carry counts, ids, and hashes only. Copying raw data into a
scratch directory inside the repo makes it one `git add -A` away from publication.

---

## 2. Substring regexes over natural-language options inflate counts severalfold

Characterising item-writing flaws in a 59-item question bank, an "all of the
above" detector reported **44% (26/59)**. The real figure was **12% (7/59)** —
a 3.7× overstatement, reported to the user before being caught.

Cause: the pattern matched the bare Vietnamese word `cả` ("all/both"), which also
occurs inside ordinary phrases such as `bao gồm cả …` ("including also …") and
`cả nước` ("nationwide"). Each individual match looked plausible in isolation,
which is exactly why the aggregate was believed.

Mitigations, in order of strength:

1. **Anchor to the option slot, not the sentence.** These distractors are whole
   options. Match the option text in full (`^(Tất cả|Cả) (các )?(phương án|đáp
   án|A, B, C)`), not a token appearing anywhere in the line.
2. **Print the matched items and eyeball a sample before quoting a rate.** Seven
   printed options are checkable by hand in seconds; 26 are not, which is a
   signal in itself.
3. **Sanity-check the magnitude against the domain.** A 44% rate for one specific
   flaw in one bank is implausibly high; implausibility is a prompt to re-verify,
   not a finding.

**On retraction:** state the corrected number, name the mechanism (substring
match on a common word), and say explicitly where the bad figure was used so the
user knows the blast radius. Here it had not yet entered the manuscript, which
was worth saying — an unreported wrong number and a published one need different
remediation.

---

## 3. Structural claims need the artifact's own key, not an inference

The same bank was described as having a length cue because the longest option ran
a median 4 words longer than the runner-up. That measurement is fine; the
*conclusion* that the longest option is the correct one is not — the public file
shipped **without an answer key**, so no ground truth existed.

Report the measurable (length asymmetry, position distribution) and state the
absent key as a limitation of the source. Do not close the inferential gap with
the plausible reading.

---

## 4. Locating a bundle that is not where the paper says it is

Search in this order, because each step is cheaper than the next:

1. **The platform the user named, by that exact name and close variants.** A 0-hit
   API result is an answer, not a dead end — but query it before widening, or you
   spend a round trip characterising the wrong dataset.
2. **Release assets of the code repository.** An asset of a few hundred bytes is a
   synthetic fixture, not data; read it and say so rather than treating it as the
   corpus.
3. **Cloud archive by keyword listing.** A recursive listing of the archive's
   top-level directories filtered by project terms (`rclone lsf -R --max-depth 4 …
   | grep -iE 'project|frame|bundle|dataset'`) takes minutes. Start it backgrounded
   and keep working; do not block the session on it.

### Copy only the channel you measure

Once located, filter at copy time instead of mirroring the tree: excluding image and
PDF extensions turned a 745 MiB workspace into 4.4 MB of JSON — enough for every
corpus measurement, and it kept copyrighted pixels off the machine entirely. State in
the report which channel you copied and which you deliberately skipped, so a later
reader knows the measurement never saw the images.

This is also what makes the upstream-channel rule in the main skill actionable: the
text/OCR channel usually ships inside those JSON files, so copying them is what
avoids regenerating the signal with a different engine.

### A sibling directory that looks like more data may be out of scope

Archive trees often hold a companion directory of extra units beside the main set.
Read that directory's own MANIFEST before adding anything to a pool: a scope
declaration ("built from documents outside the dataset scope", "relocated rather than
discarded") means those units are neither in-frame nor rights-cleared for this work.
Counting them silently inflates every downstream denominator — held-out pool size,
power, feasibility fractions — and the inflation is invisible in the final numbers.

---

## 5. A staged release answers a different question than "is it published?"

Finding nothing on the public platform and finding a `release/` or `hf_upload/` tree
in the archive are both true at once. Report both: "not public" alone leaves the user
believing there is nothing to review, when in fact the payload is one upload command
from being public and its licensing needs a decision *now*.

### Check these before recommending or blocking an upload

- **Sibling release directories differ.** Two staged copies of one release usually
  differ by a single record file and by the hash of their verifier script. If either
  is published, one must be chosen, not merged; diff the file lists and the hashes
  first and say which one is current.
- **A MANIFEST's exclusion list is scoped to the files it enumerates.** Before calling
  a payload a redistribution violation, check whether the manifest's own file list
  covers it — a manifest written for `records/` says nothing about a sibling `.jsonl`.
  Report it anyway: a downloader reads the manifest as governing the whole repository,
  so the mismatch misleads even when it is technically a scoping artefact.
- **A redaction rule is a claim about the builder that enforces it.** "Any string
  carrying diacritics is not emitted; the builder fails closed" can be verified by
  counting the forbidden characters per directory — measured 0 across the records
  files. Verify it where it is claimed, then separately measure the payload it does
  *not* govern, and state which directory each claim holds for. Never generalise a
  per-builder invariant to a whole repository.

### Compliance is checkable without reading the text

A well-built payload ships a per-item metric beside each withheld field — longest
verbatim run in words — plus the threshold used for withholding. Histogram the metric
over the published items and confirm the published maximum sits under the threshold;
that audits the rule with zero reproduction. Expect and explain denominator
differences between the payload summary and the derived records (published items only
vs all admitted items); they are not an inconsistency.

---

## 6. Inspecting restricted text without reproducing it

When the payload itself is restricted, measure shape and never print values:

- Classify each string field by shape — hash-like (length ≥32, all hex), id-like (one
  token), free-text (several words, long) — and print field name, length, word count,
  diacritic count. That is enough to find which fields carry source-derived prose.
- Count the language's distinctive characters rather than eyeballing: a text-free
  channel scores 0, a published question field scores near 100%, and the difference is
  the finding.
- Extend the shingle index used for artifact scanning (§1) to cover generated text the
  payload publishes, not only the source OCR. Scanning your own report against source
  shingles alone passes a report that quotes a generated question.

Keep the downloaded payload in a scratch directory outside the repository tree and say
where it lives, so no `git add -A` can carry it out.
