import os
from typing import Any, Dict

import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer, NotFoundError
from tests.custom import test_prefix
from tests.custom.conftest import region


# Helper to get client kwargs that work in both local and production environments
def get_test_client_kwargs() -> Dict[str, Any]:
    # If there's an explicit base URL set that doesn't use {region}, use it directly
    base_url = os.environ.get("TURBOPUFFER_BASE_URL")
    if base_url and "{region}" not in base_url:
        return {"base_url": base_url}
    else:
        # Use region-based approach for production URLs
        return {"region": region}


def test_compression_disabled(tpuf: Turbopuffer):
    # Test both ways of disabling compression
    kwargs = get_test_client_kwargs()
    kwargs["compression"] = False
    clients = [
        tpuf.with_options(compression=False),  # via with_options()
        Turbopuffer(**kwargs),  # via constructor
    ]

    for i, client in enumerate(clients):
        ns = client.namespace(f"{test_prefix}compression-disabled-{i}")

        try:
            ns.delete_all()
        except NotFoundError:
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
    kwargs = get_test_client_kwargs()
    kwargs["compression"] = False
    client = Turbopuffer(**kwargs)
    assert client.compression is False


@pytest.mark.asyncio
async def test_async_compression_disabled(async_tpuf: AsyncTurbopuffer):
    # Test via with_options()
    client = async_tpuf.with_options(compression=False)
    ns = client.namespace(f"{test_prefix}async-compression-disabled-with-options")

    try:
        await ns.delete_all()
    except NotFoundError:
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
    assert perf.client_compress_ms == 0  # Should be 0 since compression is disabled
    assert perf.client_response_ms is not None and perf.client_response_ms > 0
    assert perf.client_body_read_ms is not None and perf.client_body_read_ms > 0
    assert perf.client_deserialize_ms > 0

    # Test via constructor (with proper async context manager)
    kwargs = get_test_client_kwargs()
    kwargs["compression"] = False
    async with AsyncTurbopuffer(**kwargs) as constructor_client:
        ns2 = constructor_client.namespace(f"{test_prefix}async-compression-disabled-constructor")

        try:
            await ns2.delete_all()
        except NotFoundError:
            pass

        await ns2.write(
            upsert_rows=[
                {
                    "id": 1,
                    "vector": [0.1] * 1024,
                    "title": "test doc",
                },
            ],
            distance_metric="euclidean_squared",
        )

        result = await ns2.query(
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
    kwargs = get_test_client_kwargs()
    kwargs["compression"] = False
    client = AsyncTurbopuffer(**kwargs)
    assert client.compression is False