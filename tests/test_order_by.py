import turbopuffer as tpuf
import tests

def test_order_by_attribute():
    ns = tpuf.Namespace(tests.test_prefix + "order_by_attribute")

    ns.write(
        upsert_columns={
            "id": [1, 2, 3, 4],
            "vector": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
            "fact_id": ["a", "b", "c", "d"],
        },
        distance_metric='euclidean_squared',
    )

    results = ns.query(
        rank_by=("fact_id", "asc"),
        top_k=10
    )
    assert [item.id for item in results] == [1, 2, 3, 4]

    results = ns.query(
        rank_by=("fact_id", "desc"),
        top_k=10
    )
    assert [item.id for item in results] == [4, 3, 2, 1]
