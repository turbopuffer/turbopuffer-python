from turbopuffer.vectors import Cursor, VectorResult, VectorColumns, VectorRow, DATA, ITERATOR_BATCH_SIZE, batch_iter
from turbopuffer.backend import Backend
from turbopuffer.query import VectorQuery, FilterTuple
from typing import Dict, List, Optional, Iterable, Union, overload

class Namespace:
    """
    The Namespace type represents a set of vectors stored in turbopuffer.
    Within a namespace, vectors are uniquely referred to by their ID.
    All vectors in a namespace must have the same dimensions.
    """

    name: str
    backend: Backend

    def __init__(self, name: str, api_key: Optional[str] = None):
        """
        Creates a new turbopuffer.Namespace object for querying the turbopuffer API.

        This function does not make any API calls on its own.

        Specifying an api_key here will override the global configuration for API calls to this namespace.
        """
        self.name = name
        self.backend = Backend(api_key)

    def __str__(self) -> str:
        return f'tpuf-namespace:{self.name}'

    @overload
    def upsert(self, ids: List[int], vectors: List[List[float]], attributes: Optional[Dict[str, List[Optional[str]]]] = None) -> None:
        """
        Creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    def upsert(self, data: Union[dict, VectorColumns]) -> None:
        """
        Creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    def upsert(self, data: Union[Iterable[dict], Iterable[VectorRow]]) -> None:
        """
        Creates or updates a multiple vectors provided as a list or iterator.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    def upsert(self, data: VectorResult) -> None:
        """
        Creates or updates multiple vectors.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    def upsert(self, data=None, ids=None, vectors=None, attributes=None) -> None:
        if data is None:
            if ids is not None and vectors is not None:
                return self.upsert(VectorColumns(ids=ids, vectors=vectors, attributes=attributes))
            else:
                raise ValueError('upsert() requires both ids= and vectors= be set.')
        elif isinstance(data, VectorColumns):
            if None in data.vectors:
                raise ValueError('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.')
            response = self.backend.make_api_request('vectors', self.name, payload=data)
        elif isinstance(data, VectorRow):
            raise ValueError('upsert() should be called on a list of vectors, got single vector.')
        elif isinstance(data, list):
            if isinstance(data[0], dict):
                return self.upsert(VectorColumns.from_rows(data))
            elif isinstance(data[0], VectorRow):
                return self.upsert(VectorColumns.from_rows(data))
            elif isinstance(data[0], VectorColumns):
                for columns in data:
                    self.upsert(columns)
                return
            else:
                raise ValueError(f'Unsupported list data type: {type(data[0])}')
        elif isinstance(data, dict):
            if 'id' in data:
                raise ValueError('upsert() should be called on a list of vectors, got single vector.')
            elif 'ids' in data:
                return self.upsert(VectorColumns.from_dict(data))
            else:
                raise ValueError('Provided dict is missing ids.')
        elif isinstance(data, Iterable):
            for batch in batch_iter(data, ITERATOR_BATCH_SIZE):
                self.upsert(batch)
            return
        else:
            raise ValueError(f'Unsupported data type: {type(data)}')

        assert response.get('status', '') == 'OK', f'Invalid upsert() response: {response}'

    def delete(self, ids: Union[int, List[int]]) -> None:
        """
        Deletes vectors by id.
        """

        if isinstance(ids, int):
            response = self.backend.make_api_request('vectors', self.name, payload={
                'ids': [ids],
                'vectors': [None],
            })
        elif isinstance(ids, list):
            response = self.backend.make_api_request('vectors', self.name, payload={
                'ids': ids,
                'vectors': [None] * len(ids),
            })
        else:
            raise ValueError(f'Unsupported ids type: {type(ids)}')

        assert response.get('status', '') == 'OK', f'Invalid delete() response: {response}'

    @overload
    def query(self,
              vector: Optional[List[float]] = None,
              distance_metric: Optional[str] = None,
              top_k: int = 10,
              include_vectors: bool = False,
              include_attributes: Optional[List[str]] = None,
              filters: Optional[Dict[str, List[FilterTuple]]] = None):
        ...

    @overload
    def query(self, query_data: VectorQuery):
        ...

    @overload
    def query(self, query_data: dict):
        ...

    def query(self,
              query_data = None,
              vector = None,
              distance_metric = None,
              top_k = None,
              include_vectors = None,
              include_attributes = None,
              filters = None) -> VectorResult:
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
                filters=filters
            ))
        if not isinstance(query_data, VectorQuery):
            if isinstance(query_data, dict):
                query_data = VectorQuery.from_dict(query_data)
            else:
                raise ValueError(f'query() input type must be compatible with turbopuffer.VectorQuery: {type(query_data)}')

        response = self.backend.make_api_request('vectors', self.name, 'query', payload=query_data)
        return VectorResult(response, namespace=self)

    def vectors(self, cursor: Optional[Cursor] = None) -> VectorResult:
        """
        This function exports the entire dataset at full precision.
        A VectorResult is returned that will lazily load batches of vectors if treated as an Iterator.

        If you want to look up vectors by ID, use the query function with an id filter.
        """

        response = self.backend.make_api_request('vectors', self.name, query={'cursor': cursor})
        next_cursor = response.pop('next_cursor', None)
        return VectorResult(response, namespace=self, next_cursor=next_cursor)

    def delete_all_indexes(self) -> None:
        """
        Deletes all indexes in a namespace.
        """

        response = self.backend.make_api_request('vectors', self.name, 'index', method='DELETE')
        assert response.get('status', '') == 'ok', f'Invalid delete_all_indexes() response: {response}'

    def delete_all(self) -> None:
        """
        Deletes all data as well as all indexes.
        """

        response = self.backend.make_api_request('vectors', self.name, method='DELETE')
        assert response.get('status', '') == 'ok', f'Invalid delete_all() response: {response}'

    def recall(self, num=20, top_k=10) -> float:
        """
        This function evaluates the recall performance of ANN queries in this namespace.

        When you call this function, it selects 'num' random vectors that were previously inserted.
        For each of these vectors, it performs an ANN index search as well as a ground truth exhaustive search.

        Recall is calculated as the ratio of matching vectors between the two search results.
        """

        response = self.backend.make_api_request('vectors', self.name, '_debug', 'recall', query={'num': num, 'top_k': top_k})
        assert 'recall' in response, f'Invalid recall() response: {response}'
        return float(response.get('recall'))
