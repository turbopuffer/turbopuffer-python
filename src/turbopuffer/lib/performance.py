from typing import Dict, Optional

from .._models import BaseModel
from .._observer import Timings


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


def compute_durations(timings: Timings, end: int) -> Dict[str, int]:
    """Returns the duration in nanoseconds of each client-side phase of an attempt ending at `end`.

    Phases that weren't observed are left out.
    """
    durations: Dict[str, int] = {}
    if timings.attempt_begin is None:
        return durations
    durations["total"] = end - timings.attempt_begin

    if timings.serialize_begin is not None and timings.serialize_end is not None:
        durations["serialize"] = timings.serialize_end - timings.serialize_begin

    # Set by our transports, which may compress request bodies.
    compress_begin = timings.extra.get("compress_begin")
    compress_end = timings.extra.get("compress_end")
    if compress_begin is not None and compress_end is not None:
        durations["compress"] = compress_end - compress_begin

    # Waiting for a free connection, until connecting a new one or sending on a reused one.
    pool_begin = compress_end if compress_end is not None else timings.request_ready
    connection_ready = timings.connect_begin if timings.connect_begin is not None else timings.send_begin
    if pool_begin is not None and connection_ready is not None:
        durations["pool"] = max(connection_ready - pool_begin, 0)

    if timings.connect_begin is not None and timings.connect_end is not None:
        durations["connect"] = timings.connect_end - timings.connect_begin

    if timings.send_begin is not None and timings.send_end is not None:
        durations["send"] = timings.send_end - timings.send_begin

    # Covers the network round trip and the server. aiohttp sends the body concurrently with
    # reading the response, so it can finish sending after headers arrive.
    if timings.send_end is not None and timings.response_headers is not None:
        durations["wait"] = max(timings.response_headers - timings.send_end, 0)

    if timings.response_headers is not None:
        durations["response"] = timings.response_headers - timings.attempt_begin

    if timings.body_end is not None and timings.response_headers is not None:
        durations["body_read"] = timings.body_end - timings.response_headers

    if timings.deserialize_begin is not None and timings.deserialize_end is not None:
        durations["deserialize"] = timings.deserialize_end - timings.deserialize_begin

    return durations


def merge_into_performance(parsed: object, durations: Dict[str, int]) -> None:
    """Fills in the client performance fields of a parsed response from its durations."""
    # HACK: we assume any response with a `performance` property of type
    # `ClientPerformance` wants client performance metrics merged into that
    # object.
    performance = getattr(parsed, "performance", None)
    if not isinstance(performance, ClientPerformance) or "total" not in durations:
        return

    performance.client_total_ms = durations["total"] / 1e6
    performance.client_deserialize_ms = durations.get("deserialize", 0) / 1e6

    if "compress" in durations:
        performance.client_compress_ms = durations["compress"] / 1e6

    if "response" in durations:
        performance.client_response_ms = durations["response"] / 1e6

    if "body_read" in durations:
        performance.client_body_read_ms = durations["body_read"] / 1e6
