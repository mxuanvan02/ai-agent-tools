# Worked example: 64-source PRISMA thesis audit (2026-08)

Concrete record of false alarms, the oracle commands that disproved them, and the
override/regeneration chain. Use as a template for the oracle table in SKILL.md.

## False alarms my own scans produced

### FA-1 — "24 citation keys missing from the bibliography"

**Scan said:** 126 keys cited, 102 in `references.bib`, 24 unresolved.

**Oracle that disproved it:** the build's own diagnostics.

```bash
grep 'undefined' main.log | grep -v 'Font shape'   # -> 0 lines
grep -ci 'cannot find\|error' main.blg             # -> 0
```

If 24 keys were truly missing, the toolchain would have reported 24 errors. It
reported none.

**Parser bug:** my regex only matched `@article{key,` at the start of a line, so it
silently skipped ~25 entries pasted as a single line by a metadata exporter
(`@article{Stricker_2023, title={...}, ...}` all on one line). Correct count after
brace-aware parsing: **127 entries, 126 cited, 0 missing.**

**Lesson:** never derive a "missing X" count from a regex when the toolchain already
computes it authoritatively.

### FA-2 — "5 pairs of entries share a DOI"

**Scan said:** duplicate DOIs across `hillel1998environmental`,
`vanhenten1994greenhouse`, `boyd1994linear`, and others.

**Oracle:** re-parse per entry with brace matching, then group.

```python
# count by real entry boundaries, not by nearest-DOI-on-following-lines
print("duplicate DOIs:", {d: ks for d, ks in by_doi.items() if len(ks) > 1})  # -> {}
```

**Parser bug:** entries without a `doi` field inherited the DOI of the *next*
entry, because the scan associated each key with the following DOI match rather
than one inside its own braces. Reality: **0 duplicate DOIs; 9 books/theses simply
have no DOI.**

### FA-3 — "107 sentences attribute a claim to the wrong author"

**Scan said:** 107 mismatches between an inline author name and the cited entry.

**Oracle:** read the actual matches.

The regex was capturing Vietnamese word fragments (`ất`, `ộ`, `ến`, `ằng`) and
comparing them to surnames. After restricting to real citation-with-name patterns
(`et al.`, `và cộng sự`, `Name (year)`), only **2** sentences name an author, and
both were correct.

**Lesson:** print a sample of matches before counting them. 107 "hits" that all
look like syllable fragments is a signal, not a finding.

### FA-4 — "3 bibliography years are wrong"

**Scan said:** `heinzelman2000energy` (bib 2000 vs registry 2005),
`miskowicz2003event` (2003 vs 2004), `tran2023daklak` (2023 vs 2024).

**Oracle:** Crossref date sub-fields, not the top-level year.

```python
msg = requests.get(f"https://api.crossref.org/works/{doi}").json()["message"]
for k in ("issued", "published-print", "published-online", "created"):
    print(k, msg.get(k, {}).get("date-parts"))
```

- `heinzelman`: `issued=[None]`, `created=[2005,8,24]` → 2005 is the *indexing*
  date; the conference was 2000. Bib correct.
- `miskowicz`: same shape. Bib correct.
- `tran2023daklak`: `published-online=[2023,12,19]`, `published-print=[2024,1,1]`
  → online-first; citing 2023 is conventional. Bib correct.

**Result: 0 real year errors.** Also verify arXiv DOIs via DataCite, not Crossref —
Crossref returns `404` for `10.48550/*`, which looks like a broken DOI.

### FA-5 — "figure wider than the text block"

Visual inspection of a 100 dpi render suggested a diagram overflowed the margin.
Reading the source showed `\resizebox{\textwidth}{!}{...}` — exactly text width.
The apparent overhang was box strokes at low raster resolution. **Confirm geometry
from source or the log's overfull warnings, not from a downscaled screenshot.**

### FA-6 — "3 appendix tables are never referenced"

The tables existed with labels and no `\ref`. Oracle: is the file in the build graph?

```bash
grep -rn 'phuluc_audit' --include='*.tex' . | grep -E '\\(input|include)'   # -> nothing
pdftotext main.pdf - | grep -c 'Luồng PRISMA dùng trong luận văn'           # -> 0
```

The file was never `\include`d, so its labels cannot be dangling references. The
real finding was different and more useful: **an entire appendix is missing from
the document.**

## Real findings that survived verification

| Finding | Oracle that confirmed it |
| --- | --- |
| A route named in prose never appears in the retrieval log | 17 distinct `route` values in the CSV, none matching the named service |
| Prose describes 3 source channels; data has 4 | `source_channel` value counts: `246 / 176 / 137 / 68` (the two middle ones were being summed as one) |
| A citation attributed ETC to a paper implementing STC | full-text quote: *"Self-triggered control (STC) has an advantage over event-triggered control (ETC)…"*, and `c2_trigger=self_triggered` in the coding table |
| Symbol used with two incompatible dimensions | parameter table gave cm/h; the equation required dimensionless |
| Page numbering did not start where the regulation requires | `pdftotext -bbox` folio position per page |

