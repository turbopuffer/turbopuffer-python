import turbopuffer

def test_vector_endpoints():
    namespace = turbopuffer.Namespace('hello_world')
    print(namespace)

    # Test upsert dict data
    namespace.upsert_vectors({
        "ids": [0, 1, 2, 3],
        "vectors": [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        "attributes": {"key1": ["zero", "one", "two", "three"], "key2": [" ", "a", "b", "c"]}
    })

    # Test upsert typed column data
    namespace.upsert_vectors(turbopuffer.VectorColumns(
        ids=[4, 5, 6],
        vectors=[[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
        attributes={"key1": ["one", "two", "three"], "key2": ["a", "b", "c"]},
    ))

    # Test upsert delete single row
    namespace.upsert_vectors(turbopuffer.VectorRow(id=2))

    # Test upsert single row dict
    namespace.upsert_vectors({'id': 2})

    # Test upsert typed row data
    namespace.upsert_vectors([
        turbopuffer.VectorRow(id=2, vector=[2, 2]),
        turbopuffer.VectorRow(id=7, vector=[0.7, 0.7], attributes={'hello': 'world'}),
    ])

    vector_set = namespace.export_vectors()
    for i, vector in enumerate(vector_set):
        print(f'Export {i}: ', vector)

    namespace.delete_all()
