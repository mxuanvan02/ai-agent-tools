# Building a verified source bank (never write an unverified citation)

When you are asked to turn a supplied document, a set of notes, or your own
recollection into durable reference material — a knowledge bank, a methodology
guide, a reading list, a `references/` file another agent will trust — the
citations you write become long-lived assertions. This file records the loop that
keeps them honest.

Companion to rule 2 in `SKILL.md` (identity vs content). That rule is about
checking citations someone else wrote; this one is about not creating bad ones.

---

## 1. The failure mode this prevents

A supplied document arrives with a strong body of prose and a thin bibliography.
The prose names authoritative-sounding frameworks; the reference list contains
only generic style guides. The temptation is to attach plausible author names to
each framework so the output "has sources".

That is fabrication, even when the guess is correct. A future agent cannot tell a
verified citation from a confident one, so a single invented reference poisons the
whole file.

Symptoms worth flagging in a supplied document before you build on it:

- a body section that carries the document's main contribution and has **zero**
  citations;
- a source named in running text but absent from the reference list;
- a reference list whose entries are all about *how to write* rather than about
  the subject matter being asserted.

Report those gaps to the user rather than silently repairing them.

---

## 2. The verification loop

Two passes. Do not skip the second.

**Pass 1 — search by concept, collect candidates.** Query a bibliographic API by
topic phrase, not by a guessed title. Collect several candidates per concept and
keep the returned metadata.

**Pass 2 — confirm each candidate by its stable ID.** Re-fetch by DOI and check
that author, year, container, and type match what you are about to write. A hit
in a search result is not confirmation; the search endpoint returns fuzzy matches
and near-title collisions freely.

```bash
# pass 1: concept -> candidates
curl -s 'https://api.crossref.org/works?rows=3&query.bibliographic=<concept+phrase>'

# pass 2: DOI -> authoritative record (the one that decides)
curl -s 'https://api.crossref.org/works/<doi>'
```

Print an explicit `OK / FAIL` line per DOI and a final `n/total` count. Write only
the `OK` rows into the reference file. If a concept survives pass 1 but no
candidate confirms in pass 2, the concept goes in **without** a citation, marked
as unsourced — it does not get the nearest plausible DOI.

Registry notes that save a wasted retry:

- Crossref returns `404` for many `10.48550/*` preprint DOIs; resolve those
  against DataCite instead.
- Books, monographs, and older works legitimately have no DOI. Record them as
  *not registry-checkable*, not as failures.
- A registry's `created` date is an indexing date. Use the granular date parts
  before asserting a year (see `citation-claim-verification.md` §1).

---

## 3. State the verification status inside the artifact

Every reference file you generate should carry a short section saying how its
sources were checked, so the next reader does not have to trust the file's tone:

```markdown
## Verification status of this file

Every DOI below was confirmed against Crossref (or DataCite for arXiv DOIs)
by fetching the record and matching author, year, and container: n/n OK.
Items without a DOI are marked as not registry-checkable.
Concepts listed without a citation are unsourced by design — no source was
confirmed for them.
```

This is the difference between a reference bank and a plausible-looking list.

---

## 4. Structure a knowledge bank as a decision procedure

A verified list of sources is necessary but not sufficient. Reference banks get
used when an agent must *choose*, so organise by the choice being made rather than
alphabetically:

1. **Selector first.** Lead with the question that picks a branch (what kind of
   evidence does this work rest on? what is the artifact type?).
2. **One branch per distinct logic**, each naming its own governing standard or
   source.
3. **Invariants that hold across all branches**, stated once at the end.
4. **A short list of failure modes**, phrased as the mistaken behaviour, not as
   abstract advice.

Test the result by asking whether a reader who knows nothing about the domain can
land in the right branch from the selector alone. If they need the prose to
disambiguate, the selector is wrong.

---

## 5. Reporting shape

```
Sources verified : 23/23 by DOI (Crossref; arXiv DOIs via DataCite)
Not checkable    : 2 (monographs, no DOI) — recorded as such
Unsourced        : 1 concept retained without citation, marked in file
Refused          : did not attach guessed authors to the N frameworks the
                   supplied document left uncited; reported the gap instead
```

Never report a source count without saying which registry confirmed it.
