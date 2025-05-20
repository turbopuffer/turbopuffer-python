# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal

import httpx

from ..types import (
    DistanceMetric,
    namespace_query_params,
    namespace_write_params,
    namespace_multi_query_params,
)
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
from .._base_client import make_request_options
from ..types.id_param import IDParam
from ..types.distance_metric import DistanceMetric
from ..types.document_row_param import DocumentRowParam
from ..types.attribute_schema_param import AttributeSchemaParam
from ..types.document_columns_param import DocumentColumnsParam
from ..types.namespace_query_response import NamespaceQueryResponse
from ..types.namespace_write_response import NamespaceWriteResponse
from ..types.namespace_delete_all_response import NamespaceDeleteAllResponse
from ..types.namespace_get_schema_response import NamespaceGetSchemaResponse
from ..types.namespace_multi_query_response import NamespaceMultiQueryResponse

__all__ = ["NamespacesResource", "AsyncNamespacesResource"]


class NamespacesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NamespacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/turbopuffer/turbopuffer-python#accessing-raw-response-data-eg-headers
        """
        return NamespacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NamespacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/turbopuffer/turbopuffer-python#with_streaming_response
        """
        return NamespacesResourceWithStreamingResponse(self)

    def delete_all(
        self,
        *,
        namespace: str | None = None,
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
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
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
        *,
        namespace: str | None = None,
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
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._get(
            f"/v1/namespaces/{namespace}/schema",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceGetSchemaResponse,
        )

    def multi_query(
        self,
        *,
        namespace: str | None = None,
        consistency: namespace_multi_query_params.Consistency | NotGiven = NOT_GIVEN,
        queries: Iterable[namespace_multi_query_params.Query] | NotGiven = NOT_GIVEN,
        vector_encoding: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceMultiQueryResponse:
        """
        Send multiple queries at once.

        Args:
          consistency: The consistency level for a query.

          vector_encoding: The encoding to use for vectors in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._post(
            f"/v2/namespaces/{namespace}/query?overload=multi",
            body=maybe_transform(
                {
                    "consistency": consistency,
                    "queries": queries,
                    "vector_encoding": vector_encoding,
                },
                namespace_multi_query_params.NamespaceMultiQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceMultiQueryResponse,
        )

    def query(
        self,
        *,
        namespace: str | None = None,
        consistency: namespace_query_params.Consistency | NotGiven = NOT_GIVEN,
        distance_metric: DistanceMetric | NotGiven = NOT_GIVEN,
        filters: object | NotGiven = NOT_GIVEN,
        include_attributes: Union[bool, List[str]] | NotGiven = NOT_GIVEN,
        rank_by: object | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        vector_encoding: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
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

          include_attributes: Whether to include attributes in the response.

          top_k: The number of results to return.

          vector_encoding: The encoding to use for vectors in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._post(
            f"/v2/namespaces/{namespace}/query",
            body=maybe_transform(
                {
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "filters": filters,
                    "include_attributes": include_attributes,
                    "rank_by": rank_by,
                    "top_k": top_k,
                    "vector_encoding": vector_encoding,
                },
                namespace_query_params.NamespaceQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceQueryResponse,
        )

    def write(
        self,
        *,
        namespace: str | None = None,
        copy_from_namespace: str | NotGiven = NOT_GIVEN,
        delete_by_filter: object | NotGiven = NOT_GIVEN,
        deletes: List[IDParam] | NotGiven = NOT_GIVEN,
        distance_metric: DistanceMetric | NotGiven = NOT_GIVEN,
        patch_columns: DocumentColumnsParam | NotGiven = NOT_GIVEN,
        patch_rows: Iterable[DocumentRowParam] | NotGiven = NOT_GIVEN,
        schema: Dict[str, AttributeSchemaParam] | NotGiven = NOT_GIVEN,
        upsert_columns: DocumentColumnsParam | NotGiven = NOT_GIVEN,
        upsert_rows: Iterable[DocumentRowParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceWriteResponse:
        """
        Create, update, or delete documents.

        Args:
          copy_from_namespace: The namespace to copy documents from.

          delete_by_filter: The filter specifying which documents to delete.

          distance_metric: A function used to calculate vector similarity.

          patch_columns: A list of documents in columnar format. The keys are the column names.

          schema: The schema of the attributes attached to the documents.

          upsert_columns: A list of documents in columnar format. The keys are the column names.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return self._post(
            f"/v2/namespaces/{namespace}",
            body=maybe_transform(
                {
                    "copy_from_namespace": copy_from_namespace,
                    "delete_by_filter": delete_by_filter,
                    "deletes": deletes,
                    "distance_metric": distance_metric,
                    "patch_columns": patch_columns,
                    "patch_rows": patch_rows,
                    "schema": schema,
                    "upsert_columns": upsert_columns,
                    "upsert_rows": upsert_rows,
                },
                namespace_write_params.NamespaceWriteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceWriteResponse,
        )


class AsyncNamespacesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNamespacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/turbopuffer/turbopuffer-python#accessing-raw-response-data-eg-headers
        """
        return AsyncNamespacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNamespacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/turbopuffer/turbopuffer-python#with_streaming_response
        """
        return AsyncNamespacesResourceWithStreamingResponse(self)

    async def delete_all(
        self,
        *,
        namespace: str | None = None,
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
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
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
        *,
        namespace: str | None = None,
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
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._get(
            f"/v1/namespaces/{namespace}/schema",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceGetSchemaResponse,
        )

    async def multi_query(
        self,
        *,
        namespace: str | None = None,
        consistency: namespace_multi_query_params.Consistency | NotGiven = NOT_GIVEN,
        queries: Iterable[namespace_multi_query_params.Query] | NotGiven = NOT_GIVEN,
        vector_encoding: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceMultiQueryResponse:
        """
        Send multiple queries at once.

        Args:
          consistency: The consistency level for a query.

          vector_encoding: The encoding to use for vectors in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._post(
            f"/v2/namespaces/{namespace}/query?overload=multi",
            body=await async_maybe_transform(
                {
                    "consistency": consistency,
                    "queries": queries,
                    "vector_encoding": vector_encoding,
                },
                namespace_multi_query_params.NamespaceMultiQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceMultiQueryResponse,
        )

    async def query(
        self,
        *,
        namespace: str | None = None,
        consistency: namespace_query_params.Consistency | NotGiven = NOT_GIVEN,
        distance_metric: DistanceMetric | NotGiven = NOT_GIVEN,
        filters: object | NotGiven = NOT_GIVEN,
        include_attributes: Union[bool, List[str]] | NotGiven = NOT_GIVEN,
        rank_by: object | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        vector_encoding: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
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

          include_attributes: Whether to include attributes in the response.

          top_k: The number of results to return.

          vector_encoding: The encoding to use for vectors in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._post(
            f"/v2/namespaces/{namespace}/query",
            body=await async_maybe_transform(
                {
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "filters": filters,
                    "include_attributes": include_attributes,
                    "rank_by": rank_by,
                    "top_k": top_k,
                    "vector_encoding": vector_encoding,
                },
                namespace_query_params.NamespaceQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceQueryResponse,
        )

    async def write(
        self,
        *,
        namespace: str | None = None,
        copy_from_namespace: str | NotGiven = NOT_GIVEN,
        delete_by_filter: object | NotGiven = NOT_GIVEN,
        deletes: List[IDParam] | NotGiven = NOT_GIVEN,
        distance_metric: DistanceMetric | NotGiven = NOT_GIVEN,
        patch_columns: DocumentColumnsParam | NotGiven = NOT_GIVEN,
        patch_rows: Iterable[DocumentRowParam] | NotGiven = NOT_GIVEN,
        schema: Dict[str, AttributeSchemaParam] | NotGiven = NOT_GIVEN,
        upsert_columns: DocumentColumnsParam | NotGiven = NOT_GIVEN,
        upsert_rows: Iterable[DocumentRowParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NamespaceWriteResponse:
        """
        Create, update, or delete documents.

        Args:
          copy_from_namespace: The namespace to copy documents from.

          delete_by_filter: The filter specifying which documents to delete.

          distance_metric: A function used to calculate vector similarity.

          patch_columns: A list of documents in columnar format. The keys are the column names.

          schema: The schema of the attributes attached to the documents.

          upsert_columns: A list of documents in columnar format. The keys are the column names.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_default_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        return await self._post(
            f"/v2/namespaces/{namespace}",
            body=await async_maybe_transform(
                {
                    "copy_from_namespace": copy_from_namespace,
                    "delete_by_filter": delete_by_filter,
                    "deletes": deletes,
                    "distance_metric": distance_metric,
                    "patch_columns": patch_columns,
                    "patch_rows": patch_rows,
                    "schema": schema,
                    "upsert_columns": upsert_columns,
                    "upsert_rows": upsert_rows,
                },
                namespace_write_params.NamespaceWriteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceWriteResponse,
        )


class NamespacesResourceWithRawResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.delete_all = to_raw_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = to_raw_response_wrapper(
            namespaces.get_schema,
        )
        self.multi_query = to_raw_response_wrapper(
            namespaces.multi_query,
        )
        self.query = to_raw_response_wrapper(
            namespaces.query,
        )
        self.write = to_raw_response_wrapper(
            namespaces.write,
        )


class AsyncNamespacesResourceWithRawResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.delete_all = async_to_raw_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = async_to_raw_response_wrapper(
            namespaces.get_schema,
        )
        self.multi_query = async_to_raw_response_wrapper(
            namespaces.multi_query,
        )
        self.query = async_to_raw_response_wrapper(
            namespaces.query,
        )
        self.write = async_to_raw_response_wrapper(
            namespaces.write,
        )


class NamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: NamespacesResource) -> None:
        self._namespaces = namespaces

        self.delete_all = to_streamed_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = to_streamed_response_wrapper(
            namespaces.get_schema,
        )
        self.multi_query = to_streamed_response_wrapper(
            namespaces.multi_query,
        )
        self.query = to_streamed_response_wrapper(
            namespaces.query,
        )
        self.write = to_streamed_response_wrapper(
            namespaces.write,
        )


class AsyncNamespacesResourceWithStreamingResponse:
    def __init__(self, namespaces: AsyncNamespacesResource) -> None:
        self._namespaces = namespaces

        self.delete_all = async_to_streamed_response_wrapper(
            namespaces.delete_all,
        )
        self.get_schema = async_to_streamed_response_wrapper(
            namespaces.get_schema,
        )
        self.multi_query = async_to_streamed_response_wrapper(
            namespaces.multi_query,
        )
        self.query = async_to_streamed_response_wrapper(
            namespaces.query,
        )
        self.write = async_to_streamed_response_wrapper(
            namespaces.write,
        )
