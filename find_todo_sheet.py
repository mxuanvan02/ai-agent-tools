#!/usr/bin/env python3
"""find_todo_sheet.py — tìm Google Sheet 'việc cần làm' của anh trên Drive.

Liệt kê mọi spreadsheet (mimeType google-apps.spreadsheet), in tên + id + ngày sửa,
rồi đánh dấu những cái khớp từ khoá TODO/việc/công việc/task...
Không in nội dung, chỉ metadata. Phân trang để không sót.
"""
import importlib.util
import os
import re

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
spec = importlib.util.spec_from_file_location("gapi", _SKILL)
gapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gapi)

drive = gapi.build_service("drive", "v3")

KEYWORDS = [
    "việc", "viec", "cần làm", "can lam", "todo", "to do", "to-do", "task",
    "công việc", "cong viec", "note", "ghi chú", "lich", "lịch", "schedule",
    "kế hoạch", "ke hoach", "plan", "deadline", "hạn", "daily", "ngày",
    "week", "tuần", "thuky", "thư ký", "assistant", "hermes",
]

sheets = []
page_token = None
while True:
    resp = drive.files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
        fields="nextPageToken, files(id, name, modifiedTime, owners(emailAddress), webViewLink)",
        pageSize=300, pageToken=page_token,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    sheets.extend(resp.get("files", []))
    page_token = resp.get("nextPageToken")
    if not page_token:
        break

print(f"tổng số Google Sheet trong Drive: {len(sheets)}\n")

def score(name):
    n = name.lower()
    hit = [k for k in KEYWORDS if k.lower() in n]
    return hit

ranked = []
for s in sheets:
    ranked.append((len(score(s["name"])), s))
ranked.sort(key=lambda x: (-x[0], x[1].get("modifiedTime", "")), reverse=False)
ranked.sort(key=lambda x: x[1].get("modifiedTime", ""), reverse=True)  # mới sửa trước
ranked.sort(key=lambda x: -x[0])  # rồi khớp nhiều keyword trước

print("=== TOP khớp từ khoá 'việc cần làm' (khớp nhiều + mới sửa trước) ===")
shown = 0
for sc, s in ranked:
    if sc == 0:
        continue
    shown += 1
    if shown > 20:
        break
    print(f"[khớp {sc}] {s['name'][:55]}")
    print(f"        id={s['id']} | sửa={s['modifiedTime'][:10]} | {s.get('webViewLink','')[:60]}")

if shown == 0:
    print("(không sheet nào khớp từ khoá — in 25 sheet mới sửa nhất bên dưới)")

print("\n=== 25 sheet MỚI SỬA nhất (phòng khi tên không khớp từ khoá) ===")
for s in sorted(sheets, key=lambda x: x.get("modifiedTime", ""), reverse=True)[:25]:
    tag = f"[kw{len(score(s['name']))}]" if score(s["name"]) else "     "
    print(f"{tag} {s['modifiedTime'][:10]} | {s['name'][:50]:<50} | {s['id']}")
