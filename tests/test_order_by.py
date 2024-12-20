import turbopuffer as tpuf
import tests

def test_order_by_attribute():
    ns = tpuf.Namespace(tests.test_prefix + "order_by_attribute")

    ns.upsert(
        {
            "ids": [1, 2, 3, 4],
            "vectors": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
            "attributes": {
                "fact_id": ["a", "b", "c", "d"],
            },
        }
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
