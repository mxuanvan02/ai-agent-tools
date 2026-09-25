---
name: evidence-verified-auditing
description: Use when reporting findings from a bulk code or data scan.
license: MIT
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags:
      - audit
      - verification
      - false-positives
      - provenance
      - reporting
    related_skills:
      - latex-thesis-evidence-audit
      - grounded-citations
      - precise-read-and-edit
---

# Evidence-Verified Auditing

Auditing at scale means running greps, regexes, and parsers across a tree and
turning the output into findings. The hard part is not finding candidates — it is
proving each candidate is real before it reaches the user. This skill governs that
proof step, plus the discipline for fixing what the audit finds without corrupting
provenance.

Use together with the domain skill for the artifact type (e.g. a thesis/manuscript
audit skill for `.tex` trees). This skill owns *how you validate and report your
own scan output*, independent of domain.

## When to Use

- You ran a repo-wide or corpus-wide scan (grep, regex, CSV parse, AST walk) and
  are about to tell the user how many problems exist.
- You are about to repair data that some pipeline generated.
- A file, directory, or document section has been declared off-limits, but a fix
  appears to be needed inside it.
- You are about to claim a side effect happened (push, upload, delivery, build).
- The user asked to reduce a project tree to one copy of each file (no `v2`/`v3`/`_final`
  clutter, delete the redundant, keep only the newest) — see rule 14.
- You are about to write or regenerate a status report *about* the tree (validation
  report, delivery summary) — see rule 14 §8.

## Core rules

### 1. A scan produces candidates, not findings

Every regex over real-world source produces false positives. Reporting them as
findings costs more trust than missing a real error, because the user must then
re-verify everything you said. Before stating a count, confirm it against an
**independent oracle** — a different mechanism that would disagree if your
extraction were broken.

| Your scan claims | Independent oracle |
| --- | --- |
| missing / unresolved references or keys | the build's own diagnostics (`*.log`, `*.blg`, linker/compiler output). If the toolchain reports 0 errors, your extractor is wrong, not the data |
| metadata mismatch (author, year, title) | authoritative registry by stable ID (Crossref/DataCite by DOI, package registry by name+version) — never a string compare against your own capture group |
| duplicate IDs | re-parse with a real brace/bracket-aware parser, then compare normalised IDs |
| unreferenced label / dead symbol | is the defining file actually included in the build graph? An orphan file's symbols are not dead code |
| formatting violation (separators, units) | context filter first; many "violations" are a different syntax entirely (see coordinates pitfall below) |
| N items changed | hash or byte-compare before/after, and diff cell-by-cell rather than trusting file size |

Retract false alarms **explicitly** and name the parser bug that caused them. A
quietly dropped claim reads as an unresolved risk.

Classify **before** you report the count, not after. A leak/neutrality/policy scan
is the worst case for this, because every hit looks individually damning. Four
filters, applied by reading each hit's own line rather than by pattern:

| Hit shape | Why it is usually not a finding |
| --- | --- |
| the token appears in a comment or docstring | it documents intent; it is not data the program acts on |
| the file's role is to *compare* that value against a record | a checker legitimately pins expectations, and it fails when the artefact drifts — removing the pin removes the test |
| the token is an ordinary word or an identifier (`accepted` in "only --help is accepted", a function named `accepted()`) | substring matching a common word is the inflation rule below, in a policy guise |
| the file is a rights/provenance/copyright notice | naming the funder or copyright holder is that file's function, not a leak |

Then report the verdict **per surface**, never as one pooled count. A private
working tree legitimately holds one-off maintenance scripts, review logs and
changelogs that the shipped repository never sees; mixing the two surfaces makes
a clean release look dirty and sends the fix to the wrong tree. Measure the
shipped checkout (and any pending branch of it) separately from the working tree,
and state which surface each number describes.

When scanning for identity leakage specifically, build the pattern from distinctive
tokens — grant codes, funder names, institution names — never from a personal name
that is also a common substring in the corpus, and write non-ASCII alternatives as
literal characters. `\xNN` escapes inside a raw string make `re.compile` die with
`incomplete escape` before a single file is read, so the scan reports nothing and
looks clean.

**Scan breadth and file-class breadth are both part of the claim.** A path-leak scan
that matches only two of the machine-specific prefixes in use reported "0 machine paths"
while five tracked
files still carried absolute paths: widening the pattern to `/var`, `/mnt`, `/srv`, `/opt`
found them, and scanning only `.py`/`.sh` had hidden four more in `.md`/`.json`/`.txt`.
State which extensions and which path prefixes a scan covered, or the "0" describes the
scanner, not the tree.

**Classify by what the file IS, and let the classification carry the reason.** The same
absolute path is a defect in code and evidence in a record:

| File class | Verdict on an absolute path |
| --- | --- |
| executable (`.py`, `.sh`) | defect — the location must be an input or derived from `__file__` |
| sealed pre-registration / digest-pinned manifest | evidence — the path records where the check ran; editing breaks the pin |
| measurement record (`"bundle": ...`) | evidence — names the input the numbers came from |
| provenance notes, build logs | evidence — the `cd` lines and TeX Live toolchain paths are what make them checkable elsewhere |
| the document that DEFINES the exemption | must quote the paths it exempts, or the rule cannot be checked by reading; tolerate only while it carries no personal path |

