#!/usr/bin/env python3
"""gsh.py — Google Sheets backend cho trợ lý cá nhân của anh Văn.

Tái dùng credential của skill google-workspace (không tự quản lý token).
Mọi hàm ghi đều nhận dry_run=True để xem trước khi ghi thật.
Tab dùng tên ASCII: tasks, events, habits, log, meta.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import os

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py"
)

_GAPI = None


def _gapi():
    global _GAPI
    if _GAPI is None:
        spec = importlib.util.spec_from_file_location("gapi_skill", _SKILL)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _GAPI = mod
    return _GAPI


def sheets():
    return _gapi().build_service("sheets", "v4")


def _rng(tab: str, cell: str = "") -> str:
    return f"'{tab}'!{cell}" if cell else f"'{tab}'"


def create_workbook(title: str, tabs: dict, dry_run: bool = False) -> dict:
    """tabs: {tab_name: [header,...]}. Trả {sheet_id, url, tabs}."""
    body = {
        "properties": {
            "title": title,
            "locale": "vi_VN",
            "timeZone": "Asia/Ho_Chi_Minh",
        },
        "sheets": [
            {
                "properties": {
                    "title": n,
                    "gridProperties": {"rowCount": 1000, "columnCount": max(4, len(h) + 1)},
                }
            }
            for n, h in tabs.items()
        ],
    }
    if dry_run:
        return {"dry_run": True, "title": title, "tabs": {n: list(h) for n, h in tabs.items()}}
    resp = sheets().spreadsheets().create(body=body).execute()
    sid = resp["spreadsheetId"]
    for name, header in tabs.items():
        sheets().spreadsheets().values().update(
            spreadsheetId=sid,
            range=_rng(name, "A1"),
            valueInputOption="RAW",
            body={"values": [header]},
        ).execute()
    return {"sheet_id": sid, "url": resp.get("spreadsheetUrl"), "tabs": list(tabs)}


def _norm(v) -> str:
    """Chuẩn hoá 1 ô để so sánh sau ghi: '5.0' == '5', ' 3 ' == '3'."""
    s = "" if v is None else str(v).strip()
    if not s:
        return ""
    try:
        f = float(s.replace(",", "."))
    except ValueError:
        return s
    return str(int(f)) if f == int(f) else repr(f)


def read_rows(sheet_id: str, tab: str, include_row: bool = False) -> list:
    """Trả list[dict] theo header dòng 1. Dòng rỗng bị bỏ.

    include_row=True: mỗi record có thêm `_row` = số dòng THẬT trên sheet
    (1-based, dòng 1 là header). Dòng rỗng vẫn bị bỏ khỏi kết quả, nhưng
    `_row` của các dòng còn lại vẫn đúng vị trí vật lý.

    Vì sao cần: bản cũ để find_row tự cộng +2 trên danh sách đã lọc dòng
    rỗng. Sau một lần `rm` (ghi rỗng cả dòng) thì mọi find_row phía sau trả
    index nhỏ hơn vị trí thật, và `done` ghi đè sang bản ghi khác.
    """
    resp = (
        sheets()
        .spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=_rng(tab), valueRenderOption="FORMATTED_VALUE")
        .execute()
    )
    rows = resp.get("values") or []
    if not rows:
        return []
    header = [str(c).strip() for c in rows[0]]
    out = []
    for offset, r in enumerate(rows[1:]):
        if not any(str(c).strip() for c in r):
            continue
        rec = {header[i]: (str(r[i]).strip() if i < len(r) else "") for i in range(len(header))}
        if include_row:
            rec["_row"] = offset + 2
        out.append(rec)
    return out


def append_rows(sheet_id: str, tab: str, values: list, dry_run: bool = False) -> dict:
    if dry_run:
        return {"dry_run": True, "tab": tab, "would_append": len(values), "rows": values}
    resp = (
        sheets()
        .spreadsheets()
        .values()
        .append(
            spreadsheetId=sheet_id,
            range=_rng(tab),
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        )
        .execute()
    )
    return {"appended": resp.get("updates", {}).get("updatedRows", 0), "range": resp.get("updates", {}).get("updatedRange")}


def write_cell_row(sheet_id: str, tab: str, row_index: int, values: list, dry_run: bool = False) -> dict:
    """Ghi đè 1 dòng. row_index: 1-based theo sheet (dòng 1 = header)."""
    cell = f"A{row_index}"
    if dry_run:
        return {"dry_run": True, "tab": tab, "row": row_index, "values": values}
    sheets().spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=_rng(tab, cell),
        valueInputOption="RAW",
        body={"values": [values]},
    ).execute()
    return {"updated_row": row_index, "tab": tab}


def find_row(sheet_id: str, tab: str, column: str, value: str):
    """Trả (row_index_vật_lý, record) hoặc (None, None).

    `column` là TÊN CỘT THEO HEADER ('id'), KHÔNG phải chữ cái cột.
    row_index lấy từ `_row` do read_rows gắn, nên vẫn đúng sau khi có dòng
    rỗng nằm giữa (vết của `rm` bản cũ) — đây là chỗ trước đây gây ghi đè
    nhầm bản ghi.
    """
    rows = read_rows(sheet_id, tab, include_row=True)
    if not rows or column not in rows[0]:
        return None, None
    for rec in rows:
        if rec.get(column, "") == value:
            return rec.get("_row"), rec
    return None, None


def write_row_verified(sheet_id: str, tab: str, row_index: int, values: list,
                       dry_run: bool = False) -> dict:
    """Ghi đè 1 dòng rồi ĐỌC LẠI đúng dòng vật lý đó và so từng trường."""
    header = header_of(sheet_id, tab)
    if not header:
        return {"ok": False, "error": f"tab {tab} không có header"}
    if len(values) != len(header):
        return {"ok": False, "error": f"độ dài dòng {len(values)} != header {len(header)} ({tab})"}
    if dry_run:
        return {"dry_run": True, "ok": True, "tab": tab, "row": row_index, "values": values}
    write_cell_row(sheet_id, tab, row_index, values)
    after = read_rows(sheet_id, tab, include_row=True)
    hit = next((r for r in after if r.get("_row") == row_index), None)
    if hit is None:
        return {"ok": False, "tab": tab, "row": row_index,
                "error": f"read-back không thấy dòng {row_index} trong {tab}"}
    diffs = {}
    for i, h in enumerate(header):
        if _norm(values[i]) != _norm(hit.get(h, "")):
            diffs[h] = {"wrote": values[i], "read": hit.get(h, "")}
    return {"ok": not diffs, "tab": tab, "row": row_index, "verified": not diffs,
            **({} if not diffs else {"diffs": diffs, "error": "read-back lệch"})}


def append_rows_verified(sheet_id: str, tab: str, values: list, dry_run: bool = False,
                         id_col: str = "id") -> dict:
    """Append rồi ĐỌC LẠI và so từng trường của mỗi dòng vừa thêm."""
    header = header_of(sheet_id, tab)
    if not header:
        return {"ok": False, "error": f"tab {tab} không có header"}
    for row in values:
        if len(row) != len(header):
            return {"ok": False, "error": f"độ dài dòng {len(row)} != header {len(header)} ({tab})"}
    if dry_run:
        return {"dry_run": True, "ok": True, "tab": tab, "would_append": len(values), "rows": values}
    res = append_rows(sheet_id, tab, values)
    after = read_rows(sheet_id, tab, include_row=True)
    idx = header.index(id_col) if id_col in header else 0
    verified, missing = [], []
    for row in values:
        key = str(row[idx]).strip()
        hit = next((r for r in after if str(r.get(header[idx], "")).strip() == key), None)
        if hit is None:
            missing.append(key)
            continue
        diffs = {h: {"wrote": row[i], "read": hit.get(h, "")}
                 for i, h in enumerate(header) if _norm(row[i]) != _norm(hit.get(h, ""))}
        verified.append({"key": key, "row": hit.get("_row"), "ok": not diffs, "diffs": diffs})
    ok = not missing and all(v["ok"] for v in verified)
    return {"ok": ok, "tab": tab, "appended": res.get("appended"), "verified": verified,
            "missing": missing, **({} if ok else {"error": "read-back lệch"})}


def delete_row(sheet_id: str, tab: str, row_index: int, dry_run: bool = False) -> dict:
    """Xoá THẬT một dòng bằng deleteDimension — không để lại dòng rỗng.

    Dùng cái này thay cho `rm` kiểu ghi rỗng: ghi rỗng tạo lỗ hổng giữa grid,
    và chính lỗ hổng đó là nguồn của lỗi ghi đè nhầm dòng.
    """
    if dry_run:
        return {"dry_run": True, "tab": tab, "would_delete_row": row_index}
    meta = sheets().spreadsheets().get(spreadsheetId=sheet_id, fields="sheets.properties").execute()
    sid_num = next((s["properties"]["sheetId"] for s in meta.get("sheets", [])
                    if s.get("properties", {}).get("title") == tab), None)
    if sid_num is None:
        return {"ok": False, "error": f"không thấy tab {tab}"}
    sheets().spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": [{"deleteDimension": {"range": {
            "sheetId": sid_num, "dimension": "ROWS",
            "startIndex": row_index - 1, "endIndex": row_index}}}]},
    ).execute()
    after = read_rows(sheet_id, tab, include_row=True)
    return {"ok": True, "tab": tab, "deleted_row": row_index, "rows_after": len(after)}


def header_of(sheet_id: str, tab: str) -> list:
    resp = (
        sheets()
        .spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=_rng(tab, "1:1"))
        .execute()
    )
    rows = resp.get("values") or []
    return [str(c).strip() for c in rows[0]] if rows else []


def today() -> str:
    return dt.date.today().isoformat()


def now_ts() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")
