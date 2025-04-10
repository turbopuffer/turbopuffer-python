import sys
import iso8601
import json
from datetime import datetime
from turbopuffer.error import APIError
from turbopuffer.vectors import Cursor, VectorResult, VectorColumns, VectorRow, batch_iter, b64encode_vector
from turbopuffer.backend import Backend
from turbopuffer.query import VectorQuery, Filters, RankInput, ConsistencyDict
from typing import Dict, List, Literal, Optional, Iterable, Union, overload
import turbopuffer as tpuf

CmekDict = Dict[Literal['key_name'], str]
EncryptionDict = Dict[Literal['cmek'], CmekDict]

class FullTextSearchParams:
    """
    Used for configuring BM25 full-text indexing for a given attribute.
    """

    language: str
    stemming: bool
    remove_stopwords: bool
    case_sensitive: bool

    def __init__(self, language: str, stemming: bool, remove_stopwords: bool, case_sensitive: bool):
        self.language = language
        self.stemming = stemming
        self.remove_stopwords = remove_stopwords
        self.case_sensitive = case_sensitive

    def as_dict(self) -> dict:
        return {
            "language": self.language,
            "stemming": self.stemming,
            "remove_stopwords": self.remove_stopwords,
            "case_sensitive": self.case_sensitive,
        }

class AttributeSchema:
    """
    The schema for a particular attribute within a namespace.
    """

    type: str # one of: 'string', 'uint', '[]string', '[]uint'
    filterable: bool
    full_text_search: Optional[FullTextSearchParams] = None

    def __init__(self, type: str, filterable: bool, full_text_search: Optional[FullTextSearchParams] = None):
        self.type = type
        self.filterable = filterable
        self.full_text_search = full_text_search

    def as_dict(self) -> dict:
        result = {
            "type": self.type,
            "filterable": self.filterable,
        }
        if self.full_text_search:
            result["full_text_search"] = self.full_text_search.as_dict()
        return result

# Type alias for a namespace schema
NamespaceSchema = Dict[str, AttributeSchema]

def parse_namespace_schema(data: dict) -> NamespaceSchema:
    namespace_schema = {}
    for key, value in data.items():
        fts_params = value.get('full_text_search')
        fts_instance = None
        if fts_params:
            fts_instance = FullTextSearchParams(
                language=fts_params['language'],
                stemming=fts_params['stemming'],
                remove_stopwords=fts_params['remove_stopwords'],
                case_sensitive=fts_params['case_sensitive']
            )
        attribute_schema = AttributeSchema(
            type=value['type'],
            filterable=value['filterable'],
            full_text_search=fts_instance
        )
        namespace_schema[key] = attribute_schema
    return namespace_schema

