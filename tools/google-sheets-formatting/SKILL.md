---
name: google-sheets-formatting
description: "Use when creating or formatting a Google Sheet through the Sheets API: professional formatting from the first write, correct data types and real formulas, and two-layer read-back verification (API properties plus rendered screenshots)."
metadata:
  version: "1.0.0"
  license: "MIT"
  status: active
  default_on: false
  related: "evidence-verified-auditing; system-one-work-loop"
---

# Google Sheets — Professional Formatting via API

> Google Sheets renders its grid on a **canvas**: UI-driving agents (computer-use
> loops, DOM clickers) cannot see or verify cells. The reliable path is the Sheets
> API — deterministic, reviewable, and reversible. This skill is the discipline
> for making a sheet professional **from the first write**, not "create raw,
> beautify later".

## When this applies

- Creating a new workbook that must look presentable immediately.
- Reformatting an existing sheet (status trackers, price lists, project plans).
- Any sheet work where a human will review the result visually afterwards.

## Toolchain

- Use the official `google-api-python-client` (Sheets v4 + Drive v3). It needs
  Python ≥ 3.10 for modern type syntax in wrapper scripts.
- OAuth: user-level token with the `spreadsheets` and `drive` scopes. On
  `invalid_grant` (expired/revoked), re-run the consent flow; an authorization
  code is single-use and expires in ~10 minutes. If the exchange prints nothing
  and the check still fails, retry the exchange exactly once before regenerating
  the auth URL.
- Screenshots for visual verification come from a browser you control via CDP:
  navigate to `…/edit#gid=<sheetId>`, wait ~6 s for the canvas to render, then
  `Page.captureScreenshot`.

## Mandatory workflow (no step is optional)

0. **New sheets are born formatted.** Design before calling the API: tab list,
   per-tab column headers, the data type of every column (text / number /
   currency / date / percent / status), which columns get dropdowns, which
   cells are formulas. Then issue ONE `spreadsheets.create()` payload that
   already declares `sheets[].properties.title`, `gridProperties.frozenRowCount`,
   `tabColorStyle`, plus a `requests` batch (column widths, header style,
   conditional formats, data validation). The create response is a finished
   sheet, not a draft.
1. **Back up existing sheets first.** Drive `files().copy()` named
   `BACKUP <title> <timestamp>`. Never edit an original without a copy.
2. **Measure before editing.** Read metadata (tab names, sheetId, frozen rows,
   hidden tabs) and `values().get()` to find the REAL `last_row`/`max_col` —
   the default grid claims 1000 rows and lies. Persist the extents as JSON.
3. **One batchUpdate** for the whole formatting change: fast, atomic, replayable.
4. **Two-layer read-back.** (a) API: re-read properties, `conditionalFormats`,
   and header cell formats. (b) Visual: screenshot the rendered tabs and show
   them to the human. API properties alone are NOT sufficient evidence.

## Standard formatting kit (field-tested)

- Header row: dark navy `#1F3864` background, white bold size-11 text, centered,
  `WRAP`, row height 34 px. Banner title row (row 1 of a landing tab): blue
  `#1A73E8`, size 14, left-aligned, 40 px.
- Body cells: size 10, `WRAP`, `verticalAlignment: TOP`; finish with
  `autoResizeDimensions` on the data rows.
- Freeze exactly the real header rows (`gridProperties.frozenRowCount`) — a tab
  with a banner + header on row 4 freezes 4, not 1.
- One distinct `tabColorStyle` per tab (blue / green / yellow / red / purple) so
  a multi-tab workbook is navigable at a glance.
- Column widths by content: ordinal ~46 px, names ~150–260 px, notes/evidence
  ~280–300 px.
- Status colors as conditional formats (`TEXT_CONTAINS` on the status emoji or
  `TEXT_EQ` on status words):
  - ✅ `#D9EAD3` · 🟢 `#E6F4EA` · 🟡 `#FFF2CC` · 🟠 `#FCE5CD` · ⚪ `#F3F3F3` · ❌ `#F4CCCC`
  - Word statuses: Done / In progress / In review / Blocked / Not started.
- Emphasis patterns: recommended row highlighted `#FFF2CC`; superseded blocks
  turned italic gray `#999999` (never deleted); columns awaiting a human
  decision tinted `#FFF9E6`.
- **Never clobber pre-existing conditional formats.** Read back the total rule
  count; old rules must still be there after your batch.

## Correct data types and real formulas

- Write numbers as numbers (`userEnteredValue` numeric) with
  `userEnteredFormat.numberFormat`: currency `{"type":"NUMBER","pattern":"#,##0 \"$\""}`
  (adapt the symbol/locale), percent `{"type":"PERCENT","pattern":"0%"}`, date
  `{"type":"DATE","pattern":"dd/mm/yyyy"}` with ISO input values. Never store
  `"99K"` as text.
- Status/category columns get `setDataValidation` (`ONE_OF_LIST`,
  `showCustomUi: true`) — dropdowns, not free text.
- Summary cells must be real functions: `=COUNTIF(...)`, `=COUNTA(...)`,
  `=SUM(...)`; progress as `=COUNTIF(range,done)/COUNTA(range)` with PERCENT
  format. No hardcoded aggregates.
- Ordinal columns: `=ROW()-n` so numbering survives inserts/deletes.
- Always `valueInputOption: "USER_ENTERED"` when any value is a formula,
  number, or date.
- Multi-tab workbooks get an Overview tab: banner + last-updated date +
  `=HYPERLINK("#gid=…",…)` links to every tab + progress cells that COUNTIF
  the detail tabs.

## batchUpdate API traps (each one caused a real HTTP 400)

- `updateDimensionProperties`: `sheetId`/`dimension`/`startIndex`/`endIndex`
  live INSIDE `range`, not at request level. `properties: {pixelSize}`,
  `fields: "pixelSize"`.
- `autoResizeDimensions`: wrap as `{"dimensions": {...}}` and use
  `startIndex`/`endIndex` — there is no `endRowIndex`.
- Reading conditional formats back: the field mask is
  `sheets(properties(...),conditionalFormats(ranges(...),booleanRule(condition(type,values),format(backgroundColor))))`
  — `conditionalFormats` lives INSIDE `sheets()`, and the range field is
  `ranges` (plural).
- Field masks are unforgiving: one wrong path fails the whole request with 400.
  When in doubt, drop the mask and read the full response.
- The batchUpdate reply count does NOT prove conditional rules were created
  (`addConditionalFormatRule` replies can be empty) — read back and count
  `conditionalFormats`.
- After CDP navigation a sheet needs ~6 s before `captureScreenshot` shows the
  new tab; snapshot/ref identifiers expire between commands if the window
  changes — always retry with a fresh state read.

## Verification checklist

1. Backup copy exists (new sheet) — Drive file id recorded.
2. `frozenRowCount` per tab equals the designed value.
3. Total conditional-format rules ≥ old count + new rules; old rules intact.
4. Header cell read-back: bold=true, background = the palette navy.
5. Dropdown validation present on every status column.
6. Every aggregate cell contains a formula, not a literal.
7. Rendered screenshots of each visible tab delivered to the human.
