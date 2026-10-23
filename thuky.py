#!/usr/bin/env python3
"""thuky.py — trợ lý cá nhân cho anh Văn. Google Sheets là database, Jev ra quyết định.

Nguyên tắc (theo typesafe-ai skill):
  - CODE tính mọi sự thật: ngày còn lại, trễ hạn, tổng effort, sự kiện hôm nay.
  - JEV chỉ chọn/đánh giá trong 1 request duy nhất (~0.3s, ~0.0002 đô).
  - Fail-open: Jev lỗi/thiếu key -> trả về dữ liệu + xếp hạng theo code, KHÔNG chặn.
  - Mọi lệnh ghi có --dry-run.

Cách dùng:
  python3 thuky.py add "Soạn hồ sơ thi GVG" --deadline 2026-10-03 --category chuyen-mon --priority 3 --effort 6
  python3 thuky.py list [--status todo]
  python3 thuky.py done T1
  python3 thuky.py event "Họp tổ chuyên môn" --date 2026-09-29 --start 14:00 --end 16:00
  python3 thuky.py habit "Học tiếng Anh" --target 5
  python3 thuky.py today [--json]        <- "hôm nay làm gì?"
  python3 thuky.py briefing [--json]     <- bản tin sáng (tasks+events+habits+mail)
  python3 thuky.py log T1 45 "đã soạn xong phần 1"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

import gsh

CONFIG = os.path.expanduser("~/.hermes/thuky.json")
DEFAULT_SHEET = "1UwzKmcW1Yb5574y5gR--4RG7w01yNWIEGhdzbPVf1Pc"

TASK_COLS = ["id", "task", "category", "deadline", "priority", "effort_h", "status", "notes", "created", "done_at"]
EVENT_COLS = ["id", "event", "date", "start", "end", "location", "type", "notes"]
HABIT_COLS = ["id", "habit", "target_per_week", "done_this_week", "streak", "notes"]


class ConfigError(RuntimeError):
    """Cấu hình thiếu/hỏng: DỪNG, tuyệt đối không ghi vào sheet mặc định."""


def cfg() -> dict:
    """Đọc config. Thiếu/hỏng -> ConfigError (fail-closed).

    Bản cũ trả {} rồi sid() rơi về DEFAULT_SHEET: chỉ cần ~/.hermes/thuky.json
    hỏng là mọi lệnh ghi VẪN chạy và ghi vào một sheet thật, không cảnh báo.
    Lỗi cấu hình phải dừng, không được đổi đích ghi.
    """
    try:
        with open(CONFIG) as f:
            d = json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"thiếu config {CONFIG} - không ghi khi chưa rõ đích")
    except Exception as e:
        raise ConfigError(f"config {CONFIG} hỏng: {e}")
    if not isinstance(d, dict):
        raise ConfigError(f"config {CONFIG} không phải object JSON")
    return d


def sid() -> str:
    s = os.environ.get("THUKY_SHEET_ID") or cfg().get("sheet_id")
    if not s:
        raise ConfigError("config thiếu sheet_id - không ghi khi chưa rõ đích")
    return s


def save_cfg(d: dict) -> None:
    merged = {**cfg(), **d}
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    json.dump(merged, open(CONFIG, "w"), ensure_ascii=False, indent=1)
    os.chmod(CONFIG, 0o600)


# ── code tính sự thật ────────────────────────────────────────────────────────

def _f(v, cast, default=None):
    try:
        return cast(str(v).strip())
    except Exception:
        return default


def enrich(tasks: list, today: dt.date) -> list:
    """Thêm facts do code tính: days_left, overdue, urgency_code, done."""
    out = []
    for t in tasks:
        d = dict(t)
        done = d.get("status", "").lower() in ("done", "xong", "hoàn thành")
        d["done"] = done
        dl = d.get("deadline", "").strip()
        days = None
        if dl:
            p = _f(dl, dt.date.fromisoformat)
            if p:
                days = (p - today).days
        d["days_left"] = days
        d["overdue"] = bool(days is not None and days < 0 and not done)
        pri = _f(d.get("priority"), float, 1.0) or 1.0
        eff = _f(d.get("effort_h"), float, 1.0) or 1.0
        # điểm khẩn do code tính: ưu tiên cao + hạn gần + effort nhỏ -> làm trước
        urgency = pri * 2.0
        if days is not None and not done:
            if days < 0:
                urgency += 6.0 + min(abs(days), 10) * 0.3
            elif days <= 1:
                urgency += 6.0
            elif days <= 3:
                urgency += 4.0
            elif days <= 7:
                urgency += 2.0
            else:
                urgency += 0.5
        d["urgency_code"] = round(urgency / max(eff, 0.25), 3)
        d["effort_num"] = eff
        out.append(d)
    return out


def open_tasks(tasks: list) -> list:
    return [t for t in tasks if not t["done"]]


def events_on(events: list, day: dt.date) -> list:
    return [e for e in events if e.get("date", "").strip() == day.isoformat()]


def habits_due(habits: list) -> list:
    out = []
    for h in habits:
        tgt = _f(h.get("target_per_week"), float, 0) or 0
        done_w = _f(h.get("done_this_week"), float, 0) or 0
        if tgt > 0 and done_w < tgt:
            out.append({**h, "remaining": round(tgt - done_w, 2), "target": tgt})
    return out


# ── Jev: 1 request, nhiều câu hỏi độc lập ────────────────────────────────────

def jev_ask(state: dict, questions: list, timeout: int = 45) -> dict | None:
    """Gọi `jev ask`. Trả None nếu Jev không khả dụng (fail-open)."""
    payload = json.dumps({"state": state, "questions": questions}, ensure_ascii=False)
    try:
        p = subprocess.run(
            ["jev", "ask"], input=payload, capture_output=True, text=True, timeout=timeout
        )
        if p.returncode != 0:
            return {"_jev_error": f"exit {p.returncode}", "_stderr": (p.stderr or "")[-300:]}
        return json.loads(p.stdout)
    except FileNotFoundError:
        return {"_jev_error": "jev CLI not on PATH"}
    except subprocess.TimeoutExpired:
        return {"_jev_error": f"timeout {timeout}s"}
    except Exception as e:
        return {"_jev_error": str(e)[:200]}


def decide_today(cands: list, ev_today: list, habits: list, today: dt.date) -> dict:
    """Jev chọn việc hôm nay + đánh giá rủi ro hạn. Code vẫn giữ facts."""
    if not cands:
        return {"source": "code", "reason": "không còn việc nào đang mở", "pick": None}

    ids = [c["id"] for c in cands]
    opts = {i: next((f'{c["task"]} | hạn {c.get("deadline") or "không"} '
                     f'({c["days_left"]} ngày) | ưu tiên {c.get("priority") or 1} | '
                     f'{c["effort_num"]}h' for c in cands if c["id"] == i), i) for i in ids}
    opts["none"] = "Không việc nào đáng làm hôm nay (để nghỉ hoặc chờ thông tin)"

    state = {
        "today": today.isoformat(),
        "weekday": today.strftime("%A"),
        "owner": "giáo viên Tin học THPT, đang làm NCS CNTT",
        "events_today": [{"event": e.get("event"), "start": e.get("start"), "end": e.get("end")} for e in ev_today],
        "tasks": [
            {k: c.get(k) for k in ("id", "task", "category", "deadline", "days_left", "overdue",
                                   "priority", "effort_h", "status", "notes", "urgency_code")}
            for c in cands
        ],
        "habits_pending": [{"habit": h.get("habit"), "remaining_this_week": h["remaining"]} for h in habits],
    }
    questions = [
        {
            "id": "pick_today", "type": "choice",
            "instructions": ("Chọn MỘT việc đáng làm nhất hôm nay cho owner. Ưu tiên việc sắp trễ hạn, "
                             "việc bị chặn thì không chọn. Trừ giờ đã bị `events_today` chiếm. "
                             "Nếu không việc nào đáng làm, chọn `none`."),
            "criteria": opts,
        },
        {
            "id": "pick_backup", "type": "choice",
            "instructions": ("Giả sử việc chọn ở `pick_today` KHÔNG làm được (bị chặn hoặc hết giờ). "
                             "Chọn việc thay thế tốt nhất còn lại. Chọn `none` nếu không có."),
            "criteria": opts,
        },
        {
            "id": "deadline_risk", "type": "noul",
            "instructions": ("Trong `tasks`, có việc nào đang mở (status khác done) có nguy cơ TRỄ hạn thật sự "
                             "không? Tính cả effort_h so với days_left còn lại: việc 8 giờ mà còn 6 ngày thì chưa "
                             "nguy, việc 3 giờ mà còn 1 ngày thì nguy. Việc không có deadline thì không tính. "
                             "Trả lời true nếu có ít nhất một việc sẽ trễ hạn khi không bắt đầu ngay, false nếu không."),
        },
        {
            "id": "load_fit", "type": "score",
            "instructions": ("Đánh giá tổng khối lượng việc đang mở so với một ngày làm việc bình thường "
                             "(đã trừ giờ họp/học trong events_today)."),
            "criteria": [
                "Rảnh: có thể nhận thêm việc mới",
                "Vừa đủ: một ngày làm việc bình thường",
                "Nặng: phải bỏ bớt hoặc dời hạn",
                "Quá tải: có việc chắc chắn phải dời, cần nói với người liên quan",
            ],
        },
    ]
    ans = jev_ask(state, questions)
    if not ans or ans.get("_jev_error") or "answers" not in ans:
        ranked = sorted(cands, key=lambda c: -c["urgency_code"])
        return {
            "source": "code-fallback",
            "jev_error": (ans or {}).get("_jev_error"),
            "pick": ranked[0]["id"] if ranked else None,
            "pick_backup": ranked[1]["id"] if len(ranked) > 1 else None,
            "ranked_by_code": [{"id": c["id"], "task": c["task"], "urgency_code": c["urgency_code"]} for c in ranked[:5]],
        }
    a = ans["answers"]
    today_q = a.get("pick_today") or {}
    pick = today_q.get("choice")
    backup_q = a.get("pick_backup") or {}
    backup = backup_q.get("choice")
    # POLICY nằm ở code, không ở model: dự phòng PHẢI khác việc đã chọn.
    # Nếu Jev lặp lại cùng một id (hoặc bỏ trống), lấy argmax còn lại trong
    # chính phân bố xác suất đó -> không tốn thêm request nào.
    backup_reason = "jev"
    if not backup or backup == pick:
        probs = backup_q.get("probabilities") or today_q.get("probabilities") or {}
        alt = [(k, v) for k, v in probs.items() if k not in (pick, "none")]
        backup = max(alt, key=lambda kv: kv[1])[0] if alt else None
        backup_reason = "code-from-probabilities"
    return {
        "source": "jev",
        "pick": pick,
        "pick_confidence": today_q.get("confidence"),
        "pick_probs": today_q.get("probabilities"),
        "pick_backup": backup,
        "pick_backup_reason": backup_reason,
        "deadline_risk": (a.get("deadline_risk") or {}).get("noul"),
        "load_fit": (a.get("load_fit") or {}).get("score"),
        "load_fit_labels": ["rảnh", "vừa đủ", "nặng", "quá tải"],
        "latency_ms": ans.get("latency_ms"),
        "usage": ans.get("usage"),
    }


# ── ghi dữ liệu ──────────────────────────────────────────────────────────────

def _num(v):
    """'3.0' -> '3', '2.5' -> '2.5' (giữ convention cột số của sheet)."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(f)) if f == int(f) else str(f)


