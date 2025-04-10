import turbopuffer as tpuf
import tests


def test_readme():
    ns = tpuf.Namespace(tests.test_prefix + 'hello_world')

    if ns.exists():
        print(f'Namespace {ns.name} exists with {ns.dimensions()} dimensions and approximately {ns.approx_count()} vectors.')

    # Upsert your dataset
    ns.write(
        upsert_columns={
            "id": [1, 2],
            "vector": [[0.1, 0.1], [0.2, 0.2]],
            "name": ["one", "two"]
        },
        distance_metric='euclidean_squared',
    )

    # Alternatively, upsert with the row-based format
    ns.write(
        upsert_rows=[
            {
                "id": id,
                "vector": [id/10, id/10],
                "name": "other"
            } for id in range(3, 10)
        ],
        distance_metric='euclidean_squared',
    )

    # Query your dataset
    results = ns.query(
        vector=[0.18, 0.19],
        top_k=10,
        filters=['And', [
            ['name', 'Glob', '*o*'],
            ['name', 'NotEq', 'other'],
        ]],
        include_attributes=['name'],
        include_vectors=True
    )
    print(results)
    # Output:
    # [
    #   VectorRow(id=2, vector=[0.2, 0.2], attributes={'name': 'two'}, dist=0.00049999997),
    #   VectorRow(id=1, vector=[0.1, 0.1], attributes={'name': 'one'}, dist=0.0145)]
    # ]

    # Delete rows
    ns.write(deletes=[1, 2])

    ns.delete_all()