class Namespace:
    """
    The Namespace type represents a set of vectors stored in turbopuffer.
    Within a namespace, vectors are uniquely referred to by their ID.
    All vectors in a namespace must have the same dimensions.
    """

    name: str
    backend: Backend

    metadata: Optional[dict] = None

    def __init__(self, name: str, api_key: Optional[str] = None, base_url: Optional[str] = None, headers: Optional[dict] = None):
        """
        Creates a new turbopuffer.Namespace object for querying the turbopuffer API.

        This function does not make any API calls on its own.

        Specifying an api_key here will override the global configuration for API calls to this namespace.

        Specifying a base_url here will override the global configuration api_base_url for this namespace.
        """
        self.name = name
        self.backend = Backend(api_key, base_url, headers)

    def __str__(self) -> str:
        return f'tpuf-namespace:{self.name}'

    def __eq__(self, other):
        if isinstance(other, Namespace):
            return self.name == other.name and self.backend == other.backend
        else:
            return False

    def refresh_metadata(self):
        response = self.backend.make_api_request('/v1/namespaces', self.name, method='HEAD')
        status_code = response.get('status_code')
        if status_code == 200:
            headers = response.get('headers', dict())
            dimensions = int(headers.get('x-turbopuffer-dimensions', '0'))
            approx_count = int(headers.get('x-turbopuffer-approx-num-vectors', '0'))
            self.metadata = {
                'exists': dimensions != 0,
                'dimensions': dimensions,
                'approx_count': approx_count,
                'created_at': iso8601.parse_date(headers.get('x-turbopuffer-created-at')),
            }
        elif status_code == 404:
            self.metadata = {
                'exists': False,
                'dimensions': 0,
                'approx_count': 0,
                'created_at': None,
            }
        else:
            raise APIError(response.status_code, 'Unexpected status code', response.get('content'))

    def exists(self) -> bool:
        """
        Returns True if the namespace exists, and False if the namespace is missing or empty.
        """
        # Always refresh the exists check since metadata from namespaces() might be delayed.
        self.refresh_metadata()
        return self.metadata['exists']

    def dimensions(self) -> int:
        """
        Returns the number of vector dimensions stored in this namespace.
        """
        if self.metadata is None or 'dimensions' not in self.metadata:
            self.refresh_metadata()
        return self.metadata.pop('dimensions', 0)

    def approx_count(self) -> int:
        """
        Returns the approximate number of vectors stored in this namespace.
        """
        if self.metadata is None or 'approx_count' not in self.metadata:
            self.refresh_metadata()
        return self.metadata.pop('approx_count', 0)

    def created_at(self) -> Optional[datetime]:
        """
        Returns the creation date of this namespace.
        """
        if self.metadata is None or 'created_at' not in self.metadata:
            self.refresh_metadata()
        return self.metadata.pop('created_at', None)

    def schema(self) -> NamespaceSchema:
        """
        Returns the current schema for the namespace.
        """
        response = self.backend.make_api_request('/v1/namespaces', self.name, 'schema', method='GET')
        return parse_namespace_schema(response["content"])

    def update_schema(self, schema_updates: NamespaceSchema):
        """
        Writes updates to the schema for a namespace.
        Returns the final schema after updates are done.

        See https://turbopuffer.com/docs/schema for specifics on allowed updates.
        """
        request_payload = json.dumps({key: value.as_dict() for key, value in schema_updates.items()}).encode()
        response = self.backend.make_api_request('/v1/namespaces', self.name, 'schema', method='POST', payload=request_payload)
        return parse_namespace_schema(response["content"])

    def copy_from_namespace(self, source_namespace: str):
        """
        Copies all documents from another namespace to this namespace.

        See: https://turbopuffer.com/docs/upsert#parameters `copy_from_namespace`
        for specifics on how this works.
        """
        payload = {
            "copy_from_namespace": source_namespace
        }
        response = self.backend.make_api_request('/v2/namespaces', self.name, payload=payload)
        assert response.get('content', dict()).get('status', '') == 'OK', f'Invalid copy_from_namespace() response: {response}'

    def write(self,
          upsert_columns: Optional[Dict[str, List]] = None,
          patch_columns: Optional[Dict[str, List]] = None,
          upsert_rows: Optional[List[Dict]] = None,
          patch_rows: Optional[List[Dict]] = None,
          deletes: Optional[List[Union[int, str]]] = None,
          delete_by_filter: Optional[Filters] = None,
          distance_metric: Optional[Literal["cosine_distance", "euclidean_squared"]] = None,
          schema: Optional[Dict] = None,
          encryption: Optional[EncryptionDict] = None) -> None:
        """
        Create, update, or delete documents.
        """
        payload = {}

        if upsert_columns is not None:
            if isinstance(upsert_columns, VectorColumns):
                payload["upsert_columns"] = upsert_columns.to_dict_for_write()
            elif isinstance(upsert_columns, Dict):
                payload["upsert_columns"] = upsert_columns
            else:
                raise ValueError("upsert_columns must be a Dict or VectorColumns")

        if patch_columns is not None:
            if isinstance(patch_columns, VectorColumns):
                payload["patch_columns"] = patch_columns.to_dict_for_write()
            elif isinstance(patch_columns, Dict):
                payload["patch_columns"] = patch_columns
            else:
                raise ValueError("patch_columns must be a Dict or VectorColumns")

        if upsert_rows is not None:
            if not isinstance(upsert_rows, List):
                raise ValueError("upsert_rows must be a List")

            if "upsert_columns" in payload:
                raise ValueError("upsert_rows cannot be used with upsert_columns")
            else:
                payload["upsert_columns"] = VectorColumns.from_rows_for_write(upsert_rows).to_dict_for_write()

        if patch_rows is not None:
            if not isinstance(patch_rows, List):
                raise ValueError("patch_rows must be a List")

            if "patch_columns" in payload:
                raise ValueError("patch_rows cannot be used with patch_columns")
            else:
                payload["patch_columns"] = VectorColumns.from_rows_for_write(patch_rows).to_dict_for_write()

        if deletes is not None:
            if not isinstance(deletes, List):
                raise ValueError("deletes must be a List")
            payload["deletes"] = deletes

        if delete_by_filter is not None:
            payload["delete_by_filter"] = delete_by_filter

        if distance_metric is not None:
            payload["distance_metric"] = distance_metric

        if schema is not None:
            payload["schema"] = schema

        if encryption is not None:
            payload["encryption"] = encryption

        response = self.backend.make_api_request('/v2/namespaces', self.name, payload=payload)
        response_content = response.get('content', dict())
        assert response_content.get('status', '') == 'OK', f'Invalid write() response: {response}'
        self.metadata = None  # Invalidate cached metadata
        return response_content.get('rows_affected')

    @overload
    def query(self,
              vector: Optional[List[float]] = None,
              distance_metric: Optional[str] = None,
              top_k: int = 10,
              include_vectors: bool = False,
              include_attributes: Optional[Union[List[str], bool]] = None,
              filters: Optional[Filters] = None,
              rank_by: Optional[RankInput] = None,
              consistency: Optional[ConsistencyDict] = None
              ) -> VectorResult:
        ...

    @overload
    def query(self, query_data: VectorQuery) -> VectorResult:
        ...

    @overload
    def query(self, query_data: dict) -> VectorResult:
        ...

    def query(self,
              query_data=None,
              vector=None,
              distance_metric=None,
              top_k=None,
              include_vectors=None,
              include_attributes=None,
              filters=None,
              rank_by=None,
              consistency=None) -> VectorResult:
        """
        Searches vectors matching the search query.

        See https://turbopuffer.com/docs/reference/query for query filter parameters.
        """

        if query_data is None:
            return self.query(VectorQuery(
                vector=vector,
                distance_metric=distance_metric,
                top_k=top_k,
                include_vectors=include_vectors,
                include_attributes=include_attributes,
                filters=filters,
                rank_by=rank_by,
                consistency=consistency
            ))
        if not isinstance(query_data, VectorQuery):
            if isinstance(query_data, dict):
                query_data = VectorQuery.from_dict(query_data)
            else:
                raise ValueError(f'query() input type must be compatible with turbopuffer.VectorQuery: {type(query_data)}')

        response = self.backend.make_api_request('/v1/namespaces', self.name, 'query', payload=query_data.__dict__)
        result = VectorResult(response.get('content', dict()), namespace=self)
        result.performance = response.get('performance')
        return result

    def vectors(self, cursor: Optional[Cursor] = None) -> VectorResult:
        """
        This function exports the entire dataset at full precision.
        A VectorResult is returned that will lazily load batches of vectors if treated as an Iterator.

        If you want to look up vectors by ID, use the query function with an id filter.
        """

        response = self.backend.make_api_request('/v1/namespaces', self.name, query={'cursor': cursor})
        content = response.get('content', dict())
        next_cursor = content.pop('next_cursor', None)
        result = VectorResult(content, namespace=self, next_cursor=next_cursor)
        result.performance = response.get('performance')
        return result

    def delete_all_indexes(self) -> None:
        """
        Deletes all indexes in a namespace.
        """

        response = self.backend.make_api_request('/v1/namespaces', self.name, 'index', method='DELETE')
        assert response.get('content', dict()).get('status', '') == 'ok', f'Invalid delete_all_indexes() response: {response}'

    def delete_all(self) -> None:
        """
        Deletes all data as well as all indexes.
        """

        response = self.backend.make_api_request('/v1/namespaces', self.name, method='DELETE')
        assert response.get('content', dict()).get('status', '') == 'ok', f'Invalid delete_all() response: {response}'
        self.metadata = None  # Invalidate cached metadata

    def recall(self, num=20, top_k=10) -> float:
        """
        This function evaluates the recall performance of ANN queries in this namespace.

        When you call this function, it selects 'num' random vectors that were previously inserted.
        For each of these vectors, it performs an ANN index search as well as a ground truth exhaustive search.

        Recall is calculated as the ratio of matching vectors between the two search results.
        """

        response = self.backend.make_api_request('/v1/namespaces', self.name, '_debug', 'recall', query={'num': num, 'top_k': top_k})
        content = response.get('content', dict())
        assert 'avg_recall' in content, f'Invalid recall() response: {response}'
        return float(content.get('avg_recall'))


