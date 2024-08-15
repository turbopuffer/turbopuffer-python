import turbopuffer as tpuf
import tests
import pytest

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
        assert schema.get(attr).type == "?string"
        assert schema.get(attr).filterable
        assert schema.get(attr).full_text_search is None
    
    # Write an update to the schema making 'hello' not filterable
    updated_hello_schema = tpuf.AttributeSchema(type="?string", filterable=False, full_text_search=None)
    updated_schema = ns.update_schema({
        'hello': updated_hello_schema
    })
    assert not updated_schema.get('hello').filterable

    # If we try to query using a filter on 'hello', we should get an error
    # since it's not filterable anymore
    with pytest.raises(tpuf.TurbopufferError):
        ns.query(
            vector=[2, 2],
            top_k=10,
            filters={
                'hello': ['Eq', 'foobar']
            }
        )
