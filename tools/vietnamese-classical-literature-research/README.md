# vietnamese-classical-literature-research

Research skill for **văn học trung đại Việt Nam** (10th–19th century) and the thought
systems the texts presuppose — Nho giáo, Phật giáo, Đạo giáo, `理學`/`心學`, `科舉`.

Field: **văn học** (literature / humanities). This is the repo's first tool in that
field; the classification travels with the skill in its frontmatter
(`metadata.hermes.category: van-hoc`) so an installer that honours categories can
place it under a literature group rather than with the engineering tools.

## What it does

Turns "I want to research X" into an auditable result, by making four things
mechanical instead of memory-based:

1. **Keyword bridges across scripts.** The corpus is bilingual by construction —
   works in chữ Hán, works in chữ Nôm, scholarship in Vietnamese, Chinese, English
   and French. Each concept gets a query set in all three layers, with the
   genre term separated from the title term because they answer different
   questions.
2. **Han character verification.** 155 terms carry a 漢字 that was **matched
   byte-for-byte in a fetched source** during the session that built the table,
   each with its evidence named. Recalled characters are the dangerous failure:
   they look right, and a wrong one returns zero results, which reads as
   "no sources exist".
3. **Source reachability.** 29 sources are classified `curl-ok` / `browser-only` /
   `dns-dead` from measured DNS + HTTP results. The middle class is the point:
   four important catalogues refuse plain `curl` while five commonly cited domains
   no longer resolve. A source list built from memory gets both wrong, in opposite
   directions.
4. **Bounded research rounds** with an evidence ledger, plus four feasibility tests
   for proposing a direction — including the veto that unreachable material
   imposes regardless of how good the question is.

## The measured failures this skill encodes

Not hypothetical. Each was produced during the build and is documented where it
can be checked:

| Failure | Measurement | Where documented |
|---|---|---|
| Recalled Han characters | 3 wrong: `阮輝似`→`阮輝嗣`, `陳文甲`→`陳文玾`, `上京紀事`→`上京記事` | glossary, "Corrections discovered" |
| Frequency heuristic for characters | 5 of 12 wrong (returns the author, a sibling work, a filename) | glossary, final section + `assets` |
| Dead domains cited as sources | 5 of 29 measured DNS-dead | source registry |
| Bot-walled catalogues read as dead | 10 of 29 return 000/403 to curl but work in a browser | source registry |
| Regex over infoboxes for dates | `nhà Lý 1054-1072`, `nhà Hồ 1400-1427`, `nhà Mạc 1594-1677` — all wrong | canon map, caveats |
| Witness date read as composition date | `上京記事` 1885, `雨中隨筆` 1906, `金雲翹新傳` 1902 | canon map, caveats |
| One-request-per-title wiki fetch | 33 of 44 titles came back empty (rate limit) | `verify_han_terms.py` docstring |

## Layout

```
SKILL.md                                 five workflows, boundaries, reference index
assets/verified_terms.json               THE evidence table: 155 terms + 29 sources
references/
  han-nom-keyword-glossary.md            generated — verified Han per term + evidence
  source-corpus-verified.md              generated — registry by layer + reachability
  period-and-canon-map.md                periodisation, canon, the four date kinds
  genre-and-poetics.md                   classification axes, forms, 平仄/對仗/押韻
  thought-frameworks.md                  三教, 理學/心學, 科舉, 文以載道/詩言志
  deep-research-protocol.md              five rounds + ledger + stop conditions
  research-direction-design.md           four feasibility tests, gap typology, scoring
  textual-criticism-caveats.md           known disputes, lost material, date traps
scripts/
  verify_han_terms.py                    check/discover Han candidates against fetched pages
  probe_sources.py                       print or re-measure the source registry
  build_glossary.py                      regenerate the two generated references
  public_hygiene_check.py                repository publication gate
tests/test_skill_integrity.py            25 tests
```

The two largest reference files are **generated from `assets/verified_terms.json`**.
A hand-edited table quietly stops being evidence, so `build_glossary.py --check` is
part of validation and a test fails on drift.

## Scripts

Dependency-free: Python stdlib plus `curl`. No third-party packages, no API keys,
no network access unless you ask for it.

```bash
# print the registry offline (default — no network needed)
python3 scripts/probe_sources.py --layer 1

# re-measure reachability, and fail if the registry is stale
python3 scripts/probe_sources.py --live --check-dead

# verify Han characters for your own term list
python3 scripts/verify_han_terms.py \
  --fetch-vi "Truyền kỳ mạn lục;Nguyễn Dữ" \
  --corpus /tmp/c --terms my_terms.txt --discover
```

`verify_han_terms.py` exits 1 when any candidate is NOT-FOUND, so it can gate a
build. `--discover` prints candidates for a human to read and never auto-accepts
them — that restraint is the lesson from the 5-of-12 measurement.

Terms file format, one per line:

```
label ; han ; gloss
Truyền kỳ mạn lục ; 傳奇漫錄 ; Truyền kỳ mạn lục
```

## Validation

```bash
python3 scripts/build_glossary.py --check
python3 -m unittest discover -s tests -v
python3 scripts/public_hygiene_check.py
python3 -m py_compile scripts/*.py tests/*.py
```

All four pass locally: 25 tests, hygiene gate clean over the tool directory.

The integrity tests enforce the invariants that would otherwise rot silently:
every glossary row carries a Han string, a recognised status, and named evidence;
no URL classified `dns-dead` appears anywhere in prose as a place to go; the
generated files match the assets; and the character checker is proven able to
fail (a deliberately wrong Han string against a fixture corpus must come back
NOT-FOUND, or the verifier is decoration).

## Boundaries

**In scope:** Vietnamese literature 10th–19th century; the Hán-Nôm textual
tradition; the Confucian/Buddhist/Taoist and examination context the texts
presuppose; comparative Việt–Trung genre study; source discovery and verification;
research-direction design.

**Out of scope:** post-1900 quốc ngữ literature except as reception history of a
classical work; Chinese literature with no Vietnamese connection; chữ Nôm as a
writing system beyond keyword needs; teaching method and curriculum design.

## Related

`academic-prose` (Vietnamese academic writing, de-AI-ing, calque audit — use it
for the writing pass; this skill governs domain content and evidence),
`grounded-citations`, `deep-research`, `evidence-first-research`,
`literature-gap-recon`.

## License

MIT. See `LICENSE`.

The evidence table records which source verified each term. Sources are cited as
public catalogues and publications; no third-party code is vendored and no
upstream licence applies.
