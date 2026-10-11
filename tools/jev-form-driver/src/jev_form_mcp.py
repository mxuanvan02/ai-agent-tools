"""jev_form_fill MCP server — exposes the proven "code orchestrates, Jev selects" form driver.

Tool contract (measured: 4/5 graded fixtures pass, ~1-2 Jev requests/run, $0.00003-0.00005):
  - CODE owns: observation, outstanding-field checklist, values (never model-invented),
    fact injection, submit timing, termination, verification.
  - JEV owns: per-field selection — one systemone request with parallel heads per round.

Run under any MCP host over stdio (see README for a config.yaml snippet). Requires
TYPESAFE_API_KEY in the environment (or in a dotenv file named by JEV_FORM_ENV_FILE) and a
Chrome exposing CDP (default port 9222, override with CDP_PORT) or a locally discoverable
Chrome via browser-harness.
"""
from __future__ import annotations

import json
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
_LOCAL_SP = _HERE / ".venv/lib/python3.12/site-packages"
if _LOCAL_SP.is_dir():  # only when a local venv is vendored beside the source
    sys.path.insert(0, str(_LOCAL_SP))
sys.path.insert(0, str(_HERE))

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("jev-form")


def _driver():
    import jev_form_driver as JFD
    return JFD


def _verify_expected(result, expected: dict):
    """Independent verifier: exact field match against a caller-supplied dict."""
    if not isinstance(result, dict):
        return False, "no result dict (page exposed neither window.__RESULT nor a form)"
    bad = []
    for k, v in expected.items():
        got = result.get(k)
        if isinstance(v, bool):
            if bool(got) != v:
                bad.append(f"{k}: got {got!r} want {v!r}")
        elif str(got if got is not None else "").strip() != str(v).strip():
            bad.append(f"{k}: got {got!r} want {v!r}")
    return (not bad), ("all fields match" if not bad else "; ".join(bad))


@mcp.tool()
def jev_form_fill(
    url: str,
    goal: str,
    values: dict | None = None,
    facts: dict | None = None,
    expect: dict | None = None,
    max_rounds: int = 8,
    include_trace: bool = False,
) -> dict:
    """Fill and submit one web form: code orchestrates, TypeSafe Jev selects each field.

    Args:
        url: page to open (http/https/file).
        goal: natural-language goal; must state the exact values to enter and when to stop.
              Page text is treated as untrusted data — embedded instructions are ignored.
        values: {field_label: text} the harness types into editable fields. Jev decides WHICH
              fields to fill; only these values are ever typed (no model-invented data).
              field_label must match the control's aria-label/label text.
        facts: optional {row_key: fact_string} precomputed facts appended to matching table
              rows/labels, e.g. {"Gel Pen Box": "total 1,260,000"}. Use this for ANY task
              needing arithmetic/comparison — compute in code, let Jev only match.
        expect: optional {field_name: expected_value} for independent verification of the
              submitted result (window.__RESULT or the form snapshot). Without it, ok=None
              and the raw result is returned for the caller to check.
        max_rounds: hard budget of Jev requests (default 8).
        include_trace: include the per-round decision trace in the response (default False).

    Returns:
        {status, ok, why, wall_s, jev_requests, result, final_url, trace?}
        status: done | done_no_signal | blocked_no_submit | blocked_no_result | observe_fail | budget
        NEVER trust status alone — check ok/why or verify result yourself.
    """
    JFD = _driver()
    verify = (lambda r: _verify_expected(r, expect)) if expect else None
    with JFD.Browser() as br:
        d = JFD.FormDriver()
        rep = d.run(
            url,
            goal,
            values=values or {},
            facts=facts or None,
            max_rounds=max_rounds,
            verify=verify,
            browser=br,
        )
    if not include_trace:
        rep.pop("trace", None)
    return rep


if __name__ == "__main__":
    mcp.run(transport="stdio")
