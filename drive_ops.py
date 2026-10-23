#!/usr/bin/env python3
"""drive_ops.py — thao tác Drive có chuẩn hoá tên + phân loại + verify sau ghi.

Bổ sung phần google_api.py KHÔNG có: đổi tên file, di chuyển file giữa thư mục.
Mọi thao tác ghi đều: (1) ghi, (2) ĐỌC LẠI từ Drive, (3) so khớp, (4) trả ok.

Quy ước tên chuẩn hoá:  {STT:02d}_{LOAI}_{ten-slug}.{ext}
  - bỏ dấu tiếng Việt, chữ thường, khoảng trắng -> '-'
  - LOAI suy từ phần mở rộng: VAN-BAN / BANG-TINH / HINH-ANH / KHAC
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsh

FOLDER_MIME = "application/vnd.google-apps.folder"

TYPE_BY_EXT = {
    ".pdf": "VAN-BAN", ".docx": "VAN-BAN", ".doc": "VAN-BAN", ".txt": "VAN-BAN",
    ".xlsx": "BANG-TINH", ".xls": "BANG-TINH", ".csv": "BANG-TINH",
    ".png": "HINH-ANH", ".jpg": "HINH-ANH", ".jpeg": "HINH-ANH", ".webp": "HINH-ANH",
    ".zip": "KHAC", ".rar": "KHAC",
}


def svc():
    return gsh._gapi().build_service("drive", "v3")


# ── logic thuần (test offline được, không gọi mạng) ─────────────────────────

def slug(text: str) -> str:
    """'Báo cáo tháng 10' -> 'bao-cao-thang-10'."""
    s = unicodedata.normalize("NFD", str(text))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-{2,}", "-", s) or "khong-ten"


def file_type(name: str) -> str:
    ext = Path(name).suffix.lower()
    return TYPE_BY_EXT.get(ext, "KHAC")


def target_name(index: int, name: str) -> str:
    """Tên chuẩn hoá cuối cùng: 01_van-ban_bao-cao-thang-10.pdf"""
    p = Path(name)
    ext = p.suffix.lower()
    loai = file_type(name).lower()
    return f"{index:02d}_{loai}_{slug(p.stem)}{ext}"


def build_plan(files: list) -> list:
    """files: [{id, name, mimeType}]. Trả plan [{id, old_name, new_name, type}]."""
    plan = []
    i = 0
    for f in sorted(files, key=lambda x: x.get("name", "")):
        if f.get("mimeType") == FOLDER_MIME:
            continue
        i += 1
        plan.append({
            "id": f["id"],
            "old_name": f["name"],
            "new_name": target_name(i, f["name"]),
            "type": file_type(f["name"]),
        })
    return plan


# ── thao tác Drive có verify ────────────────────────────────────────────────

def _get(file_id: str, fields: str = "id,name,mimeType,parents,trashed,size") -> dict:
    return svc().files().get(fileId=file_id, fields=fields).execute()


def ensure_folder(name: str, parent: str | None = None) -> dict:
    """Tìm theo tên+parent; chưa có thì tạo. Trả {id, created, verified}."""
    q = (f"name = '{name}' and mimeType = '{FOLDER_MIME}' and trashed = false")
    if parent:
        q += f" and '{parent}' in parents"
    seen = svc().files().list(q=q, fields="files(id,name,parents)", pageSize=10).execute().get("files", [])
    if seen:
        got = _get(seen[0]["id"])
        return {"id": seen[0]["id"], "created": False,
                "verified": got.get("name") == name and not got.get("trashed")}
    body = {"name": name, "mimeType": FOLDER_MIME}
    if parent:
        body["parents"] = [parent]
    made = svc().files().create(body=body, fields="id,name").execute()
    got = _get(made["id"])
    return {"id": made["id"], "created": True,
            "verified": got.get("name") == name and not got.get("trashed")}


def upload(local_path: str, name: str | None = None, parent: str | None = None) -> dict:
    """Upload rồi đọc lại: tên, kích thước, parent phải khớp."""
    from googleapiclient.http import MediaFileUpload
    src = Path(local_path).expanduser()
    if not src.exists():
        return {"ok": False, "error": f"không thấy file {src}"}
    mime = mimetypes.guess_type(str(src))[0] or "application/octet-stream"
    body = {"name": name or src.name}
    if parent:
        body["parents"] = [parent]
    made = svc().files().create(
        body=body, media_body=MediaFileUpload(str(src), mimetype=mime, resumable=False),
        fields="id,name,size",
    ).execute()
    got = _get(made["id"])
    ok = (got.get("name") == body["name"]
          and int(got.get("size") or 0) == src.stat().st_size
          and (not parent or parent in (got.get("parents") or [])))
    return {"ok": ok, "id": made["id"], "name": got.get("name"),
            "size": int(got.get("size") or 0), "local_size": src.stat().st_size,
            "parents": got.get("parents")}


def rename(file_id: str, new_name: str) -> dict:
    """Đổi tên rồi đọc lại, so đúng tên mới."""
    svc().files().update(fileId=file_id, body={"name": new_name}, fields="id,name").execute()
    got = _get(file_id)
    return {"ok": got.get("name") == new_name, "id": file_id,
            "name": got.get("name"), "expected": new_name}


def move(file_id: str, new_parent: str) -> dict:
    """Chuyển thư mục: thêm parent mới, bỏ parent cũ, đọc lại parents."""
    cur = _get(file_id).get("parents") or []
    svc().files().update(
        fileId=file_id, addParents=new_parent,
        removeParents=",".join(cur) if cur else None, fields="id,parents",
    ).execute()
    got = _get(file_id)
    parents = got.get("parents") or []
    return {"ok": parents == [new_parent], "id": file_id, "parents": parents}


def list_children(folder_id: str) -> list:
    out, token = [], None
    while True:
        res = svc().files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id,name,mimeType,size)",
            pageSize=200, pageToken=token,
        ).execute()
        out.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return out


def trash(file_id: str) -> dict:
    """Đưa vào thùng rác (đảo ngược được) rồi đọc lại trạng thái."""
    svc().files().update(fileId=file_id, body={"trashed": True}, fields="id,trashed").execute()
    got = _get(file_id)
    return {"ok": bool(got.get("trashed")), "id": file_id, "trashed": got.get("trashed")}


def apply_plan(folder_id: str, plan: list, dry_run: bool = False) -> dict:
    """Đổi tên + chuyển vào thư mục con theo LOAI. Trả kết quả từng file."""
    results, folders = [], {}
    for item in plan:
        sub = f"{item['type']}"
        if sub not in folders:
            folders[sub] = ensure_folder(sub, parent=folder_id) if not dry_run else {"id": f"dry:{sub}"}
        if dry_run:
            results.append({**item, "ok": True, "dry_run": True})
            continue
        r1 = rename(item["id"], item["new_name"])
        r2 = move(item["id"], folders[sub]["id"])
        results.append({"id": item["id"], "old_name": item["old_name"],
                        "new_name": item["new_name"], "type": item["type"],
                        "rename_ok": r1["ok"], "move_ok": r2["ok"],
                        "ok": r1["ok"] and r2["ok"]})
    return {"ok": all(r["ok"] for r in results), "applied": results,
            "folders": {k: v.get("id") for k, v in folders.items()}}


def verify_layout(folder_id: str, plan: list) -> dict:
    """Đọc lại toàn bộ cây: mỗi file phải nằm trong thư mục LOAI của nó, tên đúng."""
    expected = {p["new_name"]: p["type"] for p in plan}
    found, errors = {}, []
    for child in list_children(folder_id):
        if child.get("mimeType") == FOLDER_MIME:
            for sub in list_children(child["id"]):
                found[sub["name"]] = child["name"]
    for name, loai in expected.items():
        if name not in found:
            errors.append(f"thiếu file {name}")
        elif found[name] != loai:
            errors.append(f"{name} nằm ở {found[name]}, cần {loai}")
    stray = [n for n in found if n not in expected]
    if stray:
        errors.append(f"file lạ ở thư mục con: {stray}")
    return {"ok": not errors, "expected_count": len(expected),
            "found": len(found), "errors": errors}
