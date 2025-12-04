# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ..types import (
    DistanceMetric,
    VectorEncoding,
    namespace_query_params,
    namespace_write_params,
    namespace_recall_params,
    namespace_multi_query_params,
    namespace_explain_query_params,
    namespace_update_schema_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._exceptions import NotFoundError
from .._base_client import make_request_options
from ..types.custom import Filter, RankBy, AggregateBy
from ..types.id_param import IDParam
from ..types.row_param import RowParam
from ..types.query_param import QueryParam
from ..types.columns_param import ColumnsParam
from ..types.distance_metric import DistanceMetric
from ..types.vector_encoding import VectorEncoding
from ..types.namespace_metadata import NamespaceMetadata
from ..types.attribute_schema_param import AttributeSchemaParam
from ..types.include_attributes_param import IncludeAttributesParam
from ..types.namespace_query_response import NamespaceQueryResponse
from ..types.namespace_write_response import NamespaceWriteResponse
from ..types.namespace_recall_response import NamespaceRecallResponse
from ..types.namespace_schema_response import NamespaceSchemaResponse
from ..types.namespace_delete_all_response import NamespaceDeleteAllResponse
from ..types.namespace_multi_query_response import NamespaceMultiQueryResponse
from ..types.namespace_explain_query_response import NamespaceExplainQueryResponse
from ..types.namespace_update_schema_response import NamespaceUpdateSchemaResponse
from ..types.namespace_hint_cache_warm_response import NamespaceHintCacheWarmResponse

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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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

    def explain_query(
        self,
        *,
        namespace: str | None = None,
        aggregate_by: Dict[str, AggregateBy] | Omit = omit,
        consistency: namespace_explain_query_params.Consistency | Omit = omit,
        distance_metric: DistanceMetric | Omit = omit,
        exclude_attributes: SequenceNotStr[str] | Omit = omit,
        filters: Filter | Omit = omit,
        group_by: SequenceNotStr[str] | Omit = omit,
        include_attributes: IncludeAttributesParam | Omit = omit,
        rank_by: RankBy | Omit = omit,
        top_k: int | Omit = omit,
        vector_encoding: VectorEncoding | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceExplainQueryResponse:
        """
        Explain a query plan.

        Args:
          aggregate_by: Aggregations to compute over all documents in the namespace that match the
              filters.

          consistency: The consistency level for a query.

          distance_metric: A function used to calculate vector similarity.

          exclude_attributes: List of attribute names to exclude from the response. All other attributes will
              be included in the response.

          filters: Exact filters for attributes to refine search results for. Think of it as a SQL
              WHERE clause.

          group_by: Groups documents by the specified attributes (the "group key") before computing
              aggregates. Aggregates are computed separately for each group.

          include_attributes: Whether to include attributes in the response.

          rank_by: How to rank the documents in the namespace.

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
            f"/v2/namespaces/{namespace}/explain_query",
            body=maybe_transform(
                {
                    "aggregate_by": aggregate_by,
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "exclude_attributes": exclude_attributes,
                    "filters": filters,
                    "group_by": group_by,
                    "include_attributes": include_attributes,
                    "rank_by": rank_by,
                    "top_k": top_k,
                    "vector_encoding": vector_encoding,
                },
                namespace_explain_query_params.NamespaceExplainQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceExplainQueryResponse,
        )

    def hint_cache_warm(
        self,
        *,
        namespace: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceHintCacheWarmResponse:
        """
        Signal turbopuffer to prepare for low-latency requests.

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
            f"/v1/namespaces/{namespace}/hint_cache_warm",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceHintCacheWarmResponse,
        )

    def metadata(
        self,
        *,
        namespace: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceMetadata:
        """
        Get metadata about a namespace.

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
            f"/v1/namespaces/{namespace}/metadata",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceMetadata,
        )

    def multi_query(
        self,
        *,
        namespace: str | None = None,
        queries: Iterable[QueryParam],
        consistency: namespace_multi_query_params.Consistency | Omit = omit,
        vector_encoding: VectorEncoding | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceMultiQueryResponse:
        """
        Issue multiple concurrent queries filter or search documents.

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
            f"/v2/namespaces/{namespace}/query?stainless_overload=multiQuery",
            body=maybe_transform(
                {
                    "queries": queries,
                    "consistency": consistency,
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
        aggregate_by: Dict[str, AggregateBy] | Omit = omit,
        consistency: namespace_query_params.Consistency | Omit = omit,
        distance_metric: DistanceMetric | Omit = omit,
        exclude_attributes: SequenceNotStr[str] | Omit = omit,
        filters: Filter | Omit = omit,
        group_by: SequenceNotStr[str] | Omit = omit,
        include_attributes: IncludeAttributesParam | Omit = omit,
        rank_by: RankBy | Omit = omit,
        top_k: int | Omit = omit,
        vector_encoding: VectorEncoding | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceQueryResponse:
        """
        Query, filter, full-text search and vector search documents.

        Args:
          aggregate_by: Aggregations to compute over all documents in the namespace that match the
              filters.

          consistency: The consistency level for a query.

          distance_metric: A function used to calculate vector similarity.

          exclude_attributes: List of attribute names to exclude from the response. All other attributes will
              be included in the response.

          filters: Exact filters for attributes to refine search results for. Think of it as a SQL
              WHERE clause.

          group_by: Groups documents by the specified attributes (the "group key") before computing
              aggregates. Aggregates are computed separately for each group.

          include_attributes: Whether to include attributes in the response.

          rank_by: How to rank the documents in the namespace.

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
                    "aggregate_by": aggregate_by,
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "exclude_attributes": exclude_attributes,
                    "filters": filters,
                    "group_by": group_by,
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

    def recall(
        self,
        *,
        namespace: str | None = None,
        filters: object | Omit = omit,
        include_ground_truth: bool | Omit = omit,
        num: int | Omit = omit,
        queries: Iterable[float] | Omit = omit,
        top_k: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceRecallResponse:
        """Evaluate recall.

        Args:
          filters: Filter by attributes.

        Same syntax as the query endpoint.

          include_ground_truth: Include ground truth data (query vectors and true nearest neighbors) in the
              response.

          num: The number of searches to run.

          queries: Use specific query vectors for the measurement. If omitted, sampled from the
              index.

          top_k: Search for `top_k` nearest neighbors.

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
            f"/v1/namespaces/{namespace}/_debug/recall",
            body=maybe_transform(
                {
                    "filters": filters,
                    "include_ground_truth": include_ground_truth,
                    "num": num,
                    "queries": queries,
                    "top_k": top_k,
                },
                namespace_recall_params.NamespaceRecallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceRecallResponse,
        )

    def schema(
        self,
        *,
        namespace: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceSchemaResponse:
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
            cast_to=NamespaceSchemaResponse,
        )

    def exists(self) -> bool:
        """Check whether the namespace exists."""
        try:
            self.schema()
            return True
        except NotFoundError:
            return False

    def update_schema(
        self,
        *,
        namespace: str | None = None,
        schema: Dict[str, AttributeSchemaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceUpdateSchemaResponse:
        """
        Update namespace schema.

        Args:
          schema: The desired schema for the namespace.

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
            f"/v1/namespaces/{namespace}/schema",
            body=maybe_transform(schema, namespace_update_schema_params.NamespaceUpdateSchemaParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceUpdateSchemaResponse,
        )

    def write(
        self,
        *,
        namespace: str | None = None,
        copy_from_namespace: namespace_write_params.CopyFromNamespace | Omit = omit,
        delete_by_filter: Filter | Omit = omit,
        delete_by_filter_allow_partial: bool | Omit = omit,
        delete_condition: Filter | Omit = omit,
        deletes: SequenceNotStr[IDParam] | Omit = omit,
        disable_backpressure: bool | Omit = omit,
        distance_metric: DistanceMetric | Omit = omit,
        encryption: namespace_write_params.Encryption | Omit = omit,
        patch_by_filter: namespace_write_params.PatchByFilter | Omit = omit,
        patch_by_filter_allow_partial: bool | Omit = omit,
        patch_columns: ColumnsParam | Omit = omit,
        patch_condition: Filter | Omit = omit,
        patch_rows: Iterable[RowParam] | Omit = omit,
        schema: Dict[str, AttributeSchemaParam] | Omit = omit,
        upsert_columns: ColumnsParam | Omit = omit,
        upsert_condition: Filter | Omit = omit,
        upsert_rows: Iterable[RowParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceWriteResponse:
        """
        Create, update, or delete documents.

        Args:
          copy_from_namespace: The namespace to copy documents from.

          delete_by_filter: The filter specifying which documents to delete.

          delete_by_filter_allow_partial: Allow partial completion when filter matches too many documents.

          delete_condition: A condition evaluated against the current value of each document targeted by a
              delete write. Only documents that pass the condition are deleted.

          disable_backpressure: Disables write throttling (HTTP 429 responses) during high-volume ingestion.

          distance_metric: A function used to calculate vector similarity.

          encryption: The encryption configuration for a namespace.

          patch_by_filter: The patch and filter specifying which documents to patch.

          patch_by_filter_allow_partial: Allow partial completion when filter matches too many documents.

          patch_columns: A list of documents in columnar format. Each key is a column name, mapped to an
              array of values for that column.

          patch_condition: A condition evaluated against the current value of each document targeted by a
              patch write. Only documents that pass the condition are patched.

          schema: The schema of the attributes attached to the documents.

          upsert_columns: A list of documents in columnar format. Each key is a column name, mapped to an
              array of values for that column.

          upsert_condition: A condition evaluated against the current value of each document targeted by an
              upsert write. Only documents that pass the condition are upserted.

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
                    "delete_by_filter_allow_partial": delete_by_filter_allow_partial,
                    "delete_condition": delete_condition,
                    "deletes": deletes,
                    "disable_backpressure": disable_backpressure,
                    "distance_metric": distance_metric,
                    "encryption": encryption,
                    "patch_by_filter": patch_by_filter,
                    "patch_by_filter_allow_partial": patch_by_filter_allow_partial,
                    "patch_columns": patch_columns,
                    "patch_condition": patch_condition,
                    "patch_rows": patch_rows,
                    "schema": schema,
                    "upsert_columns": upsert_columns,
                    "upsert_condition": upsert_condition,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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

    async def explain_query(
        self,
        *,
        namespace: str | None = None,
        aggregate_by: Dict[str, AggregateBy] | Omit = omit,
        consistency: namespace_explain_query_params.Consistency | Omit = omit,
        distance_metric: DistanceMetric | Omit = omit,
        exclude_attributes: SequenceNotStr[str] | Omit = omit,
        filters: Filter | Omit = omit,
        group_by: SequenceNotStr[str] | Omit = omit,
        include_attributes: IncludeAttributesParam | Omit = omit,
        rank_by: RankBy | Omit = omit,
        top_k: int | Omit = omit,
        vector_encoding: VectorEncoding | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceExplainQueryResponse:
        """
        Explain a query plan.

        Args:
          aggregate_by: Aggregations to compute over all documents in the namespace that match the
              filters.

          consistency: The consistency level for a query.

          distance_metric: A function used to calculate vector similarity.

          exclude_attributes: List of attribute names to exclude from the response. All other attributes will
              be included in the response.

          filters: Exact filters for attributes to refine search results for. Think of it as a SQL
              WHERE clause.

          group_by: Groups documents by the specified attributes (the "group key") before computing
              aggregates. Aggregates are computed separately for each group.

          include_attributes: Whether to include attributes in the response.

          rank_by: How to rank the documents in the namespace.

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
            f"/v2/namespaces/{namespace}/explain_query",
            body=await async_maybe_transform(
                {
                    "aggregate_by": aggregate_by,
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "exclude_attributes": exclude_attributes,
                    "filters": filters,
                    "group_by": group_by,
                    "include_attributes": include_attributes,
                    "rank_by": rank_by,
                    "top_k": top_k,
                    "vector_encoding": vector_encoding,
                },
                namespace_explain_query_params.NamespaceExplainQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceExplainQueryResponse,
        )

    async def hint_cache_warm(
        self,
        *,
        namespace: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceHintCacheWarmResponse:
        """
        Signal turbopuffer to prepare for low-latency requests.

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
            f"/v1/namespaces/{namespace}/hint_cache_warm",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceHintCacheWarmResponse,
        )

    async def metadata(
        self,
        *,
        namespace: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceMetadata:
        """
        Get metadata about a namespace.

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
            f"/v1/namespaces/{namespace}/metadata",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceMetadata,
        )

    async def multi_query(
        self,
        *,
        namespace: str | None = None,
        queries: Iterable[QueryParam],
        consistency: namespace_multi_query_params.Consistency | Omit = omit,
        vector_encoding: VectorEncoding | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceMultiQueryResponse:
        """
        Issue multiple concurrent queries filter or search documents.

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
            f"/v2/namespaces/{namespace}/query?stainless_overload=multiQuery",
            body=await async_maybe_transform(
                {
                    "queries": queries,
                    "consistency": consistency,
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
        aggregate_by: Dict[str, AggregateBy] | Omit = omit,
        consistency: namespace_query_params.Consistency | Omit = omit,
        distance_metric: DistanceMetric | Omit = omit,
        exclude_attributes: SequenceNotStr[str] | Omit = omit,
        filters: Filter | Omit = omit,
        group_by: SequenceNotStr[str] | Omit = omit,
        include_attributes: IncludeAttributesParam | Omit = omit,
        rank_by: RankBy | Omit = omit,
        top_k: int | Omit = omit,
        vector_encoding: VectorEncoding | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceQueryResponse:
        """
        Query, filter, full-text search and vector search documents.

        Args:
          aggregate_by: Aggregations to compute over all documents in the namespace that match the
              filters.

          consistency: The consistency level for a query.

          distance_metric: A function used to calculate vector similarity.

          exclude_attributes: List of attribute names to exclude from the response. All other attributes will
              be included in the response.

          filters: Exact filters for attributes to refine search results for. Think of it as a SQL
              WHERE clause.

          group_by: Groups documents by the specified attributes (the "group key") before computing
              aggregates. Aggregates are computed separately for each group.

          include_attributes: Whether to include attributes in the response.

          rank_by: How to rank the documents in the namespace.

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
                    "aggregate_by": aggregate_by,
                    "consistency": consistency,
                    "distance_metric": distance_metric,
                    "exclude_attributes": exclude_attributes,
                    "filters": filters,
                    "group_by": group_by,
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

    async def recall(
        self,
        *,
        namespace: str | None = None,
        filters: object | Omit = omit,
        include_ground_truth: bool | Omit = omit,
        num: int | Omit = omit,
        queries: Iterable[float] | Omit = omit,
        top_k: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceRecallResponse:
        """Evaluate recall.

        Args:
          filters: Filter by attributes.

        Same syntax as the query endpoint.

          include_ground_truth: Include ground truth data (query vectors and true nearest neighbors) in the
              response.

          num: The number of searches to run.

          queries: Use specific query vectors for the measurement. If omitted, sampled from the
              index.

          top_k: Search for `top_k` nearest neighbors.

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
            f"/v1/namespaces/{namespace}/_debug/recall",
            body=await async_maybe_transform(
                {
                    "filters": filters,
                    "include_ground_truth": include_ground_truth,
                    "num": num,
                    "queries": queries,
                    "top_k": top_k,
                },
                namespace_recall_params.NamespaceRecallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceRecallResponse,
        )

    async def schema(
        self,
        *,
        namespace: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceSchemaResponse:
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
            cast_to=NamespaceSchemaResponse,
        )

    async def exists(self) -> bool:
        """Check whether the namespace exists."""
        try:
            await self.schema()
            return True
        except NotFoundError:
            return False

    async def update_schema(
        self,
        *,
        namespace: str | None = None,
        schema: Dict[str, AttributeSchemaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceUpdateSchemaResponse:
        """
        Update namespace schema.

        Args:
          schema: The desired schema for the namespace.

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
            f"/v1/namespaces/{namespace}/schema",
            body=await async_maybe_transform(schema, namespace_update_schema_params.NamespaceUpdateSchemaParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NamespaceUpdateSchemaResponse,
        )

    async def write(
        self,
        *,
        namespace: str | None = None,
        copy_from_namespace: namespace_write_params.CopyFromNamespace | Omit = omit,
        delete_by_filter: object | Omit = omit,
        delete_by_filter_allow_partial: bool | Omit = omit,
        delete_condition: object | Omit = omit,
        deletes: SequenceNotStr[IDParam] | Omit = omit,
        disable_backpressure: bool | Omit = omit,
        distance_metric: DistanceMetric | Omit = omit,
        encryption: namespace_write_params.Encryption | Omit = omit,
        patch_by_filter: namespace_write_params.PatchByFilter | Omit = omit,
        patch_by_filter_allow_partial: bool | Omit = omit,
        patch_columns: ColumnsParam | Omit = omit,
        patch_condition: object | Omit = omit,
        patch_rows: Iterable[RowParam] | Omit = omit,
        schema: Dict[str, AttributeSchemaParam] | Omit = omit,
        upsert_columns: ColumnsParam | Omit = omit,
        upsert_condition: object | Omit = omit,
        upsert_rows: Iterable[RowParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NamespaceWriteResponse:
        """
        Create, update, or delete documents.

        Args:
          copy_from_namespace: The namespace to copy documents from.

          delete_by_filter: The filter specifying which documents to delete.

          delete_by_filter_allow_partial: Allow partial completion when filter matches too many documents.

          delete_condition: A condition evaluated against the current value of each document targeted by a
              delete write. Only documents that pass the condition are deleted.

          disable_backpressure: Disables write throttling (HTTP 429 responses) during high-volume ingestion.

          distance_metric: A function used to calculate vector similarity.

          encryption: The encryption configuration for a namespace.

          patch_by_filter: The patch and filter specifying which documents to patch.

          patch_by_filter_allow_partial: Allow partial completion when filter matches too many documents.

          patch_columns: A list of documents in columnar format. Each key is a column name, mapped to an
              array of values for that column.

          patch_condition: A condition evaluated against the current value of each document targeted by a
              patch write. Only documents that pass the condition are patched.

          schema: The schema of the attributes attached to the documents.

          upsert_columns: A list of documents in columnar format. Each key is a column name, mapped to an
              array of values for that column.

          upsert_condition: A condition evaluated against the current value of each document targeted by an
              upsert write. Only documents that pass the condition are upserted.

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
                    "delete_by_filter_allow_partial": delete_by_filter_allow_partial,
                    "delete_condition": delete_condition,
                    "deletes": deletes,
                    "disable_backpressure": disable_backpressure,
                    "distance_metric": distance_metric,
                    "encryption": encryption,
                    "patch_by_filter": patch_by_filter,
                    "patch_by_filter_allow_partial": patch_by_filter_allow_partial,
                    "patch_columns": patch_columns,
                    "patch_condition": patch_condition,
                    "patch_rows": patch_rows,
                    "schema": schema,
                    "upsert_columns": upsert_columns,
                    "upsert_condition": upsert_condition,
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
        self.explain_query = to_raw_response_wrapper(
            namespaces.explain_query,
        )
        self.hint_cache_warm = to_raw_response_wrapper(
            namespaces.hint_cache_warm,
        )
        self.metadata = to_raw_response_wrapper(
            namespaces.metadata,
        )
        self.multi_query = to_raw_response_wrapper(
            namespaces.multi_query,
        )
        self.query = to_raw_response_wrapper(
            namespaces.query,
        )
        self.recall = to_raw_response_wrapper(
            namespaces.recall,
        )
        self.schema = to_raw_response_wrapper(
            namespaces.schema,
        )
        self.update_schema = to_raw_response_wrapper(
            namespaces.update_schema,
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
        self.explain_query = async_to_raw_response_wrapper(
            namespaces.explain_query,
        )
        self.hint_cache_warm = async_to_raw_response_wrapper(
            namespaces.hint_cache_warm,
        )
        self.metadata = async_to_raw_response_wrapper(
            namespaces.metadata,
        )
        self.multi_query = async_to_raw_response_wrapper(
            namespaces.multi_query,
        )
        self.query = async_to_raw_response_wrapper(
            namespaces.query,
        )
        self.recall = async_to_raw_response_wrapper(
            namespaces.recall,
        )
        self.schema = async_to_raw_response_wrapper(
            namespaces.schema,
        )
        self.update_schema = async_to_raw_response_wrapper(
            namespaces.update_schema,
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
        self.explain_query = to_streamed_response_wrapper(
            namespaces.explain_query,
        )
        self.hint_cache_warm = to_streamed_response_wrapper(
            namespaces.hint_cache_warm,
        )
        self.metadata = to_streamed_response_wrapper(
            namespaces.metadata,
        )
        self.multi_query = to_streamed_response_wrapper(
            namespaces.multi_query,
        )
        self.query = to_streamed_response_wrapper(
            namespaces.query,
        )
        self.recall = to_streamed_response_wrapper(
            namespaces.recall,
        )
        self.schema = to_streamed_response_wrapper(
            namespaces.schema,
        )
        self.update_schema = to_streamed_response_wrapper(
            namespaces.update_schema,
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
        self.explain_query = async_to_streamed_response_wrapper(
            namespaces.explain_query,
        )
        self.hint_cache_warm = async_to_streamed_response_wrapper(
            namespaces.hint_cache_warm,
        )
        self.metadata = async_to_streamed_response_wrapper(
            namespaces.metadata,
        )
        self.multi_query = async_to_streamed_response_wrapper(
            namespaces.multi_query,
        )
        self.query = async_to_streamed_response_wrapper(
            namespaces.query,
        )
        self.recall = async_to_streamed_response_wrapper(
            namespaces.recall,
        )
        self.schema = async_to_streamed_response_wrapper(
            namespaces.schema,
        )
        self.update_schema = async_to_streamed_response_wrapper(
            namespaces.update_schema,
        )
        self.write = async_to_streamed_response_wrapper(
            namespaces.write,
        )
