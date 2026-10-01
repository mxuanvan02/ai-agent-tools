# jev-routing-relay-ops

Operate **TypeSafe Jev** model/effort routing when the provider is a *local relay* — one
OpenAI-compatible endpoint fronting several upstream accounts — instead of a catalog-known
provider such as OpenRouter.

A relay silently breaks three assumptions Jev routing is built on, and each one fails in a
way that reads as "configured correctly":

| Assumption | Reality behind a relay | Symptom |
|---|---|---|
| models.dev knows every model | relay refs (`myrelay:*`) are absent | context guard and vision pool become inert |
| price ordering = cost ordering | upstream may bill **per request** | effort routing saves nothing; only a model switch does |
| the wire carries declared fields | typed request structs drop unknown keys | `reasoning_effort` vanishes before the upstream |

This package is the verification discipline for that setup. It complements the upstream
`jev-model-routing` skill rather than replacing it.

## Contents

- [`SKILL.md`](SKILL.md) — eight rules, each tied to a measurable check, plus the
  verification checklist.
- [`scripts/probe_routing_pool.py`](scripts/probe_routing_pool.py) — offline `--self-check`
  (no network, no key) and a live wire probe (tool calling, per-level effort acceptance,
  vision proof by digit read-back).
- [`scripts/public_hygiene_check.py`](scripts/public_hygiene_check.py) — the repository's
  shared release gate.
- [`references/relay-pitfalls.md`](references/relay-pitfalls.md) — field notes: measurement
  recipes, the off-by-one that reintroduces a cache leak, and how to audit the audit.

## Quick start

Offline first. It reads the live routing config and reports which guards are actually armed:

```bash
python3 scripts/probe_routing_pool.py --self-check --prefix <your-relay-prefix>
```

Exit code 1 means a real defect. Models that reject every effort level are deliberate, so
name them instead of silencing the finding:

```bash
python3 scripts/probe_routing_pool.py --self-check --prefix <prefix> \
    --exempt-caps model-that-500s-on-every-level
```

Then prove the wire, with the credential read at runtime and never printed:

```bash
export RELAY_AUTH='Bearer ...'          # or: --auth-file /run/secrets/relay
python3 scripts/probe_routing_pool.py \
    --base-url http://localhost:PORT/v1 \
    --models cheap-model,mid-model,current-model \
    --efforts low,medium,high,max --vision --json-out probe.json
```

## What the self-check gates on

Seven areas. Each one was derived from a defect observed on a live fleet, not from reading
the upstream source:

1. `_pick` resolves a relay ref for a small non-vision turn.
2. The vision pool is reported **inert** (a warning) rather than passing silently — editing
   it has no effect while refs stay catalog-unknown.
3. The large-context guard keeps the model when neither side has a catalog price.
4. `_sticky_side` matches `decide()`'s strict `>` and the cache key separates the two sides
   of the threshold even inside one context bucket.
5. `effort.levels` parses. An enabled table that does not parse resolves to `None`, which
   skips every effort branch and reports green while effort routing is dead.
6. Every pool model has caps **or** an explicit exemption. No caps is not "effort off" —
   the request keeps the host default, often the maximum.
7. Declared levels are reachable, and the cheap tier can reach the cheapest level.

Areas 5 and 6 exist because a green report is worthless when the check never ran. The
package's own mutation history: an earlier version skipped both silently and passed a
config in which effort routing could not work at all.

## Validation

```bash
python3 -m py_compile scripts/probe_routing_pool.py
python3 scripts/probe_routing_pool.py --self-check --prefix <prefix>   # expect exit 0 or 1 with a reason
python3 scripts/public_hygiene_check.py
```

Prove the gate can fail before trusting a pass — mutate a config in a temp file and point
`JEV_ROUTING_CONFIG` at it:

```bash
printf '{"tiers":{"simple":{"general":["zzz:g"]}},"sticky_context_tokens":50000,"effort":{"enabled":true,"levels":["low","high"]}}' > /tmp/bad.json
JEV_ROUTING_CONFIG=/tmp/bad.json python3 scripts/probe_routing_pool.py --self-check --prefix zzz; echo "exit=$?"   # expect 1
```

## Scope and limits

- Requires the `hermes-jev` plugin on disk (`--plugin-dir`). The offline mode imports its
  `jevkit.route` / `jevkit.effort` modules directly and makes no paid call.
- Live probes make real upstream calls: one per model per effort level, plus tool-call and
  optional vision probes. On a per-request-billed relay that is a small but real charge.
- Vision probing needs Pillow. Without it the check reports `vision_ok: null` rather than
  guessing from a model name — name-based guesses were wrong in both directions on the
  fleet this was written against.
- Nothing here decides *which* models belong in a pool. That is a measurement (price,
  tool calling, effort acceptance, context size); `SKILL.md` Rule 4 lists the four probes.
