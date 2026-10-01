---
name: jev-routing-relay-ops
description: "Use when Jev model/effort routing runs through a local relay that fronts several upstream accounts. Verify the wire, not the config: catalog-unknown refs, per-request billing, capability probes, and guard/cache correctness."
metadata:
  version: "1.0.0"
  license: "MIT"
  status: active
  default_on: false
  related: "jev-model-routing; system-one-work-loop; evidence-verified-auditing"
---

# Jev Routing Through a Local Relay

> A local relay (one OpenAI-compatible endpoint fronting many upstream accounts) breaks
> three assumptions Jev routing makes: the models.dev catalog knows every model, price
> ordering equals cost ordering, and the wire carries every field the config declares.
> This skill is the verification discipline for that setup. It does **not** replace
> `jev-model-routing`; it covers what that skill cannot know about a relay.

## When this applies

The provider in `config.yaml` is a `custom`/self-hosted endpoint, and pool refs use a
prefix the models.dev catalog has never heard of (`omniproxy:*`, `myrelay:*`, …). Confirm
before trusting any routing behaviour:

```bash
python3 -c "
import sys; sys.path.insert(0, '<plugins>/hermes-jev')
from jevkit import route
rows = route._by_ref(None) or {}
print('catalog rows:', len(rows))
print('providers in catalog:', sorted({k.split(':')[0] for k in rows})[:12])
"
```

If the relay prefix is absent, every "Guarantee" below that depends on catalog data is
**inert**, not merely suboptimal.

## Rule 1 — verify the wire, never the config

A relay that parses requests into typed structs silently discards unknown fields. A
`reasoning_effort` the router sets can vanish before the upstream sees it, while every
config file reads correct.

Prove forwarding behaviourally: send two levels of the same parameter and measure
something that must differ — `usage.completion_tokens` (hidden thinking counts toward it)
or reasoning-token counts. Equal numbers mean the field was dropped.

```bash
# Discriminator, not a ping: thinking tokens land in completion_tokens.
for lvl in none high; do
  curl -s "$BASE/v1/chat/completions" -H "Authorization: ***" -H 'content-type: application/json' \
    -d "{\"model\":\"$M\",\"max_tokens\":6000,\"reasoning_effort\":\"$lvl\",
         \"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}]}" \
    | python3 -c "import json,sys; u=json.load(sys.stdin)['usage']; print(u)"
done
```

Then read the relay's request struct and confirm the field exists **on the protocol path
in use**. A relay may forward it on one wire (Anthropic Messages) and drop it on another
(OpenAI chat completions) — the two paths often have separate structs.

## Rule 2 — per-request billing inverts the cost model

If the relay's upstream bills **per request** (one-api `model_price`, a flat fee per
call), then effort/reasoning levels save **nothing**; only switching to a cheaper model
saves money. Effort routing then buys latency, not cost — say so plainly instead of
reporting savings.

Read real prices from the upstream, never from a model name:

```bash
curl -s "$UPSTREAM/api/pricing" -H "Authorization: ***" | \
  python3 -c "import json,sys; [print(r['model_name'], r.get('model_price')) for r in json.load(sys.stdin)['data']]"
```

Order each tier pool by that price. Expect surprises: a `-flash` name can cost more than
the flagship, and the model already in use may be among the cheapest.

## Rule 3 — catalog-unknown refs disable two guards

| Guard | Depends on | Behaviour with an unknown ref |
|---|---|---|
| Context fit (`row["context"]`) | catalog row | never checked — an oversized session can be routed anywhere |
| Large-context sticky (price comparison) | `row["price"]` | comparison skipped, so the guard never fires |
| Vision pool (`row["vision"]`) | catalog row | ref skipped ⇒ pool resolves to `None` ⇒ turn keeps current model |

Consequences to design for, not to discover:

- A `vision` pool of relay refs is **inert**. Harmless when the main model has vision,
  but it must never be reported as "fixed" on the strength of an edit alone.
- The sticky guard needs an explicit patch for unknown refs (fail safe = keep the current
  model), or large sessions keep switching onto a cold cache.
- Verify with the function the middleware calls, not with a config read:

```python
route._pick(cfg, route._by_ref(None) or {}, "simple", "general", need_vision, ctx, "relayprefix")
```

## Rule 4 — probe capability per model, per level

Nothing about a model's abilities can be inferred from its name. Four probes, all cheap:

