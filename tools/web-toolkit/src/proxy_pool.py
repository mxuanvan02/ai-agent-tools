"""Proxy pool with rotation, health checks, lease tracking and failure cooldown.

Pattern extracted (and generalised) from code-root/gmail-account-creator `src/utils/proxy-manager.js`.
The original only picked a random unused entry and reset when exhausted. This version adds what a
pool actually needs in production: leases that auto-expire, per-proxy failure counters with
exponential cooldown, an injectable health probe, and deterministic output formats.

Nothing here is tied to any particular service — proxies are plain host/port/credential records.
The health probe is injectable so tests (and offline runs) never touch the network by default.

Usage:
    pool = ProxyPool.from_strings(["1.2.3.4:8080", "5.6.7.8:3128:user:pass"])
    with pool.acquire() as p:          # auto-releases, even on exception
        do_request(proxy=p.as_url())
    pool.report_failure(p)             # -> cooldown grows 30s, 60s, 120s ... capped
"""
from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Iterable, Iterator


@dataclass
class Proxy:
    host: str
    port: int
    username: str = ""
    # repr=False: the dataclass-generated repr is what lands in tracebacks and logs, so the
    # password must never appear in it. Equality/comparison still include it.
    password: str = field(default="", repr=False)
    scheme: str = "http"
    region: str = ""
    tag: str = ""
    failures: int = 0
    cooldown_until: float = 0.0
    last_used: float = 0.0
    _leased: bool = field(default=False, repr=False)

    @property
    def id(self) -> str:
        return f"{self.host}:{self.port}"

    def as_url(self, with_auth: bool = True) -> str:
        """Return a proxy URL. Auth is embedded only when explicitly requested, because an
        embedded-credential URL leaks into logs and error messages."""
        if with_auth and self.username:
            return f"{self.scheme}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.scheme}://{self.host}:{self.port}"

    def as_dict(self, *, with_auth: bool = False) -> dict:
        """Safe serialisation for logs/config: never emits the password unless asked."""
        d = {"host": self.host, "port": self.port, "scheme": self.scheme,
             "has_auth": bool(self.username), "region": self.region, "tag": self.tag}
        if with_auth:
            d["username"] = self.username
            d["password"] = self.password
        return d

    def __str__(self) -> str:  # never leak the password through repr/print/logging
        auth = f" (auth as {self.username})" if self.username else ""
        return f"{self.scheme}://{self.host}:{self.port}{auth}"


class ProxyExhausted(RuntimeError):
    """Raised when no proxy is both healthy and free."""


