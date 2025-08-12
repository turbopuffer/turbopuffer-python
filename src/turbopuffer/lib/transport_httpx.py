import gzip
import time
from typing_extensions import override

import httpx

from .transport import MIN_GZIP_SIZE


class HttpxTransport(httpx.HTTPTransport):
    @override
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        clock = request.extensions["clock"]
        compression = request.extensions.get("compression", True)

        # Compress the request content if worthwhile.
        clock["compress_start"] = time.monotonic()
        clock["compress_end"] = clock["compress_start"]  # overwritten later if we actually compress
        if compression and len(request.content) > MIN_GZIP_SIZE:
            request._content = gzip.compress(request.content, compresslevel=1)
            request.stream = httpx.ByteStream(request._content)
            request.headers["Content-Encoding"] = "gzip"
            request.headers["Content-Length"] = str(len(request.content))
            clock["compress_end"] = time.monotonic()

        response = super().handle_request(request)
        clock["response_headers_end"] = time.monotonic()

        # Eagerly read the response content (which will be cached on the
        # response object) so that we can time the body read.
        response.read()
        clock["body_read_end"] = time.monotonic()

        # Smuggle the clock through the response object.
        response.extensions["clock"] = clock

        return response
