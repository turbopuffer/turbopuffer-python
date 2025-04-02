import turbopuffer as tpuf
import tests


def test_perf_metrics():
    ns = tpuf.Namespace(tests.test_prefix + 'perf_metrics')

    ns.upsert([
        {'id': 1, 'vector': [0.1, 0.1]},
        {'id': 2, 'vector': [0.2, 0.2], 'attributes': {'hello': 'world', 'test': 'rows'}},
    ], distance_metric='cosine_distance')

    results = ns.query(
        vector=[0.0, 0.3],
        distance_metric='cosine_distance',
        include_attributes=['hello'],
        filters=['hello', 'Eq', 'world'],
    )

    metrics = results.performance

    assert metrics['server_time'] > 0.010
    assert metrics['query_execution_time'] > 0.010
