from dataclasses import dataclass, asdict
import sys
import iso8601
import json
import asyncio
from datetime import datetime
from turbopuffer.error import APIError
from turbopuffer.vectors import Cursor, VectorResult, AsyncVectorResult, VectorColumns, VectorRow, batch_iter, abatch_iter
from turbopuffer.backend import Backend
from turbopuffer.query import VectorQuery, Filters, RankInput, ConsistencyDict
from typing import Dict, List, Literal, Optional, Iterable, Union, overload, AsyncIterable, Type, TypeVar, Generic, AsyncIterator
import turbopuffer as tpuf

T = TypeVar('T')

CmekDict = Dict[Literal['key_name'], str]
EncryptionDict = Dict[Literal['cmek'], CmekDict]

@dataclass(frozen=True)
class FullTextSearchParams:
    """
    Used for configuring BM25 full-text indexing for a given attribute.
    """

    language: str
    stemming: bool
    remove_stopwords: bool
    case_sensitive: bool

    def as_dict(self) -> dict:
        return asdict(self)

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

    def __init__(self, name: str, api_key: Optional[str] = None, headers: Optional[dict] = None):
        """
        Creates a new turbopuffer.Namespace object for querying the turbopuffer API.

        This function does not make any API calls on its own.

        Specifying an api_key here will override the global configuration for API calls to this namespace.
        """
        self.name = name
        self.backend = Backend(api_key, headers)

    def __str__(self) -> str:
        return f'tpuf-namespace:{self.name}'

    def __eq__(self, other):
        if isinstance(other, Namespace):
            return self.name == other.name and self.backend == other.backend
        else:
            return False

    def _run_async(self, coroutine):
        """Helper method to run async code from sync methods"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            # No event loop exists in this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(coroutine)

    def refresh_metadata(self):
        """
        Refreshes the namespace metadata.
        """
        # Create an async version if it doesn't exist yet
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
        
        return self._run_async(self._async_namespace.arefresh_metadata())

    def exists(self) -> bool:
        """
        Returns True if the namespace exists, and False if the namespace is missing or empty.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.aexists())

    def dimensions(self) -> int:
        """
        Returns the number of vector dimensions stored in this namespace.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.adimensions())

    def approx_count(self) -> int:
        """
        Returns the approximate number of vectors stored in this namespace.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.aapprox_count())

    def created_at(self) -> Optional[datetime]:
        """
        Returns the creation date of this namespace.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.acreated_at())

    def schema(self) -> NamespaceSchema:
        """
        Returns the current schema for the namespace.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.aschema())

    def update_schema(self, schema_updates: NamespaceSchema):
        """
        Writes updates to the schema for a namespace.
        Returns the final schema after updates are done.

        See https://turbopuffer.com/docs/schema for specifics on allowed updates.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.aupdate_schema(schema_updates))

    def copy_from_namespace(self, source_namespace: str):
        """
        Copies all documents from another namespace to this namespace.

        See: https://turbopuffer.com/docs/upsert#parameters `copy_from_namespace`
        for specifics on how this works.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.acopy_from_namespace(source_namespace))

    @overload
    def upsert(self,
               ids: Union[List[int], List[str]],
               vectors: List[List[float]],
               attributes: Optional[Dict[str, List[Optional[Union[str, int]]]]] = None,
               schema: Optional[Dict] = None,
               distance_metric: Optional[str] = None,
               encryption: Optional[EncryptionDict] = None) -> None:
        """
        Creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    def upsert(self,
               data: Union[dict, VectorColumns],
               distance_metric: Optional[str] = None,
               schema: Optional[Dict] = None,
               encryption: Optional[EncryptionDict] = None) -> None:
        """
        Creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    def upsert(self,
               data: Union[Iterable[dict], Iterable[VectorRow]],
               distance_metric: Optional[str] = None,
               schema: Optional[Dict] = None,
               encryption: Optional[EncryptionDict] = None) -> None:
        """
        Creates or updates a multiple vectors provided as a list or iterator.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    def upsert(self,
               data: VectorResult,
               distance_metric: Optional[str] = None,
               schema: Optional[Dict] = None,
               encryption: Optional[EncryptionDict] = None) -> None:
        """
        Creates or updates multiple vectors.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    def upsert(self, *args, **kwargs) -> None:
        """
        Creates or updates vectors.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.aupsert(*args, **kwargs))

    def delete(self, ids: Union[int, str, List[int], List[str]]) -> None:
        """
        Deletes vectors by id.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.adelete(ids))

    def delete_by_filter(self, filters: Filters) -> int:
        """
        Deletes vectors by filter.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.adelete_by_filter(filters))

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

    def query(self, *args, **kwargs) -> VectorResult:
        """
        Searches vectors matching the search query.
        
        See https://turbopuffer.com/docs/reference/query for query filter parameters.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        async_result = self._run_async(self._async_namespace.aquery(*args, **kwargs))
        # Convert AsyncVectorResult to VectorResult for synchronous API
        return VectorResult(async_result.data, namespace=self, next_cursor=async_result.next_cursor)

    def vectors(self, cursor: Optional[Cursor] = None) -> VectorResult:
        """
        This function exports the entire dataset at full precision.
        A VectorResult is returned that will lazily load batches of vectors if treated as an Iterator.

        If you want to look up vectors by ID, use the query function with an id filter.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        async_result = self._run_async(self._async_namespace.avectors(cursor))
        # Convert AsyncVectorResult to VectorResult for synchronous API
        return VectorResult(async_result.data, namespace=self, next_cursor=async_result.next_cursor)

    def delete_all_indexes(self) -> None:
        """
        Deletes all indexes in a namespace.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.adelete_all_indexes())

    def delete_all(self) -> None:
        """
        Deletes all data as well as all indexes.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.adelete_all())
        
    def recall(self, num=20, top_k=10) -> float:
        """
        This function evaluates the recall performance of ANN queries in this namespace.

        When you call this function, it selects 'num' random vectors that were previously inserted.
        For each of these vectors, it performs an ANN index search as well as a ground truth exhaustive search.

        Recall is calculated as the ratio of matching vectors between the two search results.
        """
        if not hasattr(self, '_async_namespace'):
            self._async_namespace = AsyncNamespace(self.name, self.backend.api_key)
            
        return self._run_async(self._async_namespace.arecall(num, top_k))


class NamespaceIterator:
    """
    The NamespaceIterator type represents a set of namespaces that can be iterated over.

    A NamespaceIterator can be treated as either a lazy iterator or a list by the user.
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

    @staticmethod
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

    def __getitem__(self, index) -> Namespace:
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


