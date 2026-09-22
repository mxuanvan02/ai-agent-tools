"""A stand-in for JevClient used ONLY to prove the guardian + benchmark logic
runs end-to-end without a real API key. It is a heuristic simulator, NOT Jev:
the real numbers must come from the live API (see run_benchmark.py --real).

It fabricates a plausible calibrated distribution from the same gold label the
dataset carries, plus a little noise, so we can watch confidence-gating,
escalate routing, and the scorecard behave. Because it is seeded from the gold
answer it will look near-perfect — that is the point of a mock, and exactly why
it cannot be reported as a Jev result.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from jev_client import ChoiceAnswer, ScoreAnswer


@dataclass
class _MockCfg:
    # How often the mock deliberately hedges on the genuinely ambiguous rows,
    # so the confidence gate has something to act on.
    hedge_on_escalate: bool = True


class MockJevClient:
    """Same surface as JevClient.ask_choice, distribution derived from `_gold`."""

    def __init__(self, gold_by_command: dict[str, str], cfg: _MockCfg | None = None) -> None:
        self._gold = gold_by_command
        self.cfg = cfg or _MockCfg()

    def ask_choice(self, state, instructions, criteria) -> ChoiceAnswer:  # noqa: ANN001
        command = state.get("command", "") if isinstance(state, dict) else str(state)
        gold = self._gold.get(command, "escalate")
        # Deterministic pseudo-noise per command so runs are reproducible.
        h = int(hashlib.sha256(command.encode()).hexdigest(), 16)
        jitter = (h % 20) / 100.0  # 0.00–0.19

        if gold == "approve":
            p_app = 0.90 - jitter
            p_deny = jitter * 0.3
        elif gold == "deny":
            p_app = jitter * 0.2
            p_deny = 0.92 - jitter
        else:  # escalate — mock hedges between approve and deny
            p_app = 0.45 + (jitter - 0.10) if self.cfg.hedge_on_escalate else 0.2
            p_deny = 0.40 - (jitter - 0.10)

        p_app = max(0.0, min(1.0, p_app))
        p_deny = max(0.0, min(1.0, p_deny))
        p_esc = max(0.0, 1.0 - p_app - p_deny)
        total = p_app + p_deny + p_esc or 1.0
        probs = {
            "approve": round(p_app / total, 4),
            "deny": round(p_deny / total, 4),
            "escalate": round(p_esc / total, 4),
        }
        choice = max(probs, key=probs.get)  # type: ignore[arg-type]
        top = probs[choice]
        runner = sorted(probs.values(), reverse=True)[1]
        confidence = round(min(1.0, top + (top - runner) * 0.5), 4)
        return ChoiceAnswer(
            choice=choice,
            probabilities=probs,
            confidence=confidence,
            input_tokens=120,
            output_tokens=20,
            model="mock-jev",
            latency_ms=1.0,
        )

    def ask_score(self, state, instructions, criteria) -> ScoreAnswer:  # noqa: ANN001
        """v2 danger-score mock: map gold -> a point on the 0..3 danger scale."""
        command = state.get("command", "") if isinstance(state, dict) else str(state)
        gold = self._gold.get(command, "escalate")
        h = int(hashlib.sha256(command.encode()).hexdigest(), 16)
        jitter = (h % 20) / 100.0  # 0.00–0.19
        if gold == "approve":
            score = 0.2 + jitter
            conf = 0.95 - jitter
        elif gold == "deny":
            score = 2.8 + (jitter * 0.5)
            conf = 0.95 - jitter
        else:  # escalate -> the consequential middle band, less certain
            score = 1.7 + (jitter - 0.10)
            conf = 0.5 + jitter
        score = max(0.0, min(3.0, score))
        n = len(criteria)
        probs = {str(i): 0.0 for i in range(n)}
        lo = int(score)
        hi = min(lo + 1, n - 1)
        frac = score - lo
        probs[str(lo)] = round(1 - frac, 4)
        probs[str(hi)] = round(frac, 4) if hi != lo else probs[str(lo)]
        legend = {str(i): criteria[i] for i in range(n)}
        return ScoreAnswer(
            score=round(score, 3),
            legend=legend,
            probabilities=probs,
            confidence=round(min(1.0, conf), 4),
            input_tokens=120,
            output_tokens=18,
            model="mock-jev",
            latency_ms=1.0,
        )
