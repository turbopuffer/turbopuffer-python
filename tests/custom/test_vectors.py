import uuid
from typing import List, Union

import numpy
import pytest

import turbopuffer
from turbopuffer import Omit, Turbopuffer, omit
from tests.custom import test_prefix
from turbopuffer.types import (
    Row,
    Vector,
    RowParam,
    ColumnsParam,
    QueryBilling,
    VectorEncoding,
    NamespaceQueryResponse,
    namespace_query_params,
)
from turbopuffer.lib.vector import b64decode_vector, b64encode_vector
from turbopuffer._utils._transform import transform, async_transform


@pytest.mark.xdist_group(name="group1")
def test_upsert_rows(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test")
    assert str(ns) == f"tpuf-namespace:{test_prefix}client_test"

    # Test upsert multiple dict rows
    ns.write(
        upsert_rows=[
            {"id": 2, "vector": [2, 2]},
            {"id": 7, "vector": [0.7, 0.7], "hello": "world"},
        ],
        distance_metric="euclidean_squared",
    )

    # Test upsert lazy row iterator
    ns.write(upsert_rows=[{"id": i, "vector": [i / 10, i / 10], "test": "rows"} for i in range(10, 100)])

    # Test upsert single rows should fail
    try:
        ns.write(
            upsert_rows={"id": 2, "vector": [2, 2]}  # type: ignore
        )
        raise AssertionError("Upserting single row should not be allowed")
    except turbopuffer.UnprocessableEntityError as err:
        assert "invalid type: map, expected a sequence" in err.message
    try:
        ns.write(
            upsert_rows={"id": 7, "vector": [0.7, 0.7], "hello": "world", "test": "rows"}  # type: ignore
        )
        raise AssertionError("Upserting single row should not be allowed")
    except turbopuffer.UnprocessableEntityError as err:
        assert "invalid type: map, expected a sequence" in err.message

    # Check to make sure the vectors were stored as expected
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 92, "Got wrong number of vectors back"
    assert dict(results.rows[0]) == {"id": 2, "vector": [2.0, 2.0]}
    assert dict(results.rows[1]) == {"id": 7, "vector": [0.7, 0.7], "hello": "world"}
    for i in range(10, 100):
        assert dict(results.rows[i - 8]) == {"id": i, "vector": [i / 10, i / 10], "test": "rows"}

    # Check to ensure recall is working
    ns.recall()


@pytest.mark.xdist_group(name="group1")
def test_delete_vectors(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test")

    # Test delete
    ns.write(deletes=[2])
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 91, "Got wrong number of vectors back"
    assert dict(results.rows[0]) == {"id": 7, "vector": [0.7, 0.7], "hello": "world"}

    ns.write(deletes=[10])
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 90, "Got wrong number of vectors back"
    assert dict(results.rows[1]) == {"id": 11, "vector": [1.1, 1.1], "test": "rows"}

    ns.write(deletes=[11])
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 89, "Got wrong number of vectors back"
    assert dict(results.rows[1]) == {"id": 12, "vector": [1.2, 1.2], "test": "rows"}

    ns.write(deletes=[12])
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 88, "Got wrong number of vectors back"
    assert dict(results.rows[1]) == {"id": 13, "vector": [1.3, 1.3], "test": "rows"}

    # Test delete single row
    ns.write(deletes=[13])
    # Test delete multi row
    ns.write(deletes=[14, 15, 16])

    # Check to make sure the vectors were removed
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 84, "Got wrong number of vectors back"
    assert dict(results.rows[0]) == {"id": 7, "vector": [0.7, 0.7], "hello": "world"}
    for i in range(17, 100):
        assert dict(results.rows[i - 16]) == {"id": i, "vector": [i / 10, i / 10], "test": "rows"}


@pytest.mark.xdist_group(name="group1")
def test_upsert_columns(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test")

    ids = [0, 1, 2, 3]
    vectors = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]]
    attributes = {
        "key1": ["zero", "one", "two", "three"],
        "key2": [" ", "a", "b", "c"],
        "test": ["cols", "cols", "cols", "cols"],
    }

    # Test upsert columns with named args
    ns.write(upsert_columns={"id": ids, "vector": vectors, **attributes})

    # Test upsert dict columns
    ns.write(
        upsert_columns={
            "id": [0, 1, 2, 3],
            "vector": [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
            "key1": ["zero", "one", "two", "three"],
            "key2": [" ", "a", "b", "c"],
            "test": ["cols", "cols", "cols", "cols"],
        }
    )

    # Test upsert typed columns
    ns.write(
        upsert_columns={
            "id": [4, 5, 6],
            "vector": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
            "key1": ["one", "two", "three"],
            "key2": ["a", "b", "c"],
            "test": ["cols", "cols", "cols"],
        }
    )

    ns.write(upsert_rows=[{"id": i, "vector": [i / 10, i / 10], "test": "cols"} for i in range(10, 100)])

    # Check to make sure the vectors were stored as expected
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 98, "Got wrong number of vectors back"
    test_count = 0
    for row in results.rows:
        if hasattr(row, "test") and row.test == "cols":
            test_count += 1
            assert isinstance(row.id, int)
            if row.id >= 10:
                assert dict(row) == {"id": row.id, "vector": [row.id / 10, row.id / 10], "test": "cols"}
        else:
            assert dict(row) == {"id": 7, "vector": [0.7, 0.7], "hello": "world"}
    assert test_count == 97, "Found wrong number of test cols"


@pytest.mark.xdist_group(name="group1")
def test_query_vectors(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test")

    def check_result(row: Row, expected: Row):
        assert len(row) == len(expected)
        assert row.id == expected.id
        if isinstance(expected.vector, list):
            assert isinstance(row.vector, list)
            assert abs(row.vector[0] - expected.vector[0]) < 0.000001
            assert abs(row.vector[1] - expected.vector[1]) < 0.000001
        else:
            assert row.vector == expected.vector
        if "$dist" in expected:
            assert abs(row["$dist"] - expected["$dist"]) < 0.000001
        else:
            assert "$dist" not in row

    def check_results(vector_set: NamespaceQueryResponse, expected: List[Row]):
        assert vector_set.rows is not None
        assert len(vector_set.rows) == len(expected)
        for i in range(len(vector_set.rows)):
            check_result(vector_set.rows[i], expected[i])

    expected = [
        Row.from_dict({"id": 7, "vector": [0.7, 0.7], "hello": "world", "$dist": 0.01}),
        Row.from_dict({"id": 10, "vector": [1.0, 1.0], "$dist": 0.13}),
        Row.from_dict({"id": 11, "vector": [1.1, 1.1], "$dist": 0.25}),
        Row.from_dict({"id": 3, "vector": [0.3, 0.3], "$dist": 0.41}),
        Row.from_dict({"id": 6, "vector": [0.3, 0.3], "$dist": 0.41}),
    ]

    # Test normal query
    vector_set = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.8, 0.7]),
        include_attributes=["hello", "vector"],
    )
    check_results(vector_set, expected)
    assert vector_set.billing == QueryBilling(
        billable_logical_bytes_queried=256000000,
        billable_logical_bytes_returned=105,
    )

    # Test query with dict
    vector_set = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.8, 0.7]),
        include_attributes=["hello", "vector"],
    )
    check_results(vector_set, expected)

    # Test query with all attributes
    vector_set = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.8, 0.7]),
        include_attributes=True,
    )
    expected = [
        Row.from_dict({"id": 7, "vector": [0.7, 0.7], "$dist": 0.01, "hello": "world"}),
        Row.from_dict({"id": 10, "vector": [1.0, 1.0], "$dist": 0.13, "test": "cols"}),
        Row.from_dict({"id": 11, "vector": [1.1, 1.1], "$dist": 0.25, "test": "cols"}),
        Row.from_dict({"id": 3, "vector": [0.3, 0.3], "$dist": 0.41, "test": "cols", "key1": "three", "key2": "c"}),
        Row.from_dict({"id": 6, "vector": [0.3, 0.3], "$dist": 0.41, "test": "cols", "key1": "three", "key2": "c"}),
    ]
    check_results(vector_set, expected)

    # Test query with typed query
    vector_set = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [1.5, 1.6]),
    )
    expected = [
        Row.from_dict({"id": 15, "$dist": 0.01}),
        Row.from_dict({"id": 16, "$dist": 0.01}),
        Row.from_dict({"id": 14, "$dist": 0.05}),
        Row.from_dict({"id": 17, "$dist": 0.05}),
        Row.from_dict({"id": 18, "$dist": 0.13}),
    ]
    check_results(vector_set, expected)

    # Test query with single filter
    expected = [
        Row.from_dict({"id": 10}),
        Row.from_dict({"id": 11}),
        Row.from_dict({"id": 12}),
    ]
    vector_set = ns.query(
        rank_by=("id", "asc"),
        top_k=3,
        include_attributes=["hello"],
        filters=("id", "In", (10, 11, 12)),
    )
    check_results(vector_set, expected)

    # Test query with no vectors
    expected = [
        Row.from_dict({"id": 10}),
        Row.from_dict({"id": 11}),
        Row.from_dict({"id": 12}),
    ]
    vector_set = ns.query(
        rank_by=("id", "asc"),
        top_k=3,
        include_attributes=["hello"],
        filters=("id", "In", (10, 11, 12)),
    )
    check_results(vector_set, expected)

    # Test query with 'eventual' consistency
    vector_set = ns.query(
        rank_by=("id", "asc"),
        top_k=3,
        consistency=namespace_query_params.Consistency(level="eventual"),
    )
    assert vector_set.rows is not None
    assert len(vector_set.rows) == 3

    # Test query with no consistency dict key should fail
    try:
        ns.query(
            rank_by=("id", "asc"),
            top_k=3,
            consistency="eventual",  # type: ignore
        )
        raise AssertionError("Using consistency without a dict that has a 'level' key should not be allowed")
    except turbopuffer.UnprocessableEntityError as err:
        assert 'invalid type: string "eventual", expected struct Consistency' in err.message

    # Test query with 'nonexistentvalue' consistency should fail
    try:
        ns.query(
            rank_by=("id", "asc"),
            top_k=3,
            consistency=namespace_query_params.Consistency(level="nonexistentvalue"),  # type: ignore
        )
        raise AssertionError("Using consistency level other than 'strong' or 'eventual' should not be allowed")
    except turbopuffer.UnprocessableEntityError as err:
        assert "unknown variant `nonexistentvalue`, expected `strong` or `eventual`" in err.message


