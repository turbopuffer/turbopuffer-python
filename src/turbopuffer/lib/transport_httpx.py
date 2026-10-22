import gzip
import time
from typing_extensions import override

import httpx2

from .transport import MIN_GZIP_SIZE
from .._observer import TIMINGS_EXTENSION


class HttpxTransport(httpx2.HTTPTransport):
    @override
    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        timings = request.extensions.get(TIMINGS_EXTENSION)
        compression = request.extensions.get("compression", True)

        # Compress the request content if worthwhile.
        compress_begin = time.perf_counter_ns()
        compress_end = compress_begin  # overwritten later if we actually compress
        if compression and len(request.content) > MIN_GZIP_SIZE:
            request._content = gzip.compress(request.content, compresslevel=1)
            request.stream = httpx2.ByteStream(request._content)
            request.headers["Content-Encoding"] = "gzip"
            request.headers["Content-Length"] = str(len(request.content))
            compress_end = time.perf_counter_ns()
        if timings is not None:
            timings.extra["compress_begin"] = compress_begin
            timings.extra["compress_end"] = compress_end

        response = super().handle_request(request)

        # Eagerly read the response content (which will be cached on the
        # response object) so that the body read is timed with the request.
        response.read()

        return response
