import time
from typing import Any, Dict, Optional

import httpx

from . import json
from .._models import BaseModel


class ClientPerformance(BaseModel):
    client_total_ms: float
    """Total request time in milliseconds, measured on the client.

    Note this only includes the time spent during the last retry.
    """

    client_compress_ms: float
    """Number of milliseconds spent compressing the request on the client."""

    client_response_ms: Optional[float]
    """Number of milliseconds between the start of the request and receiving the
    last response header from the server.
    """

    client_body_read_ms: Optional[float]
    """Number of milliseconds between receiving the last response header from
    the server and receiving the end of the response body from the server.
    """

    client_deserialize_ms: float
    """Number of milliseconds spent deserializing the response on the client."""


# Request extension that asks our transports to record connection phases in the request's clock.
TRACE_CONNECTION_EXTENSION = "trace_connection"


def timed_dumps(data: object, request_kwargs: Dict[str, Any]) -> bytes:
    """Serializes a request body, recording the time it took in the clock of the request being built."""
    start = time.perf_counter_ns()
    content = json.dumps(data)
    end = time.perf_counter_ns()
    request_kwargs.setdefault("extensions", {})["clock"] = {"serialize_start": start, "serialize_end": end}
    return content


def start_response_timing(response: httpx.Response) -> Optional[Dict[str, int]]:
    """Returns the clock of the request behind `response` with deserialization started, if it was timed."""
    clock = response.extensions.get("clock")
    if clock is None and response._request is not None:
        clock = response.request.extensions.get("clock")
    if clock is None or "request_start" not in clock:
        return None
    clock["deserialize_start"] = time.perf_counter_ns()
    return clock  # type: ignore[no-any-return]


def compute_durations(clock: Dict[str, int], end: int) -> Dict[str, int]:
    """Returns the duration in nanoseconds of each client-side phase recorded in `clock`.

    Clock values come from `time.perf_counter_ns()`.
    """
    request_start = clock["request_start"]
    durations = {"total": end - request_start}

    # Only set for requests with a JSON body.
    serialize_start = clock.get("serialize_start")
    serialize_end = clock.get("serialize_end")
    if serialize_start is not None and serialize_end is not None:
        durations["serialize"] = serialize_end - serialize_start

    # These exist only when using our default (custom) transports.
    compress_start = clock.get("compress_start")
    compress_end = clock.get("compress_end")
    response_headers_end = clock.get("response_headers_end")
    body_read_end = clock.get("body_read_end")

    if compress_start is not None and compress_end is not None:
        durations["compress"] = compress_end - compress_start

    # These exist only when our transports traced the connection.
    transport_start = clock.get("transport_start")
    connect_start = clock.get("connect_start")
    connect_end = clock.get("connect_end")
    send_start = clock.get("send_start")
    send_end = clock.get("send_end")

    # Waiting for a free connection, until connecting a new one or sending on a reused one.
    connection_ready = connect_start if connect_start is not None else send_start
    if transport_start is not None and connection_ready is not None:
        durations["pool"] = connection_ready - transport_start

    if connect_start is not None and connect_end is not None:
        durations["connect"] = connect_end - connect_start

    if send_start is not None and send_end is not None:
        durations["send"] = send_end - send_start

    # Covers the network round trip and the server. aiohttp sends the body concurrently with
    # reading the response, so it can finish sending after headers arrive.
    if send_end is not None and response_headers_end is not None:
        durations["wait"] = max(response_headers_end - send_end, 0)

    if response_headers_end is not None:
        durations["response"] = response_headers_end - request_start

    if body_read_end is not None and response_headers_end is not None:
        durations["body_read"] = body_read_end - response_headers_end

    # Not set for requests that failed before a response was parsed.
    deserialize_start = clock.get("deserialize_start")
    if deserialize_start is not None:
        durations["deserialize"] = end - deserialize_start

    return durations


def connection_reused(clock: Dict[str, int]) -> Optional[bool]:
    """Returns whether the request was sent on a reused connection, or None if that's unknown."""
    if "send_start" not in clock:
        return None
    return "connect_start" not in clock


def merge_clock_into_response(response: Any, clock: Dict[str, int]) -> Dict[str, int]:
    """Computes client durations for a parsed response and returns them in nanoseconds."""
    durations = compute_durations(clock, time.perf_counter_ns())

    # HACK: we assume any response with a `performance` property of type
    # `ClientPerformance` wants client performance metrics merged into that
    # object.
    performance = getattr(response, "performance", None)
    if isinstance(performance, ClientPerformance):
        performance.client_total_ms = durations["total"] / 1e6
        performance.client_deserialize_ms = durations["deserialize"] / 1e6

        if "compress" in durations:
            performance.client_compress_ms = durations["compress"] / 1e6

        if "response" in durations:
            performance.client_response_ms = durations["response"] / 1e6

        if "body_read" in durations:
            performance.client_body_read_ms = durations["body_read"] / 1e6

    return durations
