import asyncio
import gzip
import json
import re
import time
import traceback
from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests
import turbopuffer as tpuf
from turbopuffer.error import AuthenticationError, raise_api_error


def find_api_key(api_key: Optional[str] = None) -> str:
    if api_key is not None:
        return api_key
    elif tpuf.api_key is not None:
        return tpuf.api_key
    else:
        raise AuthenticationError(
            "No turbopuffer API key was provided.\n"
            "Set the TURBOPUFFER_API_KEY environment variable, "
            "or pass `api_key=` when creating a Namespace."
        )


def clean_api_base_url(base_url: str) -> str:
    if base_url.endswith(("/v1", "/v1/", "/")):
        return re.sub("(/v1|/v1/|/)$", "", base_url)
    else:
        return base_url


class Backend:
    api_key: str
    api_base_url: str
    session: requests.Session
    _async_session: Optional[aiohttp.ClientSession] = None

    def __init__(self, api_key: Optional[str] = None, headers: Optional[dict] = None):
        self.api_key = find_api_key(api_key)
        self.api_base_url = clean_api_base_url(tpuf.api_base_url)
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": f"tpuf-python/{tpuf.VERSION} {requests.utils.default_headers()['User-Agent']}",
            }
        )

        if headers is not None:
            self.session.headers.update(headers)

    def __eq__(self, other):
        if isinstance(other, Backend):
            return (
                self.api_key == other.api_key
                and self.api_base_url == other.api_base_url
                and self.headers == other.headers
            )
        else:
            return False

    async def __aenter__(self):
        """Enable use as an async context manager."""
        await self._get_async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the async context."""
        if self._async_session and not self._async_session.closed:
            await self._async_session.close()

    async def _get_async_session(self) -> aiohttp.ClientSession:
        """Get or create an async session."""
        if self._async_session is None or self._async_session.closed:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": f"tpuf-python/{tpuf.VERSION} aiohttp",
            }
            if self.headers is not None:
                headers.update(self.headers)
            self._async_session = aiohttp.ClientSession(headers=headers)
        return self._async_session

    async def amake_api_request(
        self,
        *args: List[str],
        method: Optional[str] = None,
        query: Optional[dict] = None,
        payload: Optional[Union[dict, bytes]] = None,
    ) -> dict:
        """
        Asynchronous version of make_api_request.
        Makes API requests to the Turbopuffer API.
        """
        start = time.monotonic()
        if method is None and payload is not None:
            method = "POST"

        url = self.api_base_url + "/v1/" + "/".join(args)

        performance = dict()
        headers = {}

        # Prepare payload data
        data = None
        if payload is not None:
            payload_start = time.monotonic()
            if isinstance(payload, dict):
                json_payload = tpuf.dump_json_bytes(payload)
                performance["json_time"] = time.monotonic() - payload_start
            elif isinstance(payload, bytes):
                json_payload = payload
            else:
                raise ValueError(f"Unsupported POST payload type: {type(payload)}")

            gzip_start = time.monotonic()
            gzip_payload = gzip.compress(json_payload, compresslevel=1)
            performance["gzip_time"] = time.monotonic() - gzip_start
            if len(gzip_payload) > 0:
                performance["gzip_ratio"] = len(json_payload) / len(gzip_payload)

            headers.update(
                {
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                }
            )
            data = gzip_payload

        session = await self._get_async_session()

        retry_attempt = 0
        timeout = aiohttp.ClientTimeout(
            connect=tpuf.connect_timeout, total=tpuf.read_timeout
        )

        while retry_attempt < tpuf.max_retries:
            request_start = time.monotonic()
            try:
                async with session.request(
                    method or "GET",
                    url,
                    params=query,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                    timeout=timeout,
                ) as response:
                    performance["request_time"] = time.monotonic() - request_start

                    # Handle server errors with retries
                    if (
                        response.status >= 500
                        or response.status == 408
                        or response.status == 429
                    ):
                        response.raise_for_status()

                    # Extract server timing information
                    server_timing_str = response.headers.get("Server-Timing", "")
                    if server_timing_str:
                        match_cache_hit_ratio = re.match(
                            r".*cache_hit_ratio;ratio=([\d\.]+)", server_timing_str
                        )
                        if match_cache_hit_ratio:
                            try:
                                performance["cache_hit_ratio"] = float(
                                    match_cache_hit_ratio.group(1)
                                )
                            except ValueError:
                                pass
                        match_processing = re.match(
                            r".*processing_time;dur=([\d\.]+)", server_timing_str
                        )
                        if match_processing:
                            try:
                                performance["server_time"] = (
                                    float(match_processing.group(1)) / 1000.0
                                )
                            except ValueError:
                                pass
                        match_exhaustive = re.match(
                            r".*exhaustive_search_count;count=([\d\.]+)",
                            server_timing_str,
                        )
                        if match_exhaustive:
                            try:
                                performance["exhaustive_search_count"] = int(
                                    match_exhaustive.group(1)
                                )
                            except ValueError:
                                pass

                    # Handle HEAD request
                    if method == "HEAD":
                        return {
                            "status_code": response.status,
                            "headers": dict(response.headers),
                            "performance": performance,
                        }

                    # Process response content
                    content_type = response.headers.get("Content-Type", "text/plain")
                    if content_type == "application/json":
                        try:
                            content = await response.json()
                        except json.JSONDecodeError as err:
                            text = await response.text()
                            raise_api_error(
                                response.status,
                                traceback.format_exception_only(err),
                                text,
                            )

                        if response.ok:
                            performance["total_time"] = time.monotonic() - start
                            return {
                                "status_code": response.status,
                                "ok": response.ok,
                                "headers": dict(response.headers),
                                "content": content,
                                "performance": performance,
                            }
                        else:
                            raise_api_error(
                                response.status,
                                content.get("status", "error"),
                                content.get("error", ""),
                            )
                    else:
                        text = await response.text()
                        raise_api_error(
                            response.status, "Server returned non-JSON response", text
                        )

            except (
                aiohttp.ClientResponseError,
                aiohttp.ClientConnectionError,
                asyncio.TimeoutError,
            ) as err:
                retry_attempt += 1

                if retry_attempt < tpuf.max_retries:
                    await asyncio.sleep(
                        2**retry_attempt
                    )  # exponential falloff up to 64 seconds for 6 retries
                else:
                    print(f"Request failed after {retry_attempt} attempts...")

                    if isinstance(err, aiohttp.ClientResponseError):
                        raise_api_error(
                            err.status,
                            f"Request to {url} failed after {retry_attempt} attempts",
                            str(err),
                        )
                    else:
                        raise

    def make_api_request(
        self,
        *args: List[str],
        method: Optional[str] = None,
        query: Optional[dict] = None,
        payload: Optional[dict] = None,
    ) -> dict:
        """
        Makes synchronous API requests to the Turbopuffer API by calling the async version.
        If this call succeeds, data is guaranteed to be durably written to object storage.
        """
        # Create an event loop or use the existing one
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            # No event loop exists in this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Call the async version and wait for the result
        return loop.run_until_complete(
            self.amake_api_request(*args, method=method, query=query, payload=payload)
        )
