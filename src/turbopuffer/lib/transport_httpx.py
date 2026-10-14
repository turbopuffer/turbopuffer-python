import gzip
import time
from typing import Any, Dict, Callable, Optional
from typing_extensions import override

import httpx

from .transport import MIN_GZIP_SIZE
from .performance import TRACE_CONNECTION_EXTENSION

# httpcore trace events that mark connection phases, and the clock keys they set. Later events
# overwrite earlier ones, so with TLS the connection ends when the handshake completes.
_TRACE_EVENTS = {
    "connection.connect_tcp.started": "connect_start",
    "connection.connect_unix_socket.started": "connect_start",
    "connection.connect_tcp.complete": "connect_end",
    "connection.connect_unix_socket.complete": "connect_end",
    "connection.start_tls.complete": "connect_end",
    "http11.send_request_headers.started": "send_start",
    "http2.send_request_headers.started": "send_start",
    "http11.send_request_body.complete": "send_end",
    "http2.send_request_body.complete": "send_end",
}


def _connection_tracer(
    clock: Dict[str, int], previous: Optional[Callable[[str, Any], None]]
) -> Callable[[str, Any], None]:
    def trace(event_name: str, info: Any) -> None:
        key = _TRACE_EVENTS.get(event_name)
        if key is not None:
            clock[key] = time.perf_counter_ns()
        if previous is not None:
            previous(event_name, info)

    return trace


class HttpxTransport(httpx.HTTPTransport):
    @override
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        clock = request.extensions["clock"]
        compression = request.extensions.get("compression", True)

        # Compress the request content if worthwhile.
        clock["compress_start"] = time.perf_counter_ns()
        clock["compress_end"] = clock["compress_start"]  # overwritten later if we actually compress
        if compression and len(request.content) > MIN_GZIP_SIZE:
            request._content = gzip.compress(request.content, compresslevel=1)
            request.stream = httpx.ByteStream(request._content)
            request.headers["Content-Encoding"] = "gzip"
            request.headers["Content-Length"] = str(len(request.content))
            clock["compress_end"] = time.perf_counter_ns()

        if request.extensions.get(TRACE_CONNECTION_EXTENSION):
            request.extensions["trace"] = _connection_tracer(clock, request.extensions.get("trace"))
        clock["transport_start"] = time.perf_counter_ns()

        response = super().handle_request(request)
        clock["response_headers_end"] = time.perf_counter_ns()

        # Eagerly read the response content (which will be cached on the
        # response object) so that we can time the body read.
        response.read()
        clock["body_read_end"] = time.perf_counter_ns()

        # Smuggle the clock through the response object.
        response.extensions["clock"] = clock

        return response
