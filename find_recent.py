#!/usr/bin/env python3
"""find_recent.py — tìm Google Sheet anh MỚI TẠO gần đây (theo createdTime),
vì sheet 'việc cần làm' có thể tên không khớp keyword. CHỈ đọc metadata."""
import datetime as dt
import importlib.util
import os

_SKILL = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
spec = importlib.util.spec_from_file_location("gapi", _SKILL)
gapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gapi)
drive = gapi.build_service("drive", "v3")

sheets = []
page_token = None
while True:
    resp = drive.files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
        fields="nextPageToken, files(id, name, createdTime, modifiedTime, webViewLink)",
        pageSize=300, pageToken=page_token,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    sheets.extend(resp.get("files", []))
    page_token = resp.get("nextPageToken")
    if not page_token:
        break

now = dt.datetime.now(dt.timezone.utc)


def parse(t):
    return dt.datetime.fromisoformat(t.replace("Z", "+00:00"))


# sheet tạo trong 14 ngày qua
recent = []
for s in sheets:
    try:
        age_days = (now - parse(s["createdTime"])).total_seconds() / 86400
    except Exception:
        continue
    if age_days <= 14:
        recent.append((age_days, s))

recent.sort(key=lambda x: x[0])
print(f"tổng {len(sheets)} sheet | tạo trong 14 ngày qua: {len(recent)}\n")
print("=== sheet MỚI TẠO (<=14 ngày), mới nhất trước ===")
for age, s in recent:
    print(f"  {age:4.1f} ngày trước | tạo {s['createdTime'][:10]} | sửa {s['modifiedTime'][:10]}")
    print(f"      {s['name'][:55]}")
    print(f"      id={s['id']}")

# thêm: mọi sheet tên có 'việc'/'cần'/'làm'/'todo' (kể cả cũ) — phòng anh tạo lâu rồi
print("\n=== sheet tên gợi ý 'việc cần làm' (mọi thời điểm) ===")
KW = ["việc", "viec", "cần làm", "can lam", "todo", "to-do", "to do", "task", "công việc",
      "list", "danh sách việc", "note", "nhắc", "nhac"]
seen = set()
for s in sorted(sheets, key=lambda x: x.get("modifiedTime", ""), reverse=True):
    n = s["name"].lower()
    if any(k in n for k in KW) and s["id"] not in seen:
        seen.add(s["id"])
        print(f"  sửa {s['modifiedTime'][:10]} | {s['name'][:50]:<50} | {s['id']}")
