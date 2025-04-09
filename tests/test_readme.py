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
            "vector": [[0.1, 0.2], [0.3, 0.4]],
            "name": ["foo", "foos"]
        }
    )

    # Alternatively, upsert using a row iterator
    ns.write(
        upsert_rows=[{
            "id": id,
            "vector": [id/10, id/10],
            "name": "food"
        } for id in range(3, 10)]
    )

    # Query your dataset
    vectors = ns.query(
        vector=[0.15, 0.22],
        distance_metric='cosine_distance',
        top_k=10,
        filters=['And', [
            ['name', 'Glob', 'foo*'],
            ['name', 'NotEq', 'food'],
        ]],
        include_attributes=['name'],
        include_vectors=True
    )
    print(vectors)
    # [
    #   VectorRow(id=2, vector=[0.30000001192092896, 0.4000000059604645], attributes={'name': 'foos'}, dist=0.001016080379486084),
    #   VectorRow(id=1, vector=[0.10000000149011612, 0.20000000298023224], attributes={'name': 'foo'}, dist=0.009067952632904053)
    # ]

    # Delete vectors using the separate delete method
    ns.write(
        deletes=[1, 2]
    )

    ns.delete_all()
