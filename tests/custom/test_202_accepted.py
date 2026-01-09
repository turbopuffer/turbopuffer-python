"""Test for 202 Accepted response handling.

This test verifies the behavior when the query endpoint returns a 202 Accepted
status code with an error body. The hypothesis from the Slack thread is that
Stainless incorrectly returns an empty result (rows=[]) instead of raising an error.

See: https://github.com/turbopuffer/turbopuffer/pull/6421

Bug summary:
- When the server returns HTTP 202 Accepted with an error body like:
  {"status": "error", "error": "Operation requires a newer index version..."}
- The SDK treats this as a successful response
- It parses the error body as a NamespaceQueryResponse
- This results in rows=None, billing=None, performance=None
- No exception is raised, even though the response indicates an error

Expected behavior:
- The SDK should recognize 202 responses with error bodies and raise an appropriate exception
"""

from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer._base_client import DefaultAsyncHttpxClient

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "tpuf_A1..."

ERROR_BODY = {
    "status": "error",
    "error": "💁 Operation requires a newer index version. We've gone ahead and queued this on your behalf. Once finished, you can retry this request!",
}


@pytest.mark.respx(base_url=base_url)
def test_query_202_accepted_returns_empty_rows(respx_mock: MockRouter) -> None:
    """
    Test that a 202 Accepted response with an error body incorrectly returns
    empty rows instead of raising an error.

    This test documents the current (buggy) behavior where the SDK silently
    returns an empty result instead of raising an error when the server returns
    a 202 Accepted with an error payload.

    The response object will have:
    - rows=None (instead of actual rows or an error)
    - billing=None (should be required per the type definition)
    - performance=None (should be required per the type definition)
    - Extra fields status='error' and error='...' from the error body
    """
    respx_mock.post("/v2/namespaces/test-namespace/query").mock(
        return_value=httpx.Response(202, json=ERROR_BODY)
    )

    client = Turbopuffer(base_url=base_url, api_key=api_key, _strict_response_validation=False)

    # Call query - this should ideally raise an error, but due to the bug
    # it returns an empty/default response instead
    result = client.namespace("test-namespace").query()

    # The bug manifests as:
    # 1. rows is None instead of containing data or an exception being raised
    assert result.rows is None

    # 2. Required fields billing and performance are None (violating the type contract)
    assert result.billing is None
    assert result.performance is None

    # 3. The error fields from the response body are silently captured as extra fields
    result_dict = result.model_dump()
    assert result_dict.get("status") == "error"
    assert "Operation requires a newer index version" in str(result_dict.get("error", ""))

    client.close()


@pytest.mark.respx(base_url=base_url)
async def test_query_202_accepted_returns_empty_rows_async(respx_mock: MockRouter) -> None:
    """
    Test that a 202 Accepted response with an error body incorrectly returns
    empty rows instead of raising an error (async version).
    """
    respx_mock.post("/v2/namespaces/test-namespace/query").mock(
        return_value=httpx.Response(202, json=ERROR_BODY)
    )

    client = AsyncTurbopuffer(
        base_url=base_url,
        api_key=api_key,
        _strict_response_validation=False,
        http_client=DefaultAsyncHttpxClient(transport=httpx.AsyncHTTPTransport()),
    )

    result = await client.namespace("test-namespace").query()

    # The bug manifests as:
    # 1. rows is None instead of containing data or an exception being raised
    assert result.rows is None

    # 2. Required fields billing and performance are None (violating the type contract)
    assert result.billing is None
    assert result.performance is None

    # 3. The error fields from the response body are silently captured as extra fields
    result_dict = result.model_dump()
    assert result_dict.get("status") == "error"
    assert "Operation requires a newer index version" in str(result_dict.get("error", ""))

    await client.close()