class AsyncNamespaceIterator:
    """
    The AsyncNamespaceIterator type represents a set of namespaces that can be asynchronously iterated over.

    An AsyncNamespaceIterator implements an async iterator interface, allowing you to use it with
    async for loops. For full buffer access, await the load() method to retrieve all results.
    """

    backend: Backend
    namespaces: List['AsyncNamespace'] = []
    index: int = -1
    offset: int = 0
    next_cursor: Optional[Cursor] = None

    def __init__(self, backend: Backend, initial_set: Union[List['AsyncNamespace'], List[dict]] = [], next_cursor: Optional[Cursor] = None):
        self.backend = backend
        self.index = -1
        self.offset = 0
        self.next_cursor = next_cursor

        if len(initial_set):
            if isinstance(initial_set[0], dict):
                self.namespaces = AsyncNamespaceIterator.load_namespaces(backend.api_key, initial_set)
            else:
                self.namespaces = initial_set

    @staticmethod
    def load_namespaces(api_key: Optional[str], initial_set: List[dict]) -> List['AsyncNamespace']:
        output = []
        for input in initial_set:
            ns = AsyncNamespace(input['id'], api_key=api_key)
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
            return ("AsyncNamespaceIterator("
                    f"offset={self.offset}, "
                    f"next_cursor='{self.next_cursor}', "
                    f"namespaces={str_list})")

    async def load(self) -> List['AsyncNamespace']:
        """
        Loads and returns all namespaces, fetching additional pages as needed.
        
        This method buffers all data in memory. For large result sets, consider
        using the async iterator interface instead.
        """
        if not self.next_cursor:
            return self.namespaces
            
        # Create new iterator and exhaust it to load all results
        result = []
        async for item in self.__aiter__():
            result.append(item)
            
        # Update our state with the fully loaded data
        self.namespaces = result
        self.offset = 0
        self.index = -1
        self.next_cursor = None
        
        return result

    def __aiter__(self) -> 'AsyncNamespaceIterator':
        # Reset state to start fresh iteration
        return AsyncNamespaceIterator(self.backend, self.namespaces, self.next_cursor)

    async def __anext__(self) -> 'AsyncNamespace':
        # Handle the case where we have data in memory
        if self.index + 1 < len(self.namespaces):
            self.index += 1
            return self.namespaces[self.index]
        # Handle the case where we're at the end of our data
        elif self.next_cursor is None:
            raise StopAsyncIteration
        # Handle the case where we need to fetch more data
        else:
            response = await self.backend.amake_api_request(
                'namespaces',
                query={'cursor': self.next_cursor}
            )
            content = response.get('content', dict())
            
            self.offset += len(self.namespaces)
            self.index = -1
            self.next_cursor = content.pop('next_cursor', None)
            self.namespaces = AsyncNamespaceIterator.load_namespaces(
                self.backend.api_key, 
                content.pop('namespaces', list())
            )
            
            # Recursively call __anext__ to handle the case where data is empty
            return await self.__anext__()


