"""Client telemetry reported to turbopuffer on subsequent requests.

When enabled, the client buffers a small timing record for each request and
attaches buffered records to a later request in the `X-turbopuffer-Client-Telemetry`
header. The server controls how many requests are recorded by advertising a
sample rate in the `X-turbopuffer-Client-Telemetry-Sample-Rate` response header.

Each recorded request is sent with an `X-Request-Id` that its record repeats, so the
server can show the client's timings in the same trace as its own.
"""

from __future__ import annotations

import os
import re
import time
import base64
import random
import logging
import weakref
import threading
from typing import Any, Dict, List, Tuple, Optional
from collections import deque
from typing_extensions import override

import httpx2

from . import json
from .._observer import RequestInfo, RequestScope, AttemptResult, RequestResult, RequestObserver
from .performance import compute_durations, merge_into_performance

log: logging.Logger = logging.getLogger(__name__)

TELEMETRY_ENV_VAR = "TURBOPUFFER_TELEMETRY"
TELEMETRY_HEADER = "X-turbopuffer-Client-Telemetry"
SAMPLE_RATE_HEADER = "X-turbopuffer-Client-Telemetry-Sample-Rate"
# Sorted by ASCII value, so that encoded IDs sort like their bytes.
REQUEST_ID_ALPHABET = b"234567abcdefghijklmnopqrstuvwxyz"
# The bytes in a request ID before it's encoded. The first `REQUEST_ID_RANDOM_BYTES` are random, and the rest
# hold the time it was generated.
REQUEST_ID_BYTES = 18
# The request header that carries the IDs of recorded requests.
REQUEST_ID_HEADER = "X-Request-Id"
# The prefix of generated request IDs.
REQUEST_ID_PREFIX = "tpreq_"
# The random bytes at the start of a request ID.
REQUEST_ID_RANDOM_BYTES = 12

TELEMETRY_VERSION = 1

# Keeps the header well under the 8 KB per-line limit of common proxies.
MAX_RECORDS_PER_HEADER = 16
MAX_BUFFERED_RECORDS = 1000

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"", "0", "false", "no", "off"}

_NAMESPACE_RE = re.compile(r"^(/v\d+/namespaces/)[^/?]+")
_OPERATION_RE = re.compile(r"(/operations/)[^/?]+")

# Maps RFC 4648's base32 alphabet to `REQUEST_ID_ALPHABET`.
_BASE32_TRANSLATION = bytes.maketrans(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", REQUEST_ID_ALPHABET)

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
        path = httpx2.URL(path).raw_path.decode("ascii", errors="replace")
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

    def observe_response(self, headers: httpx2.Headers) -> None:
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

    def sample(self) -> Optional[float]:
        """Decides whether to record a request that's starting, returning the sample rate it's recorded at."""
        rate = self._sample_rate
        if rate <= 0.0 or (rate < 1.0 and _random() >= rate):
            return None
        return rate

    def record(
        self,
        *,
        method: str,
        url: str,
        status: int,
        retries: int,
        durations: Dict[str, int],
        sample_rate: float,
        server_total_ms: Optional[float] = None,
        error: Optional[str] = None,
        reused: Optional[bool] = None,
        request_id: Optional[str] = None,
    ) -> None:
        """Buffers the record of a request sampled at `sample_rate`. `durations` are in nanoseconds."""
        rec: Dict[str, Any] = {"route": route_template(method, url), "status": status}
        if error is not None:
            rec["error"] = error
        if retries:
            rec["retries"] = retries
        if request_id is not None:
            rec["request_id"] = request_id
        if sample_rate < 1.0:
            rec["sample_rate"] = sample_rate
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


def telemetry_buffer(enabled: Optional[bool], api_key: str, base_url: httpx2.URL) -> Optional[TelemetryBuffer]:
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


def encode_base32(data: bytes) -> str:
    """Encodes `data` in base32 with `REQUEST_ID_ALPHABET`, in RFC 4648's bit order without padding."""
    return base64.b32encode(data).translate(_BASE32_TRANSLATION).rstrip(b"=").decode("ascii")


def new_request_id(millis: int, random_bytes: Optional[bytes] = None) -> str:
    """Generates the ID of a request that will be recorded, at `millis` since the Unix epoch.

    Its format is private to turbopuffer, which only links IDs in the format it expects: 12 random bytes,
    then the 48-bit millisecond time they were generated XORed with the first 6 random bytes, in base32
    after a prefix. Only tests give `random_bytes`, which otherwise come from the OS's CSPRNG.
    """
    if random_bytes is None:
        random_bytes = os.urandom(REQUEST_ID_RANDOM_BYTES)
    millis_bytes = (millis & 0xFFFF_FFFF_FFFF).to_bytes(REQUEST_ID_BYTES - REQUEST_ID_RANDOM_BYTES, "big")
    masked = bytes(m ^ r for m, r in zip(millis_bytes, random_bytes, strict=False))
    return REQUEST_ID_PREFIX + encode_base32(random_bytes + masked)


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
        # The rate the request is recorded at, or None if it isn't recorded. Sampled up front, so that only
        # requests whose records the server will get are sent with request IDs.
        self._sample_rate = buffer.sample() if buffer is not None else None
        # Sent with every attempt, so retries share the request's trace.
        self._request_id = new_request_id(time.time_ns() // 1_000_000) if self._sample_rate is not None else None

    @override
    def attempt_begin(self, attempt: int, request: httpx2.Request) -> None:
        # Taken only once a request is about to be sent, so one that fails before then can't lose it.
        if self._buffer is not None:
            self._batch = self._buffer.take()
        if self._batch is not None:
            request.headers[TELEMETRY_HEADER] = self._batch.header
        # An ID set by the caller is theirs to use, so the request keeps it and isn't linked.
        if attempt == 0 and REQUEST_ID_HEADER in request.headers:
            self._request_id = None
        if self._request_id is not None:
            request.headers[REQUEST_ID_HEADER] = self._request_id

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

        if self._buffer is None or self._sample_rate is None:
            return
        # A rate of zero asks clients to stop recording, even requests that were already sampled.
        if self._buffer.sample_rate <= 0.0:
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
            sample_rate=self._sample_rate,
            server_total_ms=server_total_ms if isinstance(server_total_ms, (int, float)) else None,
            error=error,
            reused=timings.reused,
            request_id=self._request_id,
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
