# Namespaces

Types:

```python
from turbopuffer.types import (
    AttributeSchema,
    DistanceMetric,
    DocumentColumns,
    DocumentRow,
    DocumentRowWithScore,
    FullTextSearchConfig,
    ID,
    NamespaceSummary,
    NamespaceDeleteAllResponse,
    NamespaceGetSchemaResponse,
    NamespaceQueryResponse,
    NamespaceUpsertResponse,
)
```

Methods:

- <code title="get /v1/namespaces">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">list</a>(\*\*<a href="src/turbopuffer/types/namespace_list_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_summary.py">SyncListNamespaces[NamespaceSummary]</a></code>
- <code title="delete /v1/namespaces/{namespace}">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">delete_all</a>(namespace) -> <a href="./src/turbopuffer/types/namespace_delete_all_response.py">NamespaceDeleteAllResponse</a></code>
- <code title="get /v1/namespaces/{namespace}/schema">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">get_schema</a>(namespace) -> <a href="./src/turbopuffer/types/namespace_get_schema_response.py">NamespaceGetSchemaResponse</a></code>
- <code title="post /v1/namespaces/{namespace}/query">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">query</a>(namespace, \*\*<a href="src/turbopuffer/types/namespace_query_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_query_response.py">NamespaceQueryResponse</a></code>
- <code title="post /v1/namespaces/{namespace}">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">upsert</a>(namespace, \*\*<a href="src/turbopuffer/types/namespace_upsert_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_upsert_response.py">NamespaceUpsertResponse</a></code>
