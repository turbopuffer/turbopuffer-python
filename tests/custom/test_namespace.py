from turbopuffer import Turbopuffer
from tests.custom import test_prefix


def test_namespace_hint_cache_warm(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "namespace_hint_cache_warm")

    # Upsert anything
    ns.write(
        upsert_rows=[
            {"id": 2, "vector": [2, 2]},
            {"id": 7, "vector": [0.7, 0.7], "hello": "world", "test": "rows"},
        ],
        distance_metric="euclidean_squared",
    )

    result = ns.hint_cache_warm()
    assert isinstance(result.message, str)
    assert result.status in ["ACCEPTED", "OK"]
