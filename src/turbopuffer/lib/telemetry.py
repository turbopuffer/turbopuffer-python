"""Client telemetry reported to turbopuffer on subsequent requests.

When enabled, the client buffers a small timing record for each request and
attaches buffered records to a later request in the `X-turbopuffer-Client-Telemetry`
header. The server controls how many requests are recorded by advertising a
sample rate in the `X-turbopuffer-Client-Telemetry-Sample-Rate` response header.
"""

from __future__ import annotations

import os
import re
import time
import random
import logging
import weakref
import threading
from typing import Any, Dict, List, Tuple, Optional
from collections import deque
from typing_extensions import override

import httpx

from . import json
from .._observer import RequestInfo, RequestScope, AttemptResult, RequestResult, RequestObserver
from .performance import compute_durations, merge_into_performance

log: logging.Logger = logging.getLogger(__name__)

TELEMETRY_ENV_VAR = "TURBOPUFFER_TELEMETRY"
TELEMETRY_HEADER = "X-turbopuffer-Client-Telemetry"
SAMPLE_RATE_HEADER = "X-turbopuffer-Client-Telemetry-Sample-Rate"

TELEMETRY_VERSION = 1

# Keeps the header well under the 8 KB per-line limit of common proxies.
MAX_RECORDS_PER_HEADER = 20
MAX_BUFFERED_RECORDS = 1000

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"", "0", "false", "no", "off"}

_NAMESPACE_RE = re.compile(r"^(/v\d+/namespaces/)[^/?]+")
_OPERATION_RE = re.compile(r"(/operations/)[^/?]+")

# Indirection so tests can control sampling.
_random = random.random


def resolve_enabled(value: Optional[bool]) -> bool:
    """Resolves whether telemetry is enabled, preferring an explicit value over the environment."""
    if value is not None:
        return value

    raw = os.environ.get(TELEMETRY_ENV_VAR, "")
    env = raw.strip().lower()
    if env in _TRUE_VALUES:
        return True
    if env not in _FALSE_VALUES:
        log.warning("Ignoring invalid %s=%r, expected 1 or 0", TELEMETRY_ENV_VAR, raw)
    return False


def route_template(method: str, url: str) -> str:
    """Returns the method and path of a request with identifiers like the namespace replaced."""
    path = url
    if "://" in path:
        path = httpx.URL(path).raw_path.decode("ascii", errors="replace")
    path = _NAMESPACE_RE.sub(r"\g<1>{ns}", path)
    path = _OPERATION_RE.sub(r"\g<1>{token}", path)
    return f"{method.upper()} {path}"


class TelemetryBatch:
    """Records taken from a buffer, encoded as a header value."""

    def __init__(self, records: List[Tuple[float, Dict[str, Any]]], dropped: int) -> None:
        self.records = records
        self.dropped = dropped

        now = time.monotonic()
        envelope: Dict[str, Any] = {
            "version": TELEMETRY_VERSION,
            "records": [{**rec, "age_ms": round((now - recorded_at) * 1000)} for recorded_at, rec in records],
        }
        if dropped:
            envelope["dropped"] = dropped
        self.header = json.dumps(envelope).decode("utf-8")