class NamespaceIterator:
    """
    The VectorResult type represents a set of vectors that are the result of a query.

    A VectorResult can be treated as either a lazy iterator or a list by the user.
    Reading the length of the result will internally buffer the full result.
    """

    backend: Backend
    namespaces: List[Namespace] = []
    index: int = -1
    offset: int = 0
    next_cursor: Optional[Cursor] = None

    def __init__(self, backend: Backend, initial_set: Union[List[Namespace], List[dict]] = [], next_cursor: Optional[Cursor] = None):
        self.backend = backend
        self.index = -1
        self.offset = 0
        self.next_cursor = next_cursor

        if len(initial_set):
            if isinstance(initial_set[0], Namespace):
                self.namespaces = initial_set
            else:
                self.namespaces = NamespaceIterator.load_namespaces(backend.api_key, initial_set)

    def load_namespaces(api_key: Optional[str], initial_set: List[dict]) -> List[Namespace]:
        output = []
        for input in initial_set:
            ns = tpuf.Namespace(input['id'], api_key=api_key)
            ns.metadata = {
                'exists': True,
            }
            output.append(ns)

        return output

    def __str__(self) -> str:
        str_list = [ns.name for ns in self.namespaces]
        if not self.next_cursor and self.offset == 0:
            return str(str_list)
        else:
            return ("NamespaceIterator("
                    f"offset={self.offset}, "
                    f"next_cursor='{self.next_cursor}', "
                    f"namespaces={str_list})")

    def __len__(self) -> int:
        assert self.offset == 0, "Can't call len(NamespaceIterator) after iterating"
        assert self.index == -1, "Can't call len(NamespaceIterator) after iterating"
        if not self.next_cursor:
            return len(self.namespaces)
        else:
            it = iter(self)
            self.namespaces = [next for next in it]
            self.offset = 0
            self.index = -1
            self.next_cursor = None
            return len(self.namespaces)

    def __getitem__(self, index) -> VectorRow:
        if index >= len(self.namespaces) and self.next_cursor:
            it = iter(self)
            self.namespaces = [next for next in it]
            self.offset = 0
            self.index = -1
            self.next_cursor = None
        return self.namespaces[index]

    def __iter__(self) -> 'NamespaceIterator':
        assert self.offset == 0, "Can't iterate over NamespaceIterator multiple times"
        return NamespaceIterator(self.backend, self.namespaces, self.next_cursor)

    def __next__(self):
        if self.index + 1 < len(self.namespaces):
            self.index += 1
            return self.namespaces[self.index]
        elif self.next_cursor is None:
            raise StopIteration
        else:
            response = self.backend.make_api_request(
                'namespaces',
                query={'cursor': self.next_cursor}
            )
            content = response.get('content', dict())
            self.offset += len(self.namespaces)
            self.index = -1
            self.next_cursor = content.pop('next_cursor', None)
            self.namespaces = NamespaceIterator.load_namespaces(self.backend.api_key, content.pop('namespaces', list()))
            return self.__next__()


def namespaces(api_key: Optional[str] = None, base_url: Optional[str] = None) -> Iterable[Namespace]:
    """
    Lists all turbopuffer namespaces for a given api_key.
    If no api_key is provided, the globally configured API key will be used.
    If no base_url is provided, the globally configured api_base_url will be used.
    """
    backend = Backend(api_key, base_url)
    response = backend.make_api_request('/v1/namespaces')
    content = response.get('content', dict())
    next_cursor = content.pop('next_cursor', None)
    return NamespaceIterator(backend, content.pop('namespaces', list()), next_cursor)
