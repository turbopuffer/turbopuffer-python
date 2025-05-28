from turbopuffer import Turbopuffer
from tests.custom import test_prefix


def test_perf_metrics(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "perf_metrics")

    ns.write(
        upsert_rows=[
            {"id": 1, "vector": [0.1, 0.1]},
            {"id": 2, "vector": [0.2, 0.2], "hello": "world", "test": "rows"},
        ],
        distance_metric="cosine_distance",
    )

    result = ns.query(
        rank_by=("vector", "ANN", [0.0, 0.3]),
        include_attributes=["hello"],
        filters=("hello", "Eq", "world"),
        top_k=10,
    )

    performance = result.performance

    assert type(performance.cache_hit_ratio) is float
    assert performance.cache_temperature in ["hot", "warm", "cold"]
    assert performance.exhaustive_search_count == 2
    assert performance.server_total_ms > 0
    assert performance.query_execution_ms > 0
