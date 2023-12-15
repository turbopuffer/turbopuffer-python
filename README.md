turbopuffer Python Client
=========================

The official Python client for accessing the turbopuffer API.

Usage
-----

1. Install the turbopuffer package and set your API key.
```sh
$ pip install turbopuffer
$ export TURBOPUFFER_API_KEY=your-token
```

2. Open a namespace
```py
import turbopuffer as tpuf

ns = tpuf.Namespace('hello_world')
```

3. Upsert your dataset
```py
ns.upsert({
    'ids': [1, 2],
    'vectors': [[0.1, 0.2], [0.3, 0.4]],
    'attributes': {'name': ['foo', 'bar']}
})
```

4. Query your dataset
```py
vectors = ns.query({
    'vector': [0.15, 0.22],
    'distance_metric': 'euclidean_squared',
    'top_k': 10,
    'filters': { 'name': [['Eq', 'foo'], ['NotEq', 'bar'], ['Glob', '*foo*']] },
    'include_attributes': ['name'],
    'include_vectors': False
})
print(vectors)
# [VectorRow(id=1, vector=None, attributes={'name': 'foo'}, dist=0.0029000001959502697), VectorRow(id=2, vector=None, attributes={'name': 'bar'}, dist=0.05490000173449516)]
```
