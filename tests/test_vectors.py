import uuid
import turbopuffer as tpuf
from turbopuffer.vectors import b64encode_vector
import tests
import pytest
from datetime import datetime
from typing import List
import numpy as np


@pytest.mark.xdist_group(name="group1")
def test_upsert_rows():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')
    assert str(ns) == f'tpuf-namespace:{tests.test_prefix}client_test'

    # Test upsert multiple dict rows
    ns.write(
        upsert_rows=[
            {'id': 2, 'vector': [2, 2]},
            {'id': 7, 'vector': [0.7, 0.7], 'hello': 'world', 'test': 'rows'},
        ],
        distance_metric='euclidean_squared'
    )

    # Test upsert multiple typed rows
    ns.write(
        upsert_rows=[
            tpuf.VectorRow(id=2, vector=[2, 2]),
            tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'}),
        ],
        distance_metric='euclidean_squared'
    )

    # Test upsert lazy row iterator
    ns.write(
        upsert_rows=[tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'}) for i in range(10, 100)]
    )

    # Test upsert single rows should fail
    try:
        ns.write(
            upsert_rows=tpuf.VectorRow(id=2, vector=[2, 2])
        )
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert_rows must be a list',)
    try:
        ns.write(
            upsert_rows=tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world', 'test': 'rows'})
        )
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert_rows must be a list',)
    try:
        ns.write(
            upsert_rows={'id': 2, 'vector': [2, 2]}
        )
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert_rows must be a list',)

    # Check to make sure the vectors were stored as expected
    results = ns.vectors()
    assert len(results) == 92, "Got wrong number of vectors back"
    assert results[0] == tpuf.VectorRow(id=2, vector=[2.0, 2.0], attributes={})
    assert results[1] == tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'})
    for i in range(10, 100):
        assert results[i-8] == tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'})

    # Check to ensure recall is working
    ns.recall()

@pytest.mark.xdist_group(name="group1")
def test_delete_vectors():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    # Test delete
    ns.write(
        deletes=[2]
    )
    results = ns.vectors()
    assert len(results) == 91, "Got wrong number of vectors back"
    assert results[0] == tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'})

    ns.write(
        deletes=[10]
    )
    results = ns.vectors()
    assert len(results) == 90, "Got wrong number of vectors back"
    assert results[1] == tpuf.VectorRow(id=11, vector=[1.1, 1.1], attributes={'test': 'rows'})

    ns.write(
        deletes=[11]
    )
    results = ns.vectors()
    assert len(results) == 89, "Got wrong number of vectors back"
    assert results[1] == tpuf.VectorRow(id=12, vector=[1.2, 1.2], attributes={'test': 'rows'})

    ns.write(
        deletes=[12]
    )
    results = ns.vectors()
    assert len(results) == 88, "Got wrong number of vectors back"
    assert results[1] == tpuf.VectorRow(id=13, vector=[1.3, 1.3], attributes={'test': 'rows'})

    # Test delete single row
    ns.write(
        deletes=[13]
    )
    # Test delete multi row
    ns.write(
        deletes=[14, 15, 16]
    )

    # Check to make sure the vectors were removed
    results = ns.vectors()
    assert len(results) == 84, "Got wrong number of vectors back"
    assert results[0] == tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'})
    for i in range(17, 100):
        assert results[i-16] == tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'})

@pytest.mark.xdist_group(name="group1")
def test_upsert_columns():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    ids = [0, 1, 2, 3]
    vectors = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]]
    attributes = {
        "key1": ["zero", "one", "two", "three"],
        "key2": [" ", "a", "b", "c"],
        "test": ["cols", "cols", "cols", "cols"],
    }

    # Test upsert columns with named args
    ns.write(
        upsert_columns={
            'id': ids,
            'vector': vectors,
            **attributes
        }
    )

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
        upsert_columns=tpuf.VectorColumns(
            ids=[4, 5, 6],
            vectors=[[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
            attributes={
                "key1": ["one", "two", "three"],
                "key2": ["a", "b", "c"],
                "test": ["cols", "cols", "cols"],
            },
        )
    )

    ns.write(
        upsert_rows=[
            {'id': i, 'vector': [i/10, i/10], 'test': 'cols'} for i in range(10, 100)
        ]
    )

    # Check to make sure the vectors were stored as expected
    results = ns.vectors()
    assert len(results) == 98, "Got wrong number of vectors back"
    test_count = 0
    for row in results:
        if 'test' in row.attributes and row.attributes['test'] == 'cols':
            test_count += 1
            if row.id >= 10:
                assert row == tpuf.VectorRow(id=row.id, vector=[row.id/10, row.id/10], attributes={'test': 'cols'})
        else:
            assert row == tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'})
    assert test_count == 97, "Found wrong number of test cols"

@pytest.mark.xdist_group(name="group1")
def test_query_vectors():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    def check_result(row, expected):
        assert row.id == expected.id
        assert row.attributes == expected.attributes
        if isinstance(expected.vector, list):
            assert isinstance(row.vector, list)
            assert abs(row.vector[0] - expected.vector[0]) < 0.000001
            assert abs(row.vector[1] - expected.vector[1]) < 0.000001
        else:
            assert row.vector == expected.vector
        if isinstance(expected.dist, float):
            assert abs(row.dist - expected.dist) < 0.000001
        else:
            assert row.dist == expected.dist

    expected = [
        tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'}, dist=0.01),
        tpuf.VectorRow(id=10, vector=[1.0, 1.0], dist=0.13),
        tpuf.VectorRow(id=11, vector=[1.1, 1.1], dist=0.25),
        tpuf.VectorRow(id=3, vector=[0.3, 0.3], dist=0.41),
        tpuf.VectorRow(id=6, vector=[0.3, 0.3], dist=0.41),
    ]

    # Test normal query
    vector_set = ns.query(
        top_k=5,
        vector=[0.8, 0.7],
        distance_metric='euclidean_squared',
        include_vectors=True,
        include_attributes=['hello'],
    )
    for i in range(len(vector_set)):  # Use VectorResult in index mode
        check_result(vector_set[i], expected[i])

    # Test query with dict
    vector_set = ns.query({
        'top_k': 5,
        'vector': [0.8, 0.7],
        'distance_metric': 'euclidean_squared',
        'include_vectors': True,
        'include_attributes': ['hello'],
    })
    for i in range(len(vector_set)):  # Use VectorResult in index mode
        check_result(vector_set[i], expected[i])

    # Test query with all attributes
    vector_set = ns.query(
        top_k=5,
        vector=[0.8, 0.7],
        distance_metric='euclidean_squared',
        include_vectors=True,
        include_attributes=True
    )
    expected = [
        tpuf.VectorRow(id=7, vector=[0.7, 0.7], dist=0.01, attributes={'hello': 'world'}),
        tpuf.VectorRow(id=10, vector=[1.0, 1.0], dist=0.13, attributes={'test': 'cols'}),
        tpuf.VectorRow(id=11, vector=[1.1, 1.1], dist=0.25, attributes={'test': 'cols'}),
        tpuf.VectorRow(id=3, vector=[0.3, 0.3], dist=0.41, attributes={'test': 'cols', 'key1': 'three', 'key2': 'c'}),
        tpuf.VectorRow(id=6, vector=[0.3, 0.3], dist=0.41, attributes={'test': 'cols', 'key1': 'three', 'key2': 'c'}),
    ]
    for i in range(len(vector_set)):  # Use VectorResult in index mode
        check_result(vector_set[i], expected[i])

    # Test query with typed query
    vector_set = ns.query(tpuf.VectorQuery(
        top_k=5,
        vector=[1.5, 1.6],
        distance_metric='euclidean_squared',
    ))
    expected = [
        tpuf.VectorRow(id=15, dist=0.01),
        tpuf.VectorRow(id=16, dist=0.01),
        tpuf.VectorRow(id=14, dist=0.05),
        tpuf.VectorRow(id=17, dist=0.05),
        tpuf.VectorRow(id=18, dist=0.13),
    ]
    i = 0
    for row in vector_set:  # Use VectorResult in iterator mode
        check_result(row, expected[i])
        i += 1

    # Test query with single filter
    expected = [
        tpuf.VectorRow(id=10),
        tpuf.VectorRow(id=11),
        tpuf.VectorRow(id=12),
    ]
    vector_set = ns.query(
        top_k=3,
        include_vectors=False,
        filters={
            'id': ['In', [10, 11, 12]]
        },
    )
    for i in range(len(vector_set)):  # Use VectorResult in index mode
        check_result(vector_set[i], expected[i])

    # Test query with no vectors
    expected = [
        tpuf.VectorRow(id=10),
        tpuf.VectorRow(id=11),
        tpuf.VectorRow(id=12),
    ]
    vector_set = ns.query(
        top_k=3,
        include_vectors=False,
        filters={
            'id': [['In', [10, 11, 12]]]
        },
    )
    for i in range(len(vector_set)):  # Use VectorResult in index mode
        check_result(vector_set[i], expected[i])

    # Test query with 'eventual' consistency
    vector_set = ns.query(
        top_k=3,
        consistency={'level': 'eventual'}
    )
    assert len(vector_set) == 3

    # Test query with no consistency dict key should fail
    try:
        ns.query(
            top_k=3,
            consistency='eventual'
        )
        assert False, "Using consistency without a dict that has a 'level' key should not be allowed"
    except ValueError as err:
        assert err.args == ("VectorQuery.consistency must be a dict with a 'level' key",)

    # Test query with 'nonexistentvalue' consistency should fail
    try:
        ns.query(
            top_k=3,
            consistency={'level': 'nonexistentvalue'}
        )
        assert False, "Using consistency level other than 'strong' or 'eventual' should not be allowed"
    except ValueError as err:
        assert err.args == ("VectorQuery.consistency level must be 'strong' or 'eventual', got:", 'nonexistentvalue')


@pytest.mark.xdist_group(name="group1")
def test_list_vectors():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    assert ns.exists()

    vector_set = ns.vectors()

    assert len(vector_set) == 98
    assert any(row.id == 7 for row in vector_set)
    assert any(row.vector == [0.7, 0.7] for row in vector_set)

@pytest.mark.xdist_group(name="group1")
def test_read_metadata():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    assert ns.exists()
    assert ns.dimensions() == 2
    assert ns.approx_count() == 98
    assert type(ns.created_at()) == type(datetime.now())

@pytest.mark.xdist_group(name="group1")
def test_delete_all():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    assert ns.exists()

    ns.delete_all_indexes()
    ns.delete_all()

    assert not ns.exists()
    assert ns.dimensions() == 0
    assert ns.approx_count() == 0

def test_string_ids():
    ns = tpuf.Namespace(tests.test_prefix + 'string_ids')

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
        }
    )

    # Test upsert rows
    ns.write(
        upsert_rows=[
            tpuf.VectorRow(
                id=id,
                vector=[i/10, i/10],
                attributes={
                    'test': 'rows',
                    'hello': 'world'
                }
            ) for i, id in enumerate(vec_ids)][4:],
        distance_metric='euclidean_squared',
    )

    # Check to make sure the vectors were stored as expected
    results = ns.vectors()
    assert len(results) == 8, "Got wrong number of vectors back"
    for i, row in enumerate(results):
        if 'test' in row.attributes and row.attributes['test'] == 'cols':
            assert row == tpuf.VectorRow(
                id=vec_ids[i],
                vector=[i/10, i/10],
                attributes={
                    "key1": key1[i],
                    "key2": key2[i],
                    'test': 'cols'
                })
        else:
            assert row == tpuf.VectorRow(
                id=vec_ids[i],
                vector=[i/10, i/10],
                attributes={
                    'hello': 'world',
                    'test': 'rows'
                })

    # Test query
    results = ns.query(
        top_k=5,
        vector=[0.0, 0.0],
        distance_metric='euclidean_squared',
        filters={'id': ['In', vec_ids]}
    )
    expected = [
        tpuf.VectorRow(id=vec_ids[0], dist=0.0),
        tpuf.VectorRow(id=vec_ids[1], dist=0.02),
        tpuf.VectorRow(id=vec_ids[2], dist=0.08),
        tpuf.VectorRow(id=vec_ids[3], dist=0.18),
        tpuf.VectorRow(id=vec_ids[4], dist=0.32)
    ]
    for i, row in enumerate(results):
        assert row.id == expected[i].id
        assert row.attributes == expected[i].attributes
        assert row.vector == expected[i].vector
        assert abs(row.dist - expected[i].dist) < 0.000001

    # Test delete by string id
    ns.write(
        deletes=[vec_ids[2]]
    )

    # Test query 2
    results = ns.query(
        top_k=5,
        vector=[0.0, 0.0],
        distance_metric='euclidean_squared',
        filters={'id': ['In', vec_ids]}
    )
    expected = [
        tpuf.VectorRow(id=vec_ids[0], dist=0.0),
        tpuf.VectorRow(id=vec_ids[1], dist=0.02),
        tpuf.VectorRow(id=vec_ids[3], dist=0.18),
        tpuf.VectorRow(id=vec_ids[4], dist=0.32),
        tpuf.VectorRow(id=vec_ids[5], dist=0.5)
    ]
    for i, row in enumerate(results):
        assert row.id == expected[i].id
        assert row.attributes == expected[i].attributes
        assert row.vector == expected[i].vector
        assert abs(row.dist - expected[i].dist) < 0.000001

    ns.delete_all()


