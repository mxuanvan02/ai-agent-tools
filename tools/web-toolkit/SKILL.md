---
name: web-toolkit
description: "Proxy pool, human-like timing, and declarative page-state detection for browser automation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Browser, Automation, Proxy, Testing, State-Machine]
    related_skills: [browser-qa, e2e-testing, jev-form-driver]
---

# web-toolkit

Three dependency-free Python modules for browser/scraping automation, extracted and generalised
from patterns observed in a third-party automation repo (ISC-licensed); all account-farming,
captcha-solving and fingerprint-spoofing content was discarded — only the neutral engineering
patterns are kept.

## Modules

1. `src/proxy_pool.py` — proxy pool with lease semantics (context manager, auto-release even on
   exception), LRU/round-robin/random strategies, consecutive-failure counting with capped
   exponential cooldown, permanent retirement after `max_failures`, injectable health probe
   (offline-safe tests), password-safe `repr`/logs.
2. `src/humanize.py` — jittered per-action delay bands, Bezier cursor paths with exact endpoints,
   character-by-character typing with micro-pauses and self-corrected typos. Purpose is TEST
   STABILITY (fixed sleeps are the #1 flaky-test cause), transport-agnostic via injected callbacks.
3. `src/page_state.py` — declarative page/form state machine: declare steps as data (URL
   substrings first, then element evidence, priorities, tie-breaks), get a typed
   `{state, action, score, evidence}` detection; includes `wait_for` polling with injectable sleep
   and transition-history analysis for wizard flows.

## When to use

- Scraping/crawling with a proxy list: rotation + failure handling without reinventing the pool.
- Browser E2E suites that flake on timing: replace fixed sleeps with delay bands.
- Multi-step forms/wizards: classify "which step am I on?" before acting — the same
  checklist-driven idea as `jev-form-driver`, standalone and model-free.

## Verification

`tests/test_web_toolkit.py`: 29 tests, no network, no browser — health probes injected, sleeps
faked, DOM hooks are dict lookups. Run:

```bash
uv run --python 3.12 --with pytest python -m pytest tests/test_web_toolkit.py -q
```

## Pitfalls

- Cooldown semantics: `report_failure` uses consecutive failures; a success clears the streak.
- `iter_with_pool` returns `(item, status, proxy_id)` where `proxy_id == "none"` means the final
  attempt could not acquire any proxy (exhaustion), not that no proxy was ever tried.
- `mouse_path` jitters interior points only; endpoints are exact so clicks land on target.
- `PageState.elements` is ALL-present evidence (missing one rejects the state); use
  `any_elements` for weak evidence.
