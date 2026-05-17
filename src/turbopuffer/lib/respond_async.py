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
from typing import Any, Optional
from typing_extensions import Literal

import anyio
import httpx
import pydantic

from .._types import omit
from .._compat import parse_obj
from .._models import BaseModel, FinalRequestOptions
from .._exceptions import APIResponseValidationError
from .._base_client import SyncAPIClient, AsyncAPIClient

HEADER_PREFER = "prefer"
HEADER_PREFERENCE_APPLIED = "preference-applied"
HEADER_LOCATION = "location"
RESPOND_ASYNC = "respond-async"

POLL_INTERVAL_SECS = 1


def prepare_options(options: FinalRequestOptions) -> None:
    existing = options.headers or {}

    # Don't overwrite an existing `prefer` header. This allows the caller to disable async mode.
    if any(k.lower() == HEADER_PREFER for k in existing):
        return

    options.headers = {**existing, HEADER_PREFER: RESPOND_ASYNC}


def process_response(*, response: httpx.Response, client: SyncAPIClient) -> httpx.Response:
    if not _respond_async_applied(response):
        return response

    orig_request = response.request
    location = response.headers[HEADER_LOCATION]

    while True:
        poll = client.request(
            cast_to=httpx.Response,
            options=FinalRequestOptions.construct(
                method="get",
                url=location,
                headers={HEADER_PREFER: omit},
            ),
        )
        if resp := _resolve_poll_response(poll, orig_request):
            return resp

        time.sleep(POLL_INTERVAL_SECS)


async def process_response_aio(*, response: httpx.Response, client: AsyncAPIClient) -> httpx.Response:
    if not _respond_async_applied(response):
        return response

    orig_request = response.request
    location = response.headers[HEADER_LOCATION]

    while True:
        poll = await client.request(
            cast_to=httpx.Response,
            options=FinalRequestOptions.construct(
                method="get",
                url=location,
                headers={HEADER_PREFER: omit},
            ),
        )
        if resp := _resolve_poll_response(poll, orig_request):
            return resp

        await anyio.sleep(POLL_INTERVAL_SECS)


def _respond_async_applied(response: httpx.Response) -> bool:
    if response.status_code != 202:
        return False
    applied = response.headers.get(HEADER_PREFERENCE_APPLIED, "")
    return bool(applied.strip().lower() == RESPOND_ASYNC)


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
