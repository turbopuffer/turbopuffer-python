import time
from typing import Any, Dict, Optional

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


def merge_clock_into_response(response: Any, clock: Dict[str, float]) -> None:
    # HACK: we assume any response with a `performance` property of type
    # `ClientPerformance` wants client performance metrics merged into that
    # object.
    performance = getattr(response, "performance", None)
    if isinstance(performance, ClientPerformance):
        end = time.monotonic()

        # These always exist, regardless of transport.
        request_start: float = clock["request_start"]
        deserialize_start: float = clock["deserialize_start"]

        # These exist only when using our default (custom) transports.
        compress_start: Optional[float] = clock.get("compress_start")
        compress_end: Optional[float] = clock.get("compress_end")
        response_headers_end: Optional[float] = clock.get("response_headers_end")
        body_read_end: Optional[float] = clock.get("body_read_end")

        performance.client_total_ms = (end - request_start) * 1000
        performance.client_deserialize_ms = (end - deserialize_start) * 1000

        if compress_start and compress_end:
            performance.client_compress_ms = (compress_end - compress_start) * 1000

        if response_headers_end:
            performance.client_response_ms = (response_headers_end - request_start) * 1000

        if body_read_end and response_headers_end:
            performance.client_body_read_ms = (body_read_end - response_headers_end) * 1000