def _next_id(rows: list, prefix: str) -> str:
    mx = 0
    for r in rows:
        v = str(r.get("id", "")).strip().upper()
        if v.startswith(prefix):
            n = _f(v[len(prefix):], int, 0) or 0
            mx = max(mx, n)
    return f"{prefix}{mx + 1}"


def add_task(args) -> None:
    rows = gsh.read_rows(sid(), "tasks")
    tid = args.id or _next_id(rows, "T")
    row = [tid, args.task, args.category or "", args.deadline or "", _num(args.priority),
           _num(args.effort), args.status or "todo", args.notes or "", gsh.now_ts(), ""]
    r = gsh.append_rows_verified(sid(), "tasks", [row], dry_run=args.dry_run)
    print(json.dumps({"added": tid, **r}, ensure_ascii=False))
    if not r.get("ok"):
        sys.exit(1)


def add_event(args) -> None:
    rows = gsh.read_rows(sid(), "events")
    eid = args.id or _next_id(rows, "E")
    row = [eid, args.event, args.date, args.start or "", args.end or "",
           args.location or "", args.type or "", args.notes or ""]
    r = gsh.append_rows_verified(sid(), "events", [row], dry_run=args.dry_run)
    print(json.dumps({"added": eid, **r}, ensure_ascii=False))
    if not r.get("ok"):
        sys.exit(1)


