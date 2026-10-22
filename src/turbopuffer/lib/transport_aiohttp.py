# Copyright © 2025, Karen Petrosyan. All rights reserved.
# Obtained from the following URL on 9 June 2025:
# https://github.com/karpetrosyan/httpx-aiohttp/tree/6bfcb1dcf13632aa5338e49b13dccf54bd51ca65
#
# The default async transport for `httpx2` is quite slow, so we use this
# aiohttp-based transport instead.

import gzip
import time
import typing
import asyncio
import contextlib
from types import SimpleNamespace
from typing_extensions import override

import httpx2
import aiohttp
from aiohttp import ClientTimeout
from aiohttp.client import ClientSession, ClientResponse

from .transport import MIN_GZIP_SIZE
from .._observer import TIMINGS_EXTENSION

AIOHTTP_EXC_MAP = {
    aiohttp.ServerTimeoutError: httpx2.TimeoutException,
    aiohttp.ConnectionTimeoutError: httpx2.ConnectTimeout,
    aiohttp.SocketTimeoutError: httpx2.ReadTimeout,
    aiohttp.ClientConnectorError: httpx2.ConnectError,
    aiohttp.ClientPayloadError: httpx2.ReadError,
    aiohttp.ClientProxyConnectionError: httpx2.ProxyError,
}


@contextlib.contextmanager
def map_aiohttp_exceptions() -> typing.Iterator[None]:
    try:
        yield
    except Exception as exc:
        mapped_exc = None

        for from_exc, to_exc in AIOHTTP_EXC_MAP.items():
            if not isinstance(exc, from_exc):  # type: ignore
                continue
            if mapped_exc is None or issubclass(to_exc, mapped_exc):  # type: ignore
                mapped_exc = to_exc

        if mapped_exc is None:  # pragma: no cover
            raise

        message = str(exc)
        raise mapped_exc(message) from exc


class AiohttpResponseStream(httpx2.AsyncByteStream):
    CHUNK_SIZE = 1024 * 16

    def __init__(self, aiohttp_response: ClientResponse) -> None:
        self._aiohttp_response = aiohttp_response

    @override
    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        with map_aiohttp_exceptions():
            async for chunk in self._aiohttp_response.content.iter_chunked(self.CHUNK_SIZE):
                yield chunk

    @override
    async def aclose(self) -> None:
        with map_aiohttp_exceptions():
            await self._aiohttp_response.__aexit__(None, None, None)


_TraceCallback = typing.Callable[[ClientSession, SimpleNamespace, typing.Any], typing.Awaitable[None]]


def connection_trace_config() -> aiohttp.TraceConfig:
    """Returns a trace config that records connection phases in the timings passed as a request's trace context."""

    def marker(*fields: str) -> _TraceCallback:
        async def mark(_session: ClientSession, context: SimpleNamespace, _params: typing.Any) -> None:
            timings = context.trace_request_ctx
            if timings is not None:
                now = time.perf_counter_ns()
                for field in fields:
                    setattr(timings, field, now)

        return mark

    config = aiohttp.TraceConfig()
    config.on_connection_create_start.append(marker("connect_begin"))
    # A new connection is ready to send on as soon as it's created.
    config.on_connection_create_end.append(marker("connect_end", "send_begin"))
    config.on_connection_reuseconn.append(marker("send_begin"))
    # Each chunk overwrites the last, so this ends up marking when the whole body was sent.
    config.on_request_headers_sent.append(marker("send_end"))
    config.on_request_chunk_sent.append(marker("send_end"))
    return config


class AiohttpTransport(httpx2.AsyncBaseTransport):
    def __init__(self, client: typing.Union[ClientSession, typing.Callable[[], ClientSession]]) -> None:
        self.client = client

    @override
    async def handle_async_request(
        self,
        request: httpx2.Request,
    ) -> httpx2.Response:
        timings = request.extensions.get(TIMINGS_EXTENSION)
        timeout = request.extensions.get("timeout", {})
        sni_hostname = request.extensions.get("sni_hostname")
        compression = request.extensions.get("compression", True)

        if not isinstance(self.client, ClientSession):
            self.client = self.client()

        # Compress the request content if worthwhile.
        content = request.content
        compress_begin = time.perf_counter_ns()
        compress_end = compress_begin  # overwritten later if we actually compress
        if compression and len(request.content) > MIN_GZIP_SIZE:
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(None, lambda: gzip.compress(content, compresslevel=1))
            request.headers["Content-Encoding"] = "gzip"
            request.headers["Content-Length"] = str(len(content))
            compress_end = time.perf_counter_ns()
        if timings is not None:
            timings.extra["compress_begin"] = compress_begin
            timings.extra["compress_end"] = compress_end

        with map_aiohttp_exceptions():
            response = await self.client.request(
                method=request.method,
                url=str(request.url),
                headers=request.headers,
                data=content,
                allow_redirects=False,
                auto_decompress=False,
                compress=False,
                timeout=ClientTimeout(
                    sock_connect=timeout.get("connect"),
                    sock_read=timeout.get("read"),
                    connect=timeout.get("pool"),
                ),
                server_hostname=sni_hostname,
                # Sessions without our trace config ignore it.
                trace_request_ctx=timings,
            ).__aenter__()
            if timings is not None:
                timings.response_headers = time.perf_counter_ns()

        httpx_response = httpx2.Response(
            status_code=response.status,
            headers=response.headers,
            content=AiohttpResponseStream(response),
            request=request,
        )

        # Eagerly read the response content (which will be cached on the
        # response object) so that we can time the body read.
        await httpx_response.aread()
        if timings is not None:
            timings.body_end = time.perf_counter_ns()

        return httpx_response

    @override
    async def aclose(self) -> None:
        if isinstance(self.client, ClientSession):
            await self.client.close()
