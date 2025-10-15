import httpx
import respx
import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix
from tests.custom.conftest import region


def test_compression_auto_on(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "compression-auto-on")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1] * 1024,
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # This request is large enough to be compressed.
    result = ns.query(
        rank_by=("vector", "ANN", [0.1] * 1024),
        top_k=1,
        include_attributes=True,
    )

    perf = result.performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms > 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0


def test_compression_auto_off(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "compression-auto-off")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1],
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # This request is too small to be compressed.
    result = ns.query(
        rank_by=("vector", "ANN", [0.1]),
        top_k=1,
        include_attributes=True,
    )

    perf = result.performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms == 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0


@pytest.mark.asyncio
async def test_async_compression_auto_on(async_tpuf: AsyncTurbopuffer):
    ns = async_tpuf.namespace(test_prefix + "async-compression-auto-on")

    try:
        await ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    await ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1] * 1024,
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # This request is large enough to be compressed.
    result = await ns.query(
        rank_by=("vector", "ANN", [0.1] * 1024),
        top_k=1,
        include_attributes=True,
    )

    perf = result.performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms > 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0


async def test_async_compression_auto_off(async_tpuf: AsyncTurbopuffer):
    ns = async_tpuf.namespace(test_prefix + "async-compression-auto-off")

    try:
        await ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    await ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1],
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # This request is too small to be compressed.
    result = await ns.query(
        rank_by=("vector", "ANN", [0.1]),
        top_k=1,
        include_attributes=True,
    )

    perf = result.performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms == 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0


@respx.mock
def test_accept_encoding_header_enabled():
    """Verify Accept-Encoding: gzip header is sent when compression is enabled."""
    # Mock the query endpoint
    query_route = respx.post(f"https://{region or 'api'}.turbopuffer.com/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    # Use standard httpx client for mocking to work
    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(region=region, compression=True, http_client=http_client)
    ns = client.namespace("test")
    ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "gzip"


@respx.mock
@pytest.mark.asyncio
async def test_async_accept_encoding_header_enabled():
    """Verify Accept-Encoding: gzip header is sent when compression is enabled (async)."""
    # Mock the query endpoint
    query_route = respx.post(f"https://{region or 'api'}.turbopuffer.com/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    # Use standard httpx client for mocking to work
    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(region=region, compression=True, http_client=http_client) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "gzip"
