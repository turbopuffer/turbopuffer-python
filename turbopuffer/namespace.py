import sys
from typing import Dict, Iterable, List, Optional, Union, overload

import httpx
import iso8601

import turbopuffer as tpuf
from turbopuffer.backend import AsyncBackend, Backend
from turbopuffer.error import APIError
from turbopuffer.query import FilterTuple, VectorQuery
from turbopuffer.vectors import (
    Cursor,
    VectorColumns,
    VectorResult,
    VectorRow,
    batch_iter,
)


class Namespace:
    """
    The Namespace type represents a set of vectors stored in turbopuffer.
    Within a namespace, vectors are uniquely referred to by their ID.
    All vectors in a namespace must have the same dimensions.
    """

    name: str
    backend: Backend
    async_backend: AsyncBackend

    metadata: Optional[dict] = None

    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None,
        *,
        client: Optional[httpx.Client] = None,
        async_client: Optional[httpx.AsyncClient] = None,
    ):
        """
        Creates a new turbopuffer.Namespace object for querying the turbopuffer API.

        This function does not make any API calls on its own.

        Specifying an api_key here will override the global configuration for API calls to this namespace.
        """
        self.name = name
        self.backend = Backend(api_key, client=client)
        self.async_backend = AsyncBackend(api_key, async_client=async_client)

    def __str__(self) -> str:
        return f"tpuf-namespace:{self.name}"

    def __eq__(self, other):
        if isinstance(other, Namespace):
            return (
                self.name == other.name
                and self.backend == other.backend
                and self.async_backend == other.async_backend
            )
        else:
            return False

    def refresh_metadata(self):
        response = self.backend.make_api_request("vectors", self.name, method="HEAD")
        status_code = response.get("status_code")
        if status_code == 200:
            headers = response.get("headers", dict())
            dimensions = int(headers.get("x-turbopuffer-dimensions", "0"))
            approx_count = int(headers.get("x-turbopuffer-approx-num-vectors", "0"))
            self.metadata = {
                "exists": dimensions != 0,
                "dimensions": dimensions,
                "approx_count": approx_count,
            }
        elif status_code == 404:
            self.metadata = {
                "exists": False,
                "dimensions": 0,
                "approx_count": 0,
            }
        else:
            raise APIError(
                response.status_code, "Unexpected status code", response.get("content")
            )

    async def async_refresh_metadata(self):
        response = await self.async_backend.make_api_request(
            "vectors", self.name, method="HEAD"
        )
        status_code = response.get("status_code")
        if status_code == 200:
            headers = response.get("headers", dict())
            dimensions = int(headers.get("x-turbopuffer-dimensions", "0"))
            approx_count = int(headers.get("x-turbopuffer-approx-num-vectors", "0"))
            self.metadata = {
                "exists": dimensions != 0,
                "dimensions": dimensions,
                "approx_count": approx_count,
            }
        elif status_code == 404:
            self.metadata = {
                "exists": False,
                "dimensions": 0,
                "approx_count": 0,
            }
        else:
            raise APIError(
                response.status_code, "Unexpected status code", response.get("content")
            )

    def exists(self) -> bool:
        """
        Returns True if the namespace exists, and False if the namespace is missing or empty.
        """
        # Always refresh the exists check since metadata from namespaces() might be delayed.
        self.refresh_metadata()
        return self.metadata["exists"]

    async def async_exists(self) -> bool:
        """
        Returns True if the namespace exists, and False if the namespace is missing or empty.
        """
        # Always refresh the exists check since metadata from namespaces() might be delayed.
        await self.async_refresh_metadata()
        return self.metadata["exists"]

    def dimensions(self) -> int:
        """
        Returns the number of vector dimensions stored in this namespace.
        """
        if self.metadata is None or "dimensions" not in self.metadata:
            self.refresh_metadata()
        return self.metadata.pop("dimensions", 0)

    async def async_dimensions(self) -> int:
        """
        Returns the number of vector dimensions stored in this namespace.
        """
        if self.metadata is None or "dimensions" not in self.metadata:
            await self.async_refresh_metadata()
        return self.metadata.pop("dimensions", 0)

    async def approx_count(self) -> int:
        """
        Returns the approximate number of vectors stored in this namespace.
        """
        if self.metadata is None or "approx_count" not in self.metadata:
            await self.async_refresh_metadata()
        return self.metadata.pop("approx_count", 0)

    @overload
    def upsert(
        self,
        ids: Union[List[int], List[str]],
        vectors: List[List[float]],
        attributes: Optional[Dict[str, List[Optional[str]]]] = None,
    ) -> None:
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
                return self.upsert(
                    VectorColumns(ids=ids, vectors=vectors, attributes=attributes)
                )
            else:
                raise ValueError("upsert() requires both ids= and vectors= be set.")
        elif ids is not None and attributes is None:
            # Offset arguments to handle positional arguments case with no data field.
            return self.upsert(VectorColumns(ids=data, vectors=ids, attributes=vectors))
        elif isinstance(data, VectorColumns):
            # "if None in data.vectors:" is not supported because data.vectors might be a list of np.ndarray
            # None == pd.ndarray is an ambiguous comparison in this case.
            for vec in data.vectors:
                if vec is None:
                    raise ValueError(
                        "upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead."
                    )
            response = self.backend.make_api_request(
                "vectors", self.name, payload=data.__dict__
            )

            assert (
                response.get("content", dict()).get("status", "") == "OK"
            ), f"Invalid upsert() response: {response}"
            self.metadata = None  # Invalidate cached metadata
        elif isinstance(data, VectorRow):
            raise ValueError(
                "upsert() should be called on a list of vectors, got single vector."
            )
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
                raise ValueError(f"Unsupported list data type: {type(data[0])}")
        elif isinstance(data, dict):
            if "id" in data:
                raise ValueError(
                    "upsert() should be called on a list of vectors, got single vector."
                )
            elif "ids" in data:
                return self.upsert(VectorColumns.from_dict(data))
            else:
                raise ValueError("Provided dict is missing ids.")
        elif "pandas" in sys.modules and isinstance(
            data, sys.modules["pandas"].DataFrame
        ):
            if "id" not in data.keys():
                raise ValueError("Provided pd.DataFrame is missing an id column.")
            if "vector" not in data.keys():
                raise ValueError("Provided pd.DataFrame is missing a vector column.")
            # start = time.monotonic()
            for i in range(0, len(data), tpuf.upsert_batch_size):
                batch = data[i : i + tpuf.upsert_batch_size]
                attributes = dict()
                for key, values in batch.items():
                    if key != "id" and key != "vector":
                        attributes[key] = values.tolist()
                columns = tpuf.VectorColumns(
                    ids=batch["id"].tolist(),
                    vectors=batch["vector"].transform(lambda x: x.tolist()).tolist(),
                    attributes=attributes,
                )
                # time_diff = time.monotonic() - start
                # print(f"Batch {columns.ids[0]}..{columns.ids[-1]} begin:", time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # before = time.monotonic()
                # print(columns)
                self.upsert(columns)
                # time_diff = time.monotonic() - before
                # print(f"Batch {columns.ids[0]}..{columns.ids[-1]} time:", time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # start = time.monotonic()
            return
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
            raise ValueError(f"Unsupported data type: {type(data)}")

    @overload
    async def async_upsert(
        self,
        ids: Union[List[int], List[str]],
        vectors: List[List[float]],
        attributes: Optional[Dict[str, List[Optional[str]]]] = None,
    ) -> None:
        """
        Creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    async def async_upsert(self, data: Union[dict, VectorColumns]) -> None:
        """
        Creates or updates multiple vectors provided in a column-oriented layout.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    async def async_upsert(
        self, data: Union[Iterable[dict], Iterable[VectorRow]]
    ) -> None:
        """
        Creates or updates a multiple vectors provided as a list or iterator.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    @overload
    async def async_upsert(self, data: VectorResult) -> None:
        """
        Creates or updates multiple vectors.
        If this call succeeds, data is guaranteed to be durably written to object storage.

        Upserting a vector will overwrite any existing vector with the same ID.
        """
        ...

    async def async_upsert(
        self, data=None, ids=None, vectors=None, attributes=None
    ) -> None:
        if data is None:
            if ids is not None and vectors is not None:
                return await self.async_upsert(
                    VectorColumns(ids=ids, vectors=vectors, attributes=attributes)
                )
            else:
                raise ValueError("upsert() requires both ids= and vectors= be set.")
        elif ids is not None and attributes is None:
            # Offset arguments to handle positional arguments case with no data field.
            return await self.async_upsert(
                VectorColumns(ids=data, vectors=ids, attributes=vectors)
            )
        elif isinstance(data, VectorColumns):
            # "if None in data.vectors:" is not supported because data.vectors might be a list of np.ndarray
            # None == pd.ndarray is an ambiguous comparison in this case.
            for vec in data.vectors:
                if vec is None:
                    raise ValueError(
                        "upsert() call would result in a vector deletion, use Namespace.delete([ids...]) instead."
                    )
            response = await self.async_backend.make_api_request(
                "vectors", self.name, payload=data.__dict__
            )

            assert (
                response.get("content", dict()).get("status", "") == "OK"
            ), f"Invalid upsert() response: {response}"
            self.metadata = None  # Invalidate cached metadata
        elif isinstance(data, VectorRow):
            raise ValueError(
                "upsert() should be called on a list of vectors, got single vector."
            )
        elif isinstance(data, list):
            if isinstance(data[0], dict):
                return await self.async_upsert(VectorColumns.from_rows(data))
            elif isinstance(data[0], VectorRow):
                return await self.async_upsert(VectorColumns.from_rows(data))
            elif isinstance(data[0], VectorColumns):
                for columns in data:
                    await self.async_upsert(columns)
                return
            else:
                raise ValueError(f"Unsupported list data type: {type(data[0])}")
        elif isinstance(data, dict):
            if "id" in data:
                raise ValueError(
                    "upsert() should be called on a list of vectors, got single vector."
                )
            elif "ids" in data:
                return await self.async_upsert(VectorColumns.from_dict(data))
            else:
                raise ValueError("Provided dict is missing ids.")
        elif "pandas" in sys.modules and isinstance(
            data, sys.modules["pandas"].DataFrame
        ):
            if "id" not in data.keys():
                raise ValueError("Provided pd.DataFrame is missing an id column.")
            if "vector" not in data.keys():
                raise ValueError("Provided pd.DataFrame is missing a vector column.")
            # start = time.monotonic()
            for i in range(0, len(data), tpuf.upsert_batch_size):
                batch = data[i : i + tpuf.upsert_batch_size]
                attributes = dict()
                for key, values in batch.items():
                    if key != "id" and key != "vector":
                        attributes[key] = values.tolist()
                columns = tpuf.VectorColumns(
                    ids=batch["id"].tolist(),
                    vectors=batch["vector"].transform(lambda x: x.tolist()).tolist(),
                    attributes=attributes,
                )
                # time_diff = time.monotonic() - start
                # print(f"Batch {columns.ids[0]}..{columns.ids[-1]} begin:", time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # before = time.monotonic()
                # print(columns)
                await self.async_upsert(columns)
                # time_diff = time.monotonic() - before
                # print(f"Batch {columns.ids[0]}..{columns.ids[-1]} time:", time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # start = time.monotonic()
            return
        elif isinstance(data, Iterable):
            # start = time.monotonic()
            for batch in batch_iter(data, tpuf.upsert_batch_size):
                # time_diff = time.monotonic() - start
                # print('Batch begin:', time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # before = time.monotonic()
                await self.async_upsert(batch)
                # time_diff = time.monotonic() - before
                # print('Batch time:', time_diff, '/', len(batch), '=', len(batch)/time_diff)
                # start = time.monotonic()
            return
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def delete(self, ids: Union[int, str, List[int], List[str]]) -> None:
        """
        Deletes vectors by id.
        """

        if isinstance(ids, int) or isinstance(ids, str):
            response = self.backend.make_api_request(
                "vectors",
                self.name,
                payload={
                    "ids": [ids],
                    "vectors": [None],
                },
            )
        elif isinstance(ids, list):
            response = self.backend.make_api_request(
                "vectors",
                self.name,
                payload={
                    "ids": ids,
                    "vectors": [None] * len(ids),
                },
            )
        else:
            raise ValueError(f"Unsupported ids type: {type(ids)}")

        assert (
            response.get("content", dict()).get("status", "") == "OK"
        ), f"Invalid delete() response: {response}"
        self.metadata = None  # Invalidate cached metadata

    async def async_delete(self, ids: Union[int, str, List[int], List[str]]) -> None:
        """
        Deletes vectors by id.
        """

        if isinstance(ids, int) or isinstance(ids, str):
            response = await self.async_backend.make_api_request(
                "vectors",
                self.name,
                payload={
                    "ids": [ids],
                    "vectors": [None],
                },
            )
        elif isinstance(ids, list):
            response = await self.async_backend.make_api_request(
                "vectors",
                self.name,
                payload={
                    "ids": ids,
                    "vectors": [None] * len(ids),
                },
            )
        else:
            raise ValueError(f"Unsupported ids type: {type(ids)}")

        assert (
            response.get("content", dict()).get("status", "") == "OK"
        ), f"Invalid delete() response: {response}"
        self.metadata = None  # Invalidate cached metadata

    @overload
    def query(
        self,
        vector: Optional[List[float]] = None,
        distance_metric: Optional[str] = None,
        top_k: int = 10,
        include_vectors: bool = False,
        include_attributes: Optional[Union[List[str], bool]] = None,
        filters: Optional[Dict[str, List[FilterTuple]]] = None,
    ) -> VectorResult: ...

    @overload
    def query(self, query_data: VectorQuery) -> VectorResult: ...

    @overload
    def query(self, query_data: dict) -> VectorResult: ...

    def query(
        self,
        query_data=None,
        vector=None,
        distance_metric=None,
        top_k=None,
        include_vectors=None,
        include_attributes=None,
        filters=None,
    ) -> VectorResult:
        """
        Searches vectors matching the search query.

        See https://turbopuffer.com/docs/reference/query for query filter parameters.
        """

        if query_data is None:
            return self.query(
                VectorQuery(
                    vector=vector,
                    distance_metric=distance_metric,
                    top_k=top_k,
                    include_vectors=include_vectors,
                    include_attributes=include_attributes,
                    filters=filters,
                )
            )
        if not isinstance(query_data, VectorQuery):
            if isinstance(query_data, dict):
                query_data = VectorQuery.from_dict(query_data)
            else:
                raise ValueError(
                    f"query() input type must be compatible with turbopuffer.VectorQuery: {type(query_data)}"
                )

        response = self.backend.make_api_request(
            "vectors", self.name, "query", payload=query_data.__dict__
        )
        result = VectorResult(response.get("content", dict()), namespace=self)
        result.performance = response.get("performance")
        return result

    @overload
    async def async_query(
        self,
        vector: Optional[List[float]] = None,
        distance_metric: Optional[str] = None,
        top_k: int = 10,
        include_vectors: bool = False,
        include_attributes: Optional[Union[List[str], bool]] = None,
        filters: Optional[Dict[str, List[FilterTuple]]] = None,
    ) -> VectorResult: ...

    @overload
    async def async_query(self, query_data: VectorQuery) -> VectorResult: ...

    @overload
    async def async_query(self, query_data: dict) -> VectorResult: ...

    async def async_query(
        self,
        query_data=None,
        vector=None,
        distance_metric=None,
        top_k=None,
        include_vectors=None,
        include_attributes=None,
        filters=None,
    ) -> VectorResult:
        """
        Searches vectors matching the search query.

        See https://turbopuffer.com/docs/reference/query for query filter parameters.
        """

        if query_data is None:
            return await self.async_query(
                VectorQuery(
                    vector=vector,
                    distance_metric=distance_metric,
                    top_k=top_k,
                    include_vectors=include_vectors,
                    include_attributes=include_attributes,
                    filters=filters,
                )
            )
        if not isinstance(query_data, VectorQuery):
            if isinstance(query_data, dict):
                query_data = VectorQuery.from_dict(query_data)
            else:
                raise ValueError(
                    f"query() input type must be compatible with turbopuffer.VectorQuery: {type(query_data)}"
                )

        response = await self.async_backend.make_api_request(
            "vectors", self.name, "query", payload=query_data.__dict__
        )
        result = VectorResult(response.get("content", dict()), namespace=self)
        result.performance = response.get("performance")
        return result

    def vectors(self, cursor: Optional[Cursor] = None) -> VectorResult:
        """
        This function exports the entire dataset at full precision.
        A VectorResult is returned that will lazily load batches of vectors if treated as an Iterator.

        If you want to look up vectors by ID, use the query function with an id filter.
        """

        response = self.backend.make_api_request(
            "vectors", self.name, query={"cursor": cursor}
        )
        content = response.get("content", dict())
        next_cursor = content.pop("next_cursor", None)
        result = VectorResult(content, namespace=self, next_cursor=next_cursor)
        result.performance = response.get("performance")
        return result

    async def async_vectors(self, cursor: Optional[Cursor] = None) -> VectorResult:
        """
        This function exports the entire dataset at full precision.
        A VectorResult is returned that will lazily load batches of vectors if treated as an Iterator.

        If you want to look up vectors by ID, use the query function with an id filter.
        """

        response = await self.async_backend.make_api_request(
            "vectors", self.name, query={"cursor": cursor}
        )
        content = response.get("content", dict())
        next_cursor = content.pop("next_cursor", None)
        result = VectorResult(content, namespace=self, next_cursor=next_cursor)
        result.performance = response.get("performance")
        return result

    def delete_all_indexes(self) -> None:
        """
        Deletes all indexes in a namespace.
        """

        response = self.backend.make_api_request(
            "vectors", self.name, "index", method="DELETE"
        )
        assert (
            response.get("content", dict()).get("status", "") == "ok"
        ), f"Invalid delete_all_indexes() response: {response}"

    async def async_delete_all_indexes(self) -> None:
        """
        Deletes all indexes in a namespace.
        """

        response = await self.async_backend.make_api_request(
            "vectors", self.name, "index", method="DELETE"
        )
        assert (
            response.get("content", dict()).get("status", "") == "ok"
        ), f"Invalid delete_all_indexes() response: {response}"

    def delete_all(self) -> None:
        """
        Deletes all data as well as all indexes.
        """

        response = self.backend.make_api_request("vectors", self.name, method="DELETE")
        assert (
            response.get("content", dict()).get("status", "") == "ok"
        ), f"Invalid delete_all() response: {response}"
        self.metadata = None  # Invalidate cached metadata

    async def async_delete_all(self) -> None:
        """
        Deletes all data as well as all indexes.
        """

        response = await self.async_backend.make_api_request(
            "vectors", self.name, method="DELETE"
        )
        assert (
            response.get("content", dict()).get("status", "") == "ok"
        ), f"Invalid delete_all() response: {response}"
        self.metadata = None  # Invalidate cached metadata

    def recall(self, num=20, top_k=10) -> float:
        """
        This function evaluates the recall performance of ANN queries in this namespace.

        When you call this function, it selects 'num' random vectors that were previously inserted.
        For each of these vectors, it performs an ANN index search as well as a ground truth exhaustive search.

        Recall is calculated as the ratio of matching vectors between the two search results.
        """

        response = self.backend.make_api_request(
            "vectors", self.name, "_debug", "recall", query={"num": num, "top_k": top_k}
        )
        content = response.get("content", dict())
        assert "recall" in content, f"Invalid recall() response: {response}"
        return float(content.get("recall"))

    async def async_recall(self, num=20, top_k=10) -> float:
        """
        This function evaluates the recall performance of ANN queries in this namespace.

        When you call this function, it selects 'num' random vectors that were previously inserted.
        For each of these vectors, it performs an ANN index search as well as a ground truth exhaustive search.

        Recall is calculated as the ratio of matching vectors between the two search results.
        """

        response = await self.async_backend.make_api_request(
            "vectors", self.name, "_debug", "recall", query={"num": num, "top_k": top_k}
        )
        content = response.get("content", dict())
        assert "recall" in content, f"Invalid recall() response: {response}"
        return float(content.get("recall"))


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

    def __init__(
        self,
        backend: Backend,
        initial_set: Union[List[Namespace], List[dict]] = [],
        next_cursor: Optional[Cursor] = None,
    ):
        self.backend = backend
        self.index = -1
        self.offset = 0
        self.next_cursor = next_cursor

        if len(initial_set):
            if isinstance(initial_set[0], Namespace):
                self.namespaces = initial_set
            else:
                self.namespaces = NamespaceIterator.load_namespaces(
                    backend.api_key, initial_set
                )

    def load_namespaces(
        api_key: Optional[str], initial_set: List[dict]
    ) -> List[Namespace]:
        output = []
        for input in initial_set:
            ns = tpuf.Namespace(input["id"], api_key=api_key)
            ns.metadata = {
                "exists": True,
                "dimensions": input["dimensions"],
                "approx_count": input["approx_count"],
                # rfc3339 returned by the server is compatible with iso8601
                "created_at": iso8601.parse_date(input["created_at"]),
            }
            output.append(ns)

        return output

    def __str__(self) -> str:
        str_list = [ns.name for ns in self.namespaces]
        if not self.next_cursor and self.offset == 0:
            return str(str_list)
        else:
            return (
                "NamespaceIterator("
                f"offset={self.offset}, "
                f"next_cursor='{self.next_cursor}', "
                f"namespaces={str_list})"
            )

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

    def __iter__(self) -> "NamespaceIterator":
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
                "vectors", query={"cursor": self.next_cursor}
            )
            content = response.get("content", dict())
            self.offset += len(self.namespaces)
            self.index = -1
            self.next_cursor = content.pop("next_cursor", None)
            self.namespaces = NamespaceIterator.load_namespaces(
                self.backend.api_key, content.pop("namespaces", list())
            )
            return self.__next__()


def namespaces(api_key: Optional[str] = None) -> Iterable[Namespace]:
    """
    Lists all turbopuffer namespaces for a given api_key.
    If no api_key is provided, the globally configured API key will be used.
    """
    backend = Backend(api_key)
    response = backend.make_api_request("vectors")
    content = response.get("content", dict())
    next_cursor = content.pop("next_cursor", None)
    return NamespaceIterator(backend, content.pop("namespaces", list()), next_cursor)
