import sys
from turbopuffer.vectors import Cursor, VectorResult, VectorColumns, VectorRow, batch_iter
from turbopuffer.backend import Backend
from turbopuffer.query import VectorQuery, FilterTuple
from typing import Dict, List, Optional, Iterable, Union, overload
import turbopuffer as tpuf


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

    def exists(self) -> bool:
        response = self.backend.make_api_request('vectors', self.name, method='HEAD')
        if response['status_code'] == 200:
            return response['headers'].get('x-turbopuffer-dimensions', '0') != '0'
        else:
            return False

    def dimensions(self) -> int:
        response = self.backend.make_api_request('vectors', self.name, method='HEAD')
        return int(response['headers'].get('x-turbopuffer-dimensions', '0'))

    def approx_vector_count(self) -> int:
        response = self.backend.make_api_request('vectors', self.name, method='HEAD')
        return int(response['headers'].get('x-turbopuffer-approx-num-vectors', '0'))

    @overload
    def upsert(self, ids: Union[List[int], List[str]], vectors: List[List[float]], attributes: Optional[Dict[str, List[Optional[str]]]] = None) -> None:
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
        elif ids is not None and attributes is None:
            # Offset arguments to handle positional arguments case with no data field.
            return self.upsert(VectorColumns(ids=data, vectors=ids, attributes=vectors))
        elif isinstance(data, VectorColumns):
            # "if None in data.vectors:" is not supported because data.vectors might be a list of np.ndarray
            # None == pd.ndarray is an ambiguous comparison in this case.
            for vec in data.vectors:
                if vec is None:
                    raise ValueError('upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead.')
            response = self.backend.make_api_request('vectors', self.name, payload=data.__dict__)
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
        elif 'pandas' in sys.modules and isinstance(data, sys.modules['pandas'].DataFrame):
            if 'id' not in data.keys():
                raise ValueError('Provided pd.DataFrame is missing an id column.')
            if 'vector' not in data.keys():
                raise ValueError('Provided pd.DataFrame is missing a vector column.')
            # start = time.monotonic()
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
                # time_diff = time.monotonic() - start
                # print(f"Batch {columns.ids[0]}..{columns.ids[-1]} begin:", time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # before = time.monotonic()
                # print(columns)
                self.upsert(columns)
                # time_diff = time.monotonic() - before
                # print(f"Batch {columns.ids[0]}..{columns.ids[-1]} time:", time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # start = time.monotonic()
        elif isinstance(data, Iterable):
            # start = time.monotonic()
            for batch in batch_iter(data, tpuf.upsert_batch_size):
                # time_diff = time.monotonic() - start
                # print('Batch begin:', time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # before = time.monotonic()
                self.upsert(batch)
                # time_diff = time.monotonic() - before
                # print('Batch time:', time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # start = time.monotonic()
            return
        else:
            raise ValueError(f'Unsupported data type: {type(data)}')

        assert response.get('status', '') == 'OK', f'Invalid upsert() response: {response}'

    def delete(self, ids: Union[int, str, List[int], List[str]]) -> None:
        """
        Deletes vectors by id.
        """

        if isinstance(ids, int) or isinstance(ids, str):
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
              include_attributes: Optional[Union[List[str], bool]] = None,
              filters: Optional[Dict[str, List[FilterTuple]]] = None) -> VectorResult:
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
              filters=None) -> VectorResult:
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

        response = self.backend.make_api_request('vectors', self.name, 'query', payload=query_data.__dict__)
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