@pytest.mark.xdist_group(name="group1")
def test_delete_all(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test")

    assert ns.exists() is True

    ns.delete_all()

    with pytest.raises(turbopuffer.NotFoundError):
        ns.schema()


def test_string_ids(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "string_ids")

    vec_ids = [str(uuid.uuid1()) for _ in range(0, 8)]
    key1 = ["zero", "one", "two", "three"]
    key2 = [" ", "a", "b", "c"]

    # Test upsert columns
    ns.write(
        upsert_columns={
            "id": vec_ids[0:4],
            "vector": [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
            "key1": key1,
            "key2": key2,
            "test": ["cols", "cols", "cols", "cols"],
        },
        distance_metric="euclidean_squared",
    )

    # Test upsert rows
    ns.write(
        upsert_rows=[
            {"id": id, "vector": [(i + 4) / 10, (i + 4) / 10], "test": "rows", "hello": "world"}
            for i, id in enumerate(vec_ids[4:])
        ],
        distance_metric="euclidean_squared",
    )

    # Check to make sure the vectors were stored as expected
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 8, "Got wrong number of vectors back"
    for i, row in enumerate(results.rows):
        if row.test == "cols":
            assert dict(row) == {
                "id": vec_ids[i],
                "vector": [i / 10, i / 10],
                "key1": key1[i],
                "key2": key2[i],
                "test": "cols",
            }
        else:
            assert dict(row) == {"id": vec_ids[i], "vector": [i / 10, i / 10], "hello": "world", "test": "rows"}

    # Test query
    result = ns.query(top_k=5, rank_by=("vector", "ANN", [0.0, 0.0]), filters=("id", "In", vec_ids))
    expected = [
        Row.from_dict({"id": vec_ids[0], "vector": None, "$dist": 0.0}),
        Row.from_dict({"id": vec_ids[1], "vector": None, "$dist": 0.02}),
        Row.from_dict({"id": vec_ids[2], "vector": None, "$dist": 0.08}),
        Row.from_dict({"id": vec_ids[3], "vector": None, "$dist": 0.18}),
        Row.from_dict({"id": vec_ids[4], "vector": None, "$dist": 0.32}),
    ]
    assert result.rows is not None
    assert len(result.rows) == len(expected)
    for i, row in enumerate(result.rows):
        assert len(dict(row)) == 3
        assert row["id"] == expected[i]["id"]
        assert row["vector"] == expected[i]["vector"]
        assert abs(row["$dist"] - expected[i]["$dist"]) < 0.000001

    # Test delete by string id
    ns.write(deletes=[vec_ids[2]])

    # Test query 2
    result = ns.query(top_k=5, rank_by=("vector", "ANN", [0.0, 0.0]), filters=("id", "In", vec_ids))
    expected = [
        Row.from_dict({"id": vec_ids[0], "vector": None, "$dist": 0.0}),
        Row.from_dict({"id": vec_ids[1], "vector": None, "$dist": 0.02}),
        Row.from_dict({"id": vec_ids[3], "vector": None, "$dist": 0.18}),
        Row.from_dict({"id": vec_ids[4], "vector": None, "$dist": 0.32}),
        Row.from_dict({"id": vec_ids[5], "vector": None, "$dist": 0.5}),
    ]
    assert result.rows is not None
    assert len(result.rows) == len(expected)
    for i, row in enumerate(result.rows):
        assert len(row) == 3
        assert row["id"] == expected[i]["id"]
        assert row["vector"] == expected[i]["vector"]
        assert abs(row["$dist"] - expected[i]["$dist"]) < 0.000001

    ns.delete_all()


def test_attribute_types(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test_types")

    # Test upsert multiple dict rows
    ns.write(
        upsert_rows=[
            {
                "id": 7,
                "vector": [0.7, 0.7],
                "count": 1,
                "users": ["jan", "simon"],
            },
            {
                "id": 9,
                "vector": [0.7, 0.7],
                "count": 2,
                "users": ["bojan", "morgan", "simon"],
            },
        ],
        distance_metric="euclidean_squared",
    )

    result = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.0, 0.0]),
        filters=(
            "And",
            [
                ("count", "Gt", 1),
                ("users", "In", ["simon"]),
            ],
        ),
    )
    assert result.rows is not None
    assert len(result.rows) == 1

    result = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.0, 0.0]),
        filters=(
            "Or",
            [
                ("count", "Eq", 1),
                ("users", "In", "bojan"),
            ],
        ),
    )
    assert result.rows is not None
    assert len(result.rows) == 2

    result = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.0, 0.0]),
        filters=(
            "And",
            [
                ("count", "Eq", 1),
                ("users", "In", "bojan"),
            ],
        ),
    )
    assert result.rows is not None
    assert len(result.rows) == 0

    result = ns.query(
        top_k=5,
        rank_by=("vector", "ANN", [0.0, 0.0]),
        filters=(
            "And",
            [
                ("count", "Eq", 1),
                (
                    "Or",
                    [
                        ("users", "In", "bojan"),
                        ("count", "Gt", 0),
                    ],
                ),
            ],
        ),
    )
    assert result.rows is not None
    assert len(result.rows) == 1


