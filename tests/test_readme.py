import turbopuffer as tpuf
import tests


def test_readme():
    ns = tpuf.Namespace(tests.test_prefix + 'hello_world')

    if ns.exists():
        print(f'Namespace {ns.name} exists with {ns.dimensions()} dimensions and approximately {ns.approx_count()} vectors.')

    ns.upsert(
        ids=[1, 2],
        vectors=[[0.1, 0.2], [0.3, 0.4]],
        attributes={'name': ['foo', 'foos']}
    )

    ns.upsert(
        {
            'id': id,
            'vector': [id/10, id/10],
            'attributes': {'name': 'food'}
        } for id in range(3, 10)
    )

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

    ns.delete([1, 2])

    ns.delete_all()
