"""Hooks for observing the requests a client makes, such as to record their timings.

An observer is called synchronously at fixed points of each request, so it must be cheap. Anything
it raises is logged and ignored, so it can never break a request.
"""

from __future__ import annotations

import time
import logging
from typing import TYPE_CHECKING, Any, Dict, Tuple, Callable, Optional, Awaitable
from typing_extensions import Literal

import httpx2

from ._exceptions import APIStatusError, APITimeoutError, APIConnectionError

if TYPE_CHECKING:
    from ._models import FinalRequestOptions

__all__ = [
    "AttemptResult",
    "ErrorKind",
    "RequestInfo",
    "RequestObserver",
    "RequestResult",
    "RequestScope",
    "Timings",
]

log: logging.Logger = logging.getLogger(__name__)

ErrorKind = Literal[
    "pool_timeout",
    "connect_timeout",
    "connect_error",
    "write_timeout",
    "read_timeout",
    "read_error",
    "timeout",
    "canceled",
    "other",
]

# Request extension holding the attempt's `Timings`, so custom transports can add marks.
TIMINGS_EXTENSION = "timings"

# Request extension through which request building passes its serialization timing.
SERIALIZE_TIMING_EXTENSION = "serialize_timing"

# Request extension linking a request back to its observation.
_OBSERVATION_EXTENSION = "observation"


class Timings:
    """Monotonic timestamps from `time.perf_counter_ns()` marking the progress of one attempt.

    A timestamp stays `None` when its phase didn't happen or couldn't be observed, e.g. `connect_*`
    on a reused connection. Phases may overlap.
    """

    __slots__ = (
        "attempt_begin",
        "serialize_begin",
        "serialize_end",
        "request_ready",
        "connect_begin",
        "connect_end",
        "send_begin",
        "send_end",
        "response_headers",
        "body_end",
        "deserialize_begin",
        "deserialize_end",
        "reused",
        "extra",
    )

    def __init__(self) -> None:
        self.attempt_begin: Optional[int] = None
        self.serialize_begin: Optional[int] = None
        self.serialize_end: Optional[int] = None
        # The request was built and is about to be handed to the HTTP client.
        self.request_ready: Optional[int] = None
        # Opening a new connection: DNS, TCP and TLS.
        self.connect_begin: Optional[int] = None
        self.connect_end: Optional[int] = None
        # Writing the request headers and body.
        self.send_begin: Optional[int] = None
        self.send_end: Optional[int] = None
        self.response_headers: Optional[int] = None
        self.body_end: Optional[int] = None
        self.deserialize_begin: Optional[int] = None
        self.deserialize_end: Optional[int] = None
        # Whether the attempt used an existing connection, or `None` when unknown.
        self.reused: Optional[bool] = None
        # Marks added by custom code, such as transports that compress request bodies.
        self.extra: Dict[str, int] = {}


class RequestInfo:
    """Describes a request as it starts."""

    __slots__ = ("method", "url")

    def __init__(self, *, method: str, url: str) -> None:
        self.method = method
        # The URL the request was made with, usually a path relative to the client's base URL.
        self.url = url


class AttemptResult:
    """The outcome of one attempt of a request."""

    __slots__ = ("attempt", "request", "response", "error", "error_kind", "reached_server", "timings")

    def __init__(
        self,
        *,
        attempt: int,
        request: httpx2.Request,
        response: Optional[httpx2.Response],
        error: Optional[BaseException],
        error_kind: Optional[ErrorKind],
        reached_server: Optional[bool],
        timings: Timings,
    ) -> None:
        self.attempt = attempt
        self.request = request
        self.response = response
        self.error = error
        self.error_kind = error_kind
        # False when the attempt certainly never reached the server, True when a response arrived,
        # and None when unknown.
        self.reached_server = reached_server
        self.timings = timings