def test_not_found_error(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "not_found")

    with pytest.raises(turbopuffer.NotFoundError):
        ns.query(
            top_k=5,
            rank_by=("vector", "ANN", [0.0, 0.0]),
        )


def test_list_in_empty_namespace(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "client_test")
    assert str(ns) == f"tpuf-namespace:{test_prefix}client_test"

    # Test upsert multiple dict rows
    ns.write(
        upsert_rows=[
            {"id": 2, "vector": [2, 2]},
            {"id": 7, "vector": [1, 1]},
        ],
        distance_metric="euclidean_squared",
    )

    ns.write(deletes=[2, 7])

    result = ns.query(top_k=100, rank_by=("id", "asc"))
    assert result.rows is not None
    assert len(result.rows) == 0


def test_delete_by_filter(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "delete_by_filter")

    ns.write(
        upsert_rows=[
            {"id": 5, "vector": [0.7, 0.7], "a": 0},
            {"id": 6, "vector": [0.7, 0.7], "a": 1},
            {"id": 7, "vector": [0.7, 0.7], "a": 2},
            {"id": 8, "vector": [0.7, 0.7], "a": 1},
            {"id": 9, "vector": [0.7, 0.7], "a": 3},
        ],
        distance_metric="euclidean_squared",
    )

    result = ns.write(
        delete_by_filter=("a", "Eq", 42)  # no-op, nothing matches
    )
    assert result.rows_affected == 0

    result = ns.query(top_k=100, rank_by=("id", "asc"))
    assert result.rows is not None
    assert len(result.rows) == 5, "Got wrong number of vectors back"

    result = ns.write(delete_by_filter=("a", "Eq", 1))
    assert result.rows_affected == 2

    result = ns.query(top_k=100, rank_by=("id", "asc"))
    assert result.rows is not None
    assert len(result.rows) == 3, "Got wrong number of vectors back"
    assert result.rows[0].id == 5
    assert result.rows[1].id == 7
    assert result.rows[2].id == 9

    result = ns.write(delete_by_filter=("a", "Gt", 0))
    assert result.rows_affected == 2

    result = ns.query(top_k=100, rank_by=("id", "asc"))
    assert result.rows is not None
    assert len(result.rows) == 1, "Got wrong number of vectors back"
    assert result.rows[0].id == 5

    ns.delete_all()