**A list introduced as exhaustive must be exhaustive.** After fixing four leaks, a README
listed the four exceptions; the wider scan then found a fifth class it omitted. Either the
list names every remaining hit or it must not read as complete — and the scan that checks it
should abort on any unclassified hit rather than print a count.

**A checker's own false positives abort the run before it can report.** Make the classifier
fail closed on an unclassified hit: it surfaces the mis-classification immediately instead of
letting a whitelist-shaped scan quietly pass.

### 2. Verification of identity is not verification of content

Two different questions, routinely conflated:

- **Identity/metadata**: does this reference point at the artifact it claims?
  (author/year/title match the DOI; the version matches the lockfile)
- **Content/claim**: does that artifact actually support the statement citing it?
  (the sentence's claim appears in the source's full text)

Passing the first says nothing about the second. Always report which one you did,
with the denominator — `8/124 claim-verified, 127/127 metadata-verified` — and
never let the easier check stand in for the harder one. If the content evidence
(full text, logs, raw measurements) is unavailable for part of the corpus, say so
and give that count separately.

### 3. Fix at the source of the pipeline, never in the generated artifact

Trace the dependency chain before editing anything:

```
source-of-truth (overrides/config)  →  transform script  →  generated data  →  document/figures
```

Editing the generated file makes the next pipeline run silently revert it. Find
the human-editable layer (often an `overrides.json`, a manual-adjudication file,
or a config) and correct it there, in the schema's own vocabulary.

Two obligations when you do:

1. **Use an existing valid value.** Read the schema/taxonomy file and pick a
   value that is already legal. Inventing a new enum member breaks consumers —
   including hard-coded label maps in plotting scripts, which fail with
   `KeyError` on the new value. Grep for scripts that read the field and extend
   their maps, preferably as an alias so old values keep working.
2. **Prove idempotency.** Run the pipeline twice and compare hashes:

```bash
python3 apply_overrides.py && python3 build.py && h1=$(sha256sum out.csv | cut -c1-16)
python3 apply_overrides.py && python3 build.py && h2=$(sha256sum out.csv | cut -c1-16)
[ "$h1" = "$h2" ] && echo IDEMPOTENT || echo "DRIFT $h1 -> $h2"
```

Then re-derive every downstream number and regenerate every downstream figure.
A corrected dataset with a stale figure is worse than the original error.

### 4. Hash difference ≠ content difference