1. **Tool calling** — send one tool definition, assert `finish_reason == "tool_calls"` and
   a well-formed argument object. A model that cannot call tools breaks every agent turn.
2. **Reasoning-effort acceptance** — each level individually. Relays commonly answer
   `HTTP 500` for one level (`medium`) and `200` for its neighbours. Declare only
   measured levels in `effort.models`; a model that rejects every level must have **no**
   caps entry, so the field is never sent.
3. **Vision** — draw a known digit into a generated image and require the model to read it
   back. Name-based guesses fail in both directions: a `-max` variant can be blind while
   its `-flash` sibling sees, and a blind model inside a vision pool breaks image turns.
4. **Large context** — only if Rule 3's context guard is inert. Read `usage.prompt_tokens`
   from the response to prove the size actually sent.

Record results as a table with the probe date. Upstream quota state moves hourly: a model
that answered at 09:00 can return `402 insufficient_quota` / `429` by noon, and the pool
then routes turns to a dead seat. Re-probe when turns start failing rather than trusting
an earlier run.

## Rule 5 — the runtime provider label may not be the configured name

Read it from the decision log's `from` / `decision_model` field, not from `config.yaml`:

```bash
grep route_effective "$HERMES_HOME/logs/jev-decisions.jsonl" | tail -3
```

A `provider_aliases` entry maps the label for **pool matching**, but `effort.models` keys
are built with the plugin's own alias table. Declare caps under the label the log shows
(and, when in doubt, under both), or the effort branch silently does nothing.

## Rule 6 — decisions are cached per turn and per context bucket

- A turn's routing decision is computed once and reused for every tool-loop request.
  Editing routing.json mid-turn only takes effect on the **next** turn; log lines inside
  the old turn keep the old reason.
- The decision cache buckets context size. A bucket straddling `sticky_context_tokens`
  lets a cached sub-guard SWITCH answer an over-guard turn — a session growing past the
  threshold keeps switching models. The cache key must carry the guard's own boundary,
  and its comparison must match the guard's exactly (`>` vs `>=` is the whole bug).
- Test boundaries explicitly: `threshold-1`, `threshold`, `threshold+1`, and one large
  value. Only the strict-above case may be blocked.

## Rule 7 — a relay binary can be replaced by a second deploy path

A sync script on another machine can overwrite the deployed binary mid-session. After any
deploy, prove the patch is still in the **live** binary, two independent ways:

```bash
go tool nm "$BIN/omniproxy" | grep <patch_symbol>     # symbol present
# plus one behavioural probe (Rule 1) — a symbol alone proves compilation, not routing
```

Compare against the binary's own build metadata (`go version -m <binary>`) to tell your
build from someone else's. Keep the patch as a portable `.diff` when the source tree has
no git, and archive the test file beside it.

## Rule 8 — audit the audit

A self-audit script that reports FAIL must have its own check verified before the finding
is believed. Two false alarms cost more time than the real bugs here:

- Comparing a local rebuild's hash to a binary built elsewhere (different toolchain and
  VCS stamp) can never match.
- Passing a **directory** to a binary-inspection tool instead of the binary always reads
  "symbol absent".

Re-run the same fact three independent ways before acting on a FAIL. Equally: when two
models' latencies are compared, assert `prompt_tokens` were equal — a filler built by
string repetition can differ several-fold between runs, which makes any latency verdict
worthless. Discard the conclusion rather than softening it.

## Verification checklist

Run all five; "config written" is not evidence for any of them.

1. `route.load_config()` reflects the edit (config is re-read per request).
2. Dry-run `route.decide(...)` for trivial / routine / hard / large-context / image turns
   and print tier, routed, model, and the effort the middleware would apply.
3. Plugin files compile (`python -m py_compile`), and code-level patches need a gateway
   restart to load — config edits do not.
4. One live turn produces a `route` + `effort` pair in the decision log matching the
   dry-run.
5. The relay forwards the parameter (Rule 1) on the protocol path in use.

## Secrets

Probe scripts must never print a credential, and work files must not hold one. Read the
key at runtime from the relay's config or an env var, and delete scratch auth files after
the run. Scan the work directory for the live key before finishing:

```bash
python3 scripts/probe_routing_pool.py --base-url http://localhost:PORT/v1 --models m1,m2 --self-check
```

`--self-check` runs the offline parts (catalog presence, guard behaviour, cache-key
boundaries) with no network and no key.