class ProxyPool:
    def __init__(self, proxies: Iterable[Proxy] = (), *,
                 strategy: str = "least_recently_used",
                 base_cooldown: float = 30.0,
                 max_cooldown: float = 900.0,
                 max_failures: int = 5,
                 health_probe: Callable[[Proxy], bool] | None = None,
                 rng: random.Random | None = None):
        """strategy: 'least_recently_used' (default, spreads load), 'round_robin', or 'random'.
        max_failures: a proxy that reaches this many consecutive failures is retired permanently.
        health_probe: optional callable returning True when the proxy works. Injected so the
        pool stays testable and offline-safe; without it, cooldown is the only signal."""
        if strategy not in ("least_recently_used", "round_robin", "random"):
            raise ValueError(f"unknown strategy: {strategy}")
        self._proxies: list[Proxy] = list(proxies)
        self._ids = {p.id for p in self._proxies}
        if len(self._ids) != len(self._proxies):
            raise ValueError("duplicate proxy host:port in pool")
        self._strategy = strategy
        self._base_cooldown = base_cooldown
        self._max_cooldown = max_cooldown
        self._max_failures = max_failures
        self._health_probe = health_probe
        self._rng = rng or random.Random()
        self._rr = 0
        self._lock = threading.RLock()

    # ---------------------------------------------------------------- construction

    @classmethod
    def from_strings(cls, lines: Iterable[str], **kwargs) -> "ProxyPool":
        """Parse 'host:port[:user[:pass]]' records, skipping blanks and '#' comments."""
        out: list[Proxy] = []
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(":")]
            if len(parts) < 2:
                raise ValueError(f"proxy record needs at least host:port, got {line!r}")
            try:
                port = int(parts[1])
            except ValueError:
                raise ValueError(f"proxy port must be an integer, got {parts[1]!r}") from None
            if not (0 < port < 65536):
                raise ValueError(f"proxy port out of range: {port}")
            out.append(Proxy(host=parts[0], port=port,
                             username=parts[2] if len(parts) > 2 else "",
                             password=parts[3] if len(parts) > 3 else ""))
        return cls(out, **kwargs)

    @classmethod
    def from_file(cls, path, **kwargs) -> "ProxyPool":
        with open(path, encoding="utf-8") as fh:
            return cls.from_strings(fh.read().splitlines(), **kwargs)

    # ---------------------------------------------------------------- state

    def __len__(self) -> int:
        return len(self._proxies)

    def stats(self, *, now: float | None = None) -> dict:
        """Snapshot of pool health. Use for dashboards and for deciding to stop a job."""
        now = time.monotonic() if now is None else now
        with self._lock:
            retired = [p for p in self._proxies if p.failures >= self._max_failures]
            cooling = [p for p in self._proxies
                       if p not in retired and p.cooldown_until > now]
            leased = [p for p in self._proxies if p._leased and p not in retired]
            free = [p for p in self._proxies
                    if p not in retired and p not in cooling and not p._leased]
            return {"total": len(self._proxies), "free": len(free), "leased": len(leased),
                    "cooling_down": len(cooling), "retired": len(retired),
                    "retired_ids": [p.id for p in retired]}

    # ---------------------------------------------------------------- acquisition

    def _available(self, now: float) -> list[Proxy]:
        return [p for p in self._proxies
                if p.failures < self._max_failures and p.cooldown_until <= now and not p._leased]

    def acquire(self, *, timeout: float = 0.0, now: float | None = None) -> "_Lease":
        """Take the next healthy proxy. timeout>0 waits for a lease to free up."""
        deadline = (time.monotonic() if now is None else now) + timeout
        while True:
            now = time.monotonic() if now is None else now
            with self._lock:
                cand = self._available(now)
                if cand:
                    p = self._pick(cand, now)
                    p._leased = True
                    p.last_used = now
                    return _Lease(self, p)
                if not self._proxies:
                    raise ProxyExhausted("pool is empty")
                if timeout <= 0:
                    cooling = [x for x in self._proxies if x.cooldown_until > now]
                    raise ProxyExhausted(
                        f"no proxy available ({len(cooling)} cooling down, "
                        f"{sum(1 for x in self._proxies if x._leased)} leased, "
                        f"{sum(1 for x in self._proxies if x.failures >= self._max_failures)} retired)")
            if time.monotonic() >= deadline:
                raise ProxyExhausted(f"no proxy became available within {timeout}s")
            time.sleep(min(0.25, max(0.01, deadline - time.monotonic())))

    def _pick(self, cand: list[Proxy], now: float) -> Proxy:
        if self._strategy == "random":
            return self._rng.choice(cand)
        if self._strategy == "round_robin":
            p = cand[self._rr % len(cand)]
            self._rr += 1
            return p
        return min(cand, key=lambda p: (p.last_used, p.failures))  # least recently used

    def release(self, proxy: Proxy) -> None:
        with self._lock:
            proxy._leased = False

    def report_success(self, proxy: Proxy) -> None:
        """A good result clears the failure streak — consecutive-failure semantics, not lifetime."""
        with self._lock:
            proxy.failures = 0
            proxy.cooldown_until = 0.0

    def report_failure(self, proxy: Proxy, *, now: float | None = None) -> float:
        """Record a failure and return the cooldown length applied (exponential, capped)."""
        now = time.monotonic() if now is None else now
        with self._lock:
            proxy.failures += 1
            if proxy.failures >= self._max_failures:
                proxy.cooldown_until = float("inf")
                return float("inf")
            wait = min(self._base_cooldown * (2 ** (proxy.failures - 1)), self._max_cooldown)
            proxy.cooldown_until = now + wait
            return wait

    def check_health(self, *, probe: Callable[[Proxy], bool] | None = None) -> dict:
        """Probe every proxy once and retire the dead ones. Returns per-proxy booleans.
        Network access happens only if a probe is supplied (or one was set at construction)."""
        probe = probe or self._health_probe
        if probe is None:
            raise ValueError("no health probe supplied; pass probe= or set health_probe at construction")
        results = {}
        for p in list(self._proxies):
            try:
                alive = bool(probe(p))
            except Exception:
                alive = False
            results[p.id] = alive
            if alive:
                self.report_success(p)
            else:
                self.report_failure(p)
        return results


class _Lease:
    """Context manager so a proxy is always returned to the pool, even when the caller raises."""

    def __init__(self, pool: ProxyPool, proxy: Proxy):
        self._pool = pool
        self.proxy = proxy

    def __enter__(self) -> Proxy:
        return self.proxy

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._pool.release(self.proxy)
        if exc_type is not None:
            self._pool.report_failure(self.proxy)
        return False

    def __getattr__(self, name):
        return getattr(self.proxy, name)


def iter_with_pool(pool: ProxyPool, items: Iterable, worker: Callable[[object, Proxy], None],
                   *, max_retries: int = 2) -> Iterator[tuple[object, str, str]]:
    """Run `worker(item, proxy)` over items, retrying on failure with a different proxy.
    Yields (item, status, proxy_id) so the caller can collect results without exceptions
    escaping. status is 'ok' or 'failed'. Never retries past max_retries."""
    for item in items:
        status, used = "failed", ""
        for attempt in range(max_retries + 1):
            try:
                with pool.acquire() as p:
                    used = p.id
                    worker(item, p)
                pool.report_success(p)
                status = "ok"
                break
            except ProxyExhausted:
                status, used = "failed", "none"
                break
            except Exception:
                status = "failed"
        yield item, status, used
