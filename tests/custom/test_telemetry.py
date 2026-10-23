from __future__ import annotations

import json
import asyncio
import logging
import threading
from typing import Any, Dict, List, Tuple, Iterator, Optional, cast
from unittest import mock
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing_extensions import override

import httpx2
import pytest

from turbopuffer import (
    Turbopuffer,
    NotFoundError,
    APIStatusError,
    APITimeoutError,
    AsyncTurbopuffer,
    APIConnectionError,
    DefaultAsyncHttpxClient,
)
from tests.respx2 import Route, MockRouter
from tests.conftest import api_key, base_url
from turbopuffer.lib import telemetry, respond_async
from turbopuffer._observer import Timings
from turbopuffer.lib.telemetry import (
    REQUEST_ID_BYTES,
    TELEMETRY_HEADER,
    REQUEST_ID_HEADER,
    REQUEST_ID_PREFIX,
    TELEMETRY_ENV_VAR,
    SAMPLE_RATE_HEADER,
    REQUEST_ID_ALPHABET,
    MAX_BUFFERED_RECORDS,
    MAX_RECORDS_PER_HEADER,
    REQUEST_ID_RANDOM_BYTES,
    TelemetryBuffer,
    encode_base32,
    new_request_id,
    route_template,
    resolve_enabled,
)
from turbopuffer.lib.performance import compute_durations

QUERY_PATH = "/v2/namespaces/my-ns/query"
QUERY_ROUTE = "POST /v2/namespaces/{ns}/query"