class AsyncNamespace:
    """
    The AsyncNamespace type represents a set of vectors stored in turbopuffer,
    with asynchronous access.
    
    Within a namespace, vectors are uniquely referred to by their ID.
    All vectors in a namespace must have the same dimensions.
    
    This class provides async versions of all Namespace methods.
    """

    name: str
    backend: Backend

    metadata: Optional[dict] = None

    def __init__(self, name: str, api_key: Optional[str] = None, headers: Optional[dict] = None):
        """
        Creates a new turbopuffer.AsyncNamespace object for querying the turbopuffer API asynchronously.

        This function does not make any API calls on its own.

        Specifying an api_key here will override the global configuration for API calls to this namespace.
        """
        self.name = name
        self.backend = Backend(api_key, headers)

    def __str__(self) -> str:
        return f'tpuf-async-namespace:{self.name}'

    def __eq__(self, other):
        if isinstance(other, AsyncNamespace):
            return self.name == other.name and self.backend == other.backend
        else:
            return False
            
    async def __aenter__(self):
        """Enable use as an async context manager."""
        await self.backend._get_async_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the async context."""
        if self.backend._async_session and not self.backend._async_session.closed:
            await self.backend._async_session.close()

    async def arefresh_metadata(self):
        """
        Asynchronously refreshes the namespace metadata.
        """
        response = await self.backend.amake_api_request('namespaces', self.name, method='HEAD')
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
            raise APIError(response.get('status_code'), 'Unexpected status code', response.get('content'))

    async def aexists(self) -> bool:
        """
        Asynchronously checks if the namespace exists.
        Returns True if the namespace exists, and False if the namespace is missing or empty.
        """
        # Always refresh the exists check since metadata from namespaces() might be delayed.
        await self.arefresh_metadata()
        return self.metadata['exists']

    async def adimensions(self) -> int:
        """
        Asynchronously returns the number of vector dimensions stored in this namespace.
        """
        if self.metadata is None or 'dimensions' not in self.metadata:
            await self.arefresh_metadata()
        return self.metadata.pop('dimensions', 0)

    async def aapprox_count(self) -> int:
        """
        Asynchronously returns the approximate number of vectors stored in this namespace.
        """
        if self.metadata is None or 'approx_count' not in self.metadata:
            await self.arefresh_metadata()
        return self.metadata.pop('approx_count', 0)

    async def acreated_at(self) -> Optional[datetime]:
        """
        Asynchronously returns the creation date of this namespace.
        """
        if self.metadata is None or 'created_at' not in self.metadata:
            await self.arefresh_metadata()
        return self.metadata.pop('created_at', None)

    async def aschema(self) -> NamespaceSchema:
        """
        Asynchronously returns the current schema for the namespace.
        """
        response = await self.backend.amake_api_request('namespaces', self.name, 'schema', method='GET')
        return parse_namespace_schema(response["content"])

    async def aupdate_schema(self, schema_updates: NamespaceSchema):
        """
        Asynchronously writes updates to the schema for a namespace.
        Returns the final schema after updates are done.

        See https://turbopuffer.com/docs/schema for specifics on allowed updates.
        """
        request_payload = json.dumps({key: value.as_dict() for key, value in schema_updates.items()}).encode()
        response = await self.backend.amake_api_request('namespaces', self.name, 'schema', method='POST', payload=request_payload)
        return parse_namespace_schema(response["content"])

    async def acopy_from_namespace(self, source_namespace: str):
        """
        Asynchronously copies all documents from another namespace to this namespace.

        See: https://turbopuffer.com/docs/upsert#parameters `copy_from_namespace`
        for specifics on how this works.
        """
        payload = {
            "copy_from_namespace": source_namespace
        }
        response = await self.backend.amake_api_request('namespaces', self.name, payload=payload)
        assert response.get('content', dict()).get('status', '') == 'OK', f'Invalid copy_from_namespace() response: {response}'

    @overload
    async def aupsert(self,
                ids: Union[List[int], List[str]],
                vectors: List[List[float]],
                attributes: Optional[Dict[str, List[Optional[Union[str, int]]]]] = None,
                schema: Optional[Dict] = None,
                distance_metric: Optional[str] = None,
                encryption: Optional[EncryptionDict] = None) -> None:
        """
        Asynchronously creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    async def aupsert(self,
                data: Union[dict, VectorColumns],
                distance_metric: Optional[str] = None,
                schema: Optional[Dict] = None,
                encryption: Optional[EncryptionDict] = None) -> None:
        """
        Asynchronously creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    async def aupsert(self,
                data: Union[Iterable[dict], Iterable[VectorRow]],
                distance_metric: Optional[str] = None,
                schema: Optional[Dict] = None,
                encryption: Optional[EncryptionDict] = None) -> None:
        """
        Asynchronously creates or updates a multiple vectors provided as a list or iterator.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    async def aupsert(self,
                data: VectorResult,
                distance_metric: Optional[str] = None,
                schema: Optional[Dict] = None,
                encryption: Optional[EncryptionDict] = None) -> None:
        """
        Asynchronously creates or updates multiple vectors.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    async def aupsert(self,
                data=None,
                ids=None,
                vectors=None,
                attributes=None,
                schema=None,
                distance_metric=None,
                encryption=None) -> None:
        """
        Asynchronously creates or updates vectors.
        """
        if data is None:
            if ids is not None and vectors is not None:
                return await self.aupsert(VectorColumns(ids=ids, vectors=vectors, attributes=attributes), schema=schema, distance_metric=distance_metric, encryption=encryption)
            else:
                raise ValueError('upsert() requires both ids= and vectors= be set.')
        elif (ids is not None and attributes is None) or (attributes is not None and schema is None):
            # Offset arguments to handle positional arguments case with no data field.
            return await self.aupsert(VectorColumns(ids=data, vectors=ids, attributes=vectors), schema=attributes, distance_metric=distance_metric, encryption=encryption)
        elif isinstance(data, VectorColumns):
            # "if None in data.vectors:" is not supported because data.vectors might be a list of np.ndarray
            # None == pd.ndarray is an ambiguous comparison in this case.
            for vec in data.vectors:
                if vec is None:
                    raise ValueError('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.')

            payload = {**data.__dict__}

            if distance_metric is not None:
                payload["distance_metric"] = distance_metric

            if schema is not None:
                payload["schema"] = schema
            
            if encryption is not None:
                payload["encryption"] = encryption

            response = await self.backend.amake_api_request('namespaces', self.name, payload=payload)

            assert response.get('content', dict()).get('status', '') == 'OK', f'Invalid upsert() response: {response}'
            self.metadata = None  # Invalidate cached metadata
        elif isinstance(data, VectorRow):
            raise ValueError('upsert() should be called on a list of vectors, got single vector.')
        elif isinstance(data, list):
            if len(data) == 0:
                return
            if isinstance(data[0], dict):
                return await self.aupsert(VectorColumns.from_rows(data), schema=schema, distance_metric=distance_metric, encryption=encryption)
            elif isinstance(data[0], VectorRow):
                return await self.aupsert(VectorColumns.from_rows(data), schema=schema, distance_metric=distance_metric, encryption=encryption)
            elif isinstance(data[0], VectorColumns):
                for columns in data:
                    await self.aupsert(columns, schema=schema, distance_metric=distance_metric, encryption=encryption)
                return
            else:
                raise ValueError(f'Unsupported list data type: {type(data[0])}')
        elif isinstance(data, dict):
            if 'id' in data:
                raise ValueError('upsert() should be called on a list of vectors, got single vector.')
            elif 'ids' in data:
                return await self.aupsert(VectorColumns.from_dict(data), schema=data.get('schema', None), distance_metric=distance_metric, encryption=encryption)
            else:
                raise ValueError('Provided dict is missing ids.')
        elif 'pandas' in sys.modules and isinstance(data, sys.modules['pandas'].DataFrame):
            if 'id' not in data.keys():
                raise ValueError('Provided pd.DataFrame is missing an id column.')
            if 'vector' not in data.keys():
                raise ValueError('Provided pd.DataFrame is missing a vector column.')
            
            for i in range(0, len(data), tpuf.upsert_batch_size):
                batch = data[i:i+tpuf.upsert_batch_size]
                attributes = dict()
                for key, values in batch.items():
                    if key != 'id' and key != 'vector':
                        attributes[key] = values.tolist()
                columns = tpuf.VectorColumns(
                    ids=batch['id'].tolist(),
                    vectors=batch['vector'].transform(lambda x: x.tolist()).tolist(),
                    attributes=attributes
                )
                await self.aupsert(columns, schema=schema, distance_metric=distance_metric, encryption=encryption)
            return
        elif isinstance(data, Iterable):
            async for batch in abatch_iter(data, tpuf.upsert_batch_size):
                await self.aupsert(batch, schema=schema, distance_metric=distance_metric, encryption=encryption)
            return
        else:
            raise ValueError(f'Unsupported data type: {type(data)}')

    async def adelete(self, ids: Union[int, str, List[int], List[str]]) -> None:
        """
        Asynchronously deletes vectors by id.
        """
        if isinstance(ids, int) or isinstance(ids, str):
            response = await self.backend.amake_api_request('namespaces', self.name, payload={
                'ids': [ids],
                'vectors': [None],
            })
        elif isinstance(ids, list):
            response = await self.backend.amake_api_request('namespaces', self.name, payload={
                'ids': ids,
                'vectors': [None] * len(ids),
            })
        else:
            raise ValueError(f'Unsupported ids type: {type(ids)}')

        assert response.get('content', dict()).get('status', '') == 'OK', f'Invalid delete() response: {response}'
        self.metadata = None  # Invalidate cached metadata

    async def adelete_by_filter(self, filters: Filters) -> int:
        """
        Asynchronously deletes vectors by filter.
        """
        response = await self.backend.amake_api_request('namespaces', self.name, payload={
            'delete_by_filter': filters
        })
        response_content = response.get('content', dict())
        assert response_content.get('status', '') == 'OK', f'Invalid delete_by_filter() response: {response}'
        self.metadata = None  # Invalidate cached metadata
        return response_content.get('rows_affected')

    @overload
    async def aquery(self,
               vector: Optional[List[float]] = None,
               distance_metric: Optional[str] = None,
               top_k: int = 10,
               include_vectors: bool = False,
               include_attributes: Optional[Union[List[str], bool]] = None,
               filters: Optional[Filters] = None,
               rank_by: Optional[RankInput] = None,
               consistency: Optional[ConsistencyDict] = None
               ) -> AsyncVectorResult:
        ...

    @overload
    async def aquery(self, query_data: VectorQuery) -> AsyncVectorResult:
        ...

    @overload
    async def aquery(self, query_data: dict) -> AsyncVectorResult:
        ...

    async def aquery(self,
              query_data=None,
              vector=None,
              distance_metric=None,
              top_k=None,
              include_vectors=None,
              include_attributes=None,
              filters=None,
              rank_by=None,
              consistency=None) -> AsyncVectorResult:
        """
        Asynchronously searches vectors matching the search query.

        See https://turbopuffer.com/docs/reference/query for query filter parameters.
        """
        if query_data is None:
            return await self.aquery(VectorQuery(
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

        response = await self.backend.amake_api_request('namespaces', self.name, 'query', payload=query_data.__dict__)
        result = AsyncVectorResult(response.get('content', dict()), namespace=self)
        result.performance = response.get('performance')
        return result

    async def avectors(self, cursor: Optional[Cursor] = None) -> AsyncVectorResult:
        """
        Asynchronously exports the entire dataset at full precision.
        An AsyncVectorResult is returned that will lazily load batches of vectors if treated as an async Iterator.

        If you want to look up vectors by ID, use the query function with an id filter.
        """
        # Handle None cursor by passing empty string or omitting parameter entirely
        query_params = {}
        if cursor is not None:
            query_params['cursor'] = cursor
            
        response = await self.backend.amake_api_request('namespaces', self.name, query=query_params)
        content = response.get('content', dict())
        next_cursor = content.pop('next_cursor', None)
        result = AsyncVectorResult(content, namespace=self, next_cursor=next_cursor)
        result.performance = response.get('performance')
        return result

    async def adelete_all_indexes(self) -> None:
        """
        Asynchronously deletes all indexes in a namespace.
        """
        response = await self.backend.amake_api_request('namespaces', self.name, 'index', method='DELETE')
        assert response.get('content', dict()).get('status', '') == 'ok', f'Invalid delete_all_indexes() response: {response}'

    async def adelete_all(self) -> None:
        """
        Asynchronously deletes all data as well as all indexes.
        """
        response = await self.backend.amake_api_request('namespaces', self.name, method='DELETE')
        assert response.get('content', dict()).get('status', '') == 'ok', f'Invalid delete_all() response: {response}'
        self.metadata = None  # Invalidate cached metadata

    async def arecall(self, num=20, top_k=10) -> float:
        """
        Asynchronously evaluates the recall performance of ANN queries in this namespace.

        When you call this function, it selects 'num' random vectors that were previously inserted.
        For each of these vectors, it performs an ANN index search as well as a ground truth exhaustive search.

        Recall is calculated as the ratio of matching vectors between the two search results.
        """
        response = await self.backend.amake_api_request('namespaces', self.name, '_debug', 'recall', query={'num': num, 'top_k': top_k})
        content = response.get('content', dict())
        assert 'avg_recall' in content, f'Invalid recall() response: {response}'
        return float(content.get('avg_recall'))
        
    # All sync methods in AsyncNamespace have been replaced by _run_async() helper
    # that calls their respective async counterparts in AsyncNamespace


def namespaces(api_key: Optional[str] = None) -> Iterable[Namespace]:
    """
    Lists all turbopuffer namespaces for a given api_key.
    If no api_key is provided, the globally configured API key will be used.
    """
    # Use the async version with run_until_complete
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        # No event loop exists in this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    # Call the async version and convert results to synchronous iterators
    async_iterator = loop.run_until_complete(anamespaces(api_key))
    async_namespaces = loop.run_until_complete(async_iterator.load())
    
    # Convert AsyncNamespace instances to Namespace instances
    sync_namespaces = [Namespace(ns.name, api_key=api_key) for ns in async_namespaces]
    return sync_namespaces


async def anamespaces(api_key: Optional[str] = None) -> AsyncIterator[AsyncNamespace]:
    """
    Asynchronously lists all turbopuffer namespaces for a given api_key.
    If no api_key is provided, the globally configured API key will be used.
    
    Returns an async iterator that can be used with 'async for'.
    """
    backend = Backend(api_key)
    response = await backend.amake_api_request('namespaces')
    content = response.get('content', dict())
    next_cursor = content.pop('next_cursor', None)
    return AsyncNamespaceIterator(backend, content.pop('namespaces', list()), next_cursor)
