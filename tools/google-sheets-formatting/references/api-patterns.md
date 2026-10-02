# API patterns — copy-paste shapes that survive HTTP 400

Every shape below was validated against the live Sheets v4 API after at least
one real `400 Request contains an invalid argument`. Field names matter more
than they look.

## 1. Column width / row height (`updateDimensionProperties`)

`sheetId`, `dimension`, `startIndex`, `endIndex` live INSIDE `range`:

```json
{
  "updateDimensionProperties": {
    "range": {"sheetId": 123, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
    "properties": {"pixelSize": 260},
    "fields": "pixelSize"
  }
}
```

Wrong (400): `"sheetId"` / `"dimension"` at the `updateDimensionProperties` level.

## 2. Auto-fit data rows (`autoResizeDimensions`)

Wrapped in `dimensions`; only `startIndex`/`endIndex` exist:

```json
{
  "autoResizeDimensions": {
    "dimensions": {"sheetId": 123, "dimension": "ROWS", "startIndex": 1, "endIndex": 42}
  }
}
```

Wrong (400): `endRowIndex`, or flat fields without the `dimensions` wrapper.

## 3. Header style (`repeatCell`)

```json
{
  "repeatCell": {
    "range": {"sheetId": 123, "startRowIndex": 0, "endRowIndex": 1,
              "startColumnIndex": 0, "endColumnIndex": 8},
    "cell": {"userEnteredFormat": {
      "backgroundColor": {"red": 0.12, "green": 0.22, "blue": 0.39},
      "textFormat": {"bold": true, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 11},
      "wrapStrategy": "WRAP", "verticalAlignment": "MIDDLE", "horizontalAlignment": "CENTER"
    }},
    "fields": "userEnteredFormat(backgroundColor,textFormat,wrapStrategy,verticalAlignment,horizontalAlignment)"
  }
}
```

## 4. Freeze + tab color (`updateSheetProperties`)

```json
{
  "updateSheetProperties": {
    "properties": {
      "sheetId": 123,
      "gridProperties": {"frozenRowCount": 1},
      "tabColorStyle": {"rgbColor": {"red": 0.10, "green": 0.45, "blue": 0.91}}
    },
    "fields": "gridProperties.frozenRowCount,tabColorStyle"
  }
}
```

## 5. Status conditional format (`addConditionalFormatRule`)

```json
{
  "addConditionalFormatRule": {
    "index": 0,
    "rule": {
      "ranges": [{"sheetId": 123, "startRowIndex": 1, "endRowIndex": 42,
                  "startColumnIndex": 3, "endColumnIndex": 4}],
      "booleanRule": {
        "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "✅"}]},
        "format": {"backgroundColor": {"red": 0.85, "green": 0.92, "blue": 0.83}}
      }
    }
  }
}
```

Read-back field mask (note `conditionalFormats` INSIDE `sheets()`, and
`ranges` PLURAL):

```
sheets(properties(sheetId,title,gridProperties(frozenRowCount),tabColorStyle),conditionalFormats(ranges(startRowIndex,endRowIndex,startColumnIndex,endColumnIndex,sheetId),booleanRule(condition(type,values),format(backgroundColor))))
```

The batchUpdate reply for this request can be an empty object — success is
proven only by the read-back rule count.

## 6. Dropdown validation (`setDataValidation`)

```json
{
  "setDataValidation": {
    "range": {"sheetId": 123, "startRowIndex": 1, "endRowIndex": 100,
              "startColumnIndex": 3, "endColumnIndex": 4},
    "rule": {
      "condition": {"type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": "Not started"},
                               {"userEnteredValue": "In progress"},
                               {"userEnteredValue": "Done"},
                               {"userEnteredValue": "Blocked"}]},
      "showCustomUi": true, "strict": true
    }
  }
}
```

## 7. Typed values (`values.batchUpdate`)

Always `USER_ENTERED` when formulas/numbers/dates are involved:

```json
{
  "valueInputOption": "USER_ENTERED",
  "data": [{"range": "'Tracker'!A2:C2", "values": [
    ["=ROW()-1", {"numberValue": 249000,
      "userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "#,##0 \"$\""}}},
     {"userEnteredValue": "2026-10-02",
      "userEnteredFormat": {"numberFormat": {"type": "DATE", "pattern": "dd/mm/yyyy"}}}
  ]}]}
}
```

Note: `values.batchUpdate` cells may be objects with `userEnteredValue` +
`userEnteredFormat` together — the format rides with the value in one write.

Aggregate cells are formulas, never literals:

- Progress: `=COUNTIF(D2:D42,"Done")/COUNTA(D2:D42)` with PERCENT format.
- Totals: `=SUM(B2:B42)`, counts `=COUNTIF(D2:D42,"✅*")`.
- Ordinals: `=ROW()-1`.

## 8. New workbook born formatted (`spreadsheets.create`)

One payload: sheets + properties + the formatting batch together.

```json
{
  "properties": {"title": "Project Control", "locale": "en_US"},
  "sheets": [
    {"properties": {"title": "00 Overview", "sheetId": 1000,
      "gridProperties": {"frozenRowCount": 1},
      "tabColorStyle": {"rgbColor": {"red": 0.10, "green": 0.45, "blue": 0.91}}}},
    {"properties": {"title": "01 Tracker", "sheetId": 2000,
      "gridProperties": {"frozenRowCount": 1},
      "tabColorStyle": {"rgbColor": {"red": 0.20, "green": 0.66, "blue": 0.33}}}}
  ],
  "requests": [ /* column widths, header repeatCell, conditional formats, validations */ ]
}
```

Assign explicit `sheetId`s so every later request (and every `#gid=` link in
the Overview tab's `HYPERLINK` cells) is stable from birth.

## 9. Rendered-screenshot verification (CDP)

1. `Page.navigate` to `https://docs.google.com/spreadsheets/d/<id>/edit#gid=<sheetId>`.
2. Wait ~6 s — the canvas renders asynchronously; capturing earlier yields the
   previous tab or a blank grid.
3. `Page.bringToFront`, then `Page.captureScreenshot` (PNG).
4. Deliver the images to the human; API read-back alone is not visual proof.
