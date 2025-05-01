# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable

import httpx

from ..types import DistanceMetric, namespace_list_params, namespace_query_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncListNamespaces, AsyncListNamespaces
from .._base_client import AsyncPaginator, make_request_options
from ..types.distance_metric import DistanceMetric
from ..types.namespace_summary import NamespaceSummary
from ..types.namespace_query_response import NamespaceQueryResponse
from ..types.namespace_delete_all_response import NamespaceDeleteAllResponse
from ..types.namespace_get_schema_response import NamespaceGetSchemaResponse

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

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        prefix: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncListNamespaces[NamespaceSummary]:
        """
        List namespaces.

        Args:
          cursor: Retrieve the next page of results.

          page_size: Limit the number of results per page.

          prefix: Retrieve only the namespaces that match the prefix.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/namespaces",
            page=SyncListNamespaces[NamespaceSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "page_size": page_size,
                        "prefix": prefix,
                    },
                    namespace_list_params.NamespaceListParams,
                ),
            ),
            model=NamespaceSummary,
        )

    def delete_all(
        self,
        namespace: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceDeleteAllResponse:
        """
        Delete namespace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._delete(
            f"/v2/namespaces/{namespace}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceDeleteAllResponse,
        )

    def get_schema(
        self,
        namespace: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceGetSchemaResponse:
        """
        Get namespace schema.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._get(
            f"/v1/namespaces/{namespace}/schema",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceGetSchemaResponse,
        )

    def query(
        self,
        namespace: str,
        *,
        consistency: namespace_query_params.Consistency | NotGiven = NOT_GIVEN,
        distance_metric: DistanceMetric | NotGiven = NOT_GIVEN,
        filters: object | NotGiven = NOT_GIVEN,
        include_attributes: Union[bool, List[str]] | NotGiven = NOT_GIVEN,
        include_vectors: bool | NotGiven = NOT_GIVEN,
        rank_by: object | NotGiven = NOT_GIVEN,
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
        Query, filter, full-text search and vector search documents.

        Args:
          consistency: The consistency level for a query.

          distance_metric: A function used to calculate vector similarity.

          filters: Exact filters for attributes to refine search results for. Think of it as a SQL
              WHERE clause.

          include_attributes: Whether to include attributes in the response.

          include_vectors: Whether to return vectors for the search results. Vectors are large and slow to
              deserialize on the client, so use this option only if you need them.

          rank_by: The attribute to rank the results by. Cannot be specified with `vector`.

          top_k: The number of results to return.

          vector: A vector to search for. It must have the same number of dimensions as the
              vectors in the namespace. Cannot be specified with `rank_by`.

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

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        prefix: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[NamespaceSummary, AsyncListNamespaces[NamespaceSummary]]:
        """
        List namespaces.

        Args:
          cursor: Retrieve the next page of results.

          page_size: Limit the number of results per page.

          prefix: Retrieve only the namespaces that match the prefix.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/namespaces",
            page=AsyncListNamespaces[NamespaceSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "page_size": page_size,
                        "prefix": prefix,
                    },
                    namespace_list_params.NamespaceListParams,
                ),
            ),
            model=NamespaceSummary,
        )

    async def delete_all(
        self,
        namespace: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceDeleteAllResponse:
        """
        Delete namespace.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._delete(
            f"/v2/namespaces/{namespace}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceDeleteAllResponse,
        )

    async def get_schema(
        self,
        namespace: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceGetSchemaResponse:
        """
        Get namespace schema.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._get(
            f"/v1/namespaces/{namespace}/schema",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceGetSchemaResponse,
        )

    async def query(
        self,
        namespace: str,
        *,
        consistency: namespace_query_params.Consistency | NotGiven = NOT_GIVEN,
        distance_metric: DistanceMetric | NotGiven = NOT_GIVEN,
        filters: object | NotGiven = NOT_GIVEN,
        include_attributes: Union[bool, List[str]] | NotGiven = NOT_GIVEN,
        include_vectors: bool | NotGiven = NOT_GIVEN,
        rank_by: object | NotGiven = NOT_GIVEN,
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
        Query, filter, full-text search and vector search documents.

        Args:
          consistency: The consistency level for a query.

          distance_metric: A function used to calculate vector similarity.

          filters: Exact filters for attributes to refine search results for. Think of it as a SQL
              WHERE clause.

          include_attributes: Whether to include attributes in the response.

          include_vectors: Whether to return vectors for the search results. Vectors are large and slow to
              deserialize on the client, so use this option only if you need them.

          rank_by: The attribute to rank the results by. Cannot be specified with `vector`.

          top_k: The number of results to return.

          vector: A vector to search for. It must have the same number of dimensions as the
              vectors in the namespace. Cannot be specified with `rank_by`.

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


class NamespacesResourceWithRawResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.list = to_raw_response_wrapper(
            namespaces.list,
        )
        self.delete_all = to_raw_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = to_raw_response_wrapper(
            namespaces.get_schema,
        )
        self.query = to_raw_response_wrapper(
            namespaces.query,
        )


class AsyncNamespacesResourceWithRawResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.list = async_to_raw_response_wrapper(
            namespaces.list,
        )
        self.delete_all = async_to_raw_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = async_to_raw_response_wrapper(
            namespaces.get_schema,
        )
        self.query = async_to_raw_response_wrapper(
            namespaces.query,
        )


class NamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.list = to_streamed_response_wrapper(
            namespaces.list,
        )
        self.delete_all = to_streamed_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = to_streamed_response_wrapper(
            namespaces.get_schema,
        )
        self.query = to_streamed_response_wrapper(
            namespaces.query,
        )


class AsyncNamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.list = async_to_streamed_response_wrapper(
            namespaces.list,
        )
        self.delete_all = async_to_streamed_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = async_to_streamed_response_wrapper(
            namespaces.get_schema,
        )
        self.query = async_to_streamed_response_wrapper(
            namespaces.query,
        )