def test_attribute_types():
    ns = tpuf.Namespace(tests.test_prefix + "client_test_types")

    # Test upsert multiple dict rows
    ns.write(
        upsert_rows=[
            {
                "id": 7,
                "vector": [0.7, 0.7],
                "count": 1, "users": ["jan", "simon"],
            },
            {
                "id": 9,
                "vector": [0.7, 0.7],
                "count": 2, "users": ["bojan", "morgan", "simon"],
            },
        ],
        distance_metric='euclidean_squared',
    )

    results = ns.query(
        top_k=5,
        vector=[0.0, 0.0],
        distance_metric="euclidean_squared",
        filters={"count": [["Gt", 1]], "users": [["In", "simon"]]},
    )
    assert len(results) == 1

    results = ns.query(
        top_k=5,
        vector=[0.0, 0.0],
        distance_metric="euclidean_squared",
        filters=["Or", [
            ["count", "Eq", 1],
            ["users", "Contains", "bojan"],
        ]],
    )
    assert len(results) == 2

    results = ns.query(
        top_k=5,
        vector=[0.0, 0.0],
        distance_metric="euclidean_squared",
        filters=["And", [
            ["count", "Eq", 1],
            ["users", "Contains", "bojan"],
        ]],
    )
    assert len(results) == 0

    results = ns.query(
        top_k=5,
        vector=[0.0, 0.0],
        distance_metric="euclidean_squared",
        filters=["And", [
            ["count", "Eq", 1],
            ["Or", [
                ["users", "Contains", "bojan"],
                ["count", "Gt", 0],
            ]],
        ]],
    )
    assert len(results) == 1

