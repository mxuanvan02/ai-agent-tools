---
name: jev-form-driver
description: "Form automation where code orchestrates and a System-One decision model selects each field."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Jev, TypeSafe, Browser, Forms, MCP, Automation]
    related_skills: [jev-ultrafast-browser-agent, browser-qa]
---

# jev-form-driver

Drive one web form end-to-end with a measured division of labour between deterministic code and
a fast decision model (TypeSafe Jev, `systemone` endpoint). Code owns the loop; the model owns
per-field choices. Exposed as a Python library, a CLI, and an MCP stdio tool (`jev_form_fill`).

## When to use

- A form/wizard on standard HTML must be filled and submitted repeatedly (registrations, filters,
  order forms, admin panels) and each run should cost fractions of a cent and ~1 second of model time.
- You need prompt-injection-resistant automation: page text is untrusted data, and the model is
  only ever asked "what to do with THIS field", never "what does the page say to do".
- You have ground truth to verify against (expected field values, an expected result object).

## When NOT to use

- Tasks requiring arithmetic, counting, or date ordering: the decision model cannot compute —
  precompute in code and inject as `facts`, or the run will fail (measured: 0/2 vs 2/2 on the
  same page with/without injected totals).
- Canvas/iframes/shadow-DOM surfaces, file uploads, keyboard-complex widgets: observation only
  enumerates standard interactive controls.
- Open-ended browsing or multi-page research: use a full agent loop instead.

## Workflow

1. Install deps in a venv: `typesafe-sdk`, `browser-harness`, `mcp<2` (mcp 2.x renames FastMCP).
2. Point at a Chrome exposing CDP (`CDP_PORT`, default 9222) or let browser-harness discover one.
3. Provide `TYPESAFE_API_KEY` via environment (or `JEV_FORM_ENV_FILE` dotenv path).
4. Call `FormDriver().run(url, goal, values={label: text}, facts={row_key: fact}, verify=fn)`:
   - `values` — exact text per field label; the model NEVER invents field data.
   - `facts` — precomputed facts appended to matching rows, for any comparison task.
   - `verify` — independent verifier over the resulting page state; never trust a model DONE.
5. Read `status`, `ok`, `why`, `jev_requests`, `wall_s` from the report. Check `ok/why`, not
   `status` alone.
6. Or register `src/jev_form_mcp.py` as an MCP server and call `jev_form_fill` with the same
   arguments plus `expect` (exact-match verifier) and `max_rounds`.

## Verification

- `tests/driver_regression.py` runs all 5 graded fixtures with absolute ground truth
  (self-contained HTML pages; result read from `window.__RESULT`): expect 4/5 pass, T4a
  fails by design (arithmetic). Requires live Chrome + API key.
- The 5-rung ladder results and the naive-vs-orchestrated comparison live in `README.md`.

## Pitfalls

- A radio group is outstanding only when NO member is checked; the naive rule loops forever.
- The model under-emits DONE on rich forms — code decides submission, then verifies.
- `mcp>=2` breaks the server import; pin `mcp<2`.
- Select handling needs a code-owned marker (`data-jevmark`), never a model-generated selector.
