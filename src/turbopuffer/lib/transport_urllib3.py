# Copyright (c) 2020 Florimond Manca
# Obtained from the following URL on 9 June 2025:
# https://gist.github.com/florimondmanca/d56764d78d748eb9f73165da388e546e
#
# In theory this should be faster than the default `httpx` transport, but in
# practice it seems to be slightly slower. We keep it here in case it's useful
# in the future.

import ssl
import gzip
import time
import typing
from typing_extensions import override

import httpx
import urllib3
from httpx._types import CertTypes, ProxyTypes, SyncByteStream
from httpx._config import create_ssl_context

from .transport import MIN_GZIP_SIZE


def httpx_headers_to_urllib3_headers(headers: httpx.Headers) -> urllib3.HTTPHeaderDict:
    urllib3_headers = urllib3.HTTPHeaderDict()
    for name, value in headers.multi_items():
        urllib3_headers.add(name, value)
    return urllib3_headers


class ResponseStream(SyncByteStream):
    CHUNK_SIZE = 1024

    def __init__(self, urllib3_stream: typing.Any) -> None:
        self._urllib3_stream = urllib3_stream

    @override
    def __iter__(self) -> typing.Iterator[bytes]:
        for chunk in self._urllib3_stream.stream(self.CHUNK_SIZE, decode_content=False):
            yield chunk

    @override
    def close(self) -> None:
        self._urllib3_stream.release_conn()


class Urllib3Transport(httpx.BaseTransport):
    def __init__(
        self,
        verify: typing.Union[ssl.SSLContext, str, bool] = True,
        trust_env: bool = True,
        max_pools: int = 10,
        maxsize: int = 10,
        cert: typing.Union[CertTypes, None] = None,
        proxy: typing.Union[ProxyTypes, None] = None,
    ) -> None:
        ssl_context = create_ssl_context(cert=cert, verify=verify, trust_env=trust_env)
        proxy = httpx.Proxy(url=proxy) if isinstance(proxy, (str, httpx.URL)) else proxy

        if proxy is None:
            self._pool = urllib3.PoolManager(
                ssl_context=ssl_context,
                num_pools=max_pools,
                maxsize=maxsize,
                block=False,
            )
        elif proxy.url.scheme in ("http", "https"):
            self._pool = urllib3.ProxyManager(
                str(proxy.url.netloc),
                num_pools=max_pools,
                maxsize=maxsize,
                block=False,
                proxy_ssl_context=proxy.ssl_context,
                proxy_headers=httpx_headers_to_urllib3_headers(proxy.headers),
                ssl_context=ssl_context,
            )
        elif proxy.url.scheme == "socks5":
            from urllib3.contrib.socks import SOCKSProxyManager

            username, password = proxy.auth or (None, None)

            self._pool = SOCKSProxyManager(
                proxy_url=str(proxy.url),
                num_pools=max_pools,
                maxsize=maxsize,
                block=False,
                username=username,
                password=password,
            )
        else:
            raise ValueError(
                f"Proxy protocol must be either 'http', 'https', or 'socks5', but got {proxy.url.scheme!r}."
            )

    @override
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        clock = request.extensions["clock"]
        timeouts = request.extensions.get("timeout", {})

        connect_timeout = timeouts.get("connect", None)
        read_timeout = timeouts.get("read", None)

        urllib3_timeout = urllib3.Timeout(
            connect=connect_timeout,
            read=read_timeout,
        )

        # Compress the request content if worthwhile.
        content = request.content
        clock["compress_start"] = time.monotonic()
        clock["compress_end"] = clock["compress_start"]  # overwritten later if we actually compress
        if len(request.content) > MIN_GZIP_SIZE:
            content = gzip.compress(request.content, compresslevel=1)
            request.headers["Content-Encoding"] = "gzip"
            request.headers["Content-Length"] = str(len(content))
            clock["compress_end"] = time.monotonic()

        response = self._pool.request(
            request.method,
            str(request.url),
            body=content,
            headers=httpx_headers_to_urllib3_headers(request.headers),
            redirect=False,
            preload_content=False,
            timeout=urllib3_timeout,
        )
        clock["response_headers_end"] = time.monotonic()

        httpx_response = httpx.Response(
            status_code=response.status,
            headers=httpx.Headers([(name, value) for name, value in response.headers.iteritems()]),
            content=ResponseStream(response),
            extensions={
                # Smuggle the clock through the response object.
                "clock": clock,
            },
        )

        # Eagerly read the response content (which will be cached on the
        # response object) so that we can time the body read.
        httpx_response.read()
        clock["body_read_end"] = time.monotonic()

        return httpx_response
