from turbopuffer import Turbopuffer
from tests.custom import test_prefix


def test_patches(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "patches")

    ns.write(
        upsert_rows=[
            {"id": 1, "vector": [1, 1]},
            {"id": 2, "vector": [2, 2]},
        ],
        distance_metric="euclidean_squared",
    )

    ns.write(
        patch_rows=[
            {"id": 1, "a": 1},
            {"id": 2, "b": 2},
        ],
    )

    ns.write(
        patch_rows=[
            {"id": 1, "b": 1},
            {"id": 2, "a": 2},
        ],
    )

    result = ns.query(rank_by=("id", "asc"), include_attributes=["a", "b"], top_k=10)
    assert result.rows is not None
    assert len(result.rows) == 2
    print(result.rows)
    assert result.rows[0].id == 1
    assert result.rows[0].a == 1
    assert result.rows[0].b == 1
    assert result.rows[1].id == 2
    assert result.rows[1].a == 2
    assert result.rows[1].b == 2

    ns.write(
        patch_columns={
            "id": [1, 2],
            "a": [11, 22],
            "c": [1, 2],
        },
    )

    result = ns.query(rank_by=("id", "asc"), include_attributes=["a", "b", "c"], top_k=10)
    assert result.rows is not None
    assert len(result.rows) == 2
    assert result.rows[0].id == 1
    assert result.rows[0].a == 11
    assert result.rows[0].b == 1
    assert result.rows[0].c == 1
    assert result.rows[1].id == 2
    assert result.rows[1].a == 22
    assert result.rows[1].b == 2
    assert result.rows[1].c == 2
