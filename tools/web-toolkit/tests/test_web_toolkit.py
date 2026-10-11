"""Tests for the three extracted modules: proxy_pool, humanize, page_state.
Run: uv run --with pytest python -m pytest test_web_toolkit.py -q
No network access in any test: health probes are injected, sleeps are faked, DOM hooks are dicts."""
import asyncio
import random
import time

import humanize as H
import proxy_pool as PP
import page_state as PS


# ---------------------------------------------------------------- proxy_pool

def test_parse_formats():
    pool = PP.ProxyPool.from_strings([
        "# comment", "",
        "1.2.3.4:8080",
        "5.6.7.8:3128:user:pass",
    ])
    assert len(pool) == 2
    p = pool._proxies[1]
    assert (p.host, p.port, p.username, p.password) == ("5.6.7.8", 3128, "user", "pass")
    assert "pass" not in str(p) and "pass" not in repr(p)  # never leak password in logs
    assert p.as_url(with_auth=False) == "http://5.6.7.8:3128"
    assert p.as_dict()["has_auth"] is True and "password" not in p.as_dict()


def test_parse_rejects_bad_records():
    for bad in (["hostonly"], ["1.2.3.4:notaport"], ["1.2.3.4:99999"]):
        try:
            PP.ProxyPool.from_strings(bad)
            assert False, f"should have raised for {bad}"
        except ValueError:
            pass


def test_duplicate_hostport_rejected():
    try:
        PP.ProxyPool([PP.Proxy("a", 1), PP.Proxy("a", 1)])
        assert False
    except ValueError:
        pass


def test_lru_rotation_and_lease_release():
    pool = PP.ProxyPool.from_strings(["p1:1", "p2:2", "p3:3"])
    seen = []
    for _ in range(6):
        with pool.acquire() as p:
            seen.append(p.id)
    assert set(seen) == {"p1:1", "p2:2", "p3:3"}
    # LRU: each proxy used twice, evenly spread
    assert seen.count("p1:1") == 2
    st = pool.stats()
    assert st["free"] == 3 and st["leased"] == 0


def test_lease_returns_pool_even_on_exception():
    pool = PP.ProxyPool.from_strings(["p1:1"])
    try:
        with pool.acquire() as p:
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    # released but has a failure recorded
    st = pool.stats(now=time.monotonic())
    assert st["leased"] == 0
    assert pool._proxies[0].failures == 1
    assert st["cooling_down"] == 1


def test_failure_cooldown_is_exponential_and_capped():
    pool = PP.ProxyPool.from_strings(["p1:1", "p2:2"], base_cooldown=30, max_cooldown=120, max_failures=10)
    p = pool._proxies[0]
    now = time.monotonic()
    assert pool.report_failure(p, now=now) == 30
    assert pool.report_failure(p, now=now) == 60
    assert pool.report_failure(p, now=now) == 120   # capped
    assert pool.report_failure(p, now=now) == 120
    pool.report_success(p)
    assert p.failures == 0 and p.cooldown_until == 0.0


def test_retire_after_max_failures_and_exhausted():
    pool = PP.ProxyPool.from_strings(["p1:1"], max_failures=2, base_cooldown=1)
    p = pool._proxies[0]
    pool.report_failure(p); pool.report_failure(p)
    assert pool.stats()["retired"] == 1
    try:
        pool.acquire()
        assert False
    except PP.ProxyExhausted:
        pass


def test_cooling_proxy_is_skipped_then_recovers():
    pool = PP.ProxyPool.from_strings(["p1:1", "p2:2"], base_cooldown=60)
    now = time.monotonic()
    pool.report_failure(pool._proxies[0], now=now)
    with pool.acquire(now=now) as p:
        assert p.id == "p2:2"  # p1 cooling -> not chosen
    far = now + 61
    st = pool.stats(now=far)
    assert st["cooling_down"] == 0


def test_health_probe_retires_dead():
    pool = PP.ProxyPool.from_strings(["p1:1", "p2:2"], max_failures=1)
    res = pool.check_health(probe=lambda p: p.host == "p1")
    assert res == {"p1:1": True, "p2:2": False}
    assert pool.stats()["retired"] == 1


