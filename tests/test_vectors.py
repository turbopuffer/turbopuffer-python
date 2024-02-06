import time
import uuid
import turbopuffer as tpuf
import tests


def test_upsert_rows():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')
    assert str(ns) == f'tpuf-namespace:{tests.test_prefix}client_test'

    # Test upsert multiple dict rows
    ns.upsert([
        {'id': 2, 'vector': [2, 2]},
        {'id': 7, 'vector': [0.7, 0.7], 'attributes': {'hello': 'world', 'test': 'rows'}},
    ])

    # Test upsert multiple typed rows
    ns.upsert([
        tpuf.VectorRow(id=2, vector=[2, 2]),
        tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'}),
    ])

    # Test upsert lazy row iterator
    ns.upsert(tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'}) for i in range(10, 100))

    # Test upsert single rows should fail
    try:
        ns.upsert(tpuf.VectorRow(id=2, vector=[2, 2]))
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() should be called on a list of vectors, got single vector.',)
    try:
        ns.upsert(tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world', 'test': 'rows'}))
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() should be called on a list of vectors, got single vector.',)
    try:
        ns.upsert({'id': 2, 'vector': [2, 2]})
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() should be called on a list of vectors, got single vector.',)
    try:
        ns.upsert({'id': 7, 'vector': [0.7, 0.7], 'attributes': {'hello': 'world', 'test': 'rows'}})
        assert False, "Upserting single row should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() should be called on a list of vectors, got single vector.',)

    # Check to make sure the vectors were stored as expected
    results = ns.vectors()
    assert len(results) == 92, "Got wrong number of vectors back"
    assert results[0] == tpuf.VectorRow(id=2, vector=[2.0, 2.0], attributes={})
    assert results[1] == tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'})
    for i in range(10, 100):
        assert results[i-8] == tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'})


def test_delete_vectors():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    # Test upsert delete columns
    try:
        ns.upsert(ids=[6], vectors=[None])
        assert False, "Upserting to delete should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.',)

    # Test upsert delete typed row
    try:
        ns.upsert([tpuf.VectorRow(id=2)])
        assert False, "Upserting to delete should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.',)

    try:
        ns.upsert([tpuf.VectorRow(id=2, dist=5)])
        assert False, "Upserting to delete should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.',)

    # Test upsert delete dict row
    try:
        ns.upsert([{'id': 6}])
        assert False, "Upserting to delete should not be allowed"
    except ValueError as err:
        assert err.args == ('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.',)

    # Test delete single row
    ns.delete(2)
    # Test delete multi row
    ns.delete([10, 11, 12, 13, 14, 15])

    # Check to make sure the vectors were removed
    results = ns.vectors()
    assert len(results) == 85, "Got wrong number of vectors back"
    assert results[0] == tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'})
    for i in range(16, 100):
        assert results[i-15] == tpuf.VectorRow(id=i, vector=[i/10, i/10], attributes={'test': 'rows'})


def test_upsert_columns():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    ids = [0, 1, 2, 3]
    vectors = [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]]
    attributes = {
        "key1": ["zero", "one", "two", "three"],
        "key2": [" ", "a", "b", "c"],
        "test": ["cols", "cols", "cols", "cols"],
    }

    # Test upsert columns with positional args
    ns.upsert(ids, vectors, attributes)

    # Test upsert columns with named args
    ns.upsert(
        ids=ids,
        vectors=vectors,
        attributes=attributes
    )

    # Test upsert dict columns
    ns.upsert({
        "ids": [0, 1, 2, 3],
        "vectors": [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        "attributes": {
            "key1": ["zero", "one", "two", "three"],
            "key2": [" ", "a", "b", "c"],
            "test": ["cols", "cols", "cols", "cols"],
        }
    })

    # Test upsert typed columns
    ns.upsert(tpuf.VectorColumns(
        ids=[4, 5, 6],
        vectors=[[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        attributes={
            "key1": ["one", "two", "three"],
            "key2": ["a", "b", "c"],
            "test": ["cols", "cols", "cols"],
        },
    ))

    # Test upsert lazy column batch iterator
    def make_test_batch(n):
        for i in range(1, 10):
            yield tpuf.VectorColumns.from_rows([
                {'id': i, 'vector': [i/10, i/10], 'attributes': {'test': 'cols'}} for i in range(i*n, (i+1)*n)
            ])
    ns.upsert(make_test_batch(10))

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


def test_list_vectors():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    assert ns.exists()

    vector_set = ns.vectors()
    set_str = str(vector_set)
    assert set_str.startswith(f"VectorResult(namespace='{tests.test_prefix}client_test', offset=0, next_cursor='")
    # Random cursor string in the middle
    assert set_str.endswith("', data=VectorColumns(ids=[7], vectors=[[0.7, 0.7]], attributes={'hello': ['world']}))")

    assert len(vector_set) == 98


def test_read_metadata():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')

    assert ns.exists()
    assert ns.dimensions() == 2
    assert ns.approx_count() == 92

    all_ns = tpuf.list_namespaces()
    assert ns in list(all_ns)


def test_delete_all():
    ns = tpuf.Namespace(tests.test_prefix + 'client_test')
    # print('Recall:', ns.recall())

    assert ns.exists()
    all_ns_start = tpuf.list_namespaces()
    assert ns in iter(all_ns_start)

    ns.delete_all_indexes()
    ns.delete_all()

    assert not ns.exists()
    assert ns.dimensions() == 0
    assert ns.approx_count() == 0

    # all_ns_end = tpuf.list_namespaces()
    # assert ns not in iter(all_ns_end)
    # assert len(all_ns_end) < len(all_ns_start)


def test_string_ids():
    ns = tpuf.Namespace(tests.test_prefix + 'string_ids')

    vec_ids = [str(uuid.uuid1()) for _ in range(0, 8)]
    key1 = ["zero", "one", "two", "three"]
    key2 = [" ", "a", "b", "c"]

    # Test upsert columns
    ns.upsert(
        ids=vec_ids[0:4],
        vectors=[[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        attributes={
            "key1": key1,
            "key2": key2,
            "test": ["cols", "cols", "cols", "cols"],
        }
    )

    # Test upsert rows
    ns.upsert([
        tpuf.VectorRow(
            id=id,
            vector=[i/10, i/10],
            attributes={
                'test': 'rows',
                'hello': 'world'
            }
        ) for i, id in enumerate(vec_ids)
    ][4:])

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
    ns.delete(vec_ids[2])

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