import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix


def test_compression_disabled(tpuf: Turbopuffer):
    # Create a client with compression disabled
    client = Turbopuffer(
        api_key=tpuf.api_key,
        region=tpuf.region,
        default_namespace=tpuf.default_namespace,
        compression=False
    )
    ns = client.namespace(test_prefix + "compression-disabled")

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


def test_compression_disabled_constructor():
    # Test that compression can be disabled via constructor
    client = Turbopuffer(
        api_key="test",
        region="aws-us-east-2", 
        compression=False
    )
    assert client.compression is False


@pytest.mark.asyncio
async def test_async_compression_disabled(async_tpuf: AsyncTurbopuffer):
    # Create an async client with compression disabled
    async with AsyncTurbopuffer(
        api_key=async_tpuf.api_key,
        region=async_tpuf.region,
        default_namespace=async_tpuf.default_namespace,
        compression=False
    ) as client:
        ns = client.namespace(test_prefix + "async-compression-disabled")

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

        # This request is large enough to normally be compressed, but compression is disabled.
        result = await ns.query(
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
async def test_async_compression_disabled_constructor():
    # Test that compression can be disabled via constructor
    client = AsyncTurbopuffer(
        api_key="test",
        region="aws-us-east-2",
        compression=False
    )
    assert client.compression is False