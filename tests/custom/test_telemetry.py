from __future__ import annotations

import json
import logging
import threading
from typing import Any, Dict, List, Iterator, Optional, cast
from unittest import mock
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing_extensions import override

import httpx
import pytest
from respx import Route, MockRouter

from turbopuffer import (
    Turbopuffer,
    APIStatusError,
    APITimeoutError,
    AsyncTurbopuffer,
    APIConnectionError,
    DefaultAsyncHttpxClient,
)
from tests.conftest import api_key, base_url
from turbopuffer.lib import telemetry
from turbopuffer.lib.telemetry import (
    TELEMETRY_HEADER,
    TELEMETRY_ENV_VAR,
    SAMPLE_RATE_HEADER,
    MAX_BUFFERED_RECORDS,
    MAX_RECORDS_PER_HEADER,
    TelemetryBuffer,
    route_template,
    resolve_enabled,
)
from turbopuffer.lib.performance import compute_durations, connection_reused

QUERY_PATH = "/v2/namespaces/my-ns/query"
QUERY_ROUTE = "POST /v2/namespaces/{ns}/query"


def query_response(*, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "rows": [],
            "performance": {
                "approx_namespace_size": 1,
                "cache_hit_ratio": 1.0,
                "cache_temperature": "hot",
                "exhaustive_search_count": 0,
                "query_execution_ms": 5,
                "server_total_ms": 7,
            },
        },
        headers=headers,
    )


def sent_requests(route: Route) -> List[httpx.Request]:
    calls = cast(List[Any], route.calls)
    return [call.request for call in calls]


def sent_records(request: httpx.Request) -> Optional[List[Dict[str, Any]]]:
    value = request.headers.get(TELEMETRY_HEADER)
    if value is None:
        return None
    payload = json.loads(value)
    assert payload["version"] == 1
    return payload["records"]


def take_payload(buffer: TelemetryBuffer) -> Dict[str, Any]:
    batch = buffer.take()
    assert batch is not None
    return json.loads(batch.header)


def add_record(buffer: TelemetryBuffer, *, status: int = 200) -> None:
    buffer.record(
        method="post",
        url=QUERY_PATH,
        status=status,
        retries=0,
        durations={"total": 5_000_000},
    )


def no_retry_delay(*_args: Any, **_kwargs: Any) -> float:
    return 0.0


@pytest.fixture(autouse=True)
def clear_shared_buffers() -> None:
    # Clients from earlier tests may not be garbage collected yet, and would share their buffer.
    telemetry._shared_buffers.clear()


class QueryHandler(BaseHTTPRequestHandler):
    # Keeps connections open between requests, so they can be reused.
    protocol_version = "HTTP/1.1"

    def do_POST(self) -> None:
        self.rfile.read(int(self.headers["Content-Length"]))
        body = query_response().content
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @override
    def log_message(self, format: str, *args: Any) -> None:
        pass


