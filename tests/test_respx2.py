import httpx2
import pytest

from tests import respx2 as respx
from tests.respx2 import MockRouter


@pytest.mark.parametrize("using", ["httpcore2", "httpx2"])
def test_sync_transport_and_side_effects(using: str) -> None:
    with respx.mock(using=using) as router:
        route = router.get("https://example.test/items").mock(
            side_effect=[httpx2.ConnectError("refused"), httpx2.Response(200, json={"ok": True})]
        )
        with httpx2.Client() as client:
            with pytest.raises(httpx2.ConnectError):
                client.get("https://example.test/items")
            response = client.get("https://example.test/items")

        assert response.json() == {"ok": True}
        assert isinstance(route.calls.last.request, httpx2.Request)
        assert route.call_count == 2


@pytest.mark.parametrize("using", ["httpcore2", "httpx2"])
async def test_async_transport(using: str) -> None:
    with respx.mock(using=using) as router:
        route = router.post("https://example.test/items", json={"name": "test"}).mock(
            return_value=httpx2.Response(201, json={"id": 1})
        )
        async with httpx2.AsyncClient() as client:
            response = await client.post("https://example.test/items", json={"name": "test"})

        assert response.status_code == 201
        assert response.json() == {"id": 1}
        assert isinstance(route.calls.last.response, httpx2.Response)


@pytest.mark.respx(base_url="https://example.test")
def test_fixture_marker_and_unmatched_requests(respx_mock: MockRouter) -> None:
    respx_mock.get("/items").mock(return_value=httpx2.Response(200))
    with httpx2.Client() as client:
        assert client.get("https://example.test/items").status_code == 200
        with pytest.raises(AssertionError, match="not mocked"):
            client.get("https://example.test/unmatched")
