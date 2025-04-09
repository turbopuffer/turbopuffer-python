import turbopuffer as tpuf
import tests


def test_copy_from_namespace():
    ns1_name = tests.test_prefix + "copy_from_namespace_1"
    ns1 = tpuf.Namespace(ns1_name)
    ns2 = tpuf.Namespace(tests.test_prefix + "copy_from_namespace_2")

    ns1.write(
        upsert_columns={
            "id": [1, 2, 3, 4],
            "vector": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
            "fact_id": ["a", "b", "c", "d"],
        },
        distance_metric="euclidean_squared",
    )

    ns2.copy_from_namespace(ns1_name)

    query_results = ns2.query(vector=[0.1, 0.1], top_k=10)
    assert len(query_results) == 4
