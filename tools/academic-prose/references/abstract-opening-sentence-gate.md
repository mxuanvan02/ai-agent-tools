# The opening sentence gate

Move order is necessary and not sufficient. An abstract can carry every required
move, in the required order, and still open with a sentence the author rejects on
first read — because move order fixes *what information* comes first, not *how
that sentence is built*. A passing move checklist therefore proves nothing about
the first sentence, and answering a first-sentence complaint with "the abstract
has all five moves" is a true statement about a different tier that reads as
refusing the critique.

Gate the first sentence on the source, before the first build:

| Check | Failure it catches |
|---|---|
| The grammatical subject is the entity that actually changes state | `Lúa phát thải thấp ... thành tín chỉ` — the crop does not become a credit; the *reduction* does |
| No content word repeats inside the sentence unless the repeat is the referential point, and then it is marked | `khâu đo lường chiếm 77% chi phí đo đạc`; `mức giảm phát thải của lúa phát thải thấp`; `tín chỉ ... thành tín chỉ` |
| Every percentage carries its denominator in the same sentence | `77% chi phí` — of what? → `77% chi phí MRV` |
| Every causal connective has its middle step present | `chiếm 77% chi phí, nên chưa thành tín chỉ` — cost alone does not block a credit; the missing step is who will not pay it |
| The sentence opens on the study object, not on a definition or a bare cost | `Tín chỉ hình thành khi...` delays the object; `Chi phí chiếm 77%...` opens mid-argument |

A sentence failing any row is **rewritten, not patched**: each patch tends to
break a different row, and checking against the rendered PDF costs a build per
attempt. Run the five rows on the source sentence first.

## Measured cost of skipping the gate

One abstract opening took six build-and-look rounds:

1. `Khâu đo lường chiếm 77% chi phí đo đạc...` — row 2 (circular repeat) and row 4 (no middle step)
2. `Tín chỉ các-bon từ lúa phát thải thấp chỉ hình thành khi...` — row 5 (opens on a definition) and row 2 (`chỉ` twice)
3. `Trên lúa phát thải thấp, tưới khô ướt...` — row 1 (subject is a practice, not the thing that changes state)
4. `Chứng minh ... tốn kém vì...` — row 3 (`chi phí` with no denominator) and register (opens on cost, not object)
5. `Mức giảm phát thải của lúa phát thải thấp...` — row 2 (`phát thải` twice)
6. Final: `Mức giảm khí mê-tan của lúa phát thải thấp chỉ thành tín chỉ các-bon khi được đo đạc, báo cáo, thẩm định (MRV) chứng minh, nhưng 77% chi phí đó nằm ở khâu đo.`

Each round fixed the row the previous round broke. A static pass over the five
rows yields the final form immediately.

## Related Vietnamese-specific traps

- `Mức giảm phát thải của lúa phát thải thấp` — the compound `lúa phát thải thấp`
  is a locked term, so the collision must be resolved on the *other* side:
  `mức giảm khí mê-tan`. Never rename the locked term.
- `khâu đo` vs `đo đạc`: when `đo đạc, báo cáo, thẩm định` is the spelled-out MRV,
  the measurement component is `khâu đo`, not `đo lường` — `đo lường` collides
  with `đo đạc` and creates the circular repeat.
- A percentage whose denominator is a process already named in the same sentence
  can use `chi phí đó` on second mention rather than repeating `MRV`.
