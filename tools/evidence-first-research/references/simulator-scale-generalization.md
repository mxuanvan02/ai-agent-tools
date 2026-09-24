# Generalizing a fixed-size simulator to larger N (and the regime-flip risk)

Trigger: người dùng wants a paper's scale changed (e.g. "N=3 vs manuscript says N=30
— make it N=30 real"). This is a research-design decision with an expensive,
one-shot re-run, so GATE it before running full.

## First: is the claimed N even materializable from the data?

Read the dataset before promising N. If the raw data has only K real traces
(e.g. greenhouse dataset = 3 `loop` ids), there is NO honest way to get "30
independent real sensors". Any N>K is semi-synthetic and MUST be disclosed.
Present the honest options to người dùng and let him choose — do not silently
bootstrap and call it real:
- **A — match the code (N=K), honest framing.** Rewrite narrative to "K monitored
  zones", drop any "B << N / dense field" claim. No re-run, numbers unchanged,
  story smaller. (In the session người dùng first leaned A, then after seeing the
  N=30 numbers flip, chose C3 = back to A.)
- **B — expand to N>K semi-synthetically.** Honest design: N virtual sensors in K
  groups, each replaying one real trace through an independent random time offset
  + independent Gilbert-Elliott channel, keeping every (x, mu, p, v) a real
  measured tuple (no fabricated readings). Declare "derived from K measured traces"
  in the manuscript.
- **C — keep N but change the paper's thesis** to whatever the data actually shows
  (often a negative/regime result).

## The N-scaling constant pitfall (this is the core lesson)

When you parametrize `range(K)` -> `range(N)`, additive per-budget penalty
constants silently mis-scale. An objective like `loss + 0.04*B + 0.015*aoi`:
at small N each served sensor cuts loss by ~1/N (big at N=3), but the `0.04*B`
cost is absolute. At large N the per-sensor benefit shrinks while the cost stays,
so the Oracle/lower-bound looks WORSE than the heuristic — a tell that scaling,
not logic, is broken. Fix with a principled coverage-fraction rescale:
`BW_SCALE = K/N` applied to every per-B penalty term (=1 at N=K, preserving the
original calibration). Also normalize AoI by served fraction. Diagnose from the
symptom (oracle inverts, age-based dominates) — don't fudge constants to force a
pretty result; that is fabrication.

## Smoke results are NOT evidence — and the narrative can flip

Per the skill's existing rule, a 3-window/few-seed smoke only catches bugs.
Concretely this session: smoke N=30 hinted the proposed method lost; full N=320
(16 windows x 20 seeds) + paired Wilcoxon CONFIRMED it lost decisively
(p<1e-50, r=-0.87) because the regime changed (B/N coverage 7-27% => tracking
error dominates risk timing; saturated p-distribution kills risk discrimination).
ALWAYS run full N + Wilcoxon before letting scale results rewrite the thesis, and
report the honest outcome to người dùng rather than tuning to rescue the method.

## Mechanics that worked

- Back up code AND CSVs before the re-run (`code/_backups/<ts>/`,
  `outputs/_backup_N3_<ts>/`) so reverting to the original scale is one `cp`.
- Generalize the base simulator (`range(K)`->`range(N)`, budget set, AoI norm);
  `importlib`-loaded sibling scripts (nonstationary, weight-sweep) inherit it —
  patch their own hardcoded `range(K)` / `/K` divisors too.
- For a drift/non-stationary variant, monkeypatch `M.channel` and register a
  virtual network key rather than duplicating the whole run loop.
- `random.Random()` does NOT accept a tuple seed — use an int hash of the key.
