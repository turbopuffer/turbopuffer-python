# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, overload

import httpx

from ..types import namespace_query_params, namespace_upsert_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.namespace_list_response import NamespaceListResponse
from ..types.namespace_query_response import NamespaceQueryResponse
from ..types.namespace_upsert_response import NamespaceUpsertResponse
from ..types.namespace_retrieve_response import NamespaceRetrieveResponse

__all__ = ["NamespacesResource", "AsyncNamespacesResource"]


class NamespacesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NamespacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/turbopuffer-python#accessing-raw-response-data-eg-headers
        """
        return NamespacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NamespacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/turbopuffer-python#with_streaming_response
        """
        return NamespacesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        namespace: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceRetrieveResponse:
        """
        Retrieve metadata for a specific namespace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._get(
            f"/v1/namespaces/{namespace}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceRetrieveResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceListResponse:
        """Retrieve a list of all namespaces."""
        return self._get(
            "/v1/namespaces",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceListResponse,
        )

    def query(
        self,
        namespace: str,
        *,
        consistency: namespace_query_params.Consistency | NotGiven = NOT_GIVEN,
        distance_metric: Literal["cosine_distance", "euclidean_squared"] | NotGiven = NOT_GIVEN,
        filters: Union[Iterable[object], object] | NotGiven = NOT_GIVEN,
        include_attributes: Union[List[str], bool] | NotGiven = NOT_GIVEN,
        include_vectors: bool | NotGiven = NOT_GIVEN,
        rank_by: List[str] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        vector: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceQueryResponse:
        """
        Searches documents in a namespace using a vector (and optionally attribute
        filters). Provide a query vector, filters, ranking, and other parameters to
        retrieve matching documents.

        Args:
          consistency: Consistency level for the query.

          distance_metric: Required if a query vector is provided.

          filters: Filters to narrow down search results (e.g., attribute conditions).

          include_attributes: A list of attribute names to return or `true` to include all attributes.

          include_vectors: Whether to include the stored vectors in the response.

          rank_by: Parameter to order results (either BM25 for full-text search or attribute-based
              ordering).

          top_k: Number of results to return.

          vector: The query vector.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._post(
            f"/v1/namespaces/{namespace}/query",
            body=maybe_transform(
                {
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "filters": filters,
                    "include_attributes": include_attributes,
                    "include_vectors": include_vectors,
                    "rank_by": rank_by,
                    "top_k": top_k,
                    "vector": vector,
                },
                namespace_query_params.NamespaceQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceQueryResponse,
        )

    @overload
    def upsert(
        self,
        namespace: str,
        *,
        distance_metric: Literal["cosine_distance", "euclidean_squared"],
        ids: List[Union[int, str]],
        vectors: Iterable[Optional[Iterable[float]]],
        attributes: Dict[str, Iterable[object]] | NotGiven = NOT_GIVEN,
        copy_from_namespace: str | NotGiven = NOT_GIVEN,
        schema: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceUpsertResponse:
        """Creates, updates, or deletes documents in a namespace.

        Documents are upserted in
        a column-oriented format (using `ids`, `vectors`, `attributes`, etc.) or in a
        row-based format (using `upserts`). To delete a document, send a `null` vector.

        Args:
          distance_metric: The function used to calculate vector similarity.

          ids: Array of document IDs (unsigned 64-bit integers, UUIDs, or strings).

          vectors: Array of vectors. Each vector is an array of numbers. Use `null` to delete a
              document.

          attributes: Object mapping attribute names to arrays of attribute values.

          copy_from_namespace: Copy all documents from another namespace into this one.

          schema: Manually specify the schema for the documents.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def upsert(
        self,
        namespace: str,
        *,
        upserts: Iterable[namespace_upsert_params.Variant1Upsert],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceUpsertResponse:
        """Creates, updates, or deletes documents in a namespace.

        Documents are upserted in
        a column-oriented format (using `ids`, `vectors`, `attributes`, etc.) or in a
        row-based format (using `upserts`). To delete a document, send a `null` vector.

        Args:
          upserts: Array of document operations in row-based format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["distance_metric", "ids", "vectors"], ["upserts"])
    def upsert(
        self,
        namespace: str,
        *,
        distance_metric: Literal["cosine_distance", "euclidean_squared"] | NotGiven = NOT_GIVEN,
        ids: List[Union[int, str]] | NotGiven = NOT_GIVEN,
        vectors: Iterable[Optional[Iterable[float]]] | NotGiven = NOT_GIVEN,
        attributes: Dict[str, Iterable[object]] | NotGiven = NOT_GIVEN,
        copy_from_namespace: str | NotGiven = NOT_GIVEN,
        schema: object | NotGiven = NOT_GIVEN,
        upserts: Iterable[namespace_upsert_params.Variant1Upsert] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceUpsertResponse:
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._post(
            f"/v1/namespaces/{namespace}",
            body=maybe_transform(
                {
                    "distance_metric": distance_metric,
                    "ids": ids,
                    "vectors": vectors,
                    "attributes": attributes,
                    "copy_from_namespace": copy_from_namespace,
                    "schema": schema,
                    "upserts": upserts,
                },
                namespace_upsert_params.NamespaceUpsertParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceUpsertResponse,
        )


class AsyncNamespacesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNamespacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/turbopuffer-python#accessing-raw-response-data-eg-headers
        """
        return AsyncNamespacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNamespacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/turbopuffer-python#with_streaming_response
        """
        return AsyncNamespacesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        namespace: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceRetrieveResponse:
        """
        Retrieve metadata for a specific namespace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._get(
            f"/v1/namespaces/{namespace}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceRetrieveResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceListResponse:
        """Retrieve a list of all namespaces."""
        return await self._get(
            "/v1/namespaces",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceListResponse,
        )

    async def query(
        self,
        namespace: str,
        *,
        consistency: namespace_query_params.Consistency | NotGiven = NOT_GIVEN,
        distance_metric: Literal["cosine_distance", "euclidean_squared"] | NotGiven = NOT_GIVEN,
        filters: Union[Iterable[object], object] | NotGiven = NOT_GIVEN,
        include_attributes: Union[List[str], bool] | NotGiven = NOT_GIVEN,
        include_vectors: bool | NotGiven = NOT_GIVEN,
        rank_by: List[str] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        vector: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceQueryResponse:
        """
        Searches documents in a namespace using a vector (and optionally attribute
        filters). Provide a query vector, filters, ranking, and other parameters to
        retrieve matching documents.

        Args:
          consistency: Consistency level for the query.

          distance_metric: Required if a query vector is provided.

          filters: Filters to narrow down search results (e.g., attribute conditions).

          include_attributes: A list of attribute names to return or `true` to include all attributes.

          include_vectors: Whether to include the stored vectors in the response.

          rank_by: Parameter to order results (either BM25 for full-text search or attribute-based
              ordering).

          top_k: Number of results to return.

          vector: The query vector.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._post(
            f"/v1/namespaces/{namespace}/query",
            body=await async_maybe_transform(
                {
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "filters": filters,
                    "include_attributes": include_attributes,
                    "include_vectors": include_vectors,
                    "rank_by": rank_by,
                    "top_k": top_k,
                    "vector": vector,
                },
                namespace_query_params.NamespaceQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceQueryResponse,
        )

    @overload
    async def upsert(
        self,
        namespace: str,
        *,
        distance_metric: Literal["cosine_distance", "euclidean_squared"],
        ids: List[Union[int, str]],
        vectors: Iterable[Optional[Iterable[float]]],
        attributes: Dict[str, Iterable[object]] | NotGiven = NOT_GIVEN,
        copy_from_namespace: str | NotGiven = NOT_GIVEN,
        schema: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceUpsertResponse:
        """Creates, updates, or deletes documents in a namespace.

        Documents are upserted in
        a column-oriented format (using `ids`, `vectors`, `attributes`, etc.) or in a
        row-based format (using `upserts`). To delete a document, send a `null` vector.

        Args:
          distance_metric: The function used to calculate vector similarity.

          ids: Array of document IDs (unsigned 64-bit integers, UUIDs, or strings).

          vectors: Array of vectors. Each vector is an array of numbers. Use `null` to delete a
              document.

          attributes: Object mapping attribute names to arrays of attribute values.

          copy_from_namespace: Copy all documents from another namespace into this one.

          schema: Manually specify the schema for the documents.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def upsert(
        self,
        namespace: str,
        *,
        upserts: Iterable[namespace_upsert_params.Variant1Upsert],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceUpsertResponse:
        """Creates, updates, or deletes documents in a namespace.

        Documents are upserted in
        a column-oriented format (using `ids`, `vectors`, `attributes`, etc.) or in a
        row-based format (using `upserts`). To delete a document, send a `null` vector.

        Args:
          upserts: Array of document operations in row-based format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["distance_metric", "ids", "vectors"], ["upserts"])
    async def upsert(
        self,
        namespace: str,
        *,
        distance_metric: Literal["cosine_distance", "euclidean_squared"] | NotGiven = NOT_GIVEN,
        ids: List[Union[int, str]] | NotGiven = NOT_GIVEN,
        vectors: Iterable[Optional[Iterable[float]]] | NotGiven = NOT_GIVEN,
        attributes: Dict[str, Iterable[object]] | NotGiven = NOT_GIVEN,
        copy_from_namespace: str | NotGiven = NOT_GIVEN,
        schema: object | NotGiven = NOT_GIVEN,
        upserts: Iterable[namespace_upsert_params.Variant1Upsert] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceUpsertResponse:
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._post(
            f"/v1/namespaces/{namespace}",
            body=await async_maybe_transform(
                {
                    "distance_metric": distance_metric,
                    "ids": ids,
                    "vectors": vectors,
                    "attributes": attributes,
                    "copy_from_namespace": copy_from_namespace,
                    "schema": schema,
                    "upserts": upserts,
                },
                namespace_upsert_params.NamespaceUpsertParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceUpsertResponse,
        )


class NamespacesResourceWithRawResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.retrieve = to_raw_response_wrapper(
            namespaces.retrieve,
        )
        self.list = to_raw_response_wrapper(
            namespaces.list,
        )
        self.query = to_raw_response_wrapper(
            namespaces.query,
        )
        self.upsert = to_raw_response_wrapper(
            namespaces.upsert,
        )


class AsyncNamespacesResourceWithRawResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.retrieve = async_to_raw_response_wrapper(
            namespaces.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            namespaces.list,
        )
        self.query = async_to_raw_response_wrapper(
            namespaces.query,
        )
        self.upsert = async_to_raw_response_wrapper(
            namespaces.upsert,
        )


class NamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.retrieve = to_streamed_response_wrapper(
            namespaces.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            namespaces.list,
        )
        self.query = to_streamed_response_wrapper(
            namespaces.query,
        )
        self.upsert = to_streamed_response_wrapper(
            namespaces.upsert,
        )


class AsyncNamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.retrieve = async_to_streamed_response_wrapper(
            namespaces.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            namespaces.list,
        )
        self.query = async_to_streamed_response_wrapper(
            namespaces.query,
        )
        self.upsert = async_to_streamed_response_wrapper(
            namespaces.upsert,
        )