def query_response(*, headers: Optional[Dict[str, str]] = None) -> httpx2.Response:
    return httpx2.Response(
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


def sent_requests(route: Route) -> List[httpx2.Request]:
    calls = cast(List[Any], route.calls)
    return [call.request for call in calls]


def sent_records(request: httpx2.Request) -> Optional[List[Dict[str, Any]]]:
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


def add_record(buffer: TelemetryBuffer, *, status: int = 200, sample_rate: float = 1.0) -> None:
    buffer.record(
        method="post",
        url=QUERY_PATH,
        status=status,
        retries=0,
        durations={"total": 5_000_000},
        sample_rate=sample_rate,
    )


def decode_request_id(request_id: str) -> Tuple[int, bytes]:
    """Returns the millisecond time and random bytes of a generated request ID, checking its format."""
    assert request_id.startswith(REQUEST_ID_PREFIX), request_id
    encoded = request_id[len(REQUEST_ID_PREFIX) :]
    alphabet = REQUEST_ID_ALPHABET.decode("ascii")
    assert len(encoded) == 29 and all(c in alphabet for c in encoded), request_id
    value = 0
    for c in encoded:
        value = (value << 5) | alphabet.index(c)
    # The 29 characters hold one bit more than the bytes, which pads them with a zero.
    assert value & 1 == 0, request_id
    data = (value >> 1).to_bytes(REQUEST_ID_BYTES, "big")
    random_bytes = data[:REQUEST_ID_RANDOM_BYTES]
    millis = bytes(m ^ r for m, r in zip(data[REQUEST_ID_RANDOM_BYTES:], random_bytes, strict=False))
    return int.from_bytes(millis, "big"), random_bytes


def no_retry_delay(*_args: Any, **_kwargs: Any) -> float:
    return 0.0


@pytest.fixture(autouse=True)
def clear_shared_buffers() -> None:
    # Clients from earlier tests may not be garbage collected yet, and would share their buffer.
    telemetry._shared_buffers.clear()


class QueryHandler(BaseHTTPRequestHandler):
    # Keeps connections open between requests, so they can be reused.
    protocol_version = "HTTP/1.1"
    # The request IDs that requests arrived with, in order.
    request_ids: List[Optional[str]] = []

    def do_POST(self) -> None:
        QueryHandler.request_ids.append(self.headers.get(REQUEST_ID_HEADER))
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
        for key in ("pool_us", "send_us", "wait_us", "body_read_us"):
            assert isinstance(record[key], int) and record[key] >= 0, key
        assert record["wait_us"] + record["body_read_us"] <= record["total_us"]


def make_timings(*, extra: Optional[Dict[str, int]] = None, **marks: int) -> Timings:
    timings = Timings()
    for name, value in marks.items():
        setattr(timings, name, value)
    timings.extra = extra or {}
    return timings


def assert_client_performance(performance: Any) -> None:
    assert performance.client_total_ms > 0
    assert performance.client_response_ms is not None
    assert 0 < performance.client_response_ms <= performance.client_total_ms
    assert performance.client_body_read_ms is not None and performance.client_body_read_ms >= 0
    assert performance.client_deserialize_ms > 0


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
            sample_rate=1.0,
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

    def test_samples_requests(self, monkeypatch: pytest.MonkeyPatch) -> None:
        buffer = TelemetryBuffer()
        monkeypatch.setattr(telemetry, "_random", lambda: 0.3)
        buffer.observe_response(httpx2.Headers({SAMPLE_RATE_HEADER: "0.5"}))
        assert buffer.sample() == 0.5
        add_record(buffer, sample_rate=0.5)
        assert take_payload(buffer)["records"][0]["sample_rate"] == 0.5

        buffer.observe_response(httpx2.Headers({SAMPLE_RATE_HEADER: "0.25"}))
        assert buffer.sample() is None

        monkeypatch.setattr(telemetry, "_random", lambda: 0.0)
        buffer.observe_response(httpx2.Headers({SAMPLE_RATE_HEADER: "0"}))
        assert buffer.sample() is None

        # A full rate isn't reported.
        buffer.observe_response(httpx2.Headers({SAMPLE_RATE_HEADER: "1"}))
        assert buffer.sample() == 1.0
        add_record(buffer)
        assert "sample_rate" not in take_payload(buffer)["records"][0]

    @pytest.mark.parametrize("value", ["abc", "1.5", "-0.1", "nan", ""])
    def test_invalid_sample_rate_is_ignored(self, value: str) -> None:
        buffer = TelemetryBuffer()
        buffer.observe_response(httpx2.Headers({SAMPLE_RATE_HEADER: "0.5"}))
        buffer.observe_response(httpx2.Headers({SAMPLE_RATE_HEADER: value}))
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
    def test_failure_before_sending_keeps_records(self, telemetry_client: Turbopuffer) -> None:
        assert telemetry_client._telemetry is not None
        add_record(telemetry_client._telemetry)

        # Building the request fails, so it's never sent.
        with pytest.raises(TypeError):
            telemetry_client.post(QUERY_PATH, cast_to=object, body={"unserializable": object()})

        assert len(take_payload(telemetry_client._telemetry)["records"]) == 1

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
        # Mocked transports never open connections, so network phases are only covered by TestConnectionPhases.
        for key in ("total_us", "serialize_us", "deserialize_us"):
            assert isinstance(record[key], int) and record[key] >= 0, key
        assert record["total_us"] >= record["serialize_us"] + record["deserialize_us"]
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
        assert all(REQUEST_ID_HEADER not in request.headers for request in sent_requests(route))

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
        # Unrecorded requests have no request IDs to link.
        assert all(REQUEST_ID_HEADER not in request.headers for request in sent_requests(route)[1:])

    @pytest.mark.respx(base_url=base_url)
    def test_server_sample_rate_is_applied(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response(headers={SAMPLE_RATE_HEADER: "0.25"}))
        ns = telemetry_client.namespace("my-ns")

        monkeypatch.setattr(telemetry, "_random", lambda: 0.2)
        ns.query(top_k=1)
        ns.query(top_k=1)
        monkeypatch.setattr(telemetry, "_random", lambda: 0.3)
        ns.query(top_k=1)
        ns.query(top_k=1)

        # Requests are sampled as they start, so the first is at the full rate the server hadn't changed yet.
        requests = sent_requests(route)
        records = sent_records(requests[1])
        assert records is not None
        assert "sample_rate" not in records[0]
        records = sent_records(requests[2])
        assert records is not None
        assert records[0]["sample_rate"] == 0.25
        assert sent_records(requests[3]) is None
        # Unrecorded requests have no request IDs to link.
        assert REQUEST_ID_HEADER not in requests[2].headers

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    def test_batch_is_resent_after_connect_error(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [query_response(), httpx2.ConnectError("refused"), query_response()]
        ns = telemetry_client.namespace("my-ns")

        ns.query(top_k=1)
        ns.query(top_k=1)

        first_attempt = sent_records(sent_requests(route)[1])
        second_attempt = sent_records(sent_requests(route)[2])
        assert first_attempt is not None and second_attempt is not None
        # Ages are recomputed whenever a batch is taken, so only they may differ.
        for record in (*first_attempt, *second_attempt):
            del record["age_ms"]
        assert second_attempt == first_attempt

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    def test_batch_is_kept_when_interrupted_before_retry(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer
    ) -> None:
        class Interrupted(BaseException):
            pass

        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [query_response(), httpx2.ConnectError("refused"), query_response()]
        ns = telemetry_client.namespace("my-ns")

        ns.query(top_k=1)
        # Interrupted while waiting to retry, so the request never finishes.
        with mock.patch.object(Turbopuffer, "_sleep_for_retry", side_effect=Interrupted()):
            with pytest.raises(Interrupted):
                ns.query(top_k=1)
        ns.query(top_k=1)

        records = sent_records(sent_requests(route)[2])
        assert records is not None
        assert [r["route"] for r in records] == [QUERY_ROUTE]

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    def test_batch_is_not_resent_after_server_error(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer
    ) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [query_response(), httpx2.Response(503), query_response(), query_response()]
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
    def test_interrupted_requests_are_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        class Interrupted(BaseException):
            pass

        def interrupt(_request: httpx2.Request) -> httpx2.Response:
            raise Interrupted()

        route = respx_mock.post(QUERY_PATH).mock(side_effect=interrupt)
        ns = telemetry_client.namespace("my-ns")

        with pytest.raises(Interrupted):
            ns.query(top_k=1)
        route.mock(return_value=query_response())
        ns.query(top_k=1)

        records = sent_records(sent_requests(route)[-1])
        assert records is not None
        assert [(r["status"], r["error"]) for r in records] == [(0, "canceled")]

    @pytest.mark.respx(base_url=base_url)
    def test_parse_failures_are_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [
            httpx2.Response(200, content=b"not json", headers={"Content-Type": "application/json"}),
            query_response(),
        ]
        ns = telemetry_client.namespace("my-ns")

        with pytest.raises(ValueError):
            ns.query(top_k=1)
        ns.query(top_k=1)

        records = sent_records(sent_requests(route)[1])
        assert records is not None
        assert [(r["status"], r["error"]) for r in records] == [(200, "other")]

    @pytest.mark.respx(base_url=base_url)
    def test_failures_are_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [
            httpx2.ReadTimeout("slow"),
            httpx2.ConnectError("refused"),
            httpx2.Response(400, json={"error": "bad request"}),
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
        respx_mock.get("/v1/namespaces").mock(return_value=httpx2.Response(200, json={"namespaces": []}))

        telemetry_client.namespaces(prefix="secret-prefix")

        assert telemetry_client._telemetry is not None
        [record] = take_payload(telemetry_client._telemetry)["records"]
        assert record["route"] == "GET /v1/namespaces"

    @pytest.mark.respx(base_url=base_url)
    def test_parsing_twice_records_once(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        respx_mock.post(QUERY_PATH).mock(return_value=query_response())

        response = telemetry_client.namespace("my-ns").with_raw_response.query(top_k=1)
        response.parse()
        response.parse(to=httpx2.Response)

        assert telemetry_client._telemetry is not None
        assert len(take_payload(telemetry_client._telemetry)["records"]) == 1


class TestRequestIds:
    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (bytes(16), "22222222222222222222222222"),
            (bytes(15) + b"\x01", "22222222222222222222222226"),
            (bytes(15) + b"\x0f", "2222222222222222222222223w"),
            (bytes(15) + b"\xff", "222222222222222222222222zw"),
            (b"\xff" * 16, "zzzzzzzzzzzzzzzzzzzzzzzzzw"),
        ],
    )
    def test_encodes_base32(self, data: bytes, expected: str) -> None:
        # The vectors of riverpro's uuidbase32, which uses the same encoding.
        assert encode_base32(data) == expected

    def test_encodes_request_ids(self) -> None:
        # Generated with Python's base64 module, independently of the implementation.
        random_bytes = bytes.fromhex("9f1c2e7a4b6d8e0f1a2b3c4d")
        request_id = new_request_id(1_792_497_600_123, random_bytes)
        assert request_id == "tpreq_nwi4wymfhqb2yalfblatxjfremalg"
        assert decode_request_id(request_id) == (1_792_497_600_123, random_bytes)

    def test_generates_request_ids(self) -> None:
        millis, random_bytes = decode_request_id(new_request_id(1_792_497_600_123))
        assert millis == 1_792_497_600_123
        _, other = decode_request_id(new_request_id(1_792_497_600_123))
        assert other != random_bytes

    @pytest.mark.respx(base_url=base_url)
    def test_sends_request_ids_that_records_repeat(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response())
        ns = telemetry_client.namespace("my-ns")

        ns.query(top_k=1)
        ns.query(top_k=1)

        first, second = (request.headers[REQUEST_ID_HEADER] for request in sent_requests(route))
        assert first != second
        for request_id in (first, second):
            decode_request_id(request_id)
        records = sent_records(sent_requests(route)[1])
        assert records is not None
        assert records[0]["request_id"] == first

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    def test_retries_keep_their_request_ids(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [httpx2.Response(503), query_response()]

        telemetry_client.namespace("my-ns").query(top_k=1)

        first, second = (request.headers[REQUEST_ID_HEADER] for request in sent_requests(route))
        assert first == second
        assert telemetry_client._telemetry is not None
        [record] = take_payload(telemetry_client._telemetry)["records"]
        assert record["request_id"] == first
        assert record["retries"] == 1

    @pytest.mark.respx(base_url=base_url)
    @mock.patch("turbopuffer._base_client.BaseClient._calculate_retry_timeout", no_retry_delay)
    @pytest.mark.parametrize("per_request", [False, True])
    def test_keeps_request_ids_set_by_callers(self, respx_mock: MockRouter, per_request: bool) -> None:
        route = respx_mock.post(QUERY_PATH)
        route.side_effect = [httpx2.Response(503), query_response()]
        default_headers = {} if per_request else {"X-Request-Id": "my-request"}
        extra_headers = {"x-request-id": "my-request"} if per_request else None

        with Turbopuffer(base_url=base_url, api_key=api_key, telemetry=True, default_headers=default_headers) as client:
            client.namespace("my-ns").query(top_k=1, extra_headers=extra_headers)
            assert client._telemetry is not None
            [record] = take_payload(client._telemetry)["records"]

        # Retries keep the caller's ID too.
        assert [request.headers[REQUEST_ID_HEADER] for request in sent_requests(route)] == ["my-request"] * 2
        assert "request_id" not in record


class TestRespondAsync:
    """Requests the server accepts with a 202 and the SDK then polls until they finish."""

    WRITE_PATH = "/v2/namespaces/my-ns"
    POLL_PATH = "/v1/namespaces/my-ns/operations/op-abc"

    @pytest.fixture(autouse=True)
    def _no_poll_delay(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(respond_async, "POLL_INTERVAL_SECS", 0)

    def accepted(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.WRITE_PATH).mock(
            return_value=httpx2.Response(
                202, headers={"preference-applied": "respond-async", "location": f"{base_url}{self.POLL_PATH}"}
            )
        )

    def write(self, client: Turbopuffer) -> None:
        client.namespace("my-ns").write(upsert_columns={"id": [1], "vector": [[0.1]]})

    def records(self, respx_mock: MockRouter, client: Turbopuffer) -> List[Dict[str, Any]]:
        """Returns the records sent on later requests, followed by those still buffered."""
        calls = cast(List[Any], respx_mock.calls)
        records = [record for call in calls for record in sent_records(call.request) or []]
        assert client._telemetry is not None
        return records + cast(List[Dict[str, Any]], take_payload(client._telemetry)["records"])

    @pytest.mark.respx(base_url=base_url)
    def test_polls_and_request_are_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        self.accepted(respx_mock)
        respx_mock.get(self.POLL_PATH).mock(
            side_effect=[
                httpx2.Response(200, json={"status": "running"}),
                httpx2.Response(200, json={"status": "finished", "result": {"success": {"status": "OK"}}}),
            ]
        )

        self.write(telemetry_client)

        *polls, request = self.records(respx_mock, telemetry_client)
        assert [(r["route"], r["status"]) for r in polls] == [
            ("GET /v1/namespaces/{ns}/operations/{token}", 200),
            ("GET /v1/namespaces/{ns}/operations/{token}", 200),
        ]
        # The request reports the final outcome, and its total spans the polling.
        assert (request["route"], request["status"]) == ("POST /v2/namespaces/{ns}", 200)
        assert "error" not in request
        assert request["total_us"] >= sum(r["total_us"] for r in polls)
        # Each poll is a request of its own, with its own ID.
        calls = cast(List[Any], respx_mock.calls)
        request_ids = [call.request.headers[REQUEST_ID_HEADER] for call in calls]
        assert len(set(request_ids)) == 3
        assert [r["request_id"] for r in (request, *polls)] == request_ids

    @pytest.mark.respx(base_url=base_url)
    def test_failed_operation_is_recorded(self, respx_mock: MockRouter, telemetry_client: Turbopuffer) -> None:
        self.accepted(respx_mock)
        respx_mock.get(self.POLL_PATH).mock(
            return_value=httpx2.Response(
                200,
                json={"status": "finished", "result": {"error": {"status_code": 404, "detail": {"error": "gone"}}}},
            )
        )

        with pytest.raises(NotFoundError):
            self.write(telemetry_client)

        _poll, request = self.records(respx_mock, telemetry_client)
        assert (request["route"], request["status"]) == ("POST /v2/namespaces/{ns}", 404)
        assert "error" not in request

    @pytest.mark.respx(base_url=base_url)
    def test_polling_timeout_is_recorded(
        self, respx_mock: MockRouter, telemetry_client: Turbopuffer, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(respond_async, "POLL_INTERVAL_SECS", 0.01)
        self.accepted(respx_mock)
        respx_mock.get(self.POLL_PATH).mock(return_value=httpx2.Response(200, json={"status": "running"}))

        with pytest.raises(APITimeoutError):
            self.write(telemetry_client.with_options(timeout=0.05))

        *_polls, request = self.records(respx_mock, telemetry_client)
        assert (request["route"], request["status"], request["error"]) == ("POST /v2/namespaces/{ns}", 202, "timeout")


class TestAsyncRequests:
    @pytest.mark.respx(base_url=base_url)
    async def test_cancelled_requests_are_recorded(self, respx_mock: MockRouter) -> None:
        async def stall(_request: httpx2.Request) -> httpx2.Response:
            await asyncio.sleep(10)
            return query_response()

        route = respx_mock.post(QUERY_PATH).mock(side_effect=stall)

        async with AsyncTurbopuffer(
            base_url=base_url,
            api_key=api_key,
            telemetry=True,
            # The default aiohttp transport can't be mocked.
            http_client=DefaultAsyncHttpxClient(transport=httpx2.AsyncHTTPTransport()),
        ) as client:
            ns = client.namespace("my-ns")
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(ns.query(top_k=1), timeout=0.05)
            route.mock(return_value=query_response())
            await ns.query(top_k=1)

        records = sent_records(sent_requests(route)[-1])
        assert records is not None
        [record] = records
        assert (record["status"], record["error"]) == (0, "canceled")
        # Covers the time until cancellation, a little less than the wait since setup came first.
        assert record["total_us"] >= 10_000

    @pytest.mark.respx(base_url=base_url)
    async def test_records_ride_on_next_request(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post(QUERY_PATH).mock(return_value=query_response())

        async with AsyncTurbopuffer(
            base_url=base_url,
            api_key=api_key,
            telemetry=True,
            # The default aiohttp transport can't be mocked.
            http_client=DefaultAsyncHttpxClient(transport=httpx2.AsyncHTTPTransport()),
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
        first, second = (request.headers[REQUEST_ID_HEADER] for request in sent_requests(route))
        assert first != second
        assert record["request_id"] == first


class TestConnectionPhases:
    def test_durations(self) -> None:
        new_connection = make_timings(
            attempt_begin=0,
            request_ready=50,
            connect_begin=150,
            connect_end=400,
            send_begin=410,
            send_end=500,
            response_headers=900,
            extra={"compress_begin": 60, "compress_end": 100},
        )
        durations = compute_durations(new_connection, 1000)
        assert {key: durations[key] for key in ("compress", "pool", "connect", "send", "wait")} == {
            "compress": 40,
            "pool": 50,
            "connect": 250,
            "send": 90,
            "wait": 400,
        }

        reused_connection = make_timings(
            attempt_begin=0, request_ready=100, send_begin=130, send_end=160, response_headers=300
        )
        durations = compute_durations(reused_connection, 400)
        assert "connect" not in durations
        assert durations["pool"] == 30

        # aiohttp can finish sending the body after the response headers arrive.
        reused_connection.send_end = 350
        assert compute_durations(reused_connection, 400)["wait"] == 0

        # Untraced requests, e.g. through a user-supplied transport.
        assert compute_durations(make_timings(attempt_begin=0), 400) == {"total": 400}

    def test_sync_client(self, local_server: str) -> None:
        QueryHandler.request_ids.clear()
        with Turbopuffer(base_url=local_server, api_key=api_key, telemetry=True) as client:
            assert client._telemetry is not None
            ns = client.namespace("my-ns")
            ns.query(top_k=1)
            [first] = take_payload(client._telemetry)["records"]
            ns.query(top_k=1)
            [second] = take_payload(client._telemetry)["records"]

        assert_connection_phases(first, second)
        assert QueryHandler.request_ids == [first["request_id"], second["request_id"]]

    async def test_async_client(self, local_server: str) -> None:
        QueryHandler.request_ids.clear()
        async with AsyncTurbopuffer(base_url=local_server, api_key=api_key, telemetry=True) as client:
            assert client._telemetry is not None
            ns = client.namespace("my-ns")
            await ns.query(top_k=1)
            [first] = take_payload(client._telemetry)["records"]
            await ns.query(top_k=1)
            [second] = take_payload(client._telemetry)["records"]

        assert_connection_phases(first, second)
        # Sent by the default aiohttp transport too.
        assert QueryHandler.request_ids == [first["request_id"], second["request_id"]]

    def test_performance_without_telemetry(self, local_server: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(TELEMETRY_ENV_VAR, raising=False)
        with Turbopuffer(base_url=local_server, api_key=api_key) as client:
            assert client._telemetry is None
            performance = client.namespace("my-ns").query(top_k=1).performance

        assert_client_performance(performance)

    async def test_async_performance_without_telemetry(
        self, local_server: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv(TELEMETRY_ENV_VAR, raising=False)
        async with AsyncTurbopuffer(base_url=local_server, api_key=api_key) as client:
            assert client._telemetry is None
            performance = (await client.namespace("my-ns").query(top_k=1)).performance

        assert_client_performance(performance)
