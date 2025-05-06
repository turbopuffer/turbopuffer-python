![](https://github.com/turbopuffer/turbopuffer-python/assets/1594638/0482aa50-4665-4998-afd3-78afe56b52f3) turbopuffer Python Client [![CI Test](https://github.com/turbopuffer/turbopuffer-python/actions/workflows/ci_test.yml/badge.svg)](https://github.com/turbopuffer/turbopuffer-python/actions/workflows/ci_test.yml)
=========================

The official Python client for accessing the turbopuffer API.

Usage
-----

1. Install the turbopuffer package and set your API key.
```sh
pip install turbopuffer
```
Or if you're able to run C binaries for JSON encoding, use:
```sh
pip install 'turbopuffer[fast]'
```

2. Start using the API
```py
import turbopuffer as tpuf
tpuf.api_key = 'your-token'  # Alternatively: export=TURBOPUFFER_API_KEY=your-token

# Choose the best region for your data: https://turbopuffer.com/docs/regions
# Setting base URL, option 1 (global):
# tpuf.api_base_url = "https://gcp-us-east4.turbopuffer.com"

# Open a namespace
# Setting base URL, option 2 (per namespace. If specified, this will override the global api_base_url):
ns = tpuf.Namespace('hello_world', base_url="https://gcp-us-east4.turbopuffer.com")

# Read namespace metadata
if ns.exists():
    print(f'Namespace {ns.name} exists with {ns.dimensions()} dimensions and approximately {ns.approx_count()} rows.')

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

# List all namespaces
namespaces = tpuf.namespaces()
print('Total namespaces:', len(namespaces))
for namespace in namespaces:
    print('Namespace', namespace.name, 'contains approximately', namespace.approx_count(),
          'rows with', namespace.dimensions(), 'dimensions.')

# Delete rows
ns.write(deletes=[1, 2])
```

Endpoint Documentation
----------------------

For more details on request parameters and query options, check the docs at https://turbopuffer.com/docs

## Development

Run `poetry install --with=test` to set up the project and dependencies.

1. `poetry run pytest`
2.  Bump version in `turbopuffer/version.py` and `pyproject.toml`
3. `git tag vX.Y.Z && git push --tags`
3. `poetry build`
4. `poetry publish`
