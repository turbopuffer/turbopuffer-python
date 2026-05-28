"""
Support for transparent polling of async tpuf APIs.

Every API request is stamped with `prefer: respond-async`. If the server
applies the preference (i.e. responds with `202 Accepted` +
`preference-applied: respond-async`) the SDK polls that URL until the operation
finishes and returns the final result as if the API call had been synchronous.

Wired in via `_prepare_options` and `_process_response` overrides on
`Turbopuffer`/`AsyncTurbopuffer`.
"""

from __future__ import annotations

import time
from typing import Any, Union, Optional
from typing_extensions import Literal

import anyio
import httpx
import pydantic

from .._types import omit
from .._utils import is_given
from .._compat import parse_obj
from .._models import BaseModel, FinalRequestOptions
from .._exceptions import APITimeoutError, APIResponseValidationError
from .._base_client import SyncAPIClient, AsyncAPIClient

HEADER_PREFER = "prefer"
HEADER_PREFERENCE_APPLIED = "preference-applied"
HEADER_LOCATION = "location"
RESPOND_ASYNC = "respond-async"

POLL_INTERVAL_SECS = 1
POLL_REQUEST_TIMEOUT_SECS = 60.0


def prepare_options(options: FinalRequestOptions) -> None:
    existing = options.headers or {}

    # Don't overwrite an existing `prefer` header. This allows the caller to disable async mode.
    if any(k.lower() == HEADER_PREFER for k in existing):
        return

    options.headers = {**existing, HEADER_PREFER: RESPOND_ASYNC}


def process_response(
    *,
    response: httpx.Response,
    client: SyncAPIClient,
    options: FinalRequestOptions,
) -> httpx.Response:
    if not _respond_async_applied(response):
        return response

    orig_request = response.request
    location = _extract_location(response)
    timeout = _Timeout(options, client.timeout)

    while True:
        if timeout.remaining() == 0:
            raise APITimeoutError(request=orig_request)

        poll = client.request(
            cast_to=httpx.Response,
            options=FinalRequestOptions.construct(
                method="get",
                url=location,
                headers={HEADER_PREFER: omit},
                timeout=timeout.poll_timeout(),
            ),
        )
        if resp := _resolve_poll_response(poll, orig_request):
            return resp

        time.sleep(timeout.sleep_duration())


async def process_response_aio(
    *,
    response: httpx.Response,
    client: AsyncAPIClient,
    options: FinalRequestOptions,
) -> httpx.Response:
    if not _respond_async_applied(response):
        return response

    orig_request = response.request
    location = _extract_location(response)
    timeout = _Timeout(options, client.timeout)

    while True:
        if timeout.remaining() == 0:
            raise APITimeoutError(request=orig_request)

        poll = await client.request(
            cast_to=httpx.Response,
            options=FinalRequestOptions.construct(
                method="get",
                url=location,
                headers={HEADER_PREFER: omit},
                timeout=timeout.poll_timeout(),
            ),
        )
        if resp := _resolve_poll_response(poll, orig_request):
            return resp

        await anyio.sleep(timeout.sleep_duration())


def _respond_async_applied(response: httpx.Response) -> bool:
    if response.status_code != 202:
        return False
    applied = response.headers.get(HEADER_PREFERENCE_APPLIED, "")
    return bool(applied.strip().lower() == RESPOND_ASYNC)


def _extract_location(response: httpx.Response) -> str:
    location: str = response.headers.get(HEADER_LOCATION, "").strip()
    if not location:
        raise APIResponseValidationError(
            response=response,
            body=response.text,
            message="missing 'Location' header on respond-async response",
        )
    return location


class _PollError(BaseModel):
    status_code: int
    detail: Any = None


class _PollResult(BaseModel):
    success: Any = None
    error: Optional[_PollError] = None


class _PollBody(BaseModel):
    status: Literal["running", "finished"]
    result: Optional[_PollResult] = None


def _resolve_poll_response(response: httpx.Response, request: httpx.Request) -> httpx.Response | None:
    try:
        body = parse_obj(_PollBody, response.json())
        if body.status == "running":
            return None
        if body.result is None:
            raise ValueError("missing 'result' field")
        if (body.result.success is None) == (body.result.error is None):
            raise ValueError("'result' must have exactly one of 'success'/'error'")
    except (pydantic.ValidationError, ValueError) as err:
        raise APIResponseValidationError(
            response=response, body=response.text, message=f"malformed poll response: {err}"
        ) from err

    if body.result.success is not None:
        return httpx.Response(
            status_code=200,
            json=body.result.success,
            request=request,
        )

    assert body.result.error is not None
    error = body.result.error
    return httpx.Response(
        status_code=error.status_code,
        json=error.detail,
        request=request,
    )


class _Timeout:
    """Timeout tracking for async polling."""

    def __init__(self, request_options: FinalRequestOptions, client_timeout: Union[float, httpx.Timeout, None]):
        timeout = request_options.timeout if is_given(request_options.timeout) else client_timeout
        if isinstance(timeout, httpx.Timeout):
            timeout = timeout.read

        if timeout is None:
            self.deadline = float("inf")
        else:
            self.deadline = time.monotonic() + timeout

    def remaining(self) -> float:
        return max(self.deadline - time.monotonic(), 0)

    def poll_timeout(self) -> float:
        return min(self.remaining(), POLL_REQUEST_TIMEOUT_SECS)

    def sleep_duration(self) -> float:
        return min(self.remaining(), POLL_INTERVAL_SECS)
