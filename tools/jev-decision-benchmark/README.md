# jev-decision-benchmark

Evidence-first harness to decide whether **TypeSafe Jev** (System One) should replace an
**LLM** at a specific decision point in an agent harness (built against Hermes, reusable
anywhere). Everything here is backed by real API runs, not marketing claims.

Jev takes unstructured `state` + typed `questions` and returns typed probabilistic answers
(`choice` / `score` / `noul`) with calibrated confidence. It does **not** generate text — a
poor chatbot, an excellent function call for routing, gating, scoring, and action selection.

## Headline finding (measured, head-to-head vs Qwen3.8-max)

Jev and LLMs win **different gate shapes** — do not generalize one result:

| Gate | Winner | Evidence |
|---|---|---|
| **Guardian** (atomic decision, hot path) | **Jev** | latency 957ms vs 14.4s/call, ~40% fewer tokens, accuracy 0.833 vs 0.80, 0 dangerous-miss |
| **Monitor/triage** (batch scoring, broad context) | **LLM** | MAE 0.85 vs 1.22, ~3x fewer tokens (one batch call vs N Jev calls) |

Rule of thumb: **per-item small judgment on a latency-sensitive path → Jev; batch scoring
that needs broad context → LLM.** Always confirm with numbers on your own data.

> The "~150ms / ~100x cheaper" figures from TypeSafe marketing did NOT hold here: measured
> Jev latency is 957ms–2.55s per call and, for batchable work, Jev costs *more* tokens than
> one LLM batch call. Jev's real edge is decision quality (typed + calibrated) and low
> per-call latency on hot paths — not raw speed or cost.

## Layout

- `src/jev_client.py` — stdlib client for `POST /v1/systemone` (retry 429/529). Reads `TYPESAFE_API_KEY`.
- `src/guardian.py` — shell-approval guardian: Jev danger-**Score** + threshold gate,
  prompt-injection hardening (strip comments, wrap `<command>`, operator policy in a TRUSTED
  field). Fail-closed = escalate.
- `src/baseline.py` — pure pattern matcher (manual-mode floor) for comparison.
- `src/baseline_llm.py` — LLM guardian arm replicating Hermes `tools/approval_smart.py` verbatim.
- `src/mock_jev.py` — offline simulator seeded from gold labels. **Proves the code runs only;
  never report its numbers as Jev results.**
- `src/run_benchmark.py` — pattern vs Jev (mock or `--real`).
- `src/run_guardian_3way.py` — pattern vs LLM vs Jev, full head-to-head.
- `src/test_guardian.py` — offline behavior tests (no pytest needed).
- `monitor/` — the batch-scoring gate (`run_monitor_bench.py` = Jev + LLM; `run_baseline_omni.py` = LLM arm).
- `data/commands.jsonl`, `monitor/items.jsonl` — labeled datasets (safe / dangerous / ambiguous / injection).
- `DECISION.md` — the worked conclusion, including the live Jevbridge MCP integration.

## Run

```bash
# offline behavior tests + logic smoke test (no key needed)
python3 src/test_guardian.py
python3 src/run_benchmark.py            # mock backend

# live Jev
export TYPESAFE_API_KEY=...
python3 src/run_benchmark.py --real
python3 src/run_guardian_3way.py        # LLM arm reads providers.omniproxy from Hermes config

# LLM baselines read the Hermes config path from $HERMES_CONFIG
# (default ~/.hermes/config.yaml); set it if yours lives elsewhere.
```

## Key metrics

- **dangerous_miss** (gold=deny scored approve): any value > 0 is a release blocker.
- **precision** on surfacing / **false_deny**: false positives that annoy or block valid work.
- Mock numbers look near-perfect because they are seeded from gold — a smoke test, not a result.

## Integration (verified)

The shipping path is **Jevbridge** (github.com/tacticocc/Jevbridge, MIT) as an MCP server —
Hermes' native MCP client picks up `jev_decide` / `jev_gate` / `jev_computer_use` / `jev_recipe`
with zero core changes. Verified live end-to-end; see `DECISION.md` §7. Two cautions: Jevbridge
has no prompt-injection hardening (sanitize state first), and never let the safety path fall
back to its keyword `heuristic` backend (force `backend: "jev"`).

## License

MIT. TypeSafe Jev and Jevbridge are separate third-party products under their own licenses.
