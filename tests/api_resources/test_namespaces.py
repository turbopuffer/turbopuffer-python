# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer.types import (
    NamespaceSummary,
    NamespaceQueryResponse,
    NamespaceUpsertResponse,
    NamespaceDeleteAllResponse,
    NamespaceGetSchemaResponse,
)
from turbopuffer.pagination import SyncListNamespaces, AsyncListNamespaces

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNamespaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.list()
        assert_matches_type(SyncListNamespaces[NamespaceSummary], namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.list(
            cursor="cursor",
            page_size=1,
            prefix="prefix",
        )
        assert_matches_type(SyncListNamespaces[NamespaceSummary], namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(SyncListNamespaces[NamespaceSummary], namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(SyncListNamespaces[NamespaceSummary], namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_all(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.delete_all(
            "namespace",
        )
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete_all(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.delete_all(
            "namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete_all(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.delete_all(
            "namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete_all(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.delete_all(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_schema(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.get_schema(
            "namespace",
        )
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_schema(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.get_schema(
            "namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_schema(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.get_schema(
            "namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_schema(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.get_schema(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_query(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.query(
            namespace="namespace",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_query_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.query(
            namespace="namespace",
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            filter={},
            include_attributes=True,
            include_vectors=True,
            rank_by={},
            top_k=0,
            vector=[0],
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_query(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.query(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_query(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.query(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_query(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.query(
                namespace="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_upsert(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.upsert(
            namespace="namespace",
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_upsert_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.upsert(
            namespace="namespace",
            documents={
                "attributes": {"foo": [{"foo": "bar"}]},
                "ids": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "vectors": [[0]],
                "distance_metric": "cosine_distance",
                "schema": {
                    "foo": [
                        {
                            "filterable": True,
                            "full_text_search": True,
                            "type": "string",
                        }
                    ]
                },
            },
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upsert(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.upsert(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upsert(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.upsert(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_upsert(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.upsert(
                namespace="",
            )


class TestAsyncNamespaces:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.list()
        assert_matches_type(AsyncListNamespaces[NamespaceSummary], namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.list(
            cursor="cursor",
            page_size=1,
            prefix="prefix",
        )
        assert_matches_type(AsyncListNamespaces[NamespaceSummary], namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(AsyncListNamespaces[NamespaceSummary], namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(AsyncListNamespaces[NamespaceSummary], namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.delete_all(
            "namespace",
        )
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.delete_all(
            "namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.delete_all(
            "namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.delete_all(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.get_schema(
            "namespace",
        )
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.get_schema(
            "namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.get_schema(
            "namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.get_schema(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_query(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.query(
            namespace="namespace",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.query(
            namespace="namespace",
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            filter={},
            include_attributes=True,
            include_vectors=True,
            rank_by={},
            top_k=0,
            vector=[0],
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.query(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.query(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_query(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.query(
                namespace="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_upsert(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.upsert(
            namespace="namespace",
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_upsert_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.upsert(
            namespace="namespace",
            documents={
                "attributes": {"foo": [{"foo": "bar"}]},
                "ids": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "vectors": [[0]],
                "distance_metric": "cosine_distance",
                "schema": {
                    "foo": [
                        {
                            "filterable": True,
                            "full_text_search": True,
                            "type": "string",
                        }
                    ]
                },
            },
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upsert(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.upsert(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upsert(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.upsert(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_upsert(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.upsert(
                namespace="",
            )
