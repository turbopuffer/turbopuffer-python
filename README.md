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
tpuf.api_key = 'your-token'  # Alternatively: export=TURBOPUFFER_API_KEY=your-token
# Choose the best region for your data https://turbopuffer.com/docs/regions
tpuf.api_base_url = "https://gcp-us-east4.turbopuffer.com"

# Open a namespace
ns = tpuf.Namespace('hello_world')

# Read namespace metadata
if ns.exists():
    print(f'Namespace {ns.name} exists with {ns.dimensions()} dimensions and approximately {ns.approx_count()} vectors.')

# Upsert your dataset
ns.upsert(
    ids=[1, 2],
    vectors=[[0.1, 0.2], [0.3, 0.4]],
    attributes={'name': ['foo', 'foos']},
    distance_metric='cosine_distance',
)

# Alternatively, upsert using a row iterator
ns.upsert(
    {
        'id': id,
        'vector': [id/10, id/10],
        'attributes': {'name': 'food', 'num': 8}
    } for id in range(3, 10),
    distance_metric='cosine_distance',
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

# List all namespaces
namespaces = tpuf.namespaces()
print('Total namespaces:', len(namespaces))
for namespace in namespaces:
    print('Namespace', namespace.name, 'contains approximately', namespace.approx_count(),
            'vectors with', namespace.dimensions(), 'dimensions.')

# Delete vectors using the separate delete method
ns.delete([1, 2])
```

Async API
-------

The turbopuffer client also provides a fully-featured async API for use with asyncio-based applications. The async API follows the same patterns as the synchronous API but with async/await syntax.

```py
import asyncio
import turbopuffer as tpuf

async def main():
    # Set API key and base URL
    tpuf.api_key = 'your-token'
    tpuf.api_base_url = "https://gcp-us-east4.turbopuffer.com"
    
    # Create an AsyncNamespace instance
    async_ns = tpuf.AsyncNamespace('hello_world')
    
    # Check if namespace exists
    if await async_ns.aexists():
        print(f'Namespace {async_ns.name} exists with {await async_ns.adimensions()} dimensions')
        print(f'and approximately {await async_ns.aapprox_count()} vectors.')
    
    # Upsert data asynchronously
    await async_ns.aupsert(
        ids=[1, 2, 3],
        vectors=[[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]],
        attributes={'name': ['foo', 'bar', 'baz']},
        distance_metric='cosine_distance',
    )
    
    # Upsert using row iterator or generator
    await async_ns.aupsert(
        {
            'id': id,
            'vector': [id/10, id/10],
            'attributes': {'name': f'item_{id}', 'value': id*10}
        } for id in range(4, 10)
    )
    
    # Query vectors asynchronously
    result = await async_ns.aquery(
        vector=[0.2, 0.3],
        distance_metric='cosine_distance',
        top_k=5,
        include_vectors=True,
        include_attributes=True,
    )
    
    # AsyncVectorResult can be used with async for
    async for row in result:
        print(f"ID: {row.id}, Distance: {row.dist}")
        
    # Or loaded completely into memory
    all_results = await result.load()
    print(f"Found {len(all_results)} results")
    
    # List all vectors in the namespace
    all_vectors = await async_ns.avectors()
    # Load all vectors into memory
    vectors_list = await all_vectors.load()
    print(f"Namespace contains {len(vectors_list)} vectors")
    
    # Delete vectors asynchronously
    await async_ns.adelete([1, 2])
    
    # List all namespaces asynchronously
    namespaces_iterator = await tpuf.anamespaces()
    # Use async for to iterate through namespaces
    async for namespace in namespaces_iterator:
        print(f"Namespace: {namespace.name}")
    
    # Or load all namespaces at once
    all_namespaces = await namespaces_iterator.load()
    print(f"Total namespaces: {len(all_namespaces)}")

# Run the async main function
asyncio.run(main())
```

### Context Manager Support

AsyncNamespace instances can be used as async context managers to ensure proper resource cleanup:

```py
async def process_data():
    async with tpuf.AsyncNamespace('my_data') as ns:
        # Perform operations
        await ns.aupsert(ids=[1, 2], vectors=[[0.1, 0.2], [0.3, 0.4]])
        results = await ns.aquery(vector=[0.15, 0.25], top_k=5)
        # Resources will be cleaned up when exiting the context
```

### Converting Between Sync and Async APIs

The synchronous Namespace methods internally use the async methods by running them in an event loop. If you're mixing sync and async code, be aware of these considerations:

- Synchronous methods create an event loop if needed
- For best performance in async applications, use the async API directly
- In async contexts, avoid calling synchronous methods as they may cause event loop issues

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