@pytest.fixture(scope="module")
def local_server() -> Iterator[str]:
    """A real server, since mocked transports never open connections to trace."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), QueryHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def assert_connection_phases(first: Dict[str, Any], second: Dict[str, Any]) -> None:
    assert first["reused"] is False
    assert "connect_us" in first
    assert second["reused"] is True
    assert "connect_us" not in second
    for record in (first, second):
        for key in ("pool_us", "send_us", "wait_us"):
            assert isinstance(record[key], int) and record[key] >= 0, key
        assert record["wait_us"] <= record["total_us"]


@pytest.fixture
def telemetry_client() -> Iterator[Turbopuffer]:
    with Turbopuffer(base_url=base_url, api_key=api_key, telemetry=True) as client:
        yield client


class TestResolveEnabled:
    def test_disabled_by_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(TELEMETRY_ENV_VAR, raising=False)
        assert resolve_enabled(None) is False

        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            assert client._telemetry is None

    @pytest.mark.parametrize(
        ("value", "expected"),
        [("1", True), ("true", True), (" ON ", True), ("yes", True), ("0", False), ("false", False), ("", False)],
    )
    def test_env_var(self, monkeypatch: pytest.MonkeyPatch, value: str, expected: bool) -> None:
        monkeypatch.setenv(TELEMETRY_ENV_VAR, value)
        assert resolve_enabled(None) is expected

    def test_env_var_enables_client(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(TELEMETRY_ENV_VAR, "1")
        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            assert client._telemetry is not None

    def test_invalid_env_var_warns_and_disables(
        self, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        monkeypatch.setenv(TELEMETRY_ENV_VAR, "sometimes")
        with caplog.at_level(logging.WARNING, logger=telemetry.__name__):
            assert resolve_enabled(None) is False
        assert TELEMETRY_ENV_VAR in caplog.text

    def test_explicit_value_beats_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(TELEMETRY_ENV_VAR, "1")
        assert resolve_enabled(False) is False
        monkeypatch.setenv(TELEMETRY_ENV_VAR, "0")
        assert resolve_enabled(True) is True


class TestRouteTemplate:
    @pytest.mark.parametrize(
        ("method", "url", "expected"),
        [
            ("post", "/v2/namespaces/my-ns/query", QUERY_ROUTE),
            (
                "post",
                "/v2/namespaces/my-ns/query?stainless_overload=multiQuery",
                "POST /v2/namespaces/{ns}/query?stainless_overload=multiQuery",
            ),
            ("post", "/v2/namespaces/my%2Fns", "POST /v2/namespaces/{ns}"),
            ("get", "/v1/namespaces", "GET /v1/namespaces"),
            (
                "get",
                "/v1/namespaces/my-ns/operations/abc123?stainless_overload=pollCopyFrom",
                "GET /v1/namespaces/{ns}/operations/{token}?stainless_overload=pollCopyFrom",
            ),
            (
                "get",
                "https://gcp-us-central1.turbopuffer.com/v1/namespaces/my-ns/metadata",
                "GET /v1/namespaces/{ns}/metadata",
            ),
        ],
    )
    def test_route_template(self, method: str, url: str, expected: str) -> None:
        assert route_template(method, url) == expected


class TestBuffer:
    def test_durations_are_integer_microseconds(self) -> None:
        buffer = TelemetryBuffer()
        buffer.record(
            method="post",
            url=QUERY_PATH,
            status=200,
            retries=2,
            durations={"total": 1_234_567, "compress": 0, "deserialize": 999},
            server_total_ms=7,
        )

        [record] = take_payload(buffer)["records"]
        assert record["total_us"] == 1234
        assert record["deserialize_us"] == 0
        assert record["server_total_us"] == 7000
        assert record["retries"] == 2
        # A zero compress duration means the body wasn't compressed.
        assert "compress_us" not in record

    def test_full_buffer_drops_oldest_records(self) -> None:
        buffer = TelemetryBuffer()
        for status in range(MAX_BUFFERED_RECORDS + 5):
            add_record(buffer, status=status)

        first = take_payload(buffer)
        assert first["dropped"] == 5
        assert len(first["records"]) == MAX_RECORDS_PER_HEADER
        assert first["records"][0]["status"] == 5

        second = take_payload(buffer)
        assert "dropped" not in second
        assert second["records"][0]["status"] == 5 + MAX_RECORDS_PER_HEADER

    def test_restore_puts_records_back_in_order(self) -> None:
        buffer = TelemetryBuffer()
        for status in range(3):
            add_record(buffer, status=status)
        batch = buffer.take()
        assert batch is not None

        add_record(buffer, status=99)
        buffer.restore(batch)

        assert [r["status"] for r in take_payload(buffer)["records"]] == [0, 1, 2, 99]

    @pytest.mark.parametrize("value", ["abc", "1.5", "-0.1", "nan", ""])
    def test_invalid_sample_rate_is_ignored(self, value: str) -> None:
        buffer = TelemetryBuffer()
        buffer.observe_response(httpx.Headers({SAMPLE_RATE_HEADER: "0.5"}))
        buffer.observe_response(httpx.Headers({SAMPLE_RATE_HEADER: value}))
        assert buffer.sample_rate == 0.5

    def test_fork_resets_buffer(self) -> None:
        buffer = TelemetryBuffer()
        add_record(buffer)
        # Simulates another thread holding the lock when the process forked.
        buffer._lock.acquire()

        telemetry._after_fork_in_child()

        assert buffer.take() is None
        add_record(buffer)
        assert buffer.take() is not None


class TestCopy:
    def test_copies_share_buffer_for_same_key_and_url(
        self, telemetry_client: Turbopuffer, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        buffer = telemetry_client._telemetry
        assert buffer is not None

        assert telemetry_client.copy()._telemetry is buffer
        assert telemetry_client.with_options(timeout=5)._telemetry is buffer
        assert telemetry_client.namespace("my-ns")._client._telemetry is buffer

        assert telemetry_client.copy(api_key="tpuf_other")._telemetry not in (None, buffer)
        assert telemetry_client.copy(base_url="http://127.0.0.1:4011")._telemetry not in (None, buffer)
        assert telemetry_client.copy(telemetry=False)._telemetry is None

        # Copies keep the resolved setting instead of reading the env var again.
        monkeypatch.setenv(TELEMETRY_ENV_VAR, "0")
        assert telemetry_client.copy()._telemetry is buffer

    def test_independent_clients_share_buffer_for_same_key_and_url(self, telemetry_client: Turbopuffer) -> None:
        with Turbopuffer(base_url=base_url, api_key=api_key, telemetry=True) as other:
            assert other._telemetry is telemetry_client._telemetry
        with Turbopuffer(base_url=base_url, api_key="tpuf_other", telemetry=True) as other:
            assert other._telemetry is not telemetry_client._telemetry


class TestRequests:
    @pytest.mark.respx(base_url=base_url)
    def test_records_ride_on_next_request(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response())
        ns = telemetry_client.namespace("my-ns")

        result = ns.query(top_k=1)
        assert sent_records(sent_requests(route)[0]) is None
        # The public performance fields are unchanged.
        assert isinstance(result.performance.client_total_ms, float)
        assert result.performance.client_total_ms > 0

        ns.query(top_k=1)
        records = sent_records(sent_requests(route)[1])
        assert records is not None
        [record] = records
        assert record["route"] == QUERY_ROUTE
        assert record["status"] == 200
        assert record["server_total_us"] == 7000
        for key in ("total_us", "serialize_us", "body_read_us", "deserialize_us"):
            assert isinstance(record[key], int) and record[key] >= 0, key
        assert record["total_us"] >= record["body_read_us"] + record["deserialize_us"]
        assert record["age_ms"] >= 0
        for key in ("compress_us", "response_us", "retries", "error", "sample_rate"):
            assert key not in record, key

    @pytest.mark.respx(base_url=base_url)
    def test_disabled_client_sends_nothing(self, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(TELEMETRY_ENV_VAR, raising=False)
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response())

        with Turbopuffer(base_url=base_url, api_key=api_key) as client:
            ns = client.namespace("my-ns")
            ns.query(top_k=1)
            ns.query(top_k=1)

        assert all(TELEMETRY_HEADER not in request.headers for request in sent_requests(route))

    @pytest.mark.respx(base_url=base_url)
    def test_compression_is_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response())
        ns = telemetry_client.with_options(compression=True).namespace("my-ns")

        ns.query(top_k=1, rank_by=("vector", "ANN", [0.1] * 512))
        ns.query(top_k=1)

        records = sent_records(sent_requests(route)[1])
        assert records is not None
        assert "compress_us" in records[0]

    @pytest.mark.respx(base_url=base_url)
    def test_server_sample_rate_of_zero_stops_recording(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer
    ) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response(headers={SAMPLE_RATE_HEADER: "0"}))
        ns = telemetry_client.namespace("my-ns")

        for _ in range(3):
            ns.query(top_k=1)

        assert all(sent_records(request) is None for request in sent_requests(route))
        assert telemetry_client._telemetry is not None
        assert telemetry_client._telemetry.sample_rate == 0.0

    @pytest.mark.respx(base_url=base_url)
    def test_server_sample_rate_is_applied(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response(headers={SAMPLE_RATE_HEADER: "0.25"}))
        ns = telemetry_client.namespace("my-ns")

        monkeypatch.setattr(telemetry, "_random", lambda: 0.2)
        ns.query(top_k=1)
        monkeypatch.setattr(telemetry, "_random", lambda: 0.3)
        ns.query(top_k=1)
        ns.query(top_k=1)

        records = sent_records(sent_requests(route)[1])
        assert records is not None
        assert records[0]["sample_rate"] == 0.25
        assert sent_records(sent_requests(route)[2]) is None

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    def test_batch_is_resent_after_connect_error(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [query_response(), httpx.ConnectError("refused"), query_response()]
        ns = telemetry_client.namespace("my-ns")

        ns.query(top_k=1)
        ns.query(top_k=1)

        first_attempt = sent_records(sent_requests(route)[1])
        assert first_attempt is not None
        assert sent_records(sent_requests(route)[2]) == first_attempt

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    def test_batch_is_not_resent_after_server_error(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer
    ) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [query_response(), httpx.Response(503), query_response(), query_response()]
        ns = telemetry_client.namespace("my-ns")

        ns.query(top_k=1)
        ns.query(top_k=1)
        ns.query(top_k=1)

        assert sent_records(sent_requests(route)[1]) is not None
        assert sent_records(sent_requests(route)[2]) is None

        # The retried query reports how many retries it took.
        records = sent_records(sent_requests(route)[3])
        assert records is not None
        assert records[0]["retries"] == 1

    @pytest.mark.respx(base_url=base_url)
    def test_failures_are_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [
            httpx.ReadTimeout("slow"),
            httpx.ConnectError("refused"),
            httpx.Response(400, json={"error": "bad request"}),
            query_response(),
        ]
        ns = telemetry_client.with_options(max_retries=0).namespace("my-ns")

        with pytest.raises(APITimeoutError):
            ns.query(top_k=1)
        with pytest.raises(APIConnectionError):
            ns.query(top_k=1)
        with pytest.raises(APIStatusError):
            ns.query(top_k=1)
        ns.query(top_k=1)

        assert sent_records(sent_requests(route)[0]) is None

        timeout = sent_records(sent_requests(route)[1])
        assert timeout is not None
        assert [(r["status"], r["error"]) for r in timeout] == [(0, "timeout")]

        # The connect error never reached the server, so its batch is sent again with the new record.
        after_connect = sent_records(sent_requests(route)[2])
        assert after_connect is not None
        assert [(r["status"], r["error"]) for r in after_connect] == [(0, "timeout"), (0, "connect")]

        after_status = sent_records(sent_requests(route)[3])
        assert after_status is not None
        [record] = after_status
        assert record["status"] == 400
        assert "error" not in record

    @pytest.mark.respx(base_url=base_url)
    def test_query_params_are_not_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        respx_mock.get("/v1/namespaces").mock(return_value=httpx.Response(200, json={"namespaces": []}))

        telemetry_client.namespaces(prefix="secret-prefix")

        assert telemetry_client._telemetry is not None
        [record] = take_payload(telemetry_client._telemetry)["records"]
        assert record["route"] == "GET /v1/namespaces"

    @pytest.mark.respx(base_url=base_url)
    def test_parsing_twice_records_once(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        respx_mock.post(QUERY_PATH).mock(return_value=query_response())

        response = telemetry_client.namespace("my-ns").with_raw_response.query(top_k=1)
        response.parse()
        response.parse(to=httpx.Response)

        assert telemetry_client._telemetry is not None
        assert len(take_payload(telemetry_client._telemetry)["records"]) == 1


class TestAsyncRequests:
    @pytest.mark.respx(base_url=base_url)
    async def test_records_ride_on_next_request(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response())

        async with AsyncTurbopuffer(
            base_url=base_url,
            api_key=api_key,
            telemetry=True,
            # The default aiohttp transport can't be mocked.
            http_client=DefaultAsyncHttpxClient(transport=httpx.AsyncHTTPTransport()),
        ) as client:
            ns = client.namespace("my-ns")
            await ns.query(top_k=1)
            await ns.query(top_k=1)

        assert sent_records(sent_requests(route)[0]) is None
        records = sent_records(sent_requests(route)[1])
        assert records is not None
        [record] = records
        assert record["route"] == QUERY_ROUTE
        assert record["server_total_us"] == 7000
        assert record["total_us"] >= record["deserialize_us"]


class TestConnectionPhases:
    def test_durations(self) -> None:
        new_connection = {
            "request_start": 0,
            "transport_start": 100,
            "connect_start": 150,
            "connect_end": 400,
            "send_start": 410,
            "send_end": 500,
            "response_headers_end": 900,
        }
        durations = compute_durations(new_connection, 1000)
        assert {key: durations[key] for key in ("pool", "connect", "send", "wait")} == {
            "pool": 50,
            "connect": 250,
            "send": 90,
            "wait": 400,
        }
        assert connection_reused(new_connection) is False

        reused_connection = {
            "request_start": 0,
            "transport_start": 100,
            "send_start": 130,
            "send_end": 160,
            "response_headers_end": 300,
        }
        durations = compute_durations(reused_connection, 400)
        assert "connect" not in durations
        assert durations["pool"] == 30
        assert connection_reused(reused_connection) is True

        # aiohttp can finish sending the body after the response headers arrive.
        assert compute_durations({**reused_connection, "send_end": 350}, 400)["wait"] == 0

        # Untraced requests, e.g. through a user-supplied transport.
        assert connection_reused({"request_start": 0}) is None

    def test_sync_client(self, local_server: str) -> None:
        with Turbopuffer(base_url=local_server, api_key=api_key, telemetry=True) as client:
            assert client._telemetry is not None
            ns = client.namespace("my-ns")
            ns.query(top_k=1)
            [first] = take_payload(client._telemetry)["records"]
            ns.query(top_k=1)
            [second] = take_payload(client._telemetry)["records"]

        assert_connection_phases(first, second)

    async def test_async_client(self, local_server: str) -> None:
        async with AsyncTurbopuffer(base_url=local_server, api_key=api_key, telemetry=True) as client:
            assert client._telemetry is not None
            ns = client.namespace("my-ns")
            await ns.query(top_k=1)
            [first] = take_payload(client._telemetry)["records"]
            await ns.query(top_k=1)
            [second] = take_payload(client._telemetry)["records"]

        assert_connection_phases(first, second)

    def test_not_traced_without_telemetry(self, local_server: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(TELEMETRY_ENV_VAR, raising=False)
        with Turbopuffer(base_url=local_server, api_key=api_key) as client:
            response = client.namespace("my-ns").with_raw_response.query(top_k=1)

        clock = response.http_request.extensions["clock"]
        assert "transport_start" in clock
        assert "send_start" not in clock
