import turbopuffer as tpuf
import tests

def test_namespace():
    ns = tpuf.Namespace(tests.test_prefix + "namespace", base_url="https://gcp-us-east4.turbopuffer.com")

    ns.upsert([
        {'id': 1, 'vector': [0.1, 0.1]},
        {'id': 2, 'vector': [0.2, 0.2], 'attributes': {'test_name': 'namespace'}},
    ], distance_metric='euclidean_squared')

    results = ns.query(
        vector=[0, 0],
        distance_metric='euclidean_squared',
        include_attributes=['test_name']
    )
    assert len(results) == 2
