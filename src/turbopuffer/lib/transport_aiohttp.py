# Copyright © 2025, Karen Petrosyan. All rights reserved.
# Obtained from the following URL on 9 June 2025:
# https://github.com/karpetrosyan/httpx-aiohttp/tree/6bfcb1dcf13632aa5338e49b13dccf54bd51ca65
#
# The default async transport for `httpx` is quite slow, so we use this
# aiohttp-based transport instead.

import gzip
import time
import typing
import asyncio
import contextlib
from typing_extensions import override

import httpx
import aiohttp
from aiohttp import ClientTimeout
from aiohttp.client import ClientSession, ClientResponse

from .transport import MIN_GZIP_SIZE

AIOHTTP_EXC_MAP = {
    aiohttp.ServerTimeoutError: httpx.TimeoutException,
    aiohttp.ConnectionTimeoutError: httpx.ConnectTimeout,
    aiohttp.SocketTimeoutError: httpx.ReadTimeout,
    aiohttp.ClientConnectorError: httpx.ConnectError,
    aiohttp.ClientPayloadError: httpx.ReadError,
    aiohttp.ClientProxyConnectionError: httpx.ProxyError,
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


class AiohttpResponseStream(httpx.AsyncByteStream):
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


class AiohttpTransport(httpx.AsyncBaseTransport):
    def __init__(self, client: typing.Union[ClientSession, typing.Callable[[], ClientSession]]) -> None:
        self.client = client

    @override
    async def handle_async_request(
        self,
        request: httpx.Request,
    ) -> httpx.Response:
        clock = request.extensions["clock"]
        timeout = request.extensions.get("timeout", {})
        sni_hostname = request.extensions.get("sni_hostname")

        if not isinstance(self.client, ClientSession):
            self.client = self.client()

        # Compress the request content if worthwhile.
        content = request.content
        clock["compress_start"] = time.monotonic()
        clock["compress_end"] = clock["compress_start"]  # overwritten later if we actually compress
        if len(request.content) > MIN_GZIP_SIZE:
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(None, lambda: gzip.compress(content, compresslevel=1))
            request.headers["Content-Encoding"] = "gzip"
            request.headers["Content-Length"] = str(len(content))
            clock["compress_end"] = time.monotonic()

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
            ).__aenter__()
            clock["response_headers_end"] = time.monotonic()

        httpx_response = httpx.Response(
            status_code=response.status,
            headers=response.headers,
            content=AiohttpResponseStream(response),
            request=request,
            extensions={
                # Smuggle the clock through the response object.
                "clock": clock,
            },
        )

        # Eagerly read the response content (which will be cached on the
        # response object) so that we can time the body read.
        await httpx_response.aread()
        clock["body_read_end"] = time.monotonic()

        return httpx_response

    @override
    async def aclose(self) -> None:
        if isinstance(self.client, ClientSession):
            await self.client.close()
