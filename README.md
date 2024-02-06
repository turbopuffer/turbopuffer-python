![](https://github.com/turbopuffer/turbopuffer-python/assets/1594638/0482aa50-4665-4998-afd3-78afe56b52f3) turbopuffer Python Client [![CI Test](https://github.com/turbopuffer/turbopuffer-python/actions/workflows/ci_test.yml/badge.svg)](https://github.com/turbopuffer/turbopuffer-python/actions/workflows/ci_test.yml)
=========================

The official Python client for accessing the turbopuffer API.

Usage
-----

1. Install the turbopuffer package and set your API key.
```sh
$ pip install turbopuffer
```
Or if you're able to run C binaries for JSON encoding, use:
```sh
$ pip install turbopuffer[fast]
```

2. Start using the API
```py
import turbopuffer as tpuf
tpuf.api_key = 'your-token' # Alternatively: export=TURBOPUFFER_API_KEY=your-token

# Open a namespace
ns = tpuf.Namespace('hello_world')

# Read namespace metadata
if ns.exists():
    print(f'Namespace {ns.name} exists with {ns.dimensions()} dimensions and approximately {ns.approx_count()} vectors.')

# Upsert your dataset
ns.upsert(
    ids=[1, 2],
    vectors=[[0.1, 0.2], [0.3, 0.4]],
    attributes={'name': ['foo', 'foos']}
)

# Alternatively, upsert using a row iterator
ns.upsert(
    {
        'id': id,
        'vector': [id/10, id/10],
        'attributes': {'name': 'food'}
    } for id in range(3, 10)
)

# Query your dataset
vectors = ns.query(
    vector=[0.15, 0.22],
    distance_metric='cosine_distance',
    top_k=10,
    filters={ 'name': [['Glob', 'foo*'], ['NotEq', 'food']] },
    include_attributes=['name'],
    include_vectors=True
)
print(vectors)
# [
#   VectorRow(id=2, vector=[0.30000001192092896, 0.4000000059604645], attributes={'name': 'foos'}, dist=0.001016080379486084),
#   VectorRow(id=1, vector=[0.10000000149011612, 0.20000000298023224], attributes={'name': 'foo'}, dist=0.009067952632904053)
# ]

# List all namespaces
namespaces = tpuf.list_namespaces()
print('Total namespaces:', len(namespaces))
for ns2 in namespaces:
    print(ns2.name)

# Delete vectors using the separate delete method
ns.delete([1, 2])
```

Endpoint Documentation
----------------------

For more details on request parameters and query options, check the docs at https://turbopuffer.com/docs