## Numeric verification that passed

All 11 `x/33` fractions recomputed from the corpus CSV rather than read:
`11` irrigation, `12` greenhouse, `8` LoRa, `9` no-network, `9` MPC, `8` fuzzy,
`14` simulation, `13` lab, `21` no-comparator, `3` self-triggered, `1`
event-triggered. Derived sums also checked: `6` field evidence = `3+2+1`, `27`
sim/lab = `14+13`.

Retrieval log claim "174 attempts across 41 sources" verified as 174 data rows and
41 distinct record IDs.

## The override → regenerate chain

Fixing one miscoded record correctly required five steps, not one edit:

```
manual_overrides.json                 <- the ONLY hand-editable layer
  -> apply_overrides.py               -> pnce_fulltext_recode.{json,csv}
                                      -> pnce_recode_locators.csv
  -> build_two_tier_corpus.py         -> two_tier_corpus.csv
  -> regen_ch3_figures_tier1.py       -> figures/ch03/*.pdf
  -> manuscript prose + tables        (hand-edited last)
```

1. **Read the schema first.** `SCHEMA.md` already listed a legal value
   (`STC_self_triggered`) — no new enum needed. Match the existing override format,
   including a `rule_error` explanation and a verbatim `quote` + `locator`.
2. **Check for a precedent.** An existing override recorded the identical failure
   mode: *"First-match rule picked 'optimal control' from a related-work sentence
   describing another paper, not the method of this paper."* Same trap, different
   record — a keyword appearing in a comparison sentence.
3. **Prove idempotency** — two full runs gave the same hash (`9c5d1bf6b66d4b53`).
4. **Fix the downstream KeyError.** The plotting script hard-coded the old value in
   `CTRL_ORDER`/`CTRL_LABEL` and died with `KeyError: 'STC_self_triggered'`. Added
   the new value as an alias so both old and new data plot.
5. **Regenerate and verify the figures.** The script wrote to a different directory
   than expected (`ROOT = parent.parent`); locate output by mtime rather than
   assuming, then confirm the new label appears in the extracted figure text and the
   matrix still totals the denominator.

## Frozen-file handling

The introduction section was declared locked mid-session, *after* I had already
edited it. There was no VCS and no pre-existing backup of my edited version.

Recovery: the user supplied the pristine file; I backed up my modified copy, wrote
the pristine content, and verified byte equality on every subsequent report.

```bash
cmp -s Chapter/modau.tex /path/to/original/modau.tex && echo IDENTICAL || echo MODIFIED
grep -c '\\rev{' Chapter/modau.tex   # expected 0 for the original
```

The restored file cited a key absent from the bibliography. Since the file could
not be edited, the fix went into the bibliography as an alias:

```bibtex
@article{zhang2013network,
  ids = {zhang2019networked},   % alias so the locked file's key resolves
  ...
}
```

Crossref confirmed both keys denote the same DOI before aliasing. One entry, two
resolvable keys, no duplicate in the printed list.

Also a **role** constraint, not just a text constraint: the section is a proposal
document and must not report result numbers at all. Correcting `41` to `40` would
still have violated it — the numbers belong in the results chapters, referenced by
cross-reference.

## Incident: interrupted build

A gateway restart killed a build between `latexmk -C` and the first pass. Result:
`main.pdf` gone and `noidung_chap1.aux` truncated mid-token, producing

```
Runaway argument?
{\contentsline {figure}{\numberline {1.4}{\ignorespaces ...
! File ended while scanning use of \@writefile.
```

This reads like a syntax error in the last edit. It was not. Fix: delete every
intermediate (`.aux .toc .lof .lot .bbl .bcf .run.xml .fls .fdb_latexmk .synctex*`)
and build from clean — exit 0, 136 pages.

## Diagnostic commands worth reusing

```bash
# folio (printed page number) position per page
pdftotext -bbox -f 7 -l 20 main.pdf - | ...   # words with y > 93% of page height, x near centre

# does a global pagestyle override exist? (a common cause of missing page numbers)
grep -rn '\\pagestyle{empty}' --include='*.tex' .   # global — overrides everything after it
grep -rn '\\thispagestyle{empty}' --include='*.tex' .   # single page — harmless

# widest citation label, to decide whether a hanging indent is even geometrically possible
# labels [100]-[127] measured 0.986 cm; forcing a 1 cm indent leaves 0.014 cm clearance
```

The last one settled a "FAIL" that was not one: the style's 1.322 cm indent is the
practical minimum, and `\bibhang` is ignored by that citation style (measured
identical before and after setting it).