def add_habit(args) -> None:
    rows = gsh.read_rows(sid(), "habits")
    hid = args.id or _next_id(rows, "H")
    row = [hid, args.habit, _num(args.target), "0", "0", args.notes or ""]
    r = gsh.append_rows_verified(sid(), "habits", [row], dry_run=args.dry_run)
    print(json.dumps({"added": hid, **r}, ensure_ascii=False))
    if not r.get("ok"):
        sys.exit(1)


def mark_done(args) -> None:
    row_i, rec = gsh.find_row(sid(), "tasks", "id", args.task_id.upper())
    if row_i is None:
        print(json.dumps({"error": f"không tìm thấy task {args.task_id}"}, ensure_ascii=False))
        sys.exit(1)
    header = gsh.header_of(sid(), "tasks")
    vals = [rec.get(c, "") for c in header]
    vals[header.index("status")] = "done"
    vals[header.index("done_at")] = gsh.now_ts()
    r = gsh.write_row_verified(sid(), "tasks", row_i, vals, dry_run=args.dry_run)
    print(json.dumps({"done": args.task_id.upper(), **r}, ensure_ascii=False))
    if not r.get("ok"):
        sys.exit(1)


def add_log(args) -> None:
    row = [gsh.now_ts(), args.task_id.upper(), "work", str(args.minutes), args.note or ""]
    r = gsh.append_rows_verified(sid(), "log", [row], dry_run=args.dry_run, id_col="task_id")
    print(json.dumps({"logged": args.task_id, **r}, ensure_ascii=False))
    if not r.get("ok"):
        sys.exit(1)


