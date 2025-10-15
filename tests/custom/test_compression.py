import httpx
import pytest

import turbopuffer
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.custom import test_prefix


def test_compression_auto_on(tpuf: Turbopuffer):
    # Capture request headers using an event hook
    captured_headers: dict[str, str] = {}

    def capture_request(request: httpx.Request) -> None:
        captured_headers["Accept-Encoding"] = request.headers.get("Accept-Encoding", "")

    # Create a custom HTTP client with event hooks
    with httpx.Client(event_hooks={"request": [capture_request]}) as http_client:
        client_with_hooks = tpuf.with_options(http_client=http_client)

        ns = client_with_hooks.namespace(test_prefix + "compression-auto-on")

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

        # Verify Accept-Encoding: gzip header was sent
        assert captured_headers.get("Accept-Encoding") == "gzip"

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
