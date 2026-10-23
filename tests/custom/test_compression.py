import gzip
import json
from io import BytesIO
from typing import Any
from unittest.mock import Mock

import httpx2
import pytest

import turbopuffer
from tests import respx2 as respx
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix
from tests.conftest import api_key, base_url


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
        return_value=httpx2.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx2.Client(transport=httpx2.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client)
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
        return_value=httpx2.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=http_client) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"


def test_compression_enabled_large_request(tpuf: Turbopuffer):
    """Test that large requests are compressed when compression is enabled."""
    client = tpuf.with_options(compression=True)
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


def test_compression_enabled_small_request(tpuf: Turbopuffer):
    """Test that small requests are not compressed even when compression is enabled."""
    client = tpuf.with_options(compression=True)
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
        return_value=httpx2.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx2.Client(transport=httpx2.HTTPTransport())
    client = Turbopuffer(base_url=base_url, api_key=api_key, compression=True, http_client=http_client)
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
        return_value=httpx2.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    http_client = httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport())
    async with AsyncTurbopuffer(
        base_url=base_url, api_key=api_key, compression=True, http_client=http_client
    ) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "gzip"


@pytest.mark.parametrize("large", [False, True], ids=["small", "large"])
@pytest.mark.parametrize(
    "options, compression_enabled",
    [({}, False), ({"compression": False}, False), ({"compression": True}, True)],
    ids=["default", "disabled", "enabled"],
)
def test_urllib3_transport_compression(
    options: dict[str, Any], compression_enabled: bool, large: bool, monkeypatch: pytest.MonkeyPatch
):
    """Verify the urllib3 transport honors the compression option, compressing only large requests."""
    urllib3 = pytest.importorskip("urllib3")
    from turbopuffer.lib.transport_urllib3 import Urllib3Transport

    # respx can't intercept urllib3, so mock the transport's pool instead.
    transport = Urllib3Transport()
    pool_request = Mock(return_value=urllib3.HTTPResponse(body=BytesIO(b"{}"), status=200, preload_content=False))
    monkeypatch.setattr(transport._pool, "request", pool_request)

    http_client = httpx2.Client(transport=transport)
    with Turbopuffer(base_url=base_url, api_key=api_key, http_client=http_client, **options) as client:
        client.namespace("test").write(upsert_rows=[{"id": 1, "vector": [0.1] * (1024 if large else 1)}])

    expect_compressed = compression_enabled and large
    sent = pool_request.call_args.kwargs
    assert (sent["headers"].get("Content-Encoding") == "gzip") is expect_compressed
    assert int(sent["headers"]["Content-Length"]) == len(sent["body"])

    body = gzip.decompress(sent["body"]) if expect_compressed else sent["body"]
    assert json.loads(body)["upsert_rows"][0]["id"] == 1
