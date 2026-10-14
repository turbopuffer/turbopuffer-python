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
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Optional
from collections import deque

import httpx

from . import json
from .performance import (
    TRACE_CONNECTION_EXTENSION,
    compute_durations,
    connection_reused,
    merge_clock_into_response,
)

if TYPE_CHECKING:
    from .._models import FinalRequestOptions
    from .._response import BaseAPIResponse

log: logging.Logger = logging.getLogger(__name__)

TELEMETRY_ENV_VAR = "TURBOPUFFER_TELEMETRY"
TELEMETRY_HEADER = "X-turbopuffer-Client-Telemetry"
SAMPLE_RATE_HEADER = "X-turbopuffer-Client-Telemetry-Sample-Rate"

TELEMETRY_VERSION = 1

# Keeps the header well under the 8 KB per-line limit of common proxies.
MAX_RECORDS_PER_HEADER = 20
MAX_BUFFERED_RECORDS = 1000

# Errors raised before a request reached the server, so its telemetry batch can be sent again.
UNSENT_ERRORS = (httpx.ConnectError, httpx.ConnectTimeout)

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


class RequestTelemetry:
    """Tracks the clock and telemetry of one request across its retry attempts."""

    def __init__(self, buffer: Optional[TelemetryBuffer]) -> None:
        self._buffer = buffer
        # Kept for later attempts until one of them reaches the server.
        self._batch = buffer.take() if buffer is not None else None
        self._options: Optional[FinalRequestOptions] = None
        self._request: Optional[httpx.Request] = None
        self._retries_taken = 0

    def before_send(
        self, options: FinalRequestOptions, request: httpx.Request, request_start: int, retries_taken: int
    ) -> None:
        request.extensions.setdefault("clock", {})["request_start"] = request_start
        if self._buffer is not None:
            request.extensions[TRACE_CONNECTION_EXTENSION] = True
        self._options = options
        self._request = request
        self._retries_taken = retries_taken
        if self._batch is not None:
            request.headers[TELEMETRY_HEADER] = self._batch.header

    def on_error(self, err: Exception, remaining_retries: int) -> None:
        if not isinstance(err, UNSENT_ERRORS):
            self._batch = None
        if remaining_retries > 0 or self._buffer is None:
            return
        # The request is giving up, so a batch that never reached the server goes back for a later request.
        if self._batch is not None:
            self._buffer.restore(self._batch)
            self._batch = None
        self._record_failure(status=0, error="timeout" if isinstance(err, httpx.TimeoutException) else "connect")

    def on_response(self, response: httpx.Response) -> None:
        # The server has seen the batch, so later attempts must not repeat it.
        self._batch = None
        if self._buffer is not None:
            self._buffer.observe_response(response.headers)

    def on_status_error(self, response: httpx.Response) -> None:
        self._record_failure(status=response.status_code)

    def _record_failure(self, *, status: int, error: Optional[str] = None) -> None:
        if self._buffer is None or self._options is None or self._request is None:
            return
        clock = self._request.extensions["clock"]
        self._buffer.record(
            method=self._options.method,
            url=self._options.url,
            status=status,
            retries=self._retries_taken,
            durations=compute_durations(clock, time.perf_counter_ns()),
            error=error,
            reused=connection_reused(clock),
        )


def finish_response_timing(api_response: BaseAPIResponse[Any], parsed: object, clock: Optional[Dict[str, int]]) -> None:
    """Fills the client performance fields of a parsed response and records its telemetry."""
    if clock is None:
        return
    durations = merge_clock_into_response(parsed, clock)

    buffer = api_response._client._telemetry
    # Parsing the same response into another type isn't another request.
    if buffer is None or clock.get("telemetry_recorded"):
        return
    clock["telemetry_recorded"] = 1

    server_total_ms = getattr(getattr(parsed, "performance", None), "server_total_ms", None)
    buffer.record(
        method=api_response._options.method,
        url=api_response._options.url,
        status=api_response.http_response.status_code,
        retries=api_response.retries_taken,
        durations=durations,
        server_total_ms=server_total_ms if isinstance(server_total_ms, (int, float)) else None,
        reused=connection_reused(clock),
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
