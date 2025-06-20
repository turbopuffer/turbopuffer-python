# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer.types import NamespaceSummary
from turbopuffer.pagination import SyncNamespacePage, AsyncNamespacePage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_namespaces(self, client: Turbopuffer) -> None:
        client_ = client.namespaces()
        assert_matches_type(SyncNamespacePage[NamespaceSummary], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_namespaces_with_all_params(self, client: Turbopuffer) -> None:
        client_ = client.namespaces(
            cursor="cursor",
            page_size=1,
            prefix="prefix",
        )
        assert_matches_type(SyncNamespacePage[NamespaceSummary], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_namespaces(self, client: Turbopuffer) -> None:
        response = client.with_raw_response.namespaces()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(SyncNamespacePage[NamespaceSummary], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_namespaces(self, client: Turbopuffer) -> None:
        with client.with_streaming_response.namespaces() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(SyncNamespacePage[NamespaceSummary], client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_namespaces(self, async_client: AsyncTurbopuffer) -> None:
        client = await async_client.namespaces()
        assert_matches_type(AsyncNamespacePage[NamespaceSummary], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_namespaces_with_all_params(self, async_client: AsyncTurbopuffer) -> None:
        client = await async_client.namespaces(
            cursor="cursor",
            page_size=1,
            prefix="prefix",
        )
        assert_matches_type(AsyncNamespacePage[NamespaceSummary], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_namespaces(self, async_client: AsyncTurbopuffer) -> None:
        response = await async_client.with_raw_response.namespaces()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(AsyncNamespacePage[NamespaceSummary], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_namespaces(self, async_client: AsyncTurbopuffer) -> None:
        async with async_client.with_streaming_response.namespaces() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(AsyncNamespacePage[NamespaceSummary], client, path=["response"])

        assert cast(Any, response.is_closed) is True
