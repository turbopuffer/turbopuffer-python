# Turbopuffer

Types:

```python
from turbopuffer.types import NamespaceSummary
```

Methods:

- <code title="get /v1/namespaces">client.<a href="./src/turbopuffer/_client.py">namespaces</a>(\*\*<a href="src/turbopuffer/types/client_namespaces_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_summary.py">SyncNamespacePage[NamespaceSummary]</a></code>

# Namespaces

Types:

```python
from turbopuffer.types import (
    AggregationGroup,
    AttributeSchema,
    AttributeSchemaConfig,
    AttributeType,
    Bm25ClauseParams,
    BranchFromNamespaceParams,
    Columns,
    ContainsAllTokensFilterParams,
    ContainsAnyTokenFilterParams,
    CopyFromNamespaceParams,
    DecayParams,
    DistanceMetric,
    Encryption,
    FullTextSearch,
    FullTextSearchConfig,
    FuzzyMaxEditDistance,
    FuzzyParams,
    ID,
    IncludeAttributes,
    Language,
    Limit,
    NamespaceMetadata,
    NamespaceMetadataPatch,
    PinningConfig,
    QueryBilling,
    QueryPerformance,
    Row,
    SaturateParams,
    SparseDistanceMetric,
    Tokenizer,
    Vector,
    VectorEncoding,
    WriteBilling,
    WritePerformance,
    NamespaceBranchFromResponse,
    NamespaceCopyFromResponse,
    NamespaceDeleteAllResponse,
    NamespaceExplainQueryResponse,
    NamespaceHintCacheWarmResponse,
    NamespaceMultiQueryResponse,
    NamespaceQueryResponse,
    NamespaceRecallResponse,
    NamespaceSchemaResponse,
    NamespaceUpdateSchemaResponse,
    NamespaceWriteResponse,
)
```

Methods:

- <code title="post /v2/namespaces/{namespace}?stainless_overload=branchFrom">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">branch_from</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_branch_from_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_branch_from_response.py">NamespaceBranchFromResponse</a></code>
- <code title="post /v2/namespaces/{namespace}?stainless_overload=copyFrom">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">copy_from</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_copy_from_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_copy_from_response.py">NamespaceCopyFromResponse</a></code>
- <code title="delete /v2/namespaces/{namespace}">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">delete_all</a>(\*, namespace) -> <a href="./src/turbopuffer/types/namespace_delete_all_response.py">NamespaceDeleteAllResponse</a></code>
- <code title="post /v2/namespaces/{namespace}/explain_query">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">explain_query</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_explain_query_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_explain_query_response.py">NamespaceExplainQueryResponse</a></code>
- <code title="get /v1/namespaces/{namespace}/hint_cache_warm">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">hint_cache_warm</a>(\*, namespace) -> <a href="./src/turbopuffer/types/namespace_hint_cache_warm_response.py">NamespaceHintCacheWarmResponse</a></code>
- <code title="get /v2/namespaces/{namespace}/metadata">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">metadata</a>(\*, namespace) -> <a href="./src/turbopuffer/types/namespace_metadata.py">NamespaceMetadata</a></code>
- <code title="post /v2/namespaces/{namespace}/query?stainless_overload=multiQuery">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">multi_query</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_multi_query_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_multi_query_response.py">NamespaceMultiQueryResponse</a></code>
- <code title="post /v2/namespaces/{namespace}/query">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">query</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_query_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_query_response.py">NamespaceQueryResponse</a></code>
- <code title="post /v1/namespaces/{namespace}/_debug/recall">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">recall</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_recall_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_recall_response.py">NamespaceRecallResponse</a></code>
- <code title="get /v1/namespaces/{namespace}/schema">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">schema</a>(\*, namespace) -> <a href="./src/turbopuffer/types/namespace_schema_response.py">NamespaceSchemaResponse</a></code>
- <code title="patch /v1/namespaces/{namespace}/metadata">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">update_metadata</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_update_metadata_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_metadata.py">NamespaceMetadata</a></code>
- <code title="post /v1/namespaces/{namespace}/schema">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">update_schema</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_update_schema_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_update_schema_response.py">NamespaceUpdateSchemaResponse</a></code>
- <code title="post /v2/namespaces/{namespace}">client.namespaces.<a href="./src/turbopuffer/resources/namespaces.py">write</a>(\*, namespace, \*\*<a href="src/turbopuffer/types/namespace_write_params.py">params</a>) -> <a href="./src/turbopuffer/types/namespace_write_response.py">NamespaceWriteResponse</a></code>