def habit_done(args) -> None:
    """Tăng bộ đếm thói quen trong tuần; tự tăng streak khi đạt target."""
    row_i, rec = gsh.find_row(sid(), "habits", "id", args.habit_id.upper())
    if row_i is None:
        print(json.dumps({"error": f"không thấy habit {args.habit_id}"}, ensure_ascii=False))
        sys.exit(1)
    header = gsh.header_of(sid(), "habits")
    vals = [rec.get(c, "") for c in header]
    cur = _f(rec.get("done_this_week"), float, 0) or 0
    new = cur + args.count
    vals[header.index("done_this_week")] = str(new)
    tgt = _f(rec.get("target_per_week"), float, 0) or 0
    streak = _f(rec.get("streak"), float, 0) or 0
    if tgt > 0 and cur < tgt and new >= tgt:
        vals[header.index("streak")] = str(int(streak) + 1)
    r = gsh.write_row_verified(sid(), "habits", row_i, vals, dry_run=args.dry_run)
    print(json.dumps({"habit": args.habit_id.upper(), "done_this_week": new, "target": tgt,
                      "streak": vals[header.index("streak")], **r}, ensure_ascii=False))
    if not r.get("ok"):
        sys.exit(1)


def rm_row(args) -> None:
    """Xoá THẬT 1 dòng bằng deleteDimension.

    Bản cũ ghi rỗng cả dòng. Dòng rỗng vẫn nằm trên grid, nhưng read_rows bỏ
    dòng rỗng, nên find_row cộng +2 lệch -> `done` sau đó ghi đè sang bản ghi
    khác (mất dữ liệu âm thầm). Vẫn in old_data để khôi phục nếu cần.
    """
    tab, key, val = args.tab, "id", args.id.upper()
    row_i, rec = gsh.find_row(sid(), tab, key, val)
    if row_i is None:
        print(json.dumps({"error": f"không thấy {key}={val} trong tab {tab}"}, ensure_ascii=False))
        sys.exit(1)
    r = gsh.delete_row(sid(), tab, row_i, dry_run=args.dry_run)
    print(json.dumps({"deleted_row": row_i, "tab": tab, "old_data": rec, **r}, ensure_ascii=False))
    if not r.get("ok") and not r.get("dry_run"):
        sys.exit(1)


