import threading
from typing import Iterator
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing_extensions import override

import httpx2
import pytest

from turbopuffer import DefaultHttpxClient, DefaultAioHttpClient, DefaultAsyncHttpxClient


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")

    @override
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture
def local_http_url() -> Iterator[str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_default_sync_client(local_http_url: str) -> None:
    with DefaultHttpxClient() as client:
        response = client.get(local_http_url)
        assert isinstance(response, httpx2.Response)
        assert response.text == "ok"


@pytest.mark.parametrize("client_type", [DefaultAsyncHttpxClient, DefaultAioHttpClient])
async def test_default_async_clients(local_http_url: str, client_type: type[httpx2.AsyncClient]) -> None:
    async with client_type() as client:
        response = await client.get(local_http_url)
        assert isinstance(response, httpx2.Response)
        assert response.text == "ok"