def test_transparent_vector_encoding():
    # Ensure that our hacked in vector encoding fast path is actually firing.
    # Due to the nature of the hack, there's a high risk of a future refactoring
    # to the Stainless specification breaking the fast path.

    transformed = transform({"id": 1, "vector": [0.1, 0.2, 0.3]}, RowParam)
    assert transformed == {"id": 1, "vector": "zczMPc3MTD6amZk+"}

    transformed = transform({"id": [1, 2], "vector": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]}, ColumnsParam)
    assert transformed == {"id": [1, 2], "vector": ["zczMPc3MTD6amZk+", "zczMPgAAAD+amRk/"]}


@pytest.mark.asyncio
async def test_transparent_vector_encoding_async():
    # Ensure that our hacked in vector encoding fast path is actually firing.
    # Due to the nature of the hack, there's a high risk of a future refactoring
    # to the Stainless specification breaking the fast path.

    transformed = await async_transform({"id": 1, "vector": [0.1, 0.2, 0.3]}, RowParam)
    assert transformed == {"id": 1, "vector": "zczMPc3MTD6amZk+"}

    transformed = await async_transform({"id": [1, 2], "vector": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]}, ColumnsParam)
    assert transformed == {"id": [1, 2], "vector": ["zczMPc3MTD6amZk+", "zczMPgAAAD+amRk/"]}