# ── đọc + quyết định ─────────────────────────────────────────────────────────

def snapshot(today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    S = sid()
    tasks = enrich(gsh.read_rows(S, "tasks"), today)
    events = gsh.read_rows(S, "events")
    habits = habits_due(gsh.read_rows(S, "habits"))
    cands = sorted(open_tasks(tasks), key=lambda c: -c["urgency_code"])
    return {
        "today": today.isoformat(),
        "tasks_all": tasks,
        "candidates": cands,
        "events_today": events_on(events, today),
        "habits_pending": habits,
        "overdue": [c for c in cands if c["overdue"]],
        "due_7d": [c for c in cands if c["days_left"] is not None and 0 <= c["days_left"] <= 7],
    }


def cmd_today(args) -> None:
    snap = snapshot()
    decision = decide_today(snap["candidates"], snap["events_today"], snap["habits_pending"],
                            dt.date.fromisoformat(snap["today"]))
    out = {
        "today": snap["today"],
        "decision": decision,
        "facts": {
            "open_tasks": len(snap["candidates"]),
            "overdue": [{"id": c["id"], "task": c["task"], "days_overdue": -c["days_left"]} for c in snap["overdue"]],
            "due_7d": [{"id": c["id"], "task": c["task"], "days_left": c["days_left"], "effort_h": c["effort_num"]}
                       for c in snap["due_7d"]],
            "events_today": [{"event": e.get("event"), "start": e.get("start"), "end": e.get("end")}
                             for e in snap["events_today"]],
            "habits_pending": [{"habit": h.get("habit"), "remaining": h["remaining"]} for h in snap["habits_pending"]],
            "top_by_code": [{"id": c["id"], "task": c["task"], "urgency_code": c["urgency_code"],
                             "deadline": c.get("deadline"), "effort_h": c["effort_num"]}
                            for c in snap["candidates"][:5]],
        },
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    d = decision
    tasks_by_id = {c["id"]: c for c in snap["candidates"]}
    pk = tasks_by_id.get(d.get("pick"))
    bk = tasks_by_id.get(d.get("pick_backup"))
    print(f"HÔM NAY {snap['today']} — {len(snap['candidates'])} việc đang mở | quyết định từ: {d['source']}")
    if pk:
        print(f"  LÀM: [{pk['id']}] {pk['task']}")
        print(f"       hạn {pk.get('deadline') or '—'} (còn {pk['days_left']} ngày) · {pk['effort_num']}h · "
              f"ưu tiên {pk.get('priority') or 1} · conf {d.get('pick_confidence')}")
    if bk:
        print(f"  DỰ PHÒNG: [{bk['id']}] {bk['task']} ({bk['effort_num']}h)")
    if snap["overdue"]:
        print("  ⚠ TRỄ HẠN: " + ", ".join(f"{c['id']}({c['task'][:20]}, {-c['days_left']} ngày)" for c in snap["overdue"]))
    if d.get("deadline_risk") is not None:
        print(f"  rủi ro trễ hạn (Jev): {d['deadline_risk']}")
    if d.get("load_fit") is not None:
        labels = d["load_fit_labels"]
        i = min(int(round(d["load_fit"])), len(labels) - 1)
        print(f"  tải công việc: {labels[i]} ({d['load_fit']})")
    if snap["events_today"]:
        print("  lịch hôm nay: " + ", ".join(f"{e.get('start','?')}-{e.get('end','?')} {e.get('event')}"
                                             for e in snap["events_today"]))
    if snap["habits_pending"]:
        print("  thói quen chưa đủ tuần: " + ", ".join(f"{h.get('habit')} (còn {h['remaining']})"
                                                        for h in snap["habits_pending"]))


def cmd_list(args) -> None:
    snap = snapshot()
    st = (args.status or "todo").lower()
    if st == "todo":
        rows = snap["candidates"]
    elif st == "all":
        rows = snap["tasks_all"]
    else:
        rows = [r for r in snap["tasks_all"] if (r.get("status") or "").lower() == st]
    for c in rows:
        dl = c.get("deadline") or "—"
        left = f"{c['days_left']}d" if c["days_left"] is not None else "—"
        print(f"{c['id']:<5} {c.get('status','todo'):<6} {dl:<11} {left:<5} "
              f"P{c.get('priority') or 1} {str(c['effort_num']):>4}h  {c['task'][:50]}")


def cmd_briefing(args) -> None:
    snap = snapshot()
    d = decide_today(snap["candidates"], snap["events_today"], snap["habits_pending"],
                     dt.date.fromisoformat(snap["today"]))
    print(json.dumps({"briefing_for": snap["today"], "decision": d,
                      "open_tasks": len(snap["candidates"]),
                      "overdue": len(snap["overdue"]), "due_7d": len(snap["due_7d"]),
                      "events_today": len(snap["events_today"]),
                      "habits_pending": len(snap["habits_pending"])}, ensure_ascii=False, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser(description="Trợ lý cá nhân: Google Sheets + Jev")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_dry(p):
        p.add_argument("--dry-run", action="store_true", help="xem trước, không ghi")
        return p

    p = add_dry(sub.add_parser("add", help="thêm việc"))
    p.add_argument("task")
    p.add_argument("--category", default="")
    p.add_argument("--deadline", default="", help="YYYY-MM-DD")
    p.add_argument("--priority", type=float, default=1.0, help="1 thấp -> 5 cao")
    p.add_argument("--effort", type=float, default=1.0, help="giờ ước tính")
    p.add_argument("--status", default="todo")
    p.add_argument("--notes", default="")
    p.add_argument("--id", default="")
    p.set_defaults(fn=add_task)

    p = add_dry(sub.add_parser("event", help="thêm sự kiện/lịch"))
    p.add_argument("event")
    p.add_argument("--date", required=True)
    p.add_argument("--start", default="")
    p.add_argument("--end", default="")
    p.add_argument("--location", default="")
    p.add_argument("--type", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--id", default="")
    p.set_defaults(fn=add_event)

    p = add_dry(sub.add_parser("habit", help="thêm thói quen theo tuần"))
    p.add_argument("habit")
    p.add_argument("--target", type=float, default=3.0, help="số lần/tuần")
    p.add_argument("--notes", default="")
    p.add_argument("--id", default="")
    p.set_defaults(fn=add_habit)

    p = add_dry(sub.add_parser("done", help="đánh dấu xong"))
    p.add_argument("task_id")
    p.set_defaults(fn=mark_done)

    p = add_dry(sub.add_parser("log", help="ghi nhận đã làm bao nhiêu phút"))
    p.add_argument("task_id")
    p.add_argument("minutes", type=int)
    p.add_argument("note", nargs="?", default="")
    p.set_defaults(fn=add_log)

    p = add_dry(sub.add_parser("habit-done", help="đánh dấu đã làm thói quen (tự tăng streak khi đủ target)"))
    p.add_argument("habit_id")
    p.add_argument("--count", type=float, default=1.0)
    p.set_defaults(fn=habit_done)

    p = add_dry(sub.add_parser("rm", help="xóa 1 dòng (in lại dữ liệu cũ để khôi phục nếu cần)"))
    p.add_argument("--tab", default="tasks", choices=["tasks", "events", "habits", "log", "meta"])
    p.add_argument("id")
    p.set_defaults(fn=rm_row)

    p = sub.add_parser("list", help="liệt kê việc")
    p.add_argument("--status", default="todo", help="todo|done|all")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("today", help="hôm nay làm gì")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_today)

    p = sub.add_parser("briefing", help="bản tin tổng hợp (JSON)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_briefing)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
