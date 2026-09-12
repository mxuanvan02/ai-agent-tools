#!/usr/bin/env python3
"""Portable PPT Master + OfficeCLI generation and publication pipeline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_LOCK_PATH = TOOL_DIR / "config" / "slide-pipeline.lock.json"
DEFAULT_STATE_PATH = TOOL_DIR / ".state" / "toolchain.json"
SCHEMA = "slide-pipeline.v1"
BLOCKING_SUBTYPES = frozenset({"broken_part_ref", "notes_unresolved_rid"})
BLOCKING_MESSAGE_RE = re.compile(
    r"text overflow|outside (?:the )?slide|overlap(?:ping)?|referenced but not declared",
    re.IGNORECASE,
)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def _load_lock() -> tuple[dict[str, Any], Path]:
    path = Path(os.environ.get("SLIDE_PIPELINE_LOCK", DEFAULT_LOCK_PATH)).expanduser()
    return _read_json(path), path.resolve()


def _default_prefix() -> Path:
    data_home = os.environ.get("XDG_DATA_HOME")
    root = Path(data_home).expanduser() if data_home else Path.home() / ".local" / "share"
    return root / "ai-agent-tools" / "ppt-master-officecli"


def _load_runtime() -> dict[str, str]:
    state_path = Path(
        os.environ.get("SLIDE_PIPELINE_STATE", DEFAULT_STATE_PATH)
    ).expanduser()
    state: dict[str, Any] = {}
    if state_path.is_file():
        state = _read_json(state_path)

    prefix = Path(str(state.get("prefix") or _default_prefix())).expanduser()
    values = {
        "repo": os.environ.get("PPT_MASTER_REPO")
        or str(state.get("ppt_master_repo") or prefix / "ppt-master"),
        "python": os.environ.get("PPT_MASTER_PYTHON")
        or str(state.get("ppt_master_python") or prefix / "venv" / "bin" / "python"),
        "officecli": os.environ.get("OFFICECLI_COMMAND")
        or str(
            state.get("officecli_command")
            or prefix / "officecli" / "node_modules" / ".bin" / "officecli"
        ),
        "state": str(state_path.resolve()),
        "prefix": str(prefix.resolve()),
    }
    return values


def _run(command: list[str]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        return {
            "command": command,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
        }
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _json_result(command: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    invocation = _run(command)
    try:
        payload = json.loads(invocation["stdout"])
    except (json.JSONDecodeError, TypeError) as exc:
        payload = {
            "success": False,
            "message": f"Command did not return valid JSON: {exc}",
        }
    if not isinstance(payload, dict):
        payload = {"success": False, "message": "Command returned non-object JSON."}
    return payload, invocation


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_version(raw: str) -> str:
    value = raw.strip()
    try:
        decoded = json.loads(value)
        if isinstance(decoded, str):
            value = decoded
    except json.JSONDecodeError:
        pass
    return value.removeprefix("v")


def _toolchain(
    lock: dict[str, Any], runtime: dict[str, str]
) -> tuple[dict[str, str], list[str]]:
    repo = Path(runtime["repo"])
    python = Path(runtime["python"])
    expected_revision = str(lock["ppt_master"]["revision"])
    expected_patch_hash = str(lock["ppt_master"]["patched_sha256"])
    patched_file = repo / str(lock["ppt_master"]["patched_file"])
    expected_officecli = str(lock["officecli"]["version"])
    blockers: list[str] = []

    git_result = _run(["git", "-C", str(repo), "rev-parse", "HEAD"])
    revision = (
        git_result["stdout"].strip() if git_result["exit_code"] == 0 else "unavailable"
    )
    if revision != expected_revision:
        blockers.append(
            f"PPT Master revision drift: expected {expected_revision}, found {revision}."
        )

    patch_hash = _sha256(patched_file) if patched_file.is_file() else "unavailable"
    if patch_hash != expected_patch_hash:
        blockers.append(
            "PPT Master compatibility patch drift: "
            f"expected {expected_patch_hash}, found {patch_hash}."
        )

    office_result = _run([runtime["officecli"], "--version"])
    office_version = (
        _normalize_version(office_result["stdout"])
        if office_result["exit_code"] == 0
        else "unavailable"
    )
    if office_version != expected_officecli:
        blockers.append(
            f"OfficeCLI version drift: expected {expected_officecli}, found {office_version}."
        )
    if not python.is_file():
        blockers.append(f"Pinned PPT Master Python is missing: {python}.")

    return {
        "ppt_master_revision": revision,
        "ppt_master_patch": str(lock["ppt_master"]["compatibility_patch"]),
        "ppt_master_patch_sha256": patch_hash,
        "officecli_version": office_version,
        "python": str(python),
        "state": runtime["state"],
    }, blockers


def _validate_pptx(path: Path) -> None:
    if not path.is_file():
        raise ValueError(f"PPTX does not exist: {path}")
    if path.suffix.lower() != ".pptx":
        raise ValueError(f"Expected a .pptx file: {path}")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _classify_office_issues(
    issues_report: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    blockers: list[str] = []
    advisories: list[dict[str, Any]] = []
    data = issues_report.get("data")
    issues = data.get("issues", []) if isinstance(data, dict) else []
    if not isinstance(issues, list):
        return ["OfficeCLI returned an invalid issue inventory."], advisories

    for issue in issues:
        if not isinstance(issue, dict):
            continue
        subtype = str(issue.get("subtype") or "")
        message = str(issue.get("message") or "")
        severity = issue.get("severity")
        is_blocking = (
            subtype in BLOCKING_SUBTYPES
            or severity == 0
            or bool(BLOCKING_MESSAGE_RE.search(message))
        )
        if is_blocking:
            blockers.append(f"OfficeCLI issue {issue.get('id', 'unknown')}: {message}")
        else:
            advisories.append(issue)
    return blockers, advisories


def inspect_pptx(pptx: Path, report_dir: Path) -> dict[str, Any]:
    _validate_pptx(pptx)
    lock, lock_path = _load_lock()
    runtime = _load_runtime()
    report_dir.mkdir(parents=True, exist_ok=True)
    preview = report_dir / "preview.png"
    tools, blockers = _toolchain(lock, runtime)

    ppt_scripts = (
        Path(runtime["repo"]) / "skills" / "ppt-master" / "scripts"
    )
    python = runtime["python"]
    officecli = runtime["officecli"]

    delivery, delivery_call = _json_result(
        [python, str(ppt_scripts / "pptx_delivery_check.py"), str(pptx)]
    )
    validation, validation_call = _json_result(
        [officecli, "validate", str(pptx), "--json"]
    )
    stats, stats_call = _json_result(
        [officecli, "view", str(pptx), "stats", "--json"]
    )
    issues, issues_call = _json_result(
        [officecli, "view", str(pptx), "issues", "--json"]
    )
    screenshot, screenshot_call = _json_result(
        [
            officecli,
            "view",
            str(pptx),
            "screenshot",
            "--grid",
            "auto",
            "-o",
            str(preview),
            "--json",
        ]
    )

    if delivery.get("status") == "failed":
        blockers.append("PPT Master delivery check failed.")
    if validation.get("success") is not True:
        blockers.append("OfficeCLI OpenXML validation failed.")
    if stats.get("success") is not True:
        blockers.append("OfficeCLI statistics inspection failed.")
    if issues.get("success") is not True:
        blockers.append("OfficeCLI issue inspection failed.")
    issue_blockers, office_advisories = _classify_office_issues(issues)
    blockers.extend(issue_blockers)
    if screenshot.get("success") is not True or not preview.is_file():
        blockers.append("OfficeCLI preview rendering failed.")

    delivery_advisories = delivery.get("advisories", [])
    if not isinstance(delivery_advisories, list):
        delivery_advisories = []
    blockers = list(dict.fromkeys(blockers))

    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "read-only-quality-gate",
        "input": {
            "path": str(pptx.resolve()),
            "bytes": pptx.stat().st_size,
            "sha256": _sha256(pptx),
        },
        "toolchain": tools,
        "configuration": {
            "lock": str(lock_path),
            "state": runtime["state"],
        },
        "policy": {
            "auto_fix": False,
            "blocking_subtypes": sorted(BLOCKING_SUBTYPES),
            "blocking_conditions": [
                "PPT Master delivery status failed",
                "OfficeCLI validation/stats/issues/render failure",
                "OfficeCLI severity 0 issue",
                "text overflow, overlap, outside-slide, or undeclared relationship",
            ],
        },
        "decision": {
            "status": "failed" if blockers else "passed",
            "blocking_reasons": blockers,
            "advisories": {
                "ppt_master": delivery_advisories,
                "officecli": office_advisories,
            },
        },
        "artifacts": {
            "preview": str(preview.resolve()) if preview.is_file() else None,
            "report_dir": str(report_dir.resolve()),
        },
        "reports": {
            "ppt_master_delivery": delivery,
            "officecli_validate": validation,
            "officecli_stats": stats,
            "officecli_issues": issues,
            "officecli_screenshot": screenshot,
        },
        "invocations": {
            "ppt_master_delivery": delivery_call,
            "officecli_validate": validation_call,
            "officecli_stats": stats_call,
            "officecli_issues": issues_call,
            "officecli_screenshot": screenshot_call,
        },
    }
    _write_json(report_dir / "manifest.json", manifest)
    for name, report in manifest["reports"].items():
        _write_json(report_dir / f"{name}.json", report)
    return manifest


def command_generate(args: argparse.Namespace) -> int:
    lock, _ = _load_lock()
    runtime = _load_runtime()
    tools, blockers = _toolchain(lock, runtime)
    if blockers:
        print(
            json.dumps(
                {"success": False, "errors": blockers, "toolchain": tools},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    script = (
        Path(runtime["repo"])
        / "skills"
        / "ppt-master"
        / "scripts"
        / "project_manager.py"
    )
    command = [runtime["python"], str(script), "init", args.project_name]
    if args.directory:
        command.extend(["--dir", str(args.directory)])
    if args.format:
        command.extend(["--format", args.format])
    if args.quick:
        command.append("--quick-generate")
    result = _run(command)
    print(
        json.dumps(
            {"success": result["exit_code"] == 0, "toolchain": tools, **result},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if result["exit_code"] == 0 else 1


def command_inspect(args: argparse.Namespace) -> int:
    pptx = args.pptx.resolve()
    report_dir = args.report_dir or pptx.parent / f"{pptx.stem}.slide-pipeline"
    manifest = inspect_pptx(pptx, report_dir.resolve())
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if manifest["decision"]["status"] == "passed" else 1


def command_finalize(args: argparse.Namespace) -> int:
    draft = args.draft.resolve()
    final = args.final.resolve()
    if draft == final:
        raise ValueError("Draft and final paths must differ.")
    report_dir = args.report_dir or final.parent / f"{final.stem}.slide-pipeline"
    manifest = inspect_pptx(draft, report_dir.resolve())
    if manifest["decision"]["status"] != "passed":
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 1

    final.parent.mkdir(parents=True, exist_ok=True)
    temporary = final.with_name(f".{final.name}.tmp")
    shutil.copy2(draft, temporary)
    temporary.replace(final)
    manifest["output"] = {
        "path": str(final),
        "bytes": final.stat().st_size,
        "sha256": _sha256(final),
    }
    manifest["decision"]["status"] = "published"
    _write_json(report_dir.resolve() / "manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser(
        "generate", help="Initialize a pinned PPT Master project"
    )
    generate.add_argument("project_name")
    generate.add_argument("--dir", dest="directory", type=Path)
    generate.add_argument("--format")
    generate.add_argument("--quick", action="store_true")
    generate.set_defaults(func=command_generate)

    inspect = subparsers.add_parser(
        "inspect", help="Run the read-only PPTX quality gate"
    )
    inspect.add_argument("pptx", type=Path)
    inspect.add_argument("--report-dir", type=Path)
    inspect.set_defaults(func=command_inspect)

    finalize = subparsers.add_parser(
        "finalize", help="Publish a draft only when all gates pass"
    )
    finalize.add_argument("draft", type=Path)
    finalize.add_argument("final", type=Path)
    finalize.add_argument("--report-dir", type=Path)
    finalize.set_defaults(func=command_finalize)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"slide_pipeline: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
