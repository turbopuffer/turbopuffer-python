# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer.types import (
    NamespaceMetadata,
    NamespaceQueryResponse,
    NamespaceWriteResponse,
    NamespaceRecallResponse,
    NamespaceSchemaResponse,
    NamespaceDeleteAllResponse,
    NamespaceMultiQueryResponse,
    NamespaceExplainQueryResponse,
    NamespaceUpdateSchemaResponse,
    NamespaceHintCacheWarmResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNamespaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete_all(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").delete_all()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete_all(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.delete_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete_all(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.delete_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete_all(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.delete_all()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_explain_query(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").explain_query()
        assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_explain_query_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").explain_query(
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            exclude_attributes=["string"],
            include_attributes=True,
            top_k=0,
            vector_encoding="float",
        )
        assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_explain_query(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.explain_query()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_explain_query(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.explain_query() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_explain_query(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.explain_query()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_hint_cache_warm(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").hint_cache_warm()
        assert_matches_type(NamespaceHintCacheWarmResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_hint_cache_warm(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.hint_cache_warm()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceHintCacheWarmResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_hint_cache_warm(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.hint_cache_warm() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceHintCacheWarmResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_hint_cache_warm(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.hint_cache_warm()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_metadata(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").metadata()
        assert_matches_type(NamespaceMetadata, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_metadata(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.metadata()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceMetadata, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_metadata(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.metadata() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceMetadata, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_metadata(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.metadata()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_multi_query(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").multi_query(
            namespace="namespace",
            queries=[{}],
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_multi_query_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").multi_query(
            namespace="namespace",
            queries=[
                {
                    "distance_metric": "cosine_distance",
                    "exclude_attributes": ["string"],
                    "include_attributes": True,
                    "rank_by": ("id", "asc"),
                    "top_k": 0,
                }
            ],
            consistency={"level": "strong"},
            vector_encoding="float",
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_multi_query(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.multi_query(
            namespace="namespace",
            queries=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_multi_query(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.multi_query(
            namespace="namespace",
            queries=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_multi_query(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("namespace").with_raw_response.multi_query(
                namespace="",
                queries=[{}],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_query(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").query()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_query_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").query(
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            exclude_attributes=["string"],
            include_attributes=True,
            rank_by=("id", "asc"),
            top_k=0,
            vector_encoding="float",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_query(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.query()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_query(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.query() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_query(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.query()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_recall(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").recall()
        assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_recall_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").recall(
            include_ground_truth=True,
            num=0,
            queries=[0],
            top_k=0,
        )
        assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_recall(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.recall()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_recall(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.recall() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_recall(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.recall()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_schema(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").schema()
        assert_matches_type(NamespaceSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_schema(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.schema()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_schema(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.schema() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_schema(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.schema()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_schema(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").update_schema()
        assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_schema_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").update_schema(
            schema={"foo": "string"},
        )
        assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update_schema(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.update_schema()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update_schema(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.update_schema() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update_schema(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.update_schema()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_write(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").write()
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_write_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespace("namespace").write(
            copy_from_namespace="string",
            delete_by_filter_allow_partial=True,
            deletes=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            disable_backpressure=True,
            distance_metric="cosine_distance",
            encryption={"cmek": {"key_name": "key_name"}},
            patch_by_filter={
                "filters": ("name", "Eq", "foo"),
                "patch": {"foo": "bar"},
            },
            patch_by_filter_allow_partial=True,
            patch_columns={
                "id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "vector": [[0]],
            },
            patch_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
            schema={"foo": "string"},
            upsert_columns={
                "id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "vector": [[0]],
            },
            upsert_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
        )
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_write(self, client: Turbopuffer) -> None:
        response = client.namespace("namespace").with_raw_response.write()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_write(self, client: Turbopuffer) -> None:
        with client.namespace("namespace").with_streaming_response.write() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_write(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespace("").with_raw_response.write()


class TestAsyncNamespaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").delete_all()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.delete_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.delete_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.delete_all()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_explain_query(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").explain_query()
        assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_explain_query_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").explain_query(
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            exclude_attributes=["string"],
            include_attributes=True,
            top_k=0,
            vector_encoding="float",
        )
        assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_explain_query(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.explain_query()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_explain_query(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.explain_query() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceExplainQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_explain_query(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.explain_query()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_hint_cache_warm(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").hint_cache_warm()
        assert_matches_type(NamespaceHintCacheWarmResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_hint_cache_warm(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.hint_cache_warm()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceHintCacheWarmResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_hint_cache_warm(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.hint_cache_warm() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceHintCacheWarmResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_hint_cache_warm(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(
            ValueError,
            match=r"Expected a non-empty value for `namespace` but received ''",
        ):
            await async_client.namespace("").with_raw_response.hint_cache_warm()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_metadata(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").metadata()
        assert_matches_type(NamespaceMetadata, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_metadata(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.metadata()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceMetadata, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_metadata(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.metadata() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceMetadata, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_metadata(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.metadata()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").multi_query(
            namespace="namespace",
            queries=[{}],
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_multi_query_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").multi_query(
            namespace="namespace",
            queries=[
                {
                    "distance_metric": "cosine_distance",
                    "exclude_attributes": ["string"],
                    "include_attributes": True,
                    "rank_by": ("id", "asc"),
                    "top_k": 0,
                }
            ],
            consistency={"level": "strong"},
            vector_encoding="float",
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.multi_query(
            namespace="namespace",
            queries=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.multi_query(
            namespace="namespace",
            queries=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("namespace").with_raw_response.multi_query(
                namespace="",
                queries=[{}],
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_query(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").query()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").query(
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            exclude_attributes=["string"],
            include_attributes=True,
            rank_by=("id", "asc"),
            top_k=0,
            vector_encoding="float",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.query()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.query() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_query(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.query()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_recall(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").recall()
        assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_recall_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").recall(
            filters={},
            include_ground_truth=True,
            num=0,
            queries=[0],
            top_k=0,
        )
        assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_recall(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.recall()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_recall(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.recall() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceRecallResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_recall(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.recall()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_schema(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").schema()
        assert_matches_type(NamespaceSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_schema(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.schema()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_schema(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.schema() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_schema(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.schema()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_schema(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").update_schema()
        assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_schema_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").update_schema(
            schema={"foo": "string"},
        )
        assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update_schema(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.update_schema()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update_schema(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.update_schema() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceUpdateSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update_schema(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.update_schema()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_write(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").write()
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_write_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespace("namespace").write(
            copy_from_namespace="string",
            delete_by_filter={},
            delete_by_filter_allow_partial=True,
            delete_condition={},
            deletes=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            disable_backpressure=True,
            distance_metric="cosine_distance",
            encryption={"cmek": {"key_name": "key_name"}},
            patch_by_filter={
                "filters": ("name", "Eq", "foo"),
                "patch": {"foo": "bar"},
            },
            patch_by_filter_allow_partial=True,
            patch_columns={
                "id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "vector": [[0]],
            },
            patch_condition={},
            patch_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
            schema={"foo": "string"},
            upsert_columns={
                "id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "vector": [[0]],
            },
            upsert_condition={},
            upsert_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
        )
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_write(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespace("namespace").with_raw_response.write()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_write(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespace("namespace").with_streaming_response.write() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_write(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespace("").with_raw_response.write()
