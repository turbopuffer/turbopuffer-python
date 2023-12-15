import turbopuffer as tpuf

def test_upsert_rows():
    ns = tpuf.Namespace('hello_world')
    print(ns)

    # Test upsert mutli row data
    ns.upsert([
        {'id': 2, 'vector': [2, 2]},
        {'id': 7, 'vector': [0.7, 0.7], 'attributes': {'hello': 'world'}},
    ])

    # Test upsert typed row data
    ns.upsert([
        tpuf.VectorRow(id=2, vector=[2, 2]),
        tpuf.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'}),
    ])

    # Test upsert lazy row iterator
    ns.upsert(tpuf.VectorRow(id=i, vector=[i/10, i/10]) for i in range(10, 100))

def test_upsert_columns():
    ns = tpuf.Namespace('hello_world')

    # Test upsert dict data
    ns.upsert({
        "ids": [0, 1, 2, 3],
        "vectors": [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        "attributes": {"key1": ["zero", "one", "two", "three"], "key2": [" ", "a", "b", "c"]}
    })

    # Test upsert typed column data
    ns.upsert(tpuf.VectorColumns(
        ids=[4, 5, 6],
        vectors=[[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        attributes={"key1": ["one", "two", "three"], "key2": ["a", "b", "c"]},
    ))

    # Test upsert lazy column batch iterator
    def make_test_batch(n, offset):
        return tpuf.VectorColumns.from_rows([
            {'id': i, 'vector': [i/10, i/10]} for i in range(offset, n+offset)
        ])
    ns.upsert(make_test_batch(100, i) for i in range(1, 10))

def test_delete_vectors():
    ns = tpuf.Namespace('hello_world')

    # Test upsert delete single row
    try:
        ns.upsert(tpuf.VectorRow(id=2))
    except ValueError as err:
        assert err.args == ('VectorRow.vector cannot be None, use Namespace.delete([ids...]) instead.',)

    # Test upsert single row dict
    try:
        ns.upsert({'id': 6})
    except ValueError as err:
        assert err.args == ('VectorRow.vector cannot be None, use Namespace.delete([ids...]) instead.',)

    # Test delete single row
    ns.delete(6)
    # Test delete multi row
    ns.delete([0, 1, 2, 3, 4, 5])

def test_query_vectors():
    ns = tpuf.Namespace('hello_world')

    # Test query with dict
    vector_set = ns.query({
        'top_k': 5,
        'vector': [0.8, 0.7],
        'distance_metric': 'euclidean_squared',
        'include_vectors': True,
        'include_attributes': ['hello'],
    })
    for i, vector in enumerate(vector_set):
        print(f'Query {i}: ', vector)

    # Test query with typed query
    vector_set = ns.query(tpuf.VectorQuery(
        top_k=5,
        vector=[0.8, 0.7],
        distance_metric='euclidean_squared',
        include_vectors=True,
        include_attributes=['hello'],
    ))
    print(vector_set)
    # for i, vector in enumerate(vector_set):
    #     print(f'Query {i}: ', vector)

def test_list_vectors():
    ns = tpuf.Namespace('hello_world')

    vector_set = ns.vectors()
    print(vector_set)

    for i in range(0, 10):
        print(f'Export {i}: ', vector_set[i])

    print(len(vector_set))

def test_delete_all():
    ns = tpuf.Namespace('hello_world')
    # print('Recall:', ns.recall())

    ns.delete_all_indexes()
    ns.delete_all()
