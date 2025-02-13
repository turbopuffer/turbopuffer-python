# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer.types import (
    NamespaceListResponse,
    NamespaceQueryResponse,
    NamespaceUpsertResponse,
    NamespaceRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNamespaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.retrieve(
            "namespace",
        )
        assert_matches_type(NamespaceRetrieveResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.retrieve(
            "namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceRetrieveResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.retrieve(
            "namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceRetrieveResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.list()
        assert_matches_type(NamespaceListResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceListResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceListResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

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
            filters=[{}],
            include_attributes=["string"],
            include_vectors=True,
            rank_by=["string"],
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
    def test_method_upsert_overload_1(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_upsert_with_all_params_overload_1(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
            attributes={"foo": [{}]},
            copy_from_namespace="copy_from_namespace",
            schema={},
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upsert_overload_1(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upsert_overload_1(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_upsert_overload_1(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.upsert(
                namespace="",
                distance_metric="cosine_distance",
                ids=[0],
                vectors=[[0]],
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_upsert_overload_2(self, client: Turbopuffer) -> None:
        namespace = client.namespaces.upsert(
            namespace="namespace",
            upserts=[{"id": 0}],
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upsert_overload_2(self, client: Turbopuffer) -> None:
        response = client.namespaces.with_raw_response.upsert(
            namespace="namespace",
            upserts=[{"id": 0}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = response.parse()
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upsert_overload_2(self, client: Turbopuffer) -> None:
        with client.namespaces.with_streaming_response.upsert(
            namespace="namespace",
            upserts=[{"id": 0}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = response.parse()
            assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_upsert_overload_2(self, client: Turbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.namespaces.with_raw_response.upsert(
                namespace="",
                upserts=[{"id": 0}],
            )


class TestAsyncNamespaces:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.retrieve(
            "namespace",
        )
        assert_matches_type(NamespaceRetrieveResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.retrieve(
            "namespace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceRetrieveResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.retrieve(
            "namespace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceRetrieveResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.list()
        assert_matches_type(NamespaceListResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceListResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceListResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

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
            filters=[{}],
            include_attributes=["string"],
            include_vectors=True,
            rank_by=["string"],
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
    async def test_method_upsert_overload_1(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_upsert_with_all_params_overload_1(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
            attributes={"foo": [{}]},
            copy_from_namespace="copy_from_namespace",
            schema={},
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upsert_overload_1(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upsert_overload_1(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.upsert(
            namespace="namespace",
            distance_metric="cosine_distance",
            ids=[0],
            vectors=[[0]],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_upsert_overload_1(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.upsert(
                namespace="",
                distance_metric="cosine_distance",
                ids=[0],
                vectors=[[0]],
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_upsert_overload_2(self, async_client: AsyncTurbopuffer) -> None:
        namespace = await async_client.namespaces.upsert(
            namespace="namespace",
            upserts=[{"id": 0}],
        )
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upsert_overload_2(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.namespaces.with_raw_response.upsert(
            namespace="namespace",
            upserts=[{"id": 0}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        namespace = await response.parse()
        assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upsert_overload_2(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.namespaces.with_streaming_response.upsert(
            namespace="namespace",
            upserts=[{"id": 0}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            namespace = await response.parse()
            assert_matches_type(NamespaceUpsertResponse, namespace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_upsert_overload_2(self, async_client: AsyncTurbopuffer) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.namespaces.with_raw_response.upsert(
                namespace="",
                upserts=[{"id": 0}],
            )