class TelemetryBuffer:
    """Buffers per-request telemetry records until a later request can carry them."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: deque[Tuple[float, Dict[str, Any]]] = deque()
        self._dropped = 0
        # Used until the server advertises a rate.
        self._sample_rate = 1.0
        _buffers.add(self)

    @property
    def sample_rate(self) -> float:
        return self._sample_rate

    def observe_response(self, headers: httpx.Headers) -> None:
        """Adopts the sample rate advertised by the server, ignoring invalid values."""
        value = headers.get(SAMPLE_RATE_HEADER)
        if value is None:
            return
        try:
            rate = float(value)
        except ValueError:
            return
        # Also rejects NaN, since every comparison with NaN is false.
        if 0.0 <= rate <= 1.0:
            self._sample_rate = rate

    def record(
        self,
        *,
        method: str,
        url: str,
        status: int,
        retries: int,
        durations: Dict[str, int],
        server_total_ms: Optional[float] = None,
        error: Optional[str] = None,
        reused: Optional[bool] = None,
    ) -> None:
        """Samples and buffers a record for one request. `durations` are in nanoseconds."""
        rate = self._sample_rate
        if rate <= 0.0 or (rate < 1.0 and _random() >= rate):
            return

        rec: Dict[str, Any] = {"route": route_template(method, url), "status": status}
        if error is not None:
            rec["error"] = error
        if retries:
            rec["retries"] = retries
        if rate < 1.0:
            rec["sample_rate"] = rate
        for name, duration in durations.items():
            # Covered by the connection phases, so it's only kept for the public performance fields.
            if name == "response":
                continue
            # A zero compress duration means the body wasn't compressed.
            if name == "compress" and duration == 0:
                continue
            rec[f"{name}_us"] = duration // 1000
        if server_total_ms is not None:
            rec["server_total_us"] = round(server_total_ms * 1000)
        if reused is not None:
            rec["reused"] = reused

        with self._lock:
            if len(self._records) >= MAX_BUFFERED_RECORDS:
                self._records.popleft()
                self._dropped += 1
            self._records.append((time.monotonic(), rec))

    def take(self) -> Optional[TelemetryBatch]:
        """Removes up to `MAX_RECORDS_PER_HEADER` of the oldest records."""
        with self._lock:
            if not self._records:
                return None
            count = min(len(self._records), MAX_RECORDS_PER_HEADER)
            records = [self._records.popleft() for _ in range(count)]
            dropped, self._dropped = self._dropped, 0
        return TelemetryBatch(records, dropped)

    def restore(self, batch: TelemetryBatch) -> None:
        """Returns a batch that never reached the server to the front of the buffer."""
        with self._lock:
            self._dropped += batch.dropped
            for item in reversed(batch.records):
                # The batch holds the oldest records, so they're the ones to drop when full.
                if len(self._records) >= MAX_BUFFERED_RECORDS:
                    self._dropped += 1
                    continue
                self._records.appendleft(item)

    def _reset_after_fork(self) -> None:
        # Another thread may have held the lock at fork time, and buffered records belong to the parent.
        self._lock = threading.Lock()
        self._records = deque()
        self._dropped = 0


def telemetry_buffer(enabled: Optional[bool], api_key: str, base_url: httpx.URL) -> Optional[TelemetryBuffer]:
    """Returns the buffer shared by clients with the same API key and base URL, or None if telemetry is disabled.

    Sharing lets records ride on any client's requests, including copies, but never to another org or region.
    """
    if not resolve_enabled(enabled):
        return None
    key = (api_key, str(base_url))
    with _shared_lock:
        buffer = _shared_buffers.get(key)
        if buffer is None:
            buffer = TelemetryBuffer()
            _shared_buffers[key] = buffer
    return buffer


class TurbopufferObserver(RequestObserver):
    """Fills in client performance fields on responses, and records telemetry when enabled."""

    def __init__(self, telemetry: Optional[TelemetryBuffer]) -> None:
        self.telemetry = telemetry

    @override
    def start(self, info: RequestInfo) -> RequestScope:
        return _RequestScope(self.telemetry, info)


class _RequestScope(RequestScope):
    def __init__(self, buffer: Optional[TelemetryBuffer], info: RequestInfo) -> None:
        self._buffer = buffer
        self._info = info
        # Held only while an attempt is in flight.
        self._batch: Optional[TelemetryBatch] = None

    @override
    def attempt_begin(self, attempt: int, request: httpx.Request) -> None:  # noqa: ARG002
        # Taken only once a request is about to be sent, so one that fails before then can't lose it.
        if self._buffer is not None:
            self._batch = self._buffer.take()
        if self._batch is not None:
            request.headers[TELEMETRY_HEADER] = self._batch.header

    @override
    def attempt_end(self, result: AttemptResult) -> None:
        # A batch that never reached the server goes back right away rather than waiting for a retry,
        # which may never come if the request is interrupted between attempts.
        if self._buffer is not None and self._batch is not None and result.reached_server is False:
            self._buffer.restore(self._batch)
        self._batch = None
        if self._buffer is not None and result.response is not None:
            self._buffer.observe_response(result.response.headers)

    @override
    def finish(self, result: RequestResult) -> None:
        timings = result.timings
        end = timings.deserialize_end if timings.deserialize_end is not None else time.perf_counter_ns()
        durations = compute_durations(timings, end)
        merge_into_performance(result.parsed, durations)

        if self._buffer is None:
            return

        error: Optional[str] = None
        if result.error_kind in ("canceled", "other"):
            error = result.error_kind
        elif result.error_kind is not None:
            error = "timeout" if result.error_kind.endswith("timeout") else "connect"
        server_total_ms = getattr(getattr(result.parsed, "performance", None), "server_total_ms", None)
        self._buffer.record(
            method=self._info.method,
            url=self._info.url,
            status=result.response.status_code if result.response is not None else 0,
            retries=result.retries,
            durations=durations,
            server_total_ms=server_total_ms if isinstance(server_total_ms, (int, float)) else None,
            error=error,
            reused=timings.reused,
        )


_buffers: weakref.WeakSet[TelemetryBuffer] = weakref.WeakSet()
_shared_buffers: weakref.WeakValueDictionary[Tuple[str, str], TelemetryBuffer] = weakref.WeakValueDictionary()
_shared_lock = threading.Lock()


def _after_fork_in_child() -> None:
    global _shared_lock
    _shared_lock = threading.Lock()
    for buffer in list(_buffers):
        buffer._reset_after_fork()


# Not available on Windows, which doesn't fork.
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_after_fork_in_child)
