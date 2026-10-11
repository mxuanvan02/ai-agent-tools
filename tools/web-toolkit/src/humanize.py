"""Human-like timing, typing and pointer motion for browser automation.

Pattern extracted (and generalised) from code-root/gmail-account-creator `src/utils/human-behavior.js`.
Purpose here is TEST STABILITY, not detection evasion: fixed sleeps are the #1 cause of flaky
browser tests (an action fires before a listener is attached, or before a transition ends). Adding
jitter and reading-the-page pauses makes automation resilient to timing variance, and makes
recorded demos / screenshots look natural.

The mouse-path maths (quadratic Bezier with jitter) is a clean, reusable piece of geometry and is
kept. Per-action delay bands are exposed as a table you can tune. Nothing is bound to any site.

These are pure, transport-agnostic helpers: `sleep_for()` and `mouse_path()` do no I/O, so they are
trivially testable; `type_like_human()`/`move_like_human()` take small injectable callbacks so they
work with Playwright, Selenium, or a raw CDP session.

Usage:
    await sleep_for("before_click")            # jittered pause, no I/O beyond asyncio.sleep
    pts = mouse_path(0, 0, 300, 200, steps=25)  # list[(x, y)] for a natural cursor arc
    await type_like_human(page.type, "#email", "user@example.com")
"""
from __future__ import annotations

import asyncio
import math
import random
from typing import Awaitable, Callable, Sequence

# Per-action delay bands in milliseconds. Tune these for your app; they are the whole point of
# the module — one table to review instead of magic sleeps scattered through test code.
DELAY_BANDS: dict[str, tuple[int, int]] = {
    "before_click": (200, 600),
    "after_click": (300, 800),
    "before_type": (150, 400),
    "after_type": (200, 500),
    "between_actions": (500, 1500),
    "page_load": (1000, 3000),
    "thinking": (1500, 4000),
    "reading": (2000, 5000),
    "short_pause": (100, 300),
    "default": (200, 500),
}


def random_delay_ms(band: str = "default", *, rng: random.Random | None = None) -> int:
    """Pick a delay in milliseconds for a named action band. Unknown bands fall back to 'default'
    rather than raising, so a typo degrades gracefully instead of breaking a long test run."""
    lo, hi = DELAY_BANDS.get(band, DELAY_BANDS["default"])
    r = rng or random
    return r.randint(lo, hi)


def jitter_ms(base: float, variance_pct: float = 30.0, *, floor: float = 50.0,
              rng: random.Random | None = None) -> float:
    """base +/- variance_pct, clamped to a floor. Mirrors the source's humanSleep()."""
    r = rng or random
    span = base * variance_pct / 100.0
    return max(floor, base + r.uniform(-span, span))


async def sleep_for(band: str = "default", *, scale: float = 1.0, rng: random.Random | None = None) -> float:
    """Await a jittered delay for an action band. `scale` lets slow CI stretch every band at once.
    Returns the actual seconds slept (useful to log/assert)."""
    ms = random_delay_ms(band, rng=rng) * scale
    secs = ms / 1000.0
    await asyncio.sleep(secs)
    return secs


async def human_sleep(base_ms: float, variance_pct: float = 30.0, *, scale: float = 1.0,
                      rng: random.Random | None = None) -> float:
    secs = jitter_ms(base_ms, variance_pct, rng=rng) / 1000.0 * scale
    await asyncio.sleep(secs)
    return secs


# ---------------------------------------------------------------- pointer geometry

def _quad_bezier(t: float, p0: Sequence[float], p1: Sequence[float], p2: Sequence[float]) -> tuple[float, float]:
    u = 1 - t
    x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
    y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
    return x, y


def mouse_path(x0: float, y0: float, x1: float, y1: float, *, steps: int = 25,
               bow: float = 0.2, jitter_px: float = 1.5,
               rng: random.Random | None = None) -> list[tuple[float, float]]:
    """A natural cursor arc from (x0,y0) to (x1,y1) as a list of points.

    bow: how far the path curves off the straight line (fraction of distance), randomised in sign.
    jitter_px: per-point noise so the path is not a perfect curve.
    Endpoints are returned exactly, so the last point always lands on the target.
    """
    r = rng or random
    steps = max(2, steps)
    sign = 1 if r.random() > 0.5 else -1
    dist = math.hypot(x1 - x0, y1 - y0)
    off = dist * bow * sign
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    # perpendicular offset for the control point -> a believable arc, not a straight line
    if dist == 0:
        cx, cy = mx, my
    else:
        nx, ny = -(y1 - y0) / dist, (x1 - x0) / dist
        cx, cy = mx + nx * off, my + ny * off
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        x, y = _quad_bezier(t, (x0, y0), (cx, cy), (x1, y1))
        if 0 < i < steps:  # jitter the interior only; keep endpoints exact
            x += r.uniform(-jitter_px, jitter_px)
            y += r.uniform(-jitter_px, jitter_px)
        pts.append((round(x, 2), round(y, 2)))
    pts[-1] = (round(x1, 2), round(y1, 2))
    return pts


async def move_like_human(move: Callable[[float, float], Awaitable[None]],
                          x1: float, y1: float, *, x0: float = 0.0, y0: float = 0.0,
                          steps: int = 25, step_delay_band: str = "short_pause",
                          scale: float = 1.0, rng: random.Random | None = None) -> int:
    """Drive a cursor along mouse_path() via an injected async move(x, y) callback.
    Returns the number of points visited. Transport-agnostic: pass page.mouse.move, a CDP
    Input.dispatchMouseEvent wrapper, etc."""
    pts = mouse_path(x0, y0, x1, y1, steps=steps, rng=rng)
    for x, y in pts:
        await move(x, y)
        await sleep_for(step_delay_band, scale=scale * 0.15, rng=rng)  # short hops
    return len(pts)


# ---------------------------------------------------------------- typing

async def type_like_human(type_char: Callable[[str], Awaitable[None]], text: str, *,
                          min_ms: int = 30, max_ms: int = 120,
                          mistake_chance: float = 0.06, pause_chance: float = 0.10,
                          backspace: Callable[[], Awaitable[None]] | None = None,
                          scale: float = 1.0, rng: random.Random | None = None) -> int:
    """Type text one character at a time with per-key jitter, occasional micro-pauses, and
    (optionally) self-corrected typos. `type_char` types one char; `backspace` deletes one.

    mistake_chance/pause_chance default low — enough to break machine-perfect timing, not enough
    to slow a suite. Set both to 0 for a fast but still-jittered run. Returns keystrokes sent
    (including corrections), so a test can assert it stayed within a bound.
    """
    r = rng or random
    keys = 0
    for i, ch in enumerate(text):
        # occasional longer pause, as if reading/thinking — more likely after punctuation/space
        if ch in " .,;:" or r.random() < pause_chance:
            await asyncio.sleep(r.uniform(min_ms, max_ms) * 3 * scale / 1000.0)
        if mistake_chance > 0 and backspace is not None and r.random() < mistake_chance and ch.isalpha():
            wrong = r.choice("abcdefghijklmnopqrstuvwxyz")
            await type_char(wrong); keys += 1
            await asyncio.sleep(r.uniform(80, 200) * scale / 1000.0)
            await backspace(); keys += 1
            await asyncio.sleep(r.uniform(40, 120) * scale / 1000.0)
        await type_char(ch); keys += 1
        await asyncio.sleep(r.uniform(min_ms, max_ms) * scale / 1000.0)
    return keys