def test_not_found_error():
    ns = tpuf.Namespace(tests.test_prefix + 'not_found')

    with pytest.raises(tpuf.NotFoundError):
        ns.query(
            top_k=5,
            vector=[0.0, 0.0],
        )

def test_list_in_empty_namespace():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')
    assert str(ns) == f'tpuf-namespace:{tests.test_prefix}client_test'

    # Test upsert multiple dict rows
    ns.write(
        upsert_rows=[
            {'id': 2, 'vector': [2, 2]},
            {'id': 7, 'vector': [1, 1]},
        ],
        distance_metric='euclidean_squared',
    )

    ns.write(
        deletes=[2, 7]
    )

    assert list(ns.vectors()) == []


def test_delete_by_filter():
    ns = tpuf.Namespace(tests.test_prefix + 'delete_by_filter')

    ns.write(
        upsert_rows=[
            {'id': 5, 'vector': [0.7, 0.7], 'a': 0},
            {'id': 6, 'vector': [0.7, 0.7], 'a': 1},
            {'id': 7, 'vector': [0.7, 0.7], 'a': 2},
            {'id': 8, 'vector': [0.7, 0.7], 'a': 1},
            {'id': 9, 'vector': [0.7, 0.7], 'a': 3},
        ],
        distance_metric='euclidean_squared',
    )

    rows_affected = ns.write(
        delete_by_filter=['a', 'Eq', 42] # no-op, nothing matches
    )
    assert rows_affected == 0

    results = ns.vectors()
    assert len(results) == 5, "Got wrong number of vectors back"

    rows_affected = ns.write(
        delete_by_filter=['a', 'Eq', 1]
    )
    assert rows_affected == 2

    results = ns.vectors()
    assert len(results) == 3, "Got wrong number of vectors back"
    assert results[0].id == 5
    assert results[1].id == 7
    assert results[2].id == 9

    rows_affected = ns.write(
        delete_by_filter=['a', 'Gt', 0]
    )
    assert rows_affected == 2

    results = ns.vectors()
    assert len(results) == 1, "Got wrong number of vectors back"
    assert results[0].id == 5

    ns.delete_all()

