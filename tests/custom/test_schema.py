import pytest

import turbopuffer
from turbopuffer import Turbopuffer
from tests.custom import test_prefix
from turbopuffer.types import AttributeSchemaConfigParam


def test_schema(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "schema")

    # Upsert some data
    ns.write(
        upsert_rows=[{"id": 2, "vector": [2, 2]}, {"id": 7, "vector": [0.7, 0.7], "hello": "world", "test": "rows"}],
        distance_metric="euclidean_squared",
    )

    # Get the schema for the namespace
    schema = ns.schema()
    for attr in ["hello", "test"]:
        assert schema[attr].type == "string"
        assert schema[attr].filterable
        assert schema[attr].full_text_search is None

    # Write an update to the schema making 'hello' not filterable
    updated_hello_schema = AttributeSchemaConfigParam(type="string", filterable=False)
    updated_schema = ns.update_schema(schema={"hello": updated_hello_schema})
    assert not updated_schema["hello"].filterable

    # If we try to query using a filter on 'hello', we should get an error
    # since it's not filterable anymore
    with pytest.raises(turbopuffer.TurbopufferError):
        ns.query(rank_by=("vector", "ANN", [2, 2]), top_k=10, filters=("hello", "Eq", "foobar"))
