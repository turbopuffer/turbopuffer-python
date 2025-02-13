# Namespaces

Types:

```python
from turbopuffer.types import (
    NamespaceRetrieveResponse,
    NamespaceListResponse,
    NamespaceQueryResponse,
    NamespaceUpsertResponse,
)
```

Methods:

- <code title="get /v1/namespaces/{namespace}">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">retrieve</a>(namespace) -> <a href="./src/turbopuffer/types/namespace_retrieve_response.py">NamespaceRetrieveResponse</a></code>
- <code title="get /v1/namespaces">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">list</a>() -> <a href="./src/turbopuffer/types/namespace_list_response.py">NamespaceListResponse</a></code>
- <code title="post /v1/namespaces/{namespace}/query">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">query</a>(namespace, \*\*<a href="src/turbopuffer/types/namespace_query_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_query_response.py">NamespaceQueryResponse</a></code>
- <code title="post /v1/namespaces/{namespace}">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">upsert</a>(namespace, \*\*<a href="src/turbopuffer/types/namespace_upsert_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_upsert_response.py">NamespaceUpsertResponse</a></code>
