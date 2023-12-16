import turbopuffer as tpuf

def test_readme():
    ns = tpuf.Namespace('hello_world')

    ns.upsert({
        'ids': [1, 2],
        'vectors': [[0.1, 0.2], [0.3, 0.4]],
        'attributes': {'name': ['foo', 'bar']}
    })

    vectors = ns.query({
        'vector': [0.15, 0.22],
        'distance_metric': 'euclidean_squared',
        'top_k': 10,
        'filters': { 'name': [['Eq', 'foo'], ['NotEq', 'bar'], ['Glob', '*foo*']] },
        'include_attributes': ['name'],
        'include_vectors': True
    })
    print(vectors)

    ns.delete_all()
