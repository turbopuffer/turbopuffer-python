import pytest

from turbopuffer import AsyncTurbopuffer
from tests.custom import test_prefix


@pytest.mark.asyncio
async def test_order_by_attribute(async_tpuf: AsyncTurbopuffer):
    ns = async_tpuf.namespace(test_prefix + "order_by_attribute")

    await ns.write(
        upsert_columns={
            "id": [1, 2, 3, 4],
            "vector": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
            "fact_id": ["a", "b", "c", "d"],
        },
        distance_metric="euclidean_squared",
    )

    results = await ns.query(rank_by=("fact_id", "asc"), top_k=10)
    assert results.rows is not None
    assert [item.id for item in results.rows] == [1, 2, 3, 4]

    results = await ns.query(rank_by=("fact_id", "desc"), top_k=10)
    assert results.rows is not None
    assert [item.id for item in results.rows] == [4, 3, 2, 1]