class RequestResult:
    """The final outcome of a request, from its last attempt."""

    __slots__ = ("retries", "response", "error", "error_kind", "parsed", "timings")

    def __init__(
        self,
        *,
        retries: int,
        response: Optional[httpx2.Response],
        error: Optional[BaseException],
        error_kind: Optional[ErrorKind],
        parsed: object,
        timings: Timings,
    ) -> None:
        self.retries = retries
        self.response = response
        self.error = error
        self.error_kind = error_kind
        # The parsed response body, or None if it wasn't parsed.
        self.parsed = parsed
        self.timings = timings


class RequestScope:
    """Observes one request across its attempts. Subclass it and override what you need."""

    def attempt_begin(self, attempt: int, request: httpx2.Request) -> None:  # noqa: ARG002
        """Called before each attempt is sent. May change the request's headers."""
        return None

    def attempt_end(self, result: AttemptResult) -> None:  # noqa: ARG002
        """Called after each attempt, before its response is closed."""
        return None

    def finish(self, result: RequestResult) -> None:  # noqa: ARG002
        """Called once when the request is done: after its response is parsed, or when it fails for
        good. Responses that are never parsed, such as raw responses, don't finish."""
        return None


class RequestObserver:
    """Observes a client's requests. Subclass it and install it on a client."""

    def start(self, info: RequestInfo) -> Optional[RequestScope]:  # noqa: ARG002
        """Called once per request, before its first attempt. Returns a scope to observe it, or None."""
        return None


def error_kind(err: BaseException) -> ErrorKind:
    # Interrupts and task cancellations, which aren't Exceptions so that they aren't caught by accident.
    if not isinstance(err, Exception):
        return "canceled"
    # The client's own connection errors wrap the error that caused them.
    if isinstance(err, APIConnectionError) and isinstance(err.__cause__, Exception):
        return error_kind(err.__cause__)
    if isinstance(err, APITimeoutError):
        return "timeout"
    if isinstance(err, httpx2.PoolTimeout):
        return "pool_timeout"
    if isinstance(err, httpx2.ConnectTimeout):
        return "connect_timeout"
    if isinstance(err, httpx2.WriteTimeout):
        return "write_timeout"
    if isinstance(err, httpx2.ReadTimeout):
        return "read_timeout"
    if isinstance(err, httpx2.TimeoutException):
        return "timeout"
    if isinstance(err, httpx2.ConnectError):
        return "connect_error"
    if isinstance(err, (httpx2.ReadError, httpx2.RemoteProtocolError)):
        return "read_error"
    return "other"


def _reached_server(err: BaseException) -> Optional[bool]:
    # These are raised before any part of the request is written.
    if isinstance(err, (httpx2.PoolTimeout, httpx2.ConnectTimeout, httpx2.ConnectError)):
        return False
    return None


# httpcore2 trace events that mark timings, and the fields they set. Later events overwrite
# earlier ones, so with TLS a connection ends when its handshake completes.
_TRACE_EVENTS = {
    "connection.connect_tcp.started": "connect_begin",
    "connection.connect_unix_socket.started": "connect_begin",
    "connection.connect_tcp.complete": "connect_end",
    "connection.connect_unix_socket.complete": "connect_end",
    "connection.start_tls.complete": "connect_end",
    "http11.send_request_headers.started": "send_begin",
    "http2.send_request_headers.started": "send_begin",
    "http11.send_request_body.complete": "send_end",
    "http2.send_request_body.complete": "send_end",
    "http11.receive_response_headers.complete": "response_headers",
    "http2.receive_response_headers.complete": "response_headers",
    "http11.receive_response_body.complete": "body_end",
    "http2.receive_response_body.complete": "body_end",
}


def _mark(timings: Timings, event_name: str) -> None:
    field = _TRACE_EVENTS.get(event_name)
    if field is not None:
        setattr(timings, field, time.perf_counter_ns())


def _sync_tracer(timings: Timings, previous: Any) -> Callable[[str, Any], None]:
    def trace(event_name: str, info: Any) -> None:
        _mark(timings, event_name)
        if previous is not None:
            previous(event_name, info)

    return trace


def _async_tracer(timings: Timings, previous: Any) -> Callable[[str, Any], Awaitable[None]]:
    async def trace(event_name: str, info: Any) -> None:
        _mark(timings, event_name)
        if previous is not None:
            await previous(event_name, info)

    return trace