def test_health_probe_raises_counts_as_dead():
    pool = PP.ProxyPool.from_strings(["p1:1"], max_failures=1)
    def boom(p): raise OSError("conn refused")
    assert pool.check_health(probe=boom) == {"p1:1": False}


def test_iter_with_pool_retries_then_reports():
    # base_cooldown=0.0 keeps every proxy acquirable, so the retry count is deterministic:
    # 1 attempt + max_retries attempts. A nonzero cooldown shorter than the loop time would
    # instead trip the exhaustion path (covered by the next test).
    pool = PP.ProxyPool.from_strings(["p1:1", "p2:2"], base_cooldown=0.0)
    calls = []
    def worker(item, p):
        calls.append((item, p.id))
        if item == "bad":
            raise RuntimeError("nope")
    out = list(PP.iter_with_pool(pool, ["good", "bad"], worker, max_retries=2))
    assert out[0] == ("good", "ok", "p1:1")
    assert out[1][1] == "failed"
    assert len(calls) == 4                      # good once + bad three attempts
    assert [c[1] for c in calls[1:]] == ["p2:2", "p1:1", "p2:2"]  # rotates proxies


def test_iter_with_pool_stops_when_pool_exhausted():
    # A real cooldown retires each proxy as it fails, so the retry loop must give up with
    # 'failed' rather than spin forever or let ProxyExhausted escape the generator.
    # Hand-computed: attempt 1 -> LRU tie picks p1 (first in list), fails -> p1 cools down;
    # attempt 2 -> only p2 free, fails -> p2 cools down; attempt 3 -> ProxyExhausted -> break.
    pool = PP.ProxyPool.from_strings(["p1:1", "p2:2"], base_cooldown=600)
    calls = []
    def worker(item, p):
        calls.append(p.id)
        raise RuntimeError("nope")
    out = list(PP.iter_with_pool(pool, ["x"], worker, max_retries=5))
    # 'none' = the FINAL attempt could not acquire any proxy (exhaustion semantics);
    # the proxies actually tried are visible via the worker's own call log below.
    assert out == [("x", "failed", "none")]
    assert calls == ["p1:1", "p2:2"]            # exactly two attempts before exhaustion
    st = pool.stats()
    assert st["cooling_down"] == 2 and st["leased"] == 0   # lease released even on failure


# ---------------------------------------------------------------- humanize

def test_delay_bands_within_range_and_fallback():
    rng = random.Random(7)
    for _ in range(200):
        d = H.random_delay_ms("before_click", rng=rng)
        assert 200 <= d <= 600
    # unknown band -> default band, no crash
    d = H.random_delay_ms("no_such_band", rng=rng)
    assert 200 <= d <= 500


def test_jitter_floor():
    rng = random.Random(1)
    for _ in range(100):
        assert H.jitter_ms(10, 50, rng=rng) >= 50  # floor clamps tiny bases


def test_mouse_path_endpoints_exact_and_count():
    pts = H.mouse_path(0, 0, 300, 200, steps=10, rng=random.Random(3))
    assert len(pts) == 11
    assert pts[0] == (0.0, 0.0)
    assert pts[-1] == (300.0, 200.0)
    # interior points are jittered/curved: not all on the straight line
    straight = all(abs(y - (200 / 300) * x) < 0.01 for x, y in pts[1:-1])
    assert not straight


def test_mouse_path_zero_distance():
    pts = H.mouse_path(5, 5, 5, 5, steps=4, rng=random.Random(0))
    assert pts[0] == pts[-1] == (5.0, 5.0)


def test_type_like_human_keystroke_bound_no_mistakes():
    typed = []
    async def type_char(c): typed.append(c)
    n = asyncio.run(H.type_like_human(type_char, "hello", mistake_chance=0, pause_chance=0,
                                      min_ms=1, max_ms=2, scale=0.01))
    assert "".join(typed) == "hello"
    assert n == 5


