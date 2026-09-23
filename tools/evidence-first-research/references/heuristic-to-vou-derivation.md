# Upgrading a heuristic scoring term into a theory-grounded VoI/VoU object

Reusable pattern for người dùng's Q1 rigor ("DERIVE-then-verify, never grid-search
for pretty numbers"). Triggered when a reviewer calls a scoring rule a "thin
heuristic" or an ablation shows a term is redundant/harmful.

## The trigger

An ablation zeroed out one term of a weighted-sum urgency/utility score and the
result got BETTER on every metric (objective, missed-events, and even the tail
CVaR/VaR). That is not noise — it means the term is either double-counted
elsewhere or points the wrong way. Reporting "every term contributes" would be a
fabricated-clean ablation; report the inversion honestly instead.

## The diagnosis (why raw probability terms misbehave)

A term `w * p_vio` (raw violation probability) inside a selection/urgency score
is usually wrong because:
- **Decision value ≠ probability.** Polling/measuring has value only if a fresh
  reading can CHANGE the downstream decision. When `p→1` the detector already
  fires, so an extra measurement carries ~zero decision value — yet `w*p` ranks
  it highest, i.e. maximal priority exactly where true value is lowest.
- **Double counting.** If the loss/detection function already uses the same `p`
  (e.g. `p >= threshold` flags a violation inside `eval_step`), then `p` appears
  twice and biases selection.

## The derivation (leading-order value-of-information)

For a binary decision (safe / violation), the Bayes-optimal leading-order
value-of-information is the **decision uncertainty**:

    g(p) = p(1-p)          (scaled to [0,1] as 4·p(1-p))
    or    H(p) = -p log2 p - (1-p) log2(1-p)   (binary entropy)

Both peak at the decision boundary p≈0.5 and vanish as p→0 or p→1. This is
"value-of-uncertainty" (VoU): pay to measure where the outcome is genuinely in
doubt, not where it is already certain. Defensible under người dùng's contract as
"leading-order truncation of a Bayes-optimal object with explicit regime
condition."

## Verify (this session's real numbers, severe-burst, N=3 real data)

Swapping `0.55*p_vio` → `0.55*4p(1-p)` in the urgency score, keeping deviation +
AoI terms and all baselines unchanged:

| urgency form | Obj ↓ | Missed% ↓ | CVaR95 ↓ |
|---|---|---|---|
| p_vio (original) | 0.1766 | 1.79 | 1.3445 |
| drop risk (2-term) | 0.1591 | 1.54 | 1.2034 |
| **VoU 4p(1-p)** | **0.1511** | **1.03** | **0.9465** |
| binary entropy | 0.1516 | 1.05 | 0.9580 |

Result: objective −14%, missed −42%, tail CVaR −30% simultaneously. Story upgrade
from "Pareto trade-off" to "dominates all feasible baselines at half bandwidth",
AND a redundant heuristic became a theory-grounded term — this answers multiple
reviewer objections at once (thin heuristic, missed-violation trade-off, weak
ablation).

## Guardrails when introducing VoU across a paper family

- If a SIBLING manuscript already uses VoU (e.g. a CAW paper), add one sentence
  in related-work distinguishing the two uses to avoid self-overlap flagged when
  both are in review. Confirm with người dùng; he may accept overlap since both are
  his.
- Adjust title/keywords to reflect the new mechanism if the scoring rule is a
  headline contribution.