def _call(fn: Callable[..., Any], *args: Any) -> Any:
    try:
        return fn(*args)
    except Exception:
        log.warning("Request observer raised an exception", exc_info=True)
        return None


class RequestObservation:
    """Drives one request's scope through its attempts. Does nothing when there's no scope."""

    __slots__ = ("_scope", "_attempt", "_request", "_timings", "_finished")

    def __init__(self, observer: Optional[RequestObserver], options: Optional[FinalRequestOptions]) -> None:
        self._scope: Optional[RequestScope] = None
        if observer is not None and options is not None:
            self._scope = _call(observer.start, RequestInfo(method=options.method, url=options.url))
        self._attempt = 0
        self._request: Optional[httpx2.Request] = None
        self._timings = Timings()
        self._finished = False

    @staticmethod
    def of(response: httpx2.Response) -> RequestObservation:
        """Returns the observation of the request behind `response`, or an inert one."""
        if response._request is not None:
            observation = response.request.extensions.get(_OBSERVATION_EXTENSION)
            if isinstance(observation, RequestObservation):
                return observation
        return _INERT

    def start_attempt(self, attempt: int) -> None:
        if self._scope is None:
            return
        self._attempt = attempt
        self._timings = Timings()
        self._timings.attempt_begin = time.perf_counter_ns()

    def before_send(self, request: httpx2.Request, *, is_async: bool = False) -> None:
        if self._scope is None:
            return
        timings = self._timings
        timings.request_ready = time.perf_counter_ns()
        serialize: Optional[Tuple[int, int]] = request.extensions.get(SERIALIZE_TIMING_EXTENSION)
        if serialize is not None:
            timings.serialize_begin, timings.serialize_end = serialize

        request.extensions[TIMINGS_EXTENSION] = timings
        request.extensions[_OBSERVATION_EXTENSION] = self
        previous = request.extensions.get("trace")
        request.extensions["trace"] = _async_tracer(timings, previous) if is_async else _sync_tracer(timings, previous)
        self._request = request
        _call(self._scope.attempt_begin, self._attempt, request)

    def on_response(self, response: httpx2.Response) -> None:
        if self._scope is None or self._request is None:
            return
        self._settle()
        result = AttemptResult(
            attempt=self._attempt,
            request=self._request,
            response=response,
            error=None,
            error_kind=None,
            reached_server=True,
            timings=self._timings,
        )
        _call(self._scope.attempt_end, result)

    def on_error(self, err: BaseException, *, final: bool) -> None:
        """Called when an attempt raises. `final` means the request won't be retried."""
        if self._scope is None or self._request is None:
            return
        self._settle()
        kind = error_kind(err)
        result = AttemptResult(
            attempt=self._attempt,
            request=self._request,
            response=None,
            error=err,
            error_kind=kind,
            reached_server=_reached_server(err),
            timings=self._timings,
        )
        _call(self._scope.attempt_end, result)
        if final:
            self.finish(error=err)

    def start_parse(self) -> None:
        if self._scope is None or self._finished:
            return
        self._timings.deserialize_begin = time.perf_counter_ns()

    def finish(
        self,
        *,
        response: Optional[httpx2.Response] = None,
        error: Optional[BaseException] = None,
        parsed: object = None,
    ) -> None:
        if self._scope is None or self._finished:
            return
        self._finished = True
        if self._timings.deserialize_begin is not None:
            self._timings.deserialize_end = time.perf_counter_ns()
        self._settle()
        kind: Optional[ErrorKind] = None
        # An error response is described by the response itself.
        if error is not None and not isinstance(error, APIStatusError):
            kind = error_kind(error)
        result = RequestResult(
            retries=self._attempt,
            response=response,
            error=error,
            error_kind=kind,
            parsed=parsed,
            timings=self._timings,
        )
        _call(self._scope.finish, result)

    def _settle(self) -> None:
        timings = self._timings
        if timings.reused is None and timings.send_begin is not None:
            timings.reused = timings.connect_begin is None


_INERT = RequestObservation(None, None)
