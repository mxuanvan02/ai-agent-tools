# Relay field notes

Measurement recipes and failure shapes that do not belong in `SKILL.md`'s rule list.
Everything here was observed on a live fleet; nothing is inferred from upstream source.

## Reading prices from a one-api style upstream

`GET <upstream>/api/pricing` returns one billing rule per model. Two fields decide
everything about pool order:

- `quota_type` — `2` means billed per request; a per-token model has `0`/`1` with ratios.
- `model_price` — USD per call when `quota_type` is per-request.

```bash
curl -s "$UPSTREAM/api/pricing" -H "Authorization: ***" | python3 -c '
import json,sys
for r in json.load(sys.stdin)["data"]:
    print(f"{r[\"model_name\"]:28s} quota_type={r.get(\"quota_type\")} price={r.get(\"model_price\")}")'
```

Observed spread on one relay: the cheapest model was **150× cheaper per request** than the
most expensive, and the model already in daily use sat in the cheap group — so the assumed
savings from routing "down" did not exist, while one candidate that looked like a fast tier
was the most expensive in the pool.

## Why effort routing saves nothing under per-request billing

Per-request billing charges the call, not the tokens. Lowering `reasoning_effort` reduces
thinking tokens and therefore latency, but the invoice is identical. State this plainly
when reporting: it buys seconds, not cents. The only lever that saves money is choosing a
cheaper model, which is why pool order comes from measured prices.

## The `medium`-only HTTP 500

A relay can accept `low`, `high` and `max` for one model and answer `HTTP 500` for
`medium`, with no error text explaining why. Observed on two different models in the same
pool, and on a third model that rejected **every** level. Consequences:

- Probe every level on every pool model. Do not extrapolate from a sibling model or from
  the same model's other levels.
- Declare only measured levels in `effort.models`.
- A model that rejects every level must have **no** caps entry at all. The middleware gate
  is `isinstance(supported, list) and supported`, so an absent key and an empty list both
  suppress the field — but absence is what the gate was written for.

Transient upstream errors look identical. A `500` whose body is an HTML document
(`<!DOCTYPE html>`) is a gateway/CDN page, not a model rejection; retry two or three times
before recording the level as unsupported.

## The cache-boundary off-by-one

`decide()` guards on `context_tokens > threshold` (strict). If the cache key's notion of
"over the guard" uses `>=`, the two disagree exactly at the threshold, and because context
is bucketed the mismatch lets a cached sub-guard SWITCH answer an over-guard turn.

The failure is invisible in a single-shot dry run: probing `threshold-1`, `threshold`,
`threshold+1` and one large value in that order shows the guard working, because the large
value lands in a different bucket. It appears in a real session that grows through the
threshold one turn at a time.

Test the boundary as a sequence over the **same prompt**, and assert the strict semantics:
switching at exactly `threshold` is correct; only strictly above must be blocked.

## Vision probing: the digit read-back

Generate an image containing one known digit and require the model to return it. This
catches both directions of a name-based guess:

- a `-max` variant answered `"T"` for a drawn `7` (blind), while its `-flash` sibling read
  it correctly;
- another model returned HTTP 200 with an empty `content` and burned its completion budget
  on hidden thinking.

For the empty-content case, read `usage.completion_tokens` before declaring a model dead:
when `completion_tokens == max_tokens` the model is alive and merely truncated. Raise the
cap and probe again.

## Large-context probes: assert the size you sent

Build the filler once and reuse the exact same string for every model in a comparison.
Two runs of a "190k token" probe differed by 5× in `usage.prompt_tokens` (397k vs 81k)
because the filler was regenerated from a different repetition count, which made the
latency verdict meaningless. Read `usage.prompt_tokens` from both responses and require
them to be close before comparing anything.

A related trap: probing a failure threshold with `max_tokens` small enough that every call
finishes in seconds never enters the failure region at all. Reproduce the failure first,
then vary one dimension.

## Auditing the audit

A self-audit script that reports FAIL must have its own check verified. Two false alarms
each cost more time than the real defects they reported:

- comparing a local rebuild's sha256 with a binary built on another machine (different Go
  toolchain, different VCS stamp) can never match, even from identical source;
- passing the *directory* containing a binary to a symbol-inspection tool instead of the
  binary itself always reads "symbol absent".

Re-run any surprising fact three independent ways — symbol table, behavioural probe, and a
second tool — before acting on it. Equally: a pipeline's `$?` reports the last command
(`tail`), not the program under test. Read exit codes without a pipe.

## Deploy-path collisions

A relay binary can be replaced by a second deploy path (a sync script on another machine)
while work is in progress. After any deploy, verify the patch is still in the **live**
binary:

```bash
go tool nm "$BIN/<binary>" | grep <patch_symbol>
go version -m "$BIN/<binary>" | head -5      # toolchain + VCS stamp: whose build is this?
```

plus one behavioural probe. A symbol proves compilation; only the probe proves routing.
When the source tree has no `.git`, keep the change as a portable `.diff` and archive the
test file beside it, so the patch survives a redeploy from elsewhere.
