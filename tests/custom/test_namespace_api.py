from __future__ import annotations

import os
import json

import httpx2
import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer
from tests.respx2 import MockRouter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "tpuf_A1..."

# Calls in these classes are only type-checked, like the generated mock server tests they replace.
skip_mock_server = pytest.mark.skip(reason="Mock server tests are disabled")


class TestNestedBody:
    @pytest.mark.respx(base_url=base_url)
    def test_branch_from(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v2/namespaces/ns").mock(return_value=httpx2.Response(200, json={}))
        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            client.namespace("ns").branch_from(source_namespace="src", extra_body={"extra": 1})
        assert json.loads(route.calls.last.request.content) == {
            "branch_from_namespace": {"source_namespace": "src"},
            "extra": 1,
        }

    @pytest.mark.respx(base_url=base_url)
    def test_copy_from(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v2/namespaces/ns").mock(return_value=httpx2.Response(200, json={}))
        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            client.namespace("ns").copy_from(source_namespace="src", source_region="gcp-us-central1")
        assert json.loads(route.calls.last.request.content) == {
            "copy_from_namespace": {"source_namespace": "src", "source_region": "gcp-us-central1"},
        }

    @pytest.mark.respx(base_url=base_url)
    def test_start_copy_from(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v2/namespaces/ns/async").mock(return_value=httpx2.Response(200, json={}))
        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            client.namespace("ns").start_copy_from(source_namespace="src")
        assert json.loads(route.calls.last.request.content) == {"copy_from_namespace": {"source_namespace": "src"}}

    @pytest.mark.respx(base_url=base_url)
    async def test_async_copy_from(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v2/namespaces/ns").mock(return_value=httpx2.Response(200, json={}))
        # An httpx2 client so respx can intercept the request, rather than the default aiohttp transport.
        async with AsyncTurbopuffer(base_url=base_url, api_key=api_key, http_client=httpx2.AsyncClient()) as client:
            await client.namespace("ns").copy_from(source_namespace="src")
        assert json.loads(route.calls.last.request.content) == {"copy_from_namespace": {"source_namespace": "src"}}

    @pytest.mark.respx(base_url=base_url)
    def test_other_requests_are_not_nested(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v2/namespaces/ns").mock(return_value=httpx2.Response(200, json={}))
        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            client.namespace("ns").write(copy_from_namespace="src")
        assert json.loads(route.calls.last.request.content) == {"copy_from_namespace": "src"}


class TestNamespaceTypes:
    @skip_mock_server
    def test_query(self, client: Turbopuffer) -> None:
        ns = client.namespace("ns")
        ns.query(
            aggregate_by={"count": ("Count",), "total": ("Sum", "price")},
            filters=("And", [("name", "Eq", "foo"), ("Not", ("price", "Lt", 10))]),
            group_by=["category"],
            rank_by=("vector", "ANN", [0.1, 0.2]),
            top_k=10,
        )
        ns.explain_query(filters=("name", "In", ["a", "b"]), rank_by=("text", "BM25", "quick fox"))
        ns.multi_query(
            queries=[{"rank_by": ("id", "asc"), "filters": ("name", "Eq", "foo"), "top_k": 10}],
            rerank_by=("RRF",),
        )
        ns.query(compute_attributes={"dist": ("vector", "VectorDist", [0.1, 0.2])}, rank_by=("id", "desc"))

    @skip_mock_server
    def test_write(self, client: Turbopuffer) -> None:
        client.namespace("ns").write(
            delete_by_filter=("name", "Eq", "foo"),
            patch_by_filter={"filters": ("name", "Eq", "foo"), "patch": {"price": 1}},
            upsert_condition=("price", "Gt", 1),
        )

    @skip_mock_server
    def test_overloads(self, client: Turbopuffer) -> None:
        ns = client.namespace("ns")
        ns.branch_from(source_namespace="src")
        ns.copy_from(source_namespace="src")
        ns.start_copy_from(source_namespace="src")
        assert ns.exists() in (True, False)
        ns.with_raw_response.query(top_k=1)
        ns.with_streaming_response.query(top_k=1)


class TestAsyncNamespaceTypes:
    @skip_mock_server
    async def test_query(self, async_client: AsyncTurbopuffer) -> None:
        ns = async_client.namespace("ns")
        await ns.query(
            aggregate_by={"count": ("Count",)},
            filters=("name", "Eq", "foo"),
            group_by=[{"tag": ("ForEachUnique", "tags")}],
            rank_by=("text", "BM25", "quick fox"),
            top_k=10,
        )
        await ns.multi_query(queries=[{"rank_by": ("id", "asc")}], rerank_by=("RRF",))

    @skip_mock_server
    async def test_write_and_overloads(self, async_client: AsyncTurbopuffer) -> None:
        ns = async_client.namespace("ns")
        await ns.write(delete_condition=("price", "Lte", 1), patch_condition=("price", "Gte", 1))
        await ns.copy_from(source_namespace="src")
        assert (await ns.exists()) in (True, False)
