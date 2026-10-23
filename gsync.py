#!/usr/bin/env python3
"""gsync.py — kéo Google Calendar + Gmail vào trợ lý thư ký.

RANH GIỚI BẢO MẬT (không được nới):
  - CHỈ ĐỌC từ Google. Không bao giờ tạo/sửa/xóa sự kiện Calendar.
  - Không bao giờ gửi, trả lời, xóa, archive, hay gắn nhãn mail.
  - Không in nội dung mail (body) ra stdout; chỉ subject + sender + lane.
  - Không cache mail xuống đĩa; chỉ ghi việc cần trả lời vào tab tasks khi có --write.
  - Mọi lệnh ghi Sheet mặc định dry_run=True.

Cách dùng:
  python3 gsync.py cal --days 14 [--write]
  python3 gsync.py mail --max 25 [--query 'is:unread'] [--write] [--json]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

import gsh
import thuky

GA = os.path.expanduser(
    "~/.hermes/skills/productivity/google-workspace/scripts/google_api.py"
)
PY = sys.executable


def _call(args: list, timeout: int = 60):
    """Chạy google_api.py; trả (ok, data_or_msg). Không in stderr thô ra ngoài."""
    try:
        p = subprocess.run([PY, GA] + args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timeout {timeout}s"
    if p.returncode != 0:
        tail = (p.stderr or p.stdout or "").strip().splitlines()
        hint = tail[-1][:200] if tail else f"exit {p.returncode}"
        # không rò token/secret: chỉ giữ phần lỗi HTTP
        return False, hint
    try:
        return True, json.loads(p.stdout) if p.stdout.strip() else []
    except json.JSONDecodeError as e:
        return False, f"json decode: {e}"


def _gid(prefix: str, raw: str) -> str:
    return prefix + hashlib.sha1(raw.encode()).hexdigest()[:8].upper()


# ── Calendar ────────────────────────────────────────────────────────────────

def cal_pull(days: int = 14, dry_run: bool = True) -> dict:
    """Kéo sự kiện [hôm nay, +days] vào tab events. Dedupe theo id Google."""
    now = dt.datetime.now().astimezone()
    start = now.isoformat()
    end = (now + dt.timedelta(days=days)).isoformat()
    ok, data = _call(["calendar", "list", "--start", start, "--end", end, "--max", "200"])
    if not ok:
        return {"error": f"calendar list: {data}"}

    existing = gsh.read_rows(thuky.sid(), "events")
    seen_ids = {r.get("id", "") for r in existing}
    seen_keys = {(r.get("event", ""), r.get("date", ""), r.get("start", "")) for r in existing}

    header = thuky.EVENT_COLS
    rows, skipped = [], 0
    for e in data if isinstance(data, list) else []:
        # cấu trúc thật: event dict từ google_api.py (đã normalize)
        title = str(e.get("summary") or e.get("title") or e.get("event") or "(không tên)").strip()
        st = e.get("start") or {}
        en = e.get("end") or {}
        s_raw = st.get("dateTime") or st.get("date") if isinstance(st, dict) else str(st)
        e_raw = en.get("dateTime") or en.get("date") if isinstance(en, dict) else str(en)
        s_raw = s_raw or str(e.get("start", ""))
        e_raw = e_raw or str(e.get("end", ""))
        date_s, start_s = _split_dt(s_raw)
        _, end_s = _split_dt(e_raw)
        eid = _gid("G", str(e.get("id") or f"{title}|{s_raw}"))
        if eid in seen_ids or (title, date_s, start_s) in seen_keys:
            skipped += 1
            continue
        loc = e.get("location") or ""
        if isinstance(loc, dict):
            loc = loc.get("displayName", "")
        rows.append([eid, title[:120], date_s, start_s, end_s, str(loc)[:80], "gcal",
                     "đồng bộ từ Google Calendar"])

    if not rows:
        return {"new": 0, "skipped_duplicate": skipped, "window_days": days,
                "fetched": len(data) if isinstance(data, list) else 0,
                "note": "không có sự kiện mới trong cửa sổ này"}
    r = gsh.append_rows(thuky.sid(), "events", rows, dry_run=dry_run)
    return {"new": len(rows), "skipped_duplicate": skipped, "dry_run": dry_run,
            "window_days": days, "fetched": len(data) if isinstance(data, list) else 0,
            "added": [{"id": x[0], "event": x[1], "date": x[2], "start": x[3]} for x in rows],
            "write": r}


def _split_dt(raw: str) -> tuple:
    """'2026-09-29T14:00:00+07:00' -> ('2026-09-29','14:00'); '2026-09-29' -> ('2026-09-29','')."""
    s = str(raw or "").strip()
    if not s:
        return "", ""
    if "T" in s:
        d, t = s.split("T", 1)
        return d, t[:5]
    return s[:10], ""


# ── Gmail ───────────────────────────────────────────────────────────────────

def mail_scan(max_msgs: int = 25, query: str = "is:unread", write: bool = False) -> dict:
    """Lấy mail (search, KHÔNG đọc body) -> `jev mail` phân luồng -> báo cáo.
    write=True: chỉ các mail needs_reply mới được tạo task (category=mail)."""
    ok, data = _call(["gmail", "search", query, "--max", str(max_msgs)])
    if not ok:
        return {"error": f"gmail search: {data}"}
    msgs = data if isinstance(data, list) else []
    if not msgs:
        return {"fetched": 0, "note": f"không có mail khớp '{query}'"}

    # CHỈ dùng snippet (không tải body) — giảm rò nội dung riêng tư
    payload = {"messages": [
        {
            "subject": str(m.get("subject", ""))[:300],
            "content": str(m.get("snippet", ""))[:800],
            "sender": str(m.get("from", ""))[:200],
            "headers": {},
        }
        for m in msgs
    ]}
    res = _jev_mail(payload)
    if res is None:
        return {"fetched": len(msgs), "error": "jev mail không khả dụng — không phân luồng (fail-closed với mail: không đoán)"}

    lanes = []
    out_msgs = res.get("messages") or []
    for i, r in enumerate(out_msgs):
        src = msgs[i] if i < len(msgs) else {}
        lanes.append({
            "lane": r.get("lane"),
            "confidence": r.get("confidence"),
            "reason": r.get("reason", ""),
            "subject": str(src.get("subject", ""))[:90],
            "from": str(src.get("from", ""))[:60],
            "date": src.get("date", ""),
            "id": str(src.get("id", "")),
        })

    summary = res.get("summary") or {}
    out = {
        "fetched": len(msgs),
        "query": query,
        "lanes": summary.get("lanes"),
        "p50_latency_ms": (summary.get("latency_ms") or {}).get("p50"),
        "messages": lanes,
        "boundary": "chỉ đọc + phân loại; không xóa/gửi/trả lời/gắn nhãn mail",
    }

    # write: chỉ needs_reply -> task mới, dedupe theo gmail id trong notes
    need = [m for m in lanes if m["lane"] == "needs_reply"]
    out["needs_reply_count"] = len(need)
    if write and need:
        existing = gsh.read_rows(thuky.sid(), "tasks")
        seen = " ".join(r.get("notes", "") for r in existing)
        new_rows, dup = [], 0
        for m in need:
            tag = f"mail:{m['id']}"
            if tag in seen:
                dup += 1
                continue
            tid = thuky._next_id(existing + [{"id": r[0]} for r in new_rows], "T")
            new_rows.append([tid, f"Trả lời mail: {m['subject'][:60]}", "mail", "",
                             "3", "0.5", "todo", f"{tag} | from {m['from']}", gsh.now_ts(), ""])
        if new_rows:
            out["tasks_written"] = gsh.append_rows(thuky.sid(), "tasks", new_rows, dry_run=not write)
            out["tasks_created"] = [{"id": r[0], "task": r[1]} for r in new_rows]
        out["tasks_skipped_duplicate"] = dup
    elif need:
        out["tasks_would_create"] = len(need)
        out["hint"] = "chạy lại với --write để tạo task cho các mail cần trả lời"
    return out


def _jev_mail(payload: dict, timeout: int = 90):
    try:
        p = subprocess.run(["jev", "mail"], input=json.dumps(payload, ensure_ascii=False),
                           capture_output=True, text=True, timeout=timeout)
        if p.returncode != 0:
            return None
        return json.loads(p.stdout)
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Đồng bộ Google Calendar/Gmail vào trợ lý thư ký (chỉ đọc)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("cal", help="kéo sự kiện Calendar vào tab events")
    p.add_argument("--days", type=int, default=14)
    p.add_argument("--write", action="store_true", help="ghi thật (mặc định dry-run)")
    p.set_defaults(fn=lambda a: print(json.dumps(cal_pull(a.days, dry_run=not a.write), ensure_ascii=False, indent=1)))

    p = sub.add_parser("mail", help="quét mail + phân luồng bằng jev mail")
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--query", default="is:unread")
    p.add_argument("--write", action="store_true", help="tạo task cho mail needs_reply")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_mail_cmd)

    a = ap.parse_args()
    a.fn(a)


def _mail_cmd(a) -> None:
    r = mail_scan(a.max, a.query, write=a.write)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return
    if r.get("error"):
        print("LỖI:", r["error"])
        sys.exit(1)
    print(f"Mail quét: {r.get('fetched', 0)} (query: {r.get('query')}) | {r['boundary']}")
    print("Luồng:", json.dumps(r.get("lanes"), ensure_ascii=False))
    for m in r.get("messages", []):
        print(f"  {str(m['lane']):<12} conf {m['confidence']:.2f} | {m['subject'][:50]:<50} | {m['from'][:30]}")
    if r.get("needs_reply_count"):
        note = r.get("hint") or ("đã tạo task" if a.write else "")
        print(f"Cần trả lời: {r['needs_reply_count']} — {note}")
    else:
        print("Không có mail nào cần trả lời.")


if __name__ == "__main__":
    main()
