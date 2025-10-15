import httpx
import respx
import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix
from tests.conftest import base_url
from tests.custom.conftest import region


def test_compression_disabled(tpuf: Turbopuffer):
    # Test both ways of disabling compression
    clients = [
        tpuf.with_options(compression=False),  # via with_options()
        Turbopuffer(region=region, compression=False),  # via constructor
    ]

    for i, client in enumerate(clients):
        assert client.compression is False

        ns = client.namespace(f"{test_prefix}compression-disabled-{i}")

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

        # This request is large enough to normally be compressed, but compression is disabled.
        response = ns.with_raw_response.query(
            rank_by=("vector", "ANN", [0.1] * 4096),
            top_k=2,
            include_attributes=True,
        )

        perf = response.parse().performance
        assert perf.client_total_ms > 0
        assert perf.client_compress_ms == 0  # Should be 0 since compression is disabled
        assert perf.client_response_ms is not None and perf.client_response_ms > 0
        assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
        assert perf.client_deserialize_ms > 0

        assert "Content-Encoding" not in response.headers


@pytest.mark.asyncio
async def test_async_compression_disabled(async_tpuf: AsyncTurbopuffer):
    # Test both ways of disabling compression
    async with AsyncTurbopuffer(region=region, compression=False) as constructor_client:
        clients = [
            async_tpuf.with_options(compression=False),  # via with_options()
            constructor_client,  # via constructor
        ]

        for i, client in enumerate(clients):
            assert client.compression is False

            ns = client.namespace(f"{test_prefix}compression-disabled-{i}")

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
            assert (
                perf.client_compress_ms == 0
            )  # Should be 0 since compression is disabled
            assert perf.client_response_ms is not None and perf.client_response_ms > 0
            assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
            assert perf.client_deserialize_ms > 0

            assert "Content-Encoding" not in response.headers


@respx.mock
def test_accept_encoding_header_disabled():
    """Verify Accept-Encoding: identity header is sent when compression is disabled."""
    # Mock the query endpoint
    query_route = respx.post(f"{base_url}/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    # Use standard httpx client for mocking to work
    http_client = httpx.Client(transport=httpx.HTTPTransport())
    client = Turbopuffer(base_url=base_url, compression=False, http_client=http_client)
    ns = client.namespace("test")
    ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"


@respx.mock
@pytest.mark.asyncio
async def test_async_accept_encoding_header_disabled():
    """Verify Accept-Encoding: identity header is sent when compression is disabled (async)."""
    # Mock the query endpoint
    query_route = respx.post(f"{base_url}/v2/namespaces/test/query").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    # Use standard httpx client for mocking to work
    http_client = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport())
    async with AsyncTurbopuffer(base_url=base_url, compression=False, http_client=http_client) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert query_route.called
    request = query_route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"
