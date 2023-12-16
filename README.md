turbopuffer Python Client
=========================

The official Python client for accessing the turbopuffer API.

Usage
-----

1. Install the turbopuffer package and set your API key.
```sh
$ pip install turbopuffer
```

2. Start using the API
```py
import turbopuffer as tpuf
tpuf.api_key = 'your-token' # Alternatively: export=TURBOPUFFER_API_KEY=your-token

# Open a namespace
ns = tpuf.Namespace('hello_world')

# Upsert your dataset
ns.upsert(
    ids=[1, 2],
    vectors=[[0.1, 0.2], [0.3, 0.4]],
    attributes={'name': ['foo', 'bar']}
)

# Query your dataset
vectors = ns.query(
    vector=[0.15, 0.22],
    distance_metric='euclidean_squared',
    top_k=10,
    filters={ 'name': [['Eq', 'foo'], ['NotEq', 'bar'], ['Glob', '*foo*']] },
    include_attributes=['name'],
    include_vectors=True
)
print(vectors)
# [VectorRow(id=1, vector=[0.10000000149011612, 0.20000000298023224], attributes={'name': 'foo'}, dist=0.0029000001959502697)]
```
