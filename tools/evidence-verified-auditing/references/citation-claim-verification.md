# Verifying that a citation supports its claim (not just that it resolves)

Companion to the "identity is not content" rule in `SKILL.md`. This file records
how to actually run the content check, the parser bug that makes it produce mass
false positives, and the structural limit that caps how much of a corpus can be
checked at all.

---

## 1. Three independent layers, three separate denominators

Report them separately, always with the denominator. Passing a cheaper layer
never implies the more expensive one.

| Layer | Question | Oracle | Typical result shape |
|---|---|---|---|
| Toolchain | do all keys resolve? | build log / bibliography log; rendered output searched for `[?]` | `0 unresolved` |
| Identity | does the entry describe the artifact it claims? | authoritative registry by stable ID (Crossref by DOI; DataCite for `10.48550/*` preprints, which Crossref returns 404 for) | `127/127 metadata-verified` |
| Content | does the cited work state what the sentence attributes to it? | the work's own full text / an extraction ledger holding verbatim quotes + locators | `19/19 claim-verified, 388 unverifiable` |

Two identity traps that look like defects and are not:

- **Year mismatch against a registry.** A registry's `created` date is the
  indexing date, not the publication date, and journals publish online-first in
  one year and in print the next. Fetch the granular date parts
  (`published-online`, `published-print`, `issued`, `created`) before calling a
  year wrong; conference papers indexed years late are the common case.
- **No DOI at all.** Books, theses, and older monographs legitimately have none.
  Count them as *not checkable by registry*, not as failures.

---

## 2. The false-positive engine: line-scoped topic inference

The bug that generated ~190 bogus findings in one pass, and the shape it takes in
any language:

A verification script infers what a claim is *about* from the text, then checks
whether each cited work matches that topic. If the topic is inferred from **the
whole source line**, every citation on that line inherits every topic mentioned
anywhere on it. One 1,681-character line held three separate `\cite` groups and
did not contain the topic word at all, yet all 28 keys were flagged as
topic-mismatched.

Rules that remove the class of error:

1. Scope the topic to the **clause immediately preceding the citation marker**,
   not the line, paragraph, or sentence-with-multiple-groups.
2. Split the line on citation markers first, then attribute each group to the
   text segment that ends at it.
3. Never flag a mismatch when the topic token is absent from the scoped segment —
   absence means "not inferable", not "contradicted".
4. Before reporting *any* count, print the funnel: total pairs, dropped by each
   filter, and how many were **actually checked**. A run that reports
   `0 discrepancies` out of 0 checked pairs is not a pass; it is an unexecuted
   check. This funnel is the single most useful diagnostic in the whole script.

---

## 3. Structural limit: multi-key citation groups are unattributable

When a sentence cites four or more works at once, no mechanism can decide which
of them carries which part of the claim — the document simply does not encode it.
In one corpus this covered 388 of 559 (clause, key) pairs, i.e. ~70 %.

Do not paper over it:

- Report it as a **denominator**, not a finding: `7 of 559 pairs checkable;
  388 sit in groups of ≥4 keys`.
- It is a property of the manuscript's citation style, not an error to fix. Say
  so, so nobody spends a session "repairing" it.
- Groups of one to three keys *are* attributable — verify those and report that
  subset honestly.

---

## 4. When a categorical claim and a citation disagree, check for two columns

A sentence of the form "only N sources did X, citing K" can be sound while a
mechanical check screams mismatch, because the dataset holds **two different
fields** that both look like "X":

- a primary/exclusive classification (每 record gets exactly one; the counts sum
  to the corpus size), and
- a crosscutting attribute (a record can carry it while being classified
  elsewhere).

A key can legitimately be the sole member of category X under the primary field
while being counted under a different label by the crosscutting field. Before
declaring the citation wrong:

1. Identify which field the surrounding counts were computed from — check whether
   the neighbouring numbers sum to the corpus total (primary) or not
   (crosscutting).
2. Read the record's verbatim extraction quote. A first-match extraction rule
   frequently captures a term from a *comparison* sentence ("A has an advantage
   over B") and codes the record as B when the work actually implements A. That is
   an extraction bug in the dataset, fixable at the override layer — not a
   citation error in the prose.
3. Fix whichever layer is actually wrong, then make the sentence name the field
   it is counting so the ambiguity cannot recur.

---

## 5. Delegated verification: a batch that stops is not a batch that passed

Fan-out verification is attractive here because the work is embarrassingly
parallel, but children die with the process and report nothing useful:

- A subagent batch can return `interrupted` or `timeout` with **no findings**.
  Treat that as `BLOCKED`, never as "no problems found".
- Before re-dispatching, read the live transcripts — partial tool output in them
  is often enough to recover the mapping work already done.
- Re-dispatch narrower: one file or chapter per child, and instruct each to write
  **one script and run it once**. The timeout in practice came from a child
  looping dozens of exploratory tool calls rather than from the analysis itself.
- If a batch fails twice, do the analysis inline. A single script over the corpus
  finished in under a second once the funnel logic was right.

---

## 6. Reporting template that survives scrutiny

```
Toolchain : 0 unresolved keys        (build log + rendered-output scan)
Identity  : 127/127 verified         (registry by DOI; 9 have no DOI, 2 via DataCite)
            0 author mismatches, 0 title mismatches
            3 year "mismatches" retracted: online-first / late indexing
Content   :  19/19 checked pairs agree
            388 pairs unattributable (citation groups of >=4 keys)
            151 clauses state no checkable attribute
             10 keys unmapped to the evidence ledger
Retracted : ~190 topic mismatches — script inferred topic per line instead of
            per clause preceding each citation marker
```