Regenerated data files routinely differ in bytes while being semantically
identical. Before reporting "the pipeline is non-deterministic", check the cheap
causes: line endings (Python's `csv` writer emits CRLF; repos often store LF),
BOM, key order, float formatting, timestamps.

```bash
wc -c old new; grep -c $'\r' old new     # CRLF vs LF
python3 -c "import csv,sys; a=list(csv.reader(open(sys.argv[1]))); b=list(csv.reader(open(sys.argv[2]))); print(sum(x!=y for ra,rb in zip(a,b) for x,y in zip(ra,rb)),'cells differ')" old new
```

If 0 cells differ, the artifact is unchanged — do not commit the churn, and warn
the user that a clean checkout will show the file as modified after a rerun.

### 5. Frozen files: fix downstream, prove untouched

When the user declares a file locked (an approved proposal, a signed section, a
vendored dependency), it is off-limits **even when it contains the bug**. Route
the fix to a layer you are allowed to change:

- a citation key that the locked file uses but the bibliography lacks → add an
  **alias** in the bibliography (`ids = {old_key}` in biblatex) instead of
  editing the key in the locked file;
- a value the locked file references → correct it where it is defined;
- a claim the locked file makes → surface it to the user, do not rewrite it.

Then prove non-interference every time you report:

```bash
cmp -s locked.txt /path/to/pristine/locked.txt && echo IDENTICAL || echo MODIFIED
```

If you already edited it before the constraint was stated: back up your version,
restore the pristine copy, verify `IDENTICAL`, and say plainly that you cannot
recover your edits if no backup existed. Never claim a restore you did not verify.

The lock can cover a file's **name**, not only its contents. A sealed record that stores a
filename beside its sha256 makes renaming equivalent to deleting: the record then points at
a file that no longer exists. Grep the records and the pre-registration JSON for the filename
before any rename, watch for a hardcoded path constant
(`X_PATH = parents[1]/"dir"/"foo_v2.py"`), and re-verify the pinned hash afterwards.

Related trap: a locked *section* often also has a **role** constraint, not just a
text constraint. An introduction/proposal section may be forbidden from carrying
result numbers at all. Removing the wrong number is not enough — the number
should not be there. Move it to the section that owns it and cross-reference.

### 6. Claim a side effect only from its own confirmation

Self-reported success is not evidence. Check the remote/receiver state:

```bash
git ls-remote origin 'refs/heads/*'        # remote truth, not local ref
git status --porcelain                      # empty = nothing left uncommitted
sha256sum artifact.pdf; unzip -p pkg.zip artifact.pdf | sha256sum   # package matches source
```

If a push over HTTPS fails on credential scope, push over SSH and re-verify with
`ls-remote`; a `403` in the middle of a script does not mean the commit landed.
Shell-quoting failures silently skip commands — `git commit -m "$(...)"` with
nested quotes can die on `unexpected EOF` while the surrounding script continues
and prints a stale "up-to-date". Write the message to a file and use
`git commit -F <file>`.

### 7. Check the unit and the context before calling a number a violation

A threshold comparison in the wrong unit produces a *whole class* of false positives
that all look individually plausible. Real case: a figure linter compared PDF font
sizes against a 6pt floor and flagged every `5.98pt` glyph. PDF records font size in
**big points** (1in = 72bp); TeX uses **printer points** (1in = 72.27pt). Factor
`0.996264`. Every 6.00pt TeX glyph appears as `5.98` — a 0.37% unit error masquerading
as 12 typography findings.

Before reporting any measured value as out-of-bounds, answer three questions:

1. **What unit does the source record, and what unit is my threshold in?**
2. **What context scales this value?** (a figure at `\resizebox{0.46\linewidth}` shows
   4.98pt as 2.67pt on the page — the raw number is not what the reader sees)
3. **What standard does the domain itself prescribe?** (LaTeX's `fontmath.ltx`
   mandates 6pt `scriptscript` at 11pt/12pt base; reproducing it is conformance)

If any answer is unknown, the correct severity is `warning`, not `error`. Add an epsilon
(~0.05 of the unit) so values sitting exactly on a threshold never fail on rounding.

### 8. A sufficient condition, inverted, is not a necessary one

Many audit heuristics are borrowed from *synthesis* literature where they are
deliberately conservative: "if the boxes are disjoint, the layout is certainly legible."
Inverting that into "if the boxes intersect, the layout is illegible" asserts the
converse and is unsound. Bounding-box intersection is **necessary but not sufficient**
for an overlap defect — combining accents, stacked Vietnamese diacritics, kerning,
sub/superscripts, and oversized math delimiters all produce legitimate intersecting
boxes.

When your predicate comes from an optimisation objective, expect a high false-positive
rate by construction, and reach for the graded form the source literature actually uses
(overlap *area*, penetration *depth*, clearance *distance*) rather than a boolean.

### 9. Verify with a fresh copy of your own scanner

Editing a tool in one location and running it from another silently measures the old
code. A rescan that returns results identical to the pre-fix baseline is a red flag for
this, not evidence the fix failed. Compare hashes of the executable itself before
trusting any before/after comparison:

```bash
sha256sum ./clone/scripts/tool.py ~/.installed/tool/scripts/tool.py   # must match
```

Note that `rsync --exclude` *protects* excluded paths from `--delete`, so stale
`__pycache__` and build directories survive a sync and must be removed explicitly.

### 10. Auditing a set of gates/filters: rank by *independent* rejection

When the artefact is a conjunction of checks (`A = G1 ∧ … ∧ G8`, a linter rule set, a
validation pipeline), absolute failure counts are misleading — a gate that fails often
may only ever reject items another gate already rejected, so removing it changes
nothing. Measure each gate's **independent rejection**: it fails while every
gate ordered before it passes. Then confirm with a leave-one-out variant table
(recompute the admission count for each gate-set subset and see which rows actually
move). A gate whose independent share is ~0 is redundant *in the conjunction*, and
that is a finding about the paper's framing: the product advertises N independent
checks while only M are doing work.

Two supporting measurements worth printing:

- **Overlap matrix.** How often two gates fail together. High overlap quantifies the
  redundancy claim instead of asserting it.
- **Pass rate by stratum.** Split each gate's pass rate by document/item type. A
  threshold systematically harsher on one stratum is a structural bias of the
  instrument, not a quality difference between items — and it means a single global
  threshold is the wrong design.

Also check whether the records name *which* gate failed. A pipeline that stores one
boolean for a whole block of upstream checks (five provenance gates collapsed into
`admitted=false`) cannot support any claim about which check did the work; widening
that field is a near-zero-cost fix worth recommending.

### 11. Before proposing an improvement, search the artefacts for a prior measurement of it

Pre-registered projects usually record **rejected** variants beside adopted ones —
docstring sections explaining what was tried, `rejected_*` / `*_chance_baseline` nodes
in a protocol JSON, comments naming a stricter rule that was abandoned. Grep for
`reject`, `chance`, `baseline`, `tried`, `abandon`, `weaker` before designing anything.

The decisive inference: **a proposal stricter than an already-measured-and-rejected
variant is refuted before you write it** — its pass rate is bounded above by the weaker
variant's observed rate. Cheaper than any new experiment, and it prevents recommending
something the project's own sealed data already kills. When a variant was rejected for a
*corpus* property rather than a design flaw, say so: the fix then lives in the sampling
frame, not in the gate, and re-proposing the gate is a category error.

The same search applies to **derived data channels**, not only to decisions. Before
installing a tool to regenerate a signal — OCR a figure, re-embed, re-tokenise — grep the
upstream archive for that signal already computed: a sealed channel usually ships per-item
confidence, coordinates, and the flags the measurement needs. If it exists, use it.
Regenerating with a new engine measures the *engine*, not the corpus, and the numbers then
become incomparable with everything already published from the sealed channel. Say which
one you measured, in the report.

### 12. A green verifier is not evidence until you make it red

Pinning numbers behind a checker only works if the checker can fail. Before reporting
`checked: N, mismatches: 0`, inject defects and watch it go red. Four classes of false
green were each found in a verifier that reported clean:

| class | shape | symptom |
| --- | --- | --- |
| vacuous aggregate | `all(...) if items else False` | an empty subset reports a verdict regardless of truth |
| wrong key | iterating a dict keyed `<id>::<variant>` while matching `row['id']` | 0 of N scored, every fraction silently 0.0 |
| neutered guard | `if False:` left around an assertion | compiles, reports success, nothing runs |
| swallowed assertion | `try: assert ... except AssertionError: pass` | call site present and "live", failure discarded |

Requirements:

- **Mutation-test the verifier**: flip a comparison (`>=` → `>`), swap a counting
  convention, gut the body, neuter the guard, swallow the exception. Every meaningful
  mutant must go red. Report survivors — a survivor is either a real hole or an
  equivalent mutant, and you must say which.
- **A mutant that fails during setup never ran.** Count it separately. Reporting
  "16/16 killed" when one mutant raised before its assertion is a false claim about your
  own test.
- **Positive mutants alone do not validate a classifier — add a negative control.** A
  hand-written "allowed residue" whitelist passed all four injected results and still
  reported nonsense, because `\d+(?:[.,]\d+)*` chops one commit hash into `041420` /
  `0625` / `4918` / `43` and calls the fragments findings; section numbers, line refs and
  harness check counts were flagged the same way. Feed it a string that contains only
  method and build tokens (`15 pages`, `15/15 clean`, `§1.3`, `L265`, `alpha 0.05`,
  `4/5`, a hex digest) and require **zero** hits. Without that, "clean" is untested.
- **When you add an exclusion, prove it did not blunt the checker.** After excluding
  pre-specified thresholds, re-inject a real p-value *on a line containing the exclusion's
  own keyword* (`below the threshold: p=0.0525`) and a bare threshold *with no context*
  (`The value was 0.05`). Both must still be caught. Make the exclusion two-condition
  (closed token set AND context hint) so no single condition can smuggle a result through.
- **Prefer classifying by token shape and context over maintaining a whitelist.** Mask hex
  digests, section refs, line refs, `n=` annotations and bare percentages first; then treat
  `n/n` tallies and `k/5` ordinal cuts as method, and only `count/denominator` plus
  decimals of 2+ places as findings. The whitelist version needed a new entry for every
  harmless token and still missed the shape that mattered.
- **A guard inside a file cannot protect itself from being deleted.** Put the check in a
  *separate* file that runs the suite and re-derives the expectation independently — from
  the source's own AST, not a hand-written constant, so lowering the threshold by hand to
  match a gutted body is impossible.
- **Pin returned values, not constants.** `"selftest": "passed"` is a vacuous pin that
  survives every mutation. Have the probe return its numbers and assert against those.
- **An equivalent mutant needs its premise pinned, not a fix.** If removing a guard cannot
  change the output because the corpus has no zero-length subsets, assert that premise —
  it converts silent equivalence into a red flag the moment the corpus changes.
- **Proving a gate is load-bearing takes two mutations at once.** Disabling a gate on a
  clean corpus proves nothing: the audit stays green because there is nothing wrong to
  find. Corrupt the document *and* disable the gate that catches it, then require the
  corruption to go undetected — green is the PASS condition, inverted relative to every
  other case, and the harness must say so or the result reads as a failure. Two files now
  need snapshots, so hash-verify both on restore and restore both if anything aborts
  part-way; one leftover mutation poisons every case after it.
- **Equivalence is a property of the corpus, not of the mutant.** Widening a fallback
  pattern is unobservable while the primary channel attributes every token (zero
  UNACCOUNTED), so the mutant is dead on this corpus and live on the next. To test
  precedence, mutate the call **order** — consult the fallback before the evidence — which
  is observable on a clean corpus and is the failure mode the gate exists for.

Depth: `references/proving-a-verifier-can-fail.md`.

### 13. Per-token provenance does not imply line-level consistency

An audit that attributes every number to a source can still pass on a false
sentence. Corrupting `41/227 = 18.1%` to `42/227 = 18.1%` left a 552-token audit
green, because `42` was pinned (as a *different* quantity), `227` was pinned, and
`18.1` was still a render of the untouched pin `0.1806`. Every token had
provenance; the line was false. Only a mutation test found it.

Attribution answers "does this number have a source". It never asks "do the
numbers printed on this line agree with each other". Where a document prints
`a/b = X`, that is an arithmetic claim: recompute it at X's own printed precision
and fail on disagreement.

The same rule covers a printed *interval* derived from a printed count. A manuscript
printing `A = 50/60 = 0.83 [0.72,0.92]` is asserting a Clopper-Pearson bound;
CP(50,60) is [0.714781, 0.917071], which prints as `[0.71,0.92]`. Both spec
verifiers stayed green — they compare recomputed values against a hand-written
expectation list and never open the rendered document. Only a check that reads the
`.tex` caught it, so a tool that reads the artefact is not redundant with one that
recomputes it, and the one that is not in the standing report is the one that stops
being run. Compare at the precision printed, not at full float: half-up and
banker's rounding both appear in real documents, so an interval test accepts every
rounding convention the document could legitimately use while still rejecting a
bound that is genuinely wrong.

- Measure the baseline first (all 8 such rows agreed) so the new gate cannot be a
  quiet reclassification of existing text, and print the row count every run so a
  future row that stops matching shows up immediately.
- Compare at the precision **printed**, not at full float: `75/227 = 33%` is a true
  claim about a rounded value and must not fail for not equalling 33.0396.
- This does not replace a "both parts sourced" rule for a count column (`73 / 300`),
  where no ratio is printed and the parts are the evidence given. The consistency
  check applies only where a ratio IS printed, which is where the extra claim lives.

Corollary: **a provenance channel can mask a wrong pin.** When records and pins
both feed the universe, a pin that drifts from the records is still "sourced"
through the records channel, so the audit stays green. Name which tool owns
pin-vs-record agreement, prove that one goes red, and report the masking as a
stated limitation instead of letting the audit's green stand in for it.

### 14. Reducing a tree to "one copy of each file"

Version-shaped names are not evidence of duplication, and the only list that proves
redundancy is a sha256 group. The procedure, in order: survey (sizes, name pattern, hash
groups, reference graph) → classify every duplicate group → check whether the tree has any
undo (`git rev-parse --git-dir`) → act in three classes only (DELETE-DUP with a twin found
by hash at delete time, DELETE-REGEN from an explicit enumerated list, ARCHIVE by move with
the destination hash verified) → prove idempotency by re-running → re-run the whole suite.

Four findings that reverse the obvious call:

- **Byte-identical is not the same as redundant** — the inverse of rule 4. A build output
  that matches a hash-pinned deliverable byte for byte is the *proof* the shipped artifact
  equals what the current sources build. Measure reproducibility first: a LaTeX/PDF rebuild
  usually gives the same size and a different hash (embedded `/CreationDate`), so the pair is
  not spare.
- **A same-named file inside two sealed run directories is per-run self-containment**, not
  duplication. Removing one breaks the run's ability to stand alone.
- **A log re-run whose files differ in content is reproducibility evidence.** Compare
  mtimes and diff the payloads before treating the older round as superseded.
- **Import-graph scans mislabel live files as orphans**: entry points (invoked by a report
  generator or a human, imported by nobody) and files that `import` *from* this tree while
  measuring data belonging to another project. The latter cannot be relocated without
  breaking its import — keep it and record why in the README so the next scan does not
  re-flag it.

Depth, including the manifest-survival fix and the generated-report pattern:
`references/dedup-to-single-version.md`.

## Reporting shape

1. Lead with the verdict per area: `PASS` / `BLOCKED`, separately.
2. For each real finding: `location → cause → fix`, with the evidence that proved
   it real (which oracle agreed).
3. State denominators for every count, and which verification level it reflects.
4. Report a reduction as an absolute against its target, not as a delta. "Cut by a
   quarter" and "meets the cap" are different assertions; when the target misses,
   give the final value and the measured gap, and leave the item open rather than
   folding it into a list of finished work.
5. List retracted false alarms with the parser bug named.
6. End with exactly one next action when work remains.

Do not present a candidate list as a findings list. Do not report a count you did
not cross-check.

## Pitfalls

- **Counter drift corrupts both halves of a before/after.** Word and line counts
  depend on how markup is normalised away: stripping LaTeX commands, braces, `$`
  and `~` before splitting yields a different total than splitting the raw source.
  Measured on one abstract, two normalisers gave `376 → 249` and `345 → 263` —
  same direction, both absolute pairs wrong, and only the second comparable to the
  stated target, so the first supported a completion claim the second refuted.
  Define the counter once, run it on baseline and current in the same invocation,
  and re-measure the baseline from the archived source instead of quoting a number
  recorded earlier in the session; once the working tree has been edited, the
  archive is the only stable baseline.
- **Vacuous matchers report 100%.** `all(k in name for k in keywords)` matches
  *every* candidate when the keyword list is empty — and it goes empty exactly for the
  items whose identifiers are opaque (`T13_r13_p1_04` has no keyword longer than the
  length filter). Assert the keyword list is non-empty per item, and treat a perfect
  match rate as a matcher bug before treating it as a result. Related trap: retrying
  with progressively fewer keywords on failure hides which items matched strictly, and
  the relaxed number becomes the headline. Report strict and relaxed separately.
- **"Tests passed" is a claim about the runner, not the tests.** A flat script-style
  suite that calls `sys.exit(0)` at module level makes pytest raise `SystemExit` during
  collection: it prints `INTERNALERROR`, collects 0 items, and exits 3 — which reads as
  green to anyone checking only "did it complain about a test". Confirm the runner RAN
  something (`collected N items`, a `PASS n FAIL 0` line, `RAN n/n`) before reporting a
  suite as passing. Fix by wrapping the body in a function plus a thin test wrapper, so
  both `python3 file.py` and `pytest file.py` exercise the same checks and cannot drift.
- **Sort one list, then zip it against another, and you compare unrelated items.** Sorting
  column A in place and pairing it positionally with unsorted column B is a silent
  mis-pairing: it produced 29 "duplicates" where 4 existed. Pair first
  (`sorted((a, b) for ...)`), then sort the columns if you need distributions.
- **A cross-check list must contain every field you assert.** Comparing two independent
  implementations agreed 27/27 while the one field with a real bug was not in the
  comparison list. Add newly-computed fields to the cross-check in the same edit that
  creates them, and prefer deriving the pair list from one side's keys over typing it.
- **Verify the runner's exit code, not the last command's.** A loop ending in
  `[ $rc -ne 0 ] && { ...; }` exits 1 when the test PASSED, so the whole run looks failed.
  Re-run with an accumulator, or end the loop on a statement that always succeeds. The
  same trap with a background process manager: `cmd > log 2>&1; echo "EXIT=$?" >> log`
  makes the reported `exit_code` belong to the *echo*, so a poll returning
  `exit_code: 0, status: exited` carries no information about the run. Read the marker
  out of the log.
- **An anchor can be correct and still ambiguous.** `($b=19,d=4,p=0.0026$)` looked unique
  but the manuscript prints the same discordant pair for two different contrasts, so it
  occurred twice and the case refused to measure — correctly, since replacing the first of
  two identical occurrences is an ambiguous mutation. Grep the target for the anchor's
  occurrence count before writing the harness, and classify `FAIL(anchor)` separately
  from `FAIL(gate)` so a setup defect is never read as a weak gate.
- **Machine-readable stdout must never be truncated.** Printing `text[:4000]` of a JSON
  report emits unparseable output and breaks every consumer that pipes it. Emit the
  whole JSON when no output file is given; otherwise emit a small summary object plus
  the path. Truncating a stream a machine is meant to parse is a defect, not a
  convenience.
- **"PATTERN NOT FOUND IN OUTPUT" diagnoses the reporter, not the cause.** A status
  report that records only `exit: 1` plus a missed regex makes a real failure
  undiagnosable and sends you to repair working code. When a check fails, dump its
  stdout/stderr into the report; the line that explained everything here was
  `No module named pytest`, which the summary line had thrown away.
- **Checks invoked as the bare string `'python3'` inherit the caller's PATH.** The same
  command passed from a login shell (venv with pytest) and failed from a backgrounded
  subprocess (a conda env without it) — the outcome was decided by an invisible property
  of the launching process, not by the code under test. Invoke every check with
  `sys.executable`, print which interpreter that is into the report, and preflight any
  third-party import so a missing module is named instead of surfacing as a pattern
  miss. A small runner that picks the first candidate interpreter able to import what
  the checks need, and refuses to run if none can, makes the report reproducible for
  whoever runs it next.
- **Quote the last verdict line, not the first.** A mutation harness prints one VERDICT per
  injected mutant plus a final baseline, so a report generator using `re.search(r'VERDICT:.*',
  out)` quoted a *mutant's* verdict as the tool's conclusion: the acceptance record then showed
  "a structural classifier changed its reach" under a check that had passed 6/6. Take the last
  match, and print how many matches were seen so a reader knows the line was selected rather
  than unique. For a single-verdict tool first == last, so nothing else changes.
- **A documented flag is a claim about behaviour and must be measured like one.** `--quick`
  printed a banner saying it skipped the mutation harnesses and then invoked the generator with
  no arguments; the generator had no skip mechanism at all, so nothing was skipped. A banner a
  script prints about itself is not evidence. After adding any flag, run with it and check an
  observable that would differ — output filename, count of items executed, elapsed time — and
  only then document it. Conversely, when a partial run is legitimate, give it a separate
  artefact name and a verdict that cannot read as clean, so a fast run can never be quoted as
  the full record.
- **`sys.exit(text)` and `sys.stdout.write(text)` are not interchangeable, and swapping them
  silently changes both the status code and the control flow.** `sys.exit(text)` prints to
  **stderr** and exits **1** — so a usage/help message delivered that way makes the one command
  that documents the tool report itself as failed, and breaks `tool --help && ...`. Replacing it
  with `sys.stdout.write(text)` fixes the stream and the status but **returns**, so execution
  falls through into the rest of the module: the help printer then runs every check and
  overwrites the report it was documenting. Use `sys.stdout.write(text)` followed by an explicit
  `sys.exit(0)`. Verify all three observables after any such change — exit code, which stream
  carried the text, and that no side effect fired (report mtime unchanged, no verdict printed):
  a help path that exits 0 but still ran the harness is worse than the original bug, because it
  looks fixed.
- **Document INPUT / OUTPUT / EXIT CODES on every entry point, and audit it as a countable
  property.** A caller who cannot distinguish exit 0 from 1 from 2 cannot tell "all quantities
  matched" from "one mismatched" from "the records were missing" — and a validation harness that
  conflates those is worse than no harness, because its green is unreadable. Scan the shipped
  tree for entry points lacking those three headings and report the ratio (`0/11`), not a prose
  impression; the count is what makes the gap actionable. Fixing one tool's help text does not
  fix the family.
- **A measurement harness must fail closed when its input is missing.** Licensed or
  off-machine data is a normal state, not an excuse to synthesise. Exit non-zero with an
  explicit `BLOCKED` status and an empty results block, and pin the exit code in a
  fixture — otherwise a later refactor turns "could not measure" into a silent pass. If
  a synthetic mode exists for code-path proof, label the whole report synthetic and
  state in the docstring that its numbers must never be cited as measurements.
- **Coordinate-shaped numbers.** `(0,0)`, `(5.1,0)`, `(4.2,2.55)` in diagram code
  match a decimal-separator regex and are not decimals. A blind fix destroys every
  figure. Filter to lines carrying a unit or percent marker; verify the coordinate
  count is unchanged afterwards.
- **Substring matches on common words inflate rates severalfold.** A detector for
  "all of the above" distractors that matched the bare Vietnamese `cả` reported
  44% (26/59) against a true 12% (7/59) — `cả` also occurs in `bao gồm cả …`,
  `cả nước`. Anchor the pattern to the field it describes (a whole answer option),
  print the matched items, and treat an implausibly high rate as a prompt to
  re-verify rather than a finding.
- **A filter key may not have survived export.** Before promising to subset a
  released dataset, `Counter` the filter field. One dominant value, an
  all-`unspecified` column, or a value naming the producing stage rather than the
  thing described means provenance was flattened — go to the upstream inventory.
- **Interrupted builds leave truncated intermediates.** A crash mid-write yields
  `Runaway argument?` / `File ended while scanning` from a half-written `.aux` or
  cache, which reads like a syntax error in your edit. Delete all intermediates
  and rebuild clean before debugging your own change.
- **Missing optional dependency is a setup step, not a blocker.** If a regeneration
  script needs a plotting or symbolic library, install it (`pip install matplotlib`)
  and continue. If symbolic math is unavailable, verify algebra with concrete
  integer matrices — stronger evidence than symbolic manipulation anyway.
- **Oversized inline shell payloads are rejected by the harness.** Write the script
  to a file and run `bash <path>`; rejected payloads are saved under
  `~/.hermes/cache/blocked-scripts/` for recovery.
- **Calibrating a copy of the matcher measures nothing.** A probe that hardcodes
  one of the matcher's inputs (`frac_reason=None`) rejects every token the real
  matcher accepts through that input, so it reports a true-positive rate below 1
  for a correct matcher and sends you to "fix" working code. Calibration must call
  the same function with the same context; if it cannot, it is measuring a stricter
  matcher than the one shipped. Same family: computing a lookup table and then
  never using it, while the probe re-derives a weaker version per token.
- **A bound fitted to the result is not a bound.** Declare thresholds before
  measuring. A fixed 2% false-accept bound was structurally unreachable: the
  analytic coverage ceiling of the pinned values was 3.4% (3dp) / 8.6% (1dp),
  because that many random numbers genuinely coincide with real ones. Compute the
  ceiling, add declared slack, print both — an unreachable bound invites loosening
  until it passes, which destroys the measurement.
- **Value-matching small integers is coincidence, not evidence.** A random integer
  in 1..60 equals some record value ~70% of the time. Accept a bare integer only
  inside a verified fraction, or as the complement of one printed on the same line
  with a `%` sign — both structural, both checkable.
- **A silent MISSING hides a broken evidence channel.** `json.loads` on a stream
  that prints human-readable lines before the JSON raises; catching that and
  setting the tree to `None` degraded a dead channel into the word MISSING with no
  cause attached, and downstream tokens went unattributed for no visible reason.
  Scan with `JSONDecoder().raw_decode` from each `{`, and let failures propagate
  with their reason.
- **An equivalent mutant injected in a dead path reads as a failing gate.** Mutating
  `X or "UNACCOUNTED"` to `X or cls or "UNACCOUNTED"` *inside* `if cls is None:`
  cannot change behaviour — `cls` is already None. The harness printed FAIL and the
  temptation was to repair correct code. Classify a failed mutation as
  `FAIL(anchor)` / `FAIL(not-applied)` / `FAIL(gate)` rather than one undifferentiated
  FAIL, and mutate a call site that can actually change control flow.
- **Check whether the number is already public before treating it as a leak.** A code file
  containing `0.83` / `[0.71,0.92]` looked like it would disclose manuscript results, but the
  repository's own public verifier already contained those same constants, and the records
  they recompute from were published deliberately. What was *not* public was the manuscript's
  **verbatim LaTeX prose** used as mutation anchors — 16 fragments and 6 long strings, matched
  by substring against the `.tex` sources, absent from every branch of the public repo. So the
  exposure was the wording, not the arithmetic, and stripping the arithmetic would have been
  pointless work. Measure both channels separately before deciding where a file may go.
- **A public README's own scope claim is a gate on what you may add.** Pushing manuscript-
  auditing tools into a repo whose README says it "does not contain manuscript files" would
  falsify that sentence with the very files that embed manuscript text. Read the scope claim
  first; when the addition contradicts it, choose a different destination rather than editing
  the claim to fit.
- **One restore trap per mutation, not one per harness.** A single `trap restore EXIT`
  let mutations accumulate, so mutation 2 was measured against mutation 1's
  already-broken file and its `exit=1` was read as its own result. Snapshot, restore,
  and hash-verify around each case; pre-check every anchor and abort before writing
  if any matches zero or more than once.
- **Parameter-name slips waste a turn — and can waste four.** `terminal` takes `command`;
  `write_file` and `execute_code` take `content`/`code`; none takes an `arguments` wrapper.
  Wrapping the payload as `{"command": ..., "timeout": ...}` inside an `arguments` object, or
  putting a second stray key beside `command`, is rejected *before* running, so no state
  changed — confirm that ("file unchanged, sha256 ...") and reissue rather than assuming a
  partial edit landed. Same family: f-strings cannot contain backslashes, so build the
  replacement text outside the literal; and a cell that fails to compile has applied nothing,
  which is worth stating explicitly before retrying.
- **A tool installed as a snap cannot read your payload files.** `gh` from `/snap/bin` has its
  own private `/tmp` and a `home` interface that excludes dotfiles, so `gh api -F body=@file`
  fails with `no such file or directory` for `/tmp/x.md` and `permission denied` for
  `~/.x.md` — while `ls` in the same command proves the file exists. Diagnose with
  `command -v gh` before retrying. Fix: let the host shell read it and pass the content as an
  argument (`-f body="$(cat /tmp/x.md)"`), which needs no path the snap can see.
- **A compile failure in your patch cell is not a failed patch.** When the edit is
  expressed as Python (`path.write_text(src.replace(old,new))`), a syntax error anywhere in
  the cell — including in a diagnostic print after the write — aborts the whole cell, so
  the file may be untouched or half-written depending on ordering. Verify the on-disk hash
  before deciding which step to redo.
- **A cleanup script's own record must survive being run twice.** Writing a manifest with
  `open(path, 'w')` means the second run — which correctly moved nothing — writes an empty
  file over the first run's evidence. The archived files survive; the reason they are there
  does not, and the whole point of archiving instead of deleting is that the archive stays
  auditable. Give every run its own timestamped manifest and refuse to clobber a non-empty
  one with an empty one.
- **Read the anchor before writing it; never type one from memory.** Three separate patch
  attempts failed because the `old_string` was recalled rather than read (wrong variable
  name `r[...]` vs `uni[...]`, wrong indent, wrong constant from a *different* file). Write
  every patch as a list of `(tag, old, new)` and pre-check `text.count(old) == 1` for all of
  them **before** any write, aborting on the first mismatch — a partial application leaves a
  file that parses but behaves differently from what was intended. Mutating by unique
  substring rather than by guessed whitespace removes the indent class of failure entirely.
- **A count quoted from memory contradicts the list sitting in the file.** `len(CHECKS)` was
  12 while "13 checks" was reported twice, and a README bullet said "all four" files were wired
  into the report when nine were. Have the tool print its own counts, and derive expected
  values from the source (AST, `len()`) rather than restating them in prose. The same applies
  to a *format* restated in documentation: changing a summary line from `checks run:` to
  `checks listed: | run: | skipped:` left two READMEs quoting a string the tool no longer
  emits, so a reader following them would conclude the tool was broken. Where a document must
  show that line, build the quoted text by reading the format string out of the source at patch
  time instead of typing it, and prefer describing the shape over the value.
- **XML from text-extraction tools is often not well-formed.** `ElementTree` dies
  on stray bytes; fall back to plain text extraction plus token positions.
- **A working directory you deleted kills every later terminal call with a misleading error.**
  When the session's cwd was a temp directory that an earlier cleanup removed, each command dies
  at the implicit `cd` with exit 126 and a hint that the target "is not executable" — the real
  command never ran, and the hint names the wrong cause. Pass an explicit `workdir` that exists,
  or `cd` to a known-good path first; do not start debugging the reported command.
- **Deleting a file that a manifest pins is a two-file edit.** Sealed manifests store `bytes` and
  `sha256` per entry, so removing the file alone leaves a record pointing at something absent.
  Before deleting anything under a manifest, parse the manifest (do not grep it — cutting JSON on
  commas hides the hash field) and remove the matching entries in the same commit. Check first
  whether the deletion breaks *reproducibility*: a packet-level digest that matches no file in the
  directory, and a reproduce script that never opens the manifest, mean the artefact survives the
  deletion — measure that before assuming the worst.

## Session detail

`references/thesis-audit-2026-08.md` records the concrete false alarms, the exact
oracle commands that disproved them, and the override/regeneration chain used in a
64-source PRISMA thesis audit. Read it when you need a worked example of the oracle
table above.

`references/proving-a-verifier-can-fail.md` is the full mutation-testing procedure for a
checker you wrote yourself: the four false-green classes with their detection, the
separate-file trust-root pattern, deriving expectations from the source AST, and the
mutation-run discipline that keeps "N/N killed" honest.

`references/dedup-to-single-version.md` is the full procedure for reducing a project tree to
one copy of each file: the survey measurements, the duplicate-group classification table,
how to tell a hash-locked protocol version from a stale copy, the byte-reproducibility probe
that decides whether an identical pair is spare or load-bearing, the archive-never-delete
contract for a tree with no git, the manifest-survival fix, the two orphan false positives,
and the generated-status-report pattern. Read it when asked to clean up or deduplicate a
project directory.

`references/derived-dataset-provenance.md` covers auditing a *released* derived
dataset before promising to filter or cite it: the provenance-flattening check,
the sufficiency ladder (has content → has ground truth → traceable to a named
source → filterable by the dimension you need), redistribution-scope fields, and
the substring-inflation retraction from a Vietnamese-language corpus. It also
covers locating a bundle in a cloud archive and copying only the measured
channel, sibling directories whose own manifest declares them out of scope,
licensing a release that is staged but not yet public (manifest scope, per-builder
redaction rules, threshold-metric compliance checks), and inspecting restricted
text by shape without reproducing it.