def test_upsert_base64_vectors(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "base64_test")
    assert str(ns) == f"tpuf-namespace:{test_prefix}base64_test"

    # Test upsert multiple typed rows
    ns.write(
        upsert_rows=[
            {
                "id": 2,
                "vector": b64encode_vector([2, 2]),
            },
            {
                "id": 3,
                "vector": b64encode_vector([0.7, 0.7]),
                "hello": "world",
            },
        ],
        distance_metric="euclidean_squared",
    )

    # Test upsert columns
    ids = [4, 5]
    vectors = [b64encode_vector([0.1, 0.1]), b64encode_vector([0.2, 0.2])]
    attributes = {
        "key1": ["zero", "one"],
        "key2": [" ", "a"],
    }
    ns.write(
        upsert_columns={
            "id": ids,
            "vector": vectors,
            **attributes,
        }
    )

    # Test upsert lazy row iterator
    ns.write(
        upsert_rows=[
            {
                "id": i,
                "vector": b64encode_vector([i / 10, i / 10]),
                "test": "rows",
            }
            for i in range(10, 100)
        ]
    )

    # Check to make sure the vectors were stored as expected
    results = ns.query(top_k=100, rank_by=("id", "asc"), include_attributes=True)
    assert results.rows is not None
    assert len(results.rows) == 94, "Got wrong number of vectors back"
    assert dict(results.rows[0]) == {"id": 2, "vector": [2.0, 2.0]}
    assert dict(results.rows[1]) == {"id": 3, "vector": [0.7, 0.7], "hello": "world"}
    assert dict(results.rows[2]) == {"id": 4, "vector": [0.1, 0.1], "key1": "zero", "key2": " "}
    assert dict(results.rows[3]) == {"id": 5, "vector": [0.2, 0.2], "key1": "one", "key2": "a"}
    for i in range(10, 100):
        assert dict(results.rows[i - 6]) == {"id": i, "vector": [i / 10, i / 10], "test": "rows"}

    ns.delete_all()


def test_query_vectors_vector_encoding_format(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "vector_encoding_format")
    assert str(ns) == f"tpuf-namespace:{test_prefix}vector_encoding_format"

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": b64encode_vector([0.1, 0.2, 0.3]),
            },
        ],
        distance_metric="euclidean_squared",
    )

    vector_encodings: List[Union[Omit, VectorEncoding]] = [omit, "float", "base64"]
    for vector_encoding in vector_encodings:
        vector_set = ns.query(
            top_k=1,
            rank_by=("vector", "ANN", [0.0, 0.0, 0.0]),
            include_attributes=True,
            vector_encoding=vector_encoding,
        )
        assert vector_set.rows is not None
        assert len(vector_set.rows) == 1
        assert vector_set.rows[0].id == 1

        # Compare using float32 to avoid precision issues if the vectors had
        # been passed through 32-bit floats.
        def float32_list(vector: Union[None, Vector]):
            assert vector is not None
            if isinstance(vector, str):
                floats = b64decode_vector(vector)
            else:
                floats = vector
            return [numpy.float32(x) for x in floats]

        assert float32_list(vector_set.rows[0].vector) == float32_list([0.1, 0.2, 0.3])


def test_exists(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "exists-test")
    assert ns.exists() is False

    ns.write(
        upsert_rows=[
            {"id": 1, "vector": [0.1, 0.2, 0.3]},
        ],
        distance_metric="euclidean_squared",
    )
    assert ns.exists() is True
