"""Declarative page/form state machine: figure out "which step am I on?" from URL + visible signals.

Pattern extracted and generalised from code-root/gmail-account-creator `src/gmail/page-detector.js`,
whose idea is genuinely good even though its implementation is hardwired to Gmail signup steps:
match URL patterns FIRST (cheapest, most reliable), fall back to presence of named elements,
and return a typed state {name, signals, suggested_action} instead of a boolean per step.

That is exactly the checklist-driven design used by ~/opt/jev-exec-bench/jev_form_driver.py,
made reusable: declare your steps as data, then drive them. This module is transport-agnostic —
you supply two small callables (current URL, element-presence probe) so it works with Playwright,
Selenium, raw CDP, or a recorded HTML fixture in tests.

Usage:
    machine = PageStateMachine([
        PageState("login", url_contains=["/login"], elements=["#email", "#password"]),
        PageState("otp",   url_contains=["/challenge"], elements=["input[name=code]"]),
        PageState("home",  url_contains=["/dashboard"], elements=["[data-testid=user-menu]"]),
    ], fallback=PageState("unknown"))
    state = machine.detect(url=page.url, elements_present=lambda sel: page.locator(sel).count() > 0)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class PageState:
    """One step/screen of a flow.

    url_contains: substrings matched case-insensitively against the current URL (cheap signals).
    url_matches:  callables url->bool for anything a substring cannot express.
    elements:     selector strings that must ALL be present for this state (strong evidence).
    any_elements: selector strings where at least ONE must be present (weak evidence).
    priority:     tie-breaker when several states match; higher wins.
    action:       opaque hint for the caller's driver (e.g. 'fill_credentials', 'wait').
    """
    name: str
    url_contains: Sequence[str] = ()
    url_matches: Sequence[Callable[[str], bool]] = ()
    elements: Sequence[str] = ()
    any_elements: Sequence[str] = ()
    priority: int = 0
    action: str = ""
    meta: dict = field(default_factory=dict, compare=False)


@dataclass(frozen=True)
class Detection:
    state: str
    action: str
    url_matched: tuple[str, ...]
    elements_found: tuple[str, ...]
    score: int
    meta: dict = field(default_factory=dict)

    @property
    def confident(self) -> bool:
        """True when the state was identified by evidence, not by fallback."""
        return self.score > 0


class PageStateMachine:
    # scoring weights: URL evidence is cheaper but weaker than actually seeing the controls
    W_URL_SUBSTR = 2
    W_URL_MATCH = 3
    W_ELEMENT = 5
    W_ANY_ELEMENT = 3

    def __init__(self, states: Iterable[PageState], *, fallback: PageState | None = None):
        self._states = list(states)
        names = [s.name for s in self._states]
        if len(set(names)) != len(names):
            raise ValueError("duplicate state names: " + ", ".join(n for n in names if names.count(n) > 1))
        self._fallback = fallback or PageState("unknown")

    @property
    def state_names(self) -> list[str]:
        return [s.name for s in self._states] + [self._fallback.name]

    def detect(self, *, url: str, elements_present: Callable[[str], bool]) -> Detection:
        """Classify the current page. elements_present(selector)->bool is the only DOM hook,
        so tests can pass a dict lookup and never open a browser."""
        url_l = (url or "").lower()
        best: tuple[int, PageState, list[str], list[str]] | None = None
        for st in self._states:
            score, hit_urls, hit_els = 0, [], []
            for sub in st.url_contains:
                if sub.lower() in url_l:
                    score += self.W_URL_SUBSTR
                    hit_urls.append(sub)
            for fn in st.url_matches:
                if fn(url or ""):
                    score += self.W_URL_MATCH
                    hit_urls.append("<matcher>")
            required_ok = True
            for sel in st.elements:
                if elements_present(sel):
                    score += self.W_ELEMENT
                    hit_els.append(sel)
                else:
                    required_ok = False  # declared as ALL-present evidence
            if st.elements and not required_ok:
                continue  # a required element is missing -> not this state
            if st.any_elements:
                found_any = False
                for sel in st.any_elements:
                    if elements_present(sel):
                        score += self.W_ANY_ELEMENT
                        hit_els.append(sel)
                        found_any = True
                if not found_any:
                    continue
            if score == 0:
                continue  # no evidence at all
            if best is None or (score, st.priority) > (best[0], best[1].priority):
                best = (score, st, hit_urls, hit_els)
        if best is None:
            return Detection(self._fallback.name, self._fallback.action, (), (), 0,
                             dict(self._fallback.meta))
        score, st, hit_urls, hit_els = best
        return Detection(st.name, st.action, tuple(hit_urls), tuple(hit_els), score, dict(st.meta))

    def wait_for(self, *, state_name: str, poll: Callable[[], Detection],
                 attempts: int = 50, sleep_fn: Callable[[float], None] | None = None,
                 interval: float = 0.2) -> Detection | None:
        """Poll until the machine reports `state_name`, or give up after `attempts` polls.
        sleep_fn is injectable so tests run instantly."""
        import time
        nap = sleep_fn or time.sleep
        last: Detection | None = None
        for _ in range(max(1, attempts)):
            last = poll()
            if last.state == state_name:
                return last
            nap(interval)
        return last


def detect_transitions(history: Sequence[Detection]) -> list[tuple[str, str]]:
    """[(from, to)] pairs of consecutive state changes — useful for asserting a wizard advanced
    and never went backwards, which is the failure mode naive form drivers loop on."""
    out: list[tuple[str, str]] = []
    prev: str | None = None
    for d in history:
        if prev is not None and d.state != prev:
            out.append((prev, d.state))
        prev = d.state
    return out
