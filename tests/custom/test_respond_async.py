import httpx
import respx
import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.conftest import api_key, base_url
from turbopuffer.lib import respond_async

WRITE_OK_BODY = {
    "billing": {
        "billable_logical_bytes_written": 0,
        "billable_logical_bytes_returned": 0,
    },
    "message": "OK",
    "rows_affected": 1,
    "status": "OK",
}


@pytest.fixture(autouse=True)
def _no_poll_delay(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    monkeypatch.setattr(respond_async, "POLL_INTERVAL_SECS", 0)


@respx.mock
def test_sync_prefer_header_sent() -> None:
    route = respx.post(f"{base_url}/v2/namespaces/test").mock(return_value=httpx.Response(200, json=WRITE_OK_BODY))

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)
    client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert route.called
    assert route.calls.last.request.headers.get("prefer") == "respond-async"


@respx.mock
@pytest.mark.asyncio
async def test_async_prefer_header_sent() -> None:
    route = respx.post(f"{base_url}/v2/namespaces/test").mock(return_value=httpx.Response(200, json=WRITE_OK_BODY))

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert route.called
    assert route.calls.last.request.headers.get("prefer") == "respond-async"


@respx.mock
def test_sync_pass_through_sync_response() -> None:
    route = respx.post(f"{base_url}/v2/namespaces/test").mock(return_value=httpx.Response(200, json=WRITE_OK_BODY))

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)
    resp = client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert route.called
    assert route.call_count == 1
    assert resp.status == "OK"
    assert resp.rows_affected == 1


@respx.mock
@pytest.mark.asyncio
async def test_async_pass_through_sync_response() -> None:
    route = respx.post(f"{base_url}/v2/namespaces/test").mock(return_value=httpx.Response(200, json=WRITE_OK_BODY))

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        resp = await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert route.called
    assert route.call_count == 1
    assert resp.status == "OK"
    assert resp.rows_affected == 1


@respx.mock
def test_sync_async_applied_and_polled_to_success() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-abc"
    write_route = respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    poll_route = respx.get(poll_url).mock(
        side_effect=[
            httpx.Response(200, json={"status": "running"}),
            httpx.Response(200, json={"status": "running"}),
            httpx.Response(
                200,
                json={"status": "finished", "result": {"success": WRITE_OK_BODY}},
            ),
        ]
    )

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)
    resp = client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert write_route.call_count == 1
    assert poll_route.call_count == 3
    assert resp.status == "OK"
    # Auth headers should propagate to the poll request.
    assert poll_route.calls.last.request.headers.get("authorization") is not None


@respx.mock
@pytest.mark.asyncio
async def test_async_async_applied_and_polled_to_success() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-abc"
    write_route = respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    poll_route = respx.get(poll_url).mock(
        side_effect=[
            httpx.Response(200, json={"status": "running"}),
            httpx.Response(200, json={"status": "running"}),
            httpx.Response(
                200,
                json={"status": "finished", "result": {"success": WRITE_OK_BODY}},
            ),
        ]
    )

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        resp = await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert write_route.call_count == 1
    assert poll_route.call_count == 3
    assert resp.status == "OK"
    # Auth headers should propagate to the poll request.
    assert poll_route.calls.last.request.headers.get("authorization") is not None


@respx.mock
def test_sync_async_finished_with_error() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-fail"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    respx.get(poll_url).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": "finished",
                "result": {"error": {"status_code": 404, "detail": {"message": "namespace not found"}}},
            },
        )
    )

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)

    with pytest.raises(turbopuffer.NotFoundError) as excinfo:
        client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})
    assert "namespace not found" in str(excinfo.value)


@respx.mock
@pytest.mark.asyncio
async def test_async_async_finished_with_error() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-fail"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    respx.get(poll_url).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": "finished",
                "result": {"error": {"status_code": 404, "detail": {"message": "namespace not found"}}},
            },
        )
    )

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        with pytest.raises(turbopuffer.NotFoundError) as excinfo:
            await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})
        assert "namespace not found" in str(excinfo.value)