def test_type_like_human_mistakes_still_produce_correct_text():
    typed = []
    async def type_char(c): typed.append(c)
    async def backspace(): typed.pop()
    n = asyncio.run(H.type_like_human(type_char, "abc", mistake_chance=1.0, pause_chance=0,
                                      backspace=backspace, min_ms=1, max_ms=2, scale=0.01,
                                      rng=random.Random(5)))
    assert "".join(typed) == "abc"      # every mistake corrected
    assert n > 3                        # corrections cost extra keystrokes


def test_sleep_for_returns_actual_seconds():
    s = asyncio.run(H.sleep_for("short_pause", scale=0.01))
    assert 0 < s < 0.05


def test_move_like_human_visits_all_points():
    visited = []
    async def move(x, y): visited.append((x, y))
    n = asyncio.run(H.move_like_human(move, 100, 50, steps=6, scale=0.01, rng=random.Random(2)))
    assert n == 7 and len(visited) == 7
    assert visited[-1] == (100.0, 50.0)


# ---------------------------------------------------------------- page_state

MACHINE = PS.PageStateMachine([
    PS.PageState("login", url_contains=["/login"], elements=["#password"], action="fill_credentials"),
    PS.PageState("otp", url_contains=["/challenge"], any_elements=["input[name=code]", "#otp"], action="enter_code"),
    PS.PageState("home", url_contains=["/dashboard"], elements=["#user-menu"], priority=5, action="done"),
], fallback=PS.PageState("unknown", action="inspect"))


def test_detect_by_url_and_elements():
    d = MACHINE.detect(url="https://x.com/login?next=1",
                       elements_present=lambda s: s == "#password")
    assert d.state == "login" and d.action == "fill_credentials" and d.confident
    assert "/login" in d.url_matched


def test_required_element_missing_rejects_state():
    # URL says /login but #password not present -> login state rejected -> unknown fallback
    d = MACHINE.detect(url="https://x.com/login", elements_present=lambda s: False)
    assert d.state == "unknown" and not d.confident and d.action == "inspect"


def test_any_elements_semantics():
    d = MACHINE.detect(url="https://x.com/challenge/sms",
                       elements_present=lambda s: s == "#otp")
    assert d.state == "otp" and "#otp" in d.elements_found


def test_url_matcher_callable():
    m = PS.PageStateMachine([
        PS.PageState("deep", url_matches=[lambda u: u.count("/") > 3], action="deep"),
    ])
    assert m.detect(url="https://x/a/b/c", elements_present=lambda s: False).state == "deep"
    assert m.detect(url="https://x/a", elements_present=lambda s: False).state == "unknown"


def test_priority_breaks_ties():
    m = PS.PageStateMachine([
        PS.PageState("a", url_contains=["/x"], priority=1),
        PS.PageState("b", url_contains=["/x"], priority=9),
    ])
    assert m.detect(url="https://h/x", elements_present=lambda s: False).state == "b"


def test_duplicate_names_rejected():
    try:
        PS.PageStateMachine([PS.PageState("a"), PS.PageState("a")])
        assert False
    except ValueError:
        pass


def test_wait_for_with_injected_sleep():
    seq = iter([
        PS.Detection("login", "", (), (), 2),
        PS.Detection("login", "", (), (), 2),
        PS.Detection("home", "", (), (), 5),
    ])
    slept = []
    got = MACHINE.wait_for(state_name="home", poll=lambda: next(seq),
                           sleep_fn=slept.append, interval=0.5, attempts=10)
    assert got.state == "home"
    assert slept == [0.5, 0.5]  # slept between polls only


def test_wait_for_gives_up_and_returns_last():
    d = PS.Detection("login", "", (), (), 2)
    got = MACHINE.wait_for(state_name="home", poll=lambda: d,
                           sleep_fn=lambda s: None, attempts=3)
    assert got.state == "login"


def test_detect_transitions_filters_repeats():
    hist = [PS.Detection(s, "", (), (), 1) for s in ("login", "login", "otp", "otp", "home")]
    assert PS.detect_transitions(hist) == [("login", "otp"), ("otp", "home")]
