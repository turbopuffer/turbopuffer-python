# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer.types import (
    NamespaceQueryResponse,
    NamespaceWriteResponse,
    NamespaceDeleteAllResponse,
    NamespaceGetSchemaResponse,
    NamespaceMultiQueryResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNamespaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_delete_all(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.delete_all(
            namespace="namespace",
        )
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @parametrize
    def test_raw_response_delete_all(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.delete_all(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @parametrize
    def test_streaming_response_delete_all(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.delete_all(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete_all(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.delete_all(
                namespace="",
            )

    @parametrize
    def test_method_get_schema(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.get_schema(
            namespace="namespace",
        )
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @parametrize
    def test_raw_response_get_schema(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.get_schema(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @parametrize
    def test_streaming_response_get_schema(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.get_schema(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_schema(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.get_schema(
                namespace="",
            )

    @parametrize
    def test_method_multi_query(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.multi_query(
            namespace="namespace",
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @parametrize
    def test_method_multi_query_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.multi_query(
            namespace="namespace",
            consistency={"level": "strong"},
            queries=[
                {
                    "distance_metric": "cosine_distance",
                    "filters": {},
                    "include_attributes": True,
                    "rank_by": [{}],
                    "top_k": 0,
                }
            ],
            vector_encoding="float",
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @parametrize
    def test_raw_response_multi_query(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.multi_query(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @parametrize
    def test_streaming_response_multi_query(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.multi_query(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_multi_query(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.multi_query(
                namespace="",
            )

    @parametrize
    def test_method_query(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.query(
            namespace="namespace",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.query(
            namespace="namespace",
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            filters={},
            include_attributes=True,
            rank_by=[{}],
            top_k=0,
            vector_encoding="float",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.query(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

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

    @parametrize
    def test_path_params_query(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.query(
                namespace="",
            )

    @parametrize
    def test_method_write(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.write(
            namespace="namespace",
        )
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @parametrize
    def test_method_write_with_all_params(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.write(
            namespace="namespace",
            copy_from_namespace="copy_from_namespace",
            delete_by_filter={},
            deletes=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            distance_metric="cosine_distance",
            patch_columns={"id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"]},
            patch_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
            schema={
                "foo": {
                    "filterable": True,
                    "full_text_search": True,
                    "type": "string",
                }
            },
            upsert_columns={"id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"]},
            upsert_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
        )
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @parametrize
    def test_raw_response_write(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.write(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @parametrize
    def test_streaming_response_write(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.write(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_write(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.write(
                namespace="",
            )


class TestAsyncNamespaces:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.delete_all(
            namespace="namespace",
        )
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @parametrize
    async def test_raw_response_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.delete_all(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

    @parametrize
    async def test_streaming_response_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.delete_all(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceDeleteAllResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete_all(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.delete_all(
                namespace="",
            )

    @parametrize
    async def test_method_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.get_schema(
            namespace="namespace",
        )
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @parametrize
    async def test_raw_response_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.get_schema(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

    @parametrize
    async def test_streaming_response_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.get_schema(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceGetSchemaResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_schema(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.get_schema(
                namespace="",
            )

    @parametrize
    async def test_method_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.multi_query(
            namespace="namespace",
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @parametrize
    async def test_method_multi_query_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.multi_query(
            namespace="namespace",
            consistency={"level": "strong"},
            queries=[
                {
                    "distance_metric": "cosine_distance",
                    "filters": {},
                    "include_attributes": True,
                    "rank_by": [{}],
                    "top_k": 0,
                }
            ],
            vector_encoding="float",
        )
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @parametrize
    async def test_raw_response_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.multi_query(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

    @parametrize
    async def test_streaming_response_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.multi_query(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceMultiQueryResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_multi_query(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.multi_query(
                namespace="",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.query(
            namespace="namespace",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.query(
            namespace="namespace",
            consistency={"level": "strong"},
            distance_metric="cosine_distance",
            filters={},
            include_attributes=True,
            rank_by=[{}],
            top_k=0,
            vector_encoding="float",
        )
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.query(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceQueryResponse, namespace, path=["response"])

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

    @parametrize
    async def test_path_params_query(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.query(
                namespace="",
            )

    @parametrize
    async def test_method_write(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.write(
            namespace="namespace",
        )
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @parametrize
    async def test_method_write_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.write(
            namespace="namespace",
            copy_from_namespace="copy_from_namespace",
            delete_by_filter={},
            deletes=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            distance_metric="cosine_distance",
            patch_columns={"id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"]},
            patch_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
            schema={
                "foo": {
                    "filterable": True,
                    "full_text_search": True,
                    "type": "string",
                }
            },
            upsert_columns={"id": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"]},
            upsert_rows=[
                {
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "vector": [0],
                }
            ],
        )
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @parametrize
    async def test_raw_response_write(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.write(
            namespace="namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

    @parametrize
    async def test_streaming_response_write(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.write(
            namespace="namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceWriteResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_write(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.write(
                namespace="",
            )
