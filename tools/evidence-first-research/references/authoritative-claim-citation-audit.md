# Claim–citation audit using authoritative databases

Use this checklist when a short conference manuscript needs enough citations to support its actual claims without bloating the bibliography.

## 1. Build a claim ledger first

Read the current manuscript, then classify each statement:

1. **External factual claim** — needs a suitable scholarly or standards citation.
2. **Author definition/formalism** — normally does not need a citation.
3. **Internal implementation/result claim** — needs artifact, log, manifest, or retained-run evidence; related work cannot verify it.
4. **Limitation or proposed future design** — may be framed as the authors’ recommendation; cite methodology literature only when presented as a general requirement.

For each external claim, record: exact sentence, intended evidence, current citation, fit (`direct`, `partial`, `mismatch`), and action.

## 2. Verify metadata against canonical sources

Prefer the source closest to the publisher:

- ACL work: ACL Anthology API/page and DOI record.
- IEEE/CVF work: IEEE DOI/Crossref plus CVF Open Access/PDF where available.
- ACM work: ACM DOI/Crossref.
- NeurIPS work: official proceedings page plus Crossref.
- Standards: immutable official standards URL (for example W3C Recommendation).
- General DOI validation: Crossref REST API.
- Identity/disambiguation fallback: OpenAlex; do not let it override a publisher’s accepted-version metadata without explanation.

Verify title, full author order, venue, year, pages/article number, entry type, DOI, and canonical URL. Never invent a DOI. When canonical sources conflict, document the conflict and prefer the accepted paper/PDF for author order and printed pages while retaining the registered DOI.

## 3. Check citation fitness, not only metadata

A correct paper can still be the wrong citation. Common mismatches:

- a benchmark cited as if it were a representation model;
- a mixed human/machine-authored dataset described as entirely program-generated;
- a model paper used to support a stronger claim about OCR information loss than it actually tests;
- a public synthetic artifact cited as evidence for private retained-run counts;
- a provenance standard cited as proof that a particular region alignment is semantically correct.

Rewrite the claim narrowly when the literature supports only part of it.

## 4. Optimize for claim coverage under a page limit

Choose the smallest set that covers distinct argumentative roles, for example:

- task/domain foundation;
- representation family;
- shortcut or leakage risk;
- long-document/multimodal benchmark;
- programmatic or structure-guided generation;
- provenance/data lineage;
- dataset documentation;
- annotation agreement.

Do not add fashionable papers unless a sentence in the manuscript uses them. Remove unused entries rather than forcing superficial citations. Recompute cited keys versus BibTeX keys after every edit.

## 5. Preserve venue formatting

Do not shrink bibliography text below the official template merely to recover a page. First:

1. remove unused or redundant references;
2. consolidate overlapping related-work prose;
3. retain only citations that cover a live claim;
4. shorten fields that the official bibliography style does not require, without corrupting canonical metadata;
5. rebuild using the official bibliography style.

## 6. Artifact-link rule

Test every repository/release URL with an actual HTTP request and, where practical, inspect the rendered repository. A guessed suffix or stale release URL is a blocker. Cite the repository root if it is stable and the exact release link is absent; keep the release/version description accurate.

## 7. Final gates

- clean LaTeX/BibTeX build;
- zero undefined citations/references;
- every cited key exists;
- every BibTeX entry is cited;
- page count remains within the official limit;
- no template-breaking font-size hacks;
- URL readback succeeds;
- clean-room ZIP contains only required source/assets;
- extract ZIP and rebuild independently;
- report page count, ZIP entries, checksum, and claim boundary.

## Evidence boundary

Literature citations establish prior work and general methodological precedent. They do **not** validate the manuscript’s private run, literal model outputs, correctness, grounding, sufficiency, or effectiveness. Those require direct experimental evidence and must be labeled author-reported when they cannot be independently reproduced.