@respx.mock
def test_sync_pass_through_unrelated_202() -> None:
    route = respx.post(f"{base_url}/v2/namespaces/test").mock(return_value=httpx.Response(202, json=WRITE_OK_BODY))

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)
    resp = client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert route.call_count == 1
    assert resp.status == "OK"


@respx.mock
@pytest.mark.asyncio
async def test_async_pass_through_unrelated_202() -> None:
    route = respx.post(f"{base_url}/v2/namespaces/test").mock(return_value=httpx.Response(202, json=WRITE_OK_BODY))

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        resp = await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert route.call_count == 1
    assert resp.status == "OK"


@respx.mock
def test_sync_poll_transient_failure() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-flaky"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    poll_route = respx.get(poll_url).mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(503),
            httpx.Response(
                200,
                json={"status": "finished", "result": {"success": WRITE_OK_BODY}},
            ),
        ]
    )

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)
    resp = client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert poll_route.call_count == 3
    assert resp.status == "OK"


@respx.mock
@pytest.mark.asyncio
async def test_async_poll_transient_failure() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-flaky"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    poll_route = respx.get(poll_url).mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(503),
            httpx.Response(
                200,
                json={"status": "finished", "result": {"success": WRITE_OK_BODY}},
            ),
        ]
    )

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        resp = await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    assert poll_route.call_count == 3
    assert resp.status == "OK"


@respx.mock
def test_sync_poll_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(respond_async, "POLL_INTERVAL_SECS", 0.01)

    poll_url = f"{base_url}/v1/namespaces/test/operations/op-slow"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={"preference-applied": "respond-async", "location": poll_url},
        )
    )
    respx.get(poll_url).mock(return_value=httpx.Response(200, json={"status": "running"}))

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client, timeout=0.05)

    with pytest.raises(turbopuffer.APITimeoutError):
        client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})


@respx.mock
@pytest.mark.asyncio
async def test_async_poll_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(respond_async, "POLL_INTERVAL_SECS", 0.01)

    poll_url = f"{base_url}/v1/namespaces/test/operations/op-slow"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={"preference-applied": "respond-async", "location": poll_url},
        )
    )
    respx.get(poll_url).mock(return_value=httpx.Response(200, json={"status": "running"}))

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client, timeout=0.05) as client:
        with pytest.raises(turbopuffer.APITimeoutError):
            await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})


@respx.mock
def test_sync_async_applied_missing_location_header() -> None:
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(202, headers={"preference-applied": "respond-async"})
    )

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)

    with pytest.raises(turbopuffer.APIResponseValidationError):
        client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})


@respx.mock
@pytest.mark.asyncio
async def test_async_async_applied_missing_location_header() -> None:
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(202, headers={"preference-applied": "respond-async"})
    )

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        with pytest.raises(turbopuffer.APIResponseValidationError):
            await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})


@respx.mock
def test_sync_poll_too_many_failures() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-dead"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    respx.get(poll_url).mock(return_value=httpx.Response(503))

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client, max_retries=0)

    with pytest.raises(turbopuffer.InternalServerError):
        client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})


@respx.mock
@pytest.mark.asyncio
async def test_async_poll_too_many_failures() -> None:
    poll_url = f"{base_url}/v1/namespaces/test/operations/op-dead"
    respx.post(f"{base_url}/v2/namespaces/test").mock(
        return_value=httpx.Response(
            202,
            headers={
                "preference-applied": "respond-async",
                "location": poll_url,
            },
        )
    )
    respx.get(poll_url).mock(return_value=httpx.Response(503))

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client, max_retries=0) as client:
        with pytest.raises(turbopuffer.InternalServerError):
            await client.namespace("test").write(upsert_columns={"id": [1], "vector": [[0.1]]})
