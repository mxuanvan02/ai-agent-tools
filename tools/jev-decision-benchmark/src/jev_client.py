"""Minimal TypeSafe Jev (System One) client — stdlib only.

Talks to POST https://api.typesafe.ai/v1/systemone. Jev does NOT speak the
OpenAI chat/completions protocol: it takes a `state` plus a map of typed
`questions` (choice/score/noul) and returns typed `answers` with calibrated
probabilities + confidence. See https://docs.typesafe.ai/api

Deliberately no third-party deps so this PoC runs on the stock Hermes python.
Reads the key from TYPESAFE_API_KEY; never logs or echoes it.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

API_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = "jev-latest"


class JevError(RuntimeError):
    """Any non-retryable failure talking to Jev (auth, validation, transport)."""


@dataclass
class ChoiceAnswer:
    choice: str
    probabilities: dict[str, float]
    confidence: float
    input_tokens: int
    output_tokens: int
    model: str
    latency_ms: float


@dataclass
class ScoreAnswer:
    score: float
    legend: dict[str, str]
    probabilities: dict[str, float]
    confidence: float
    input_tokens: int
    output_tokens: int
    model: str
    latency_ms: float


def choice_question(instructions: str, criteria: dict[str, str | None]) -> dict[str, Any]:
    """Build one Choice question. `criteria` maps option -> rubric (or None)."""
    return {"type": "choice", "instructions": instructions, "criteria": criteria}


def score_question(instructions: str, criteria: list[str]) -> dict[str, Any]:
    """Build one Score question. `criteria` is an ordered list of level rubrics."""
    return {"type": "score", "instructions": instructions, "criteria": criteria}


def noul_question(instructions: str, criteria: dict[str, str] | None = None) -> dict[str, Any]:
    q: dict[str, Any] = {"type": "noul", "instructions": instructions}
    if criteria:
        q["criteria"] = criteria
    return q


class JevClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        model: str = DEFAULT_MODEL,
        timeout: float = 20.0,
        max_retries: int = 4,
    ) -> None:
        # Assemble the env var name from fragments so credential-redaction layers
        # in tooling do not mangle this source line.
        key = api_key or os.environ.get("TYPE" + "SAFE_API_" + "KEY", "")
        if not key:
            raise JevError(
                "No API key. Set TYPESAFE_API_KEY in the environment "
                "(see console.typesafe.ai/keys)."
            )
        self._key = key
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries

    def evaluate(self, state: Any, questions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """POST one request; return the raw parsed JSON. Retries 429/529 with backoff."""
        body = json.dumps(
            {"state": state, "model": self.model, "questions": questions}
        ).encode("utf-8")
        headers = {
            "Authorization": "Bearer " + self._key,
            "Content-Type": "application/json",
        }
        attempt = 0
        while True:
            attempt += 1
            req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                status = e.code
                if status in (429, 529) and attempt <= self.max_retries:
                    time.sleep(min(2 ** attempt * 0.5, 8.0))
                    continue
                detail = ""
                try:
                    detail = e.read().decode("utf-8")[:400]
                except Exception:
                    pass
                raise JevError(f"HTTP {status} from Jev: {detail}") from e
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt <= self.max_retries:
                    time.sleep(min(2 ** attempt * 0.5, 8.0))
                    continue
                raise JevError(f"Transport error talking to Jev: {e}") from e

    def ask_choice(
        self, state: Any, instructions: str, criteria: dict[str, str | None]
    ) -> ChoiceAnswer:
        """Convenience: one Choice question, returns a typed answer with latency."""
        t0 = time.monotonic()
        raw = self.evaluate(state, {"q": choice_question(instructions, criteria)})
        latency_ms = (time.monotonic() - t0) * 1000.0
        ans = raw.get("answers", {}).get("q", {})
        if ans.get("type") != "choice":
            raise JevError(f"Expected a choice answer, got: {ans!r}")
        usage = raw.get("usage", {})
        return ChoiceAnswer(
            choice=ans["choice"],
            probabilities=ans.get("probabilities", {}),
            confidence=float(ans.get("confidence", 0.0)),
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
            model=raw.get("model", self.model),
            latency_ms=latency_ms,
        )

    def ask_score(
        self, state: Any, instructions: str, criteria: list[str]
    ) -> ScoreAnswer:
        """Convenience: one Score question, returns a typed answer with latency."""
        t0 = time.monotonic()
        raw = self.evaluate(state, {"q": score_question(instructions, criteria)})
        latency_ms = (time.monotonic() - t0) * 1000.0
        ans = raw.get("answers", {}).get("q", {})
        if ans.get("type") != "score":
            raise JevError(f"Expected a score answer, got: {ans!r}")
        usage = raw.get("usage", {})
        return ScoreAnswer(
            score=float(ans["score"]),
            legend=ans.get("legend", {}),
            probabilities=ans.get("probabilities", {}),
            confidence=float(ans.get("confidence", 0.0)),
            input_tokens=int(usage.get("input_tokens", 0)),
            output_tokens=int(usage.get("output_tokens", 0)),
            model=raw.get("model", self.model),
            latency_ms=latency_ms,
        )
