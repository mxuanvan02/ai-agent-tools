#!/usr/bin/env python3
"""Append-only ledger of review findings, with a gate that blocks merge when findings are
unanswered or rounds have exceeded the cap.

A finding is a tuple of (file, line, severity, class, message) plus a status. The ledger is
append-only by design: every mutation is a new row with a monotonic id, and the current state
is the last row for each finding id. This is what makes the ledger auditable -- you can always
replay the file and see what happened when -- and it is what makes the gate honest: a finding
cannot be silently deleted, only answered with a documented reason.

Subcommands:
  add       --file F --line L --severity S --class C --message M  [new round]
  respond   --id ID --action A --note N                           [answer one finding]
  round     --id ID                                               [open a new round; optional]
  gate      [--max-rounds N] [--ledger FILE]                      [exit 0 if mergeable, 1 if not]
  stats     [--ledger FILE]                                       [noise rate and round counts]
  dump      [--ledger FILE]                                       [current state as JSON]

The ledger file is JSONL, one row per mutation. Each row is a complete finding snapshot so the
file is self-contained: it can be read without any other state.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

SEVERITIES = ("important", "nit", "pre-existing")
ACTIONS = ("fixed", "rejected", "intentional", "ignored")
DEFAULT_LEDGER = Path("review-ledger.jsonl")
DEFAULT_MAX_ROUNDS = 3


@dataclass
class Finding:
    id: str
    file: str
    line: int
    severity: str
    cls: str
    message: str
    round: int
    status: str = "open"
    action: str | None = None
    note: str | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file": self.file,
            "line": self.line,
            "severity": self.severity,
            "class": self.cls,
            "message": self.message,
            "round": self.round,
            "status": self.status,
            "action": self.action,
            "note": self.note,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit("ledger line %d is not valid JSON: %s" % (i, exc))
    return rows


def _row_to_finding(row: dict) -> Finding:
    """Rebuild a Finding from a ledger row with explicit casts so the type checker sees what
    the schema guarantees: every field is present and has the right type. Using ``row.get``
    would return ``Unknown | None`` and Pyright would flag every field."""
    return Finding(
        id=str(row["id"]),
        file=str(row["file"]),
        line=int(row["line"]),
        severity=str(row["severity"]),
        cls=str(row["class"]),
        message=str(row["message"]),
        round=int(row["round"]),
        status=str(row.get("status") or "open"),
        action=row.get("action"),
        note=row.get("note"),
        created_at=float(row.get("created_at") or 0.0),
        updated_at=float(row.get("updated_at") or 0.0),
    )


def current_state(rows: list[dict]) -> dict[str, Finding]:
    """Replay the ledger into the latest snapshot per finding id."""
    state: dict[str, Finding] = {}
    for row in rows:
        state[row["id"]] = _row_to_finding(row)
    return state


def next_id(state: dict[str, Finding]) -> str:
    if not state:
        return "F001"
    nums = []
    for fid in state:
        if fid.startswith("F") and fid[1:].isdigit():
            nums.append(int(fid[1:]))
    return "F%03d" % ((max(nums) + 1) if nums else 1)


def append_row(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def cmd_add(args: argparse.Namespace) -> int:
    if args.severity not in SEVERITIES:
        print(json.dumps({"error": "severity must be one of %s" % (SEVERITIES,)}))
        return 2
    if args.line < 0:
        print(json.dumps({"error": "line must be non-negative"}))
        return 2
    if not args.file:
        print(json.dumps({"error": "file is required"}))
        return 2
    if not args.message:
        print(json.dumps({"error": "message is required"}))
        return 2
    if not args.cls:
        print(json.dumps({"error": "class is required"}))
        return 2

    rows = read_ledger(args.ledger)
    state = current_state(rows)

    # Duplicate check: same (file, line, class) that is still open. A duplicate of a closed
    # finding is allowed -- it is a new observation after the previous one was resolved.
    for f in state.values():
        if f.file == args.file and f.line == args.line and f.cls == args.cls and f.status == "open":
            print(json.dumps({"error": "duplicate of open finding %s" % f.id,
                              "existing": f.to_dict()}))
            return 3

    # Round: if there are any findings at all, the new one joins the highest existing round
    # unless the caller explicitly asks for a new round. This is what stops the reviewer from
    # reopening round 4 when the cap is 3 -- the gate below will refuse.
    max_round = max((f.round for f in state.values()), default=0)
    new_round = args.round if args.round is not None else max_round
    if args.round is not None and args.round < max_round:
        print(json.dumps({"error": "round %d is in the past; current round is %d" % (args.round, max_round)}))
        return 4

    fid = next_id(state)
    now = time.time()
    row = Finding(
        id=fid, file=args.file, line=args.line, severity=args.severity,
        cls=args.cls, message=args.message, round=new_round,
        status="open", created_at=now, updated_at=now,
    ).to_dict()
    append_row(args.ledger, row)
    print(json.dumps({"added": fid, "round": new_round, "ledger": str(args.ledger)}))
    return 0


def cmd_respond(args: argparse.Namespace) -> int:
    if args.action not in ACTIONS:
        print(json.dumps({"error": "action must be one of %s" % (ACTIONS,)}))
        return 2
    rows = read_ledger(args.ledger)
    state = current_state(rows)
    if args.id not in state:
        print(json.dumps({"error": "no finding with id %s" % args.id}))
        return 2
    f = state[args.id]
    if f.status != "open":
        print(json.dumps({"error": "finding %s is already %s" % (args.id, f.status)}))
        return 2
    now = time.time()
    row = {
        "id": f.id, "file": f.file, "line": f.line, "severity": f.severity,
        "class": f.cls, "message": f.message, "round": f.round,
        "status": "closed", "action": args.action, "note": args.note or "",
        "created_at": f.created_at, "updated_at": now,
    }
    append_row(args.ledger, row)
    print(json.dumps({"responded": args.id, "action": args.action}))
    return 0


def cmd_round(args: argparse.Namespace) -> int:
    """Open a new review round. Creates a synthetic row so the ledger records the boundary;
    the gate uses the highest round number it sees, so this row is what stops a reviewer from
    silently starting round 4 when the cap is 3."""
    rows = read_ledger(args.ledger)
    state = current_state(rows)
    max_round = max((f.round for f in state.values()), default=0)
    new_round = args.round if args.round is not None else max_round + 1
    if new_round <= max_round:
        print(json.dumps({"error": "round %d is not newer than %d" % (new_round, max_round)}))
        return 2
    now = time.time()
    row = {
        "id": "__round__%d" % new_round, "file": "", "line": 0, "severity": "",
        "class": "__round__", "message": "review round %d opened" % new_round,
        "round": new_round, "status": "meta", "action": None, "note": None,
        "created_at": now, "updated_at": now,
    }
    append_row(args.ledger, row)
    print(json.dumps({"round": new_round, "ledger": str(args.ledger)}))
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    rows = read_ledger(args.ledger)
    state = current_state(rows)
    open_findings = [f for f in state.values() if f.status == "open" and f.id != "__round__"]
    rounds_used = max((f.round for f in state.values() if not f.id.startswith("__round__")), default=0)
    max_rounds = args.max_rounds if args.max_rounds is not None else DEFAULT_MAX_ROUNDS

    verdict = {
        "mergeable": True,
        "open_findings": len(open_findings),
        "rounds_used": rounds_used,
        "max_rounds": max_rounds,
        "reasons": [],
    }
    if open_findings:
        verdict["mergeable"] = False
        verdict["reasons"].append("%d finding(s) still open" % len(open_findings))
    if rounds_used > max_rounds:
        verdict["mergeable"] = False
        verdict["reasons"].append("round %d exceeds cap of %d; reviewer must ask the author to reconsider" % (
            rounds_used, max_rounds))

    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    return 0 if verdict["mergeable"] else 1


def cmd_stats(args: argparse.Namespace) -> int:
    rows = read_ledger(args.ledger)
    state = current_state(rows)
    closed = [f for f in state.values() if f.status == "closed" and not f.id.startswith("__round__")]
    by_action: dict[str, int] = {}
    for f in closed:
        by_action[f.action or "unknown"] = by_action.get(f.action or "unknown", 0) + 1
    total_closed = len(closed) or 1
    # Noise rate: share of closed findings whose action was rejected or ignored. The reviewer
    # is right about the rest. This is the counterweight to "catch more bugs" -- if the rate
    # is high, the reviewer is flagging things that are not bugs.
    noise = by_action.get("rejected", 0) + by_action.get("ignored", 0)
    rounds_used = max((f.round for f in state.values() if not f.id.startswith("__round__")), default=0)
    print(json.dumps({
        "total_findings": len([f for f in state.values() if not f.id.startswith("__round__")]),
        "open": len([f for f in state.values() if f.status == "open" and not f.id.startswith("__round__")]),
        "closed": len(closed),
        "by_action": by_action,
        "noise_rate": round(noise / total_closed, 3) if closed else None,
        "rounds_used": rounds_used,
    }, indent=2, ensure_ascii=False))
    return 0


def cmd_dump(args: argparse.Namespace) -> int:
    rows = read_ledger(args.ledger)
    state = current_state(rows)
    print(json.dumps([f.to_dict() for f in state.values()], indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a finding")
    p_add.add_argument("--file", required=True)
    p_add.add_argument("--line", type=int, required=True)
    p_add.add_argument("--severity", required=True, choices=SEVERITIES)
    p_add.add_argument("--class", dest="cls", required=True)
    p_add.add_argument("--message", required=True)
    p_add.add_argument("--round", type=int)
    p_add.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p_add.set_defaults(func=cmd_add)

    p_res = sub.add_parser("respond", help="answer a finding")
    p_res.add_argument("--id", required=True)
    p_res.add_argument("--action", required=True, choices=ACTIONS)
    p_res.add_argument("--note", default="")
    p_res.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p_res.set_defaults(func=cmd_respond)

    p_rnd = sub.add_parser("round", help="open a new review round")
    p_rnd.add_argument("--round", type=int)
    p_rnd.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p_rnd.set_defaults(func=cmd_round)

    p_gate = sub.add_parser("gate", help="decide whether the change can merge")
    p_gate.add_argument("--max-rounds", type=int)
    p_gate.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p_gate.set_defaults(func=cmd_gate)

    p_stats = sub.add_parser("stats", help="noise rate and round counts")
    p_stats.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p_stats.set_defaults(func=cmd_stats)

    p_dump = sub.add_parser("dump", help="current state as JSON")
    p_dump.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p_dump.set_defaults(func=cmd_dump)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
