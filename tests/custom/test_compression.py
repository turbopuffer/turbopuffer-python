import httpx
import respx
import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix
from tests.conftest import base_url
from tests.custom.conftest import region


def test_compression_disabled_by_default(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "compression-disabled-default")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1] * 4096,
                "title": "test doc",
            },
            {
                "id": 2,
                "vector": [0.2] * 4096,
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    response = ns.with_raw_response.query(
        rank_by=("vector", "ANN", [0.1] * 4096),
        top_k=2,
        include_attributes=True,
    )

    perf = response.parse().performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms == 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    assert "Content-Encoding" not in response.headers


@pytest.mark.asyncio
async def test_async_compression_disabled_by_default(async_tpuf: AsyncTurbopuffer):
    ns = async_tpuf.namespace(test_prefix + "async-compression-disabled-default")

    try:
        await ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    await ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1] * 4096,
                "title": "test doc",
            },
            {
                "id": 2,
                "vector": [0.2] * 4096,
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    response = await ns.with_raw_response.query(
        rank_by=("vector", "ANN", [0.1] * 4096),
        top_k=2,
        include_attributes=True,
    )

    perf = (await response.parse()).performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms == 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    assert "Content-Encoding" not in response.headers


@respx.mock
def test_accept_encoding_header_disabled_by_default():
    """Verify Accept-Encoding: identity header is sent by default."""
    query_route = respx.post(f"{base_url}/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, http_client=http_client)
    ns = client.namespace("test")
    ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"


@respx.mock
@pytest.mark.asyncio
async def test_async_accept_encoding_header_disabled_by_default():
    """Verify Accept-Encoding: identity header is sent by default (async)."""
    query_route = respx.post(f"{base_url}/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, http_client=http_client) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"

def test_compression_enabled_large_request():
    """Test that large requests are compressed when compression is enabled."""
    client = Turbopuffer(region=region, compression=True)
    ns = client.namespace(test_prefix + "compression-enabled-large")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1] * 4096,
                "title": "test doc",
            },
            {
                "id": 2,
                "vector": [0.2] * 4096,
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # This request and response are large enough to be compressed.
    response = ns.with_raw_response.query(
        rank_by=("vector", "ANN", [0.1] * 4096),
        top_k=2,
        include_attributes=True,
    )

    perf = response.parse().performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms > 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    assert response.headers["Content-Encoding"] == "gzip"


def test_compression_enabled_small_request():
    """Test that small requests are not compressed even when compression is enabled."""
    client = Turbopuffer(region=region, compression=True)
    ns = client.namespace(test_prefix + "compression-enabled-small")

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
    response = ns.with_raw_response.query(
        rank_by=("vector", "ANN", [0.1]),
        top_k=1,
        include_attributes=True,
    )

    perf = response.parse().performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms == 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    assert "Content-Encoding" not in response.headers


@pytest.mark.asyncio
async def test_async_compression_enabled_large_request(async_tpuf: AsyncTurbopuffer):
    """Test that large requests are compressed when compression is enabled (async)."""
    client = async_tpuf.with_options(compression=True)
    ns = client.namespace(test_prefix + "async-compression-enabled-large")

    try:
        await ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    await ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1] * 4096,
                "title": "test doc",
            },
            {
                "id": 2,
                "vector": [0.2] * 4096,
                "title": "test doc",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # This request and response are large enough to be compressed.
    response = await ns.with_raw_response.query(
        rank_by=("vector", "ANN", [0.1] * 4096),
        top_k=1,
        include_attributes=True,
    )

    perf = (await response.parse()).performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms > 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    assert response.headers["Content-Encoding"] == "gzip"


@pytest.mark.asyncio
async def test_async_compression_enabled_small_request(async_tpuf: AsyncTurbopuffer):
    """Test that small requests are not compressed even when compression is enabled (async)."""
    client = async_tpuf.with_options(compression=True)
    ns = client.namespace(test_prefix + "async-compression-enabled-small")

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

    # This request and response are too small to be compressed.
    response = await ns.with_raw_response.query(
        rank_by=("vector", "ANN", [0.1]),
        top_k=1,
        include_attributes=True,
    )

    perf = (await response.parse()).performance
    assert perf.client_total_ms > 0
    assert perf.client_compress_ms == 0
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    assert "Content-Encoding" not in response.headers


@respx.mock
def test_accept_encoding_header_enabled():
    """Verify Accept-Encoding: gzip header is sent when compression is enabled."""
    query_route = respx.post(f"{base_url}/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, compression=True, http_client=http_client)
    ns = client.namespace("test")
    ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "gzip"


@respx.mock
@pytest.mark.asyncio
async def test_async_accept_encoding_header_enabled():
    """Verify Accept-Encoding: gzip header is sent when compression is enabled (async)."""
    query_route = respx.post(f"{base_url}/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, compression=True, http_client=http_client) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "gzip"
