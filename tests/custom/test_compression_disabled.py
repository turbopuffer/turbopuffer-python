import httpx
import respx
import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix
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
                    "vector": [0.1] * 1024,
                    "title": "test doc",
                },
            ],
            distance_metric="euclidean_squared",
        )

        # This request is large enough to normally be compressed, but compression is disabled.
        result = ns.query(
            rank_by=("vector", "ANN", [0.1] * 1024),
            top_k=1,
            include_attributes=True,
        )

        perf = result.performance
        assert perf.client_total_ms > 0
        assert perf.client_compress_ms == 0  # Should be 0 since compression is disabled
        assert perf.client_response_ms is not None and perf.client_response_ms > 0
        assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
        assert perf.client_deserialize_ms > 0


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
                        "vector": [0.1] * 1024,
                        "title": "test doc",
                    },
                ],
                distance_metric="euclidean_squared",
            )

            result = await ns.query(
                rank_by=("vector", "ANN", [0.1] * 1024),
                top_k=1,
                include_attributes=True,
            )

            perf = result.performance
            assert perf.client_total_ms > 0
            assert (
                perf.client_compress_ms == 0
            )  # Should be 0 since compression is disabled
            assert perf.client_response_ms is not None and perf.client_response_ms > 0
            assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
            assert perf.client_deserialize_ms > 0


@respx.mock
def test_accept_encoding_header_disabled():
    """Verify Accept-Encoding: identity header is sent when compression is disabled."""
    route = respx.post(f"https://{region or 'api'}.turbopuffer.com/v1/vectors").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    client = Turbopuffer(region=region, compression=False)
    ns = client.namespace("test")
    ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert route.called
    request = route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"


@respx.mock
@pytest.mark.asyncio
async def test_async_accept_encoding_header_disabled():
    """Verify Accept-Encoding: identity header is sent when compression is disabled (async)."""
    route = respx.post(f"https://{region or 'api'}.turbopuffer.com/v1/vectors").mock(
        return_value=httpx.Response(200, json={"dist_metric": "euclidean_squared", "top_k": []})
    )

    async with AsyncTurbopuffer(region=region, compression=False) as client:
        ns = client.namespace("test")
        await ns.query(rank_by=("vector", "ANN", [0.1] * 10), top_k=1)

    assert route.called
    request = route.calls.last.request
    assert request.headers.get("Accept-Encoding") == "identity"
