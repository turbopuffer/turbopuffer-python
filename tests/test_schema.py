import turbopuffer as tpuf
import tests

def test_schema():
    ns = tpuf.Namespace(tests.test_prefix + "schema")

    # Upsert some data
    ns.upsert([
        {'id': 2, 'vector': [2, 2]},
        {'id': 7, 'vector': [0.7, 0.7], 'attributes': {'hello': 'world', 'test': 'rows'}},
    ], distance_metric='euclidean_squared')

    # Get the schema for the namespace
    schema = ns.schema()
    for attr in ['hello', 'test']:
        assert schema.get(attr).type == "OptString"
        assert schema.get(attr).filterable
        assert schema.get(attr).bm25 is None
    
    # todo patch schema

