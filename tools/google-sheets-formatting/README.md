# google-sheets-formatting

Create and format **Google Sheets** through the Sheets API so the result is
professional *from the first write* — correct data types, real formulas,
dropdown validation, frozen headers, status colors — verified by a two-layer
read-back (API properties **and** rendered screenshots).

Google Sheets draws its grid on a canvas, so UI-driving agents cannot see or
verify cells; the API path is deterministic, reviewable, and reversible. This
package is the discipline for that path.

| Trap | Reality | Symptom if ignored |
|---|---|---|
| "Create raw, beautify later" | One `spreadsheets.create()` can carry the full formatting batch | Two-phase work leaves a window where the sheet is shared ugly |
| Default grid size | `rowCount: 1000` is a placeholder | Formats 960 empty rows; extents must be measured from values |
| Reply count = success | `addConditionalFormatRule` replies can be empty | "Applied" rules that do not exist; read back and count |
| Field masks | One wrong path fails the entire request (400) | Whole batch rejected; drop the mask when unsure |

## Contents

- [`SKILL.md`](SKILL.md) — the mandatory workflow (design → backup → measure →
  one batchUpdate → two-layer read-back), the standard formatting kit, data
  type/formula rules, and every batchUpdate schema trap with its fix.
- [`references/api-patterns.md`](references/api-patterns.md) — copy-paste JSON
  shapes for the requests that fail most often (dimension properties,
  auto-resize, conditional formats, data validation, number formats).
- [`scripts/public_hygiene_check.py`](scripts/public_hygiene_check.py) — the
  repository's shared release gate.

## Quick start

1. Design tabs, column types, dropdowns, and formula cells **before** any API call.
2. Existing sheet? Copy it to `BACKUP <title> <timestamp>` via Drive first.
3. Measure real extents with `values().get()`.
4. Issue one `batchUpdate` (create-time `requests` for new sheets).
5. Read back properties + `conditionalFormats`; screenshot every visible tab
   via CDP and show the human.

## Validation

```bash
python3 tools/google-sheets-formatting/scripts/public_hygiene_check.py
python3 -m py_compile tools/google-sheets-formatting/scripts/*.py
```