def test_upsert_base64_vectors():
    ns = tpuf.Namespace(tests.test_prefix + 'base64_test')
    assert str(ns) == f'tpuf-namespace:{tests.test_prefix}base64_test'

    # Test upsert multiple typed rows
    ns.write(
        upsert_rows=[
            tpuf.VectorRow(id=2, vector=b64encode_vector([2, 2])),
            tpuf.VectorRow(id=3, vector=b64encode_vector([0.7, 0.7]), attributes={'hello': 'world'}),
        ],
        distance_metric='euclidean_squared',
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
            'id': ids,
            'vector': vectors,
            **attributes,
        }
    )

    # Test upsert lazy row iterator
    ns.write(
        upsert_rows=[
            tpuf.VectorRow(id=i, vector=b64encode_vector([i/10, i/10]), attributes={'test': 'rows'}) for i in range(10, 100)
        ]
    )

    # Check to make sure the vectors were stored as expected
    results = ns.vectors()
    assert len(results) == 94, "Got wrong number of vectors back"
    assert results[0] == tpuf.VectorRow(id=2, vector=[2.0, 2.0], attributes={})
    assert results[1] == tpuf.VectorRow(id=3, vector=[0.7, 0.7], attributes={'hello': 'world'})
    assert results[2] == tpuf.VectorRow(id=4, vector=[0.1, 0.1], attributes={'key1': 'zero', 'key2': ' '})
    assert results[3] == tpuf.VectorRow(id=5, vector=[0.2, 0.2], attributes={'key1': 'one', 'key2': 'a'})
    for i in range(10, 100):
        assert results[i-6] == tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'})

    ns.delete_all()

def test_query_vectors_vector_encoding_format():
    ns = tpuf.Namespace(tests.test_prefix + 'vector_encoding_format')
    assert str(ns) == f'tpuf-namespace:{tests.test_prefix}vector_encoding_format'

    ns.write(
        upsert_rows=[
            tpuf.VectorRow(id=1, vector=b64encode_vector([0.1, 0.2, 0.3])),
        ],
        distance_metric='euclidean_squared',
    )

    for vector_encoding_format in [None, 'float', 'base64']:
        vector_set = ns.query(
            top_k=1,
            vector=[0.0, 0.0, 0.0],
            distance_metric='euclidean_squared',
            include_vectors=True,
            vector_encoding_format=vector_encoding_format,
        )
        assert len(vector_set) == 1
        assert vector_set[0].id == 1

        # Compare using float32 to avoid precision issues if the vectors had
        # been passed through 32-bit floats.
        def float32_list(vector):
            return [np.float32(x) for x in vector]
        assert float32_list(vector_set[0].vector) == float32_list([0.1, 0.2, 0.3])

