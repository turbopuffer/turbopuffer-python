import turbopuffer as tpuf
import tests


def test_perf_metrics():
    ns = tpuf.Namespace(tests.test_prefix + 'perf_metrics')

    ns.write(
        upsert_rows=[
            {'id': 1, 'vector': [0.1, 0.1]},
            {'id': 2, 'vector': [0.2, 0.2], 'hello': 'world', 'test': 'rows'},
        ],
        distance_metric='cosine_distance'
    )

    result = ns.query(
        rank_by=["vector", "ANN", [0.0, 0.3]],
        distance_metric='cosine_distance',
        include_attributes=['hello'],
        filters=['hello', 'Eq', 'world'],
    )

    metrics = result.performance

    assert type(metrics['cache_hit_ratio']) is float
    assert metrics['cache_temperature'] in ['hot', 'warm', 'cold']
    assert metrics['exhaustive_search_count'] == 2
    assert metrics['server_total_ms'] > 0
    assert metrics['query_execution_ms'] > 0
