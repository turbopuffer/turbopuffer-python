# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from .types import client_namespaces_params
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    omit,
    not_given,
)
from ._utils import (
    is_given,
    maybe_transform,
    get_async_library,
)
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from .pagination import SyncNamespacePage, AsyncNamespacePage
from ._exceptions import APIStatusError, TurbopufferError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    AsyncPaginator,
    make_request_options,
)
from .lib.namespace import (
    Namespace,
    AsyncNamespace,
    NamespaceWithRawResponse,
    AsyncNamespaceWithRawResponse,
    NamespaceWithStreamingResponse,
    AsyncNamespaceWithStreamingResponse,
)
from .types.namespace_summary import NamespaceSummary

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Turbopuffer",
    "AsyncTurbopuffer",
    "Client",
    "AsyncClient",
]


class Turbopuffer(SyncAPIClient):
    with_raw_response: TurbopufferWithRawResponse
    with_streaming_response: TurbopufferWithStreamedResponse

    # client options
    api_key: str
    region: str | None
    default_namespace: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        region: str | None = None,
        default_namespace: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable request compression. When enabled, requests larger than 1024 bytes are automatically compressed with gzip.
        compression: bool = False,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Turbopuffer client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `TURBOPUFFER_API_KEY`
        - `region` from `TURBOPUFFER_REGION` (unless base_url is overridden)
        """
        if api_key is None:
            api_key = os.environ.get("TURBOPUFFER_API_KEY")
        if api_key is None:
            raise TurbopufferError(
                "The api_key client option must be set either by passing api_key to the client or by setting the TURBOPUFFER_API_KEY environment variable"
            )
        self.api_key = api_key

        if region is None:
            region = os.environ.get("TURBOPUFFER_REGION")
        self.region = region

        self.default_namespace = default_namespace

        if base_url is None:
            base_url = os.environ.get("TURBOPUFFER_BASE_URL")
        if base_url is None:
            base_url = "https://{region}.turbopuffer.com"
        self.original_base_url = base_url

        has_region_placeholder = "{region}" in str(base_url)
        if has_region_placeholder:
            if region is None:
                raise TurbopufferError(
                    f"region is required, but not set (baseUrl has a {{region}} placeholder: {base_url})"
                )
            base_url = str(base_url).replace("{region}", region)
        elif region is not None:
            raise TurbopufferError(
                f"region is set, but would be ignored (baseUrl does not contain {{region}} placeholder: {base_url})"
            )

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
            compression=compression,
        )

        self.with_raw_response = TurbopufferWithRawResponse(self)
        self.with_streaming_response = TurbopufferWithStreamedResponse(self)

    def namespace(self, namespace: str) -> Namespace:
        """Create a namespace resource."""
        return Namespace(self.with_options(default_namespace=namespace))

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        region: str | None = None,
        default_namespace: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        compression: bool | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            region=region or self.region,
            default_namespace=default_namespace or self.default_namespace,
            base_url=base_url or self.original_base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            compression=compression if compression is not None else self.compression,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def namespaces(
        self,
        *,
        cursor: str | Omit = omit,
        page_size: int | Omit = omit,
        prefix: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncNamespacePage[NamespaceSummary]:
        """
        List namespaces.

        Args:
          cursor: Retrieve the next page of results.

          page_size: Limit the number of results per page.

          prefix: Retrieve only the namespaces that match the prefix.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.get_api_list(
            "/v1/namespaces",
            page=SyncNamespacePage[NamespaceSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "page_size": page_size,
                        "prefix": prefix,
                    },
                    client_namespaces_params.ClientNamespacesParams,
                ),
            ),
            model=NamespaceSummary,
        )

    def _get_default_namespace_path_param(self) -> str:
        from_client = self.default_namespace
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing default_namespace argument; Please provide it at the client level, e.g. Turbopuffer(default_namespace='abcd') or per method."
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncTurbopuffer(AsyncAPIClient):
    with_raw_response: AsyncTurbopufferWithRawResponse
    with_streaming_response: AsyncTurbopufferWithStreamedResponse

    # client options
    api_key: str
    region: str | None
    default_namespace: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        region: str | None = None,
        default_namespace: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable request compression. When enabled, requests larger than 1024 bytes are automatically compressed with gzip.
        compression: bool = False,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncTurbopuffer client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `TURBOPUFFER_API_KEY`
        - `region` from `TURBOPUFFER_REGION` (unless base_url is overridden)
        """
        if api_key is None:
            api_key = os.environ.get("TURBOPUFFER_API_KEY")
        if api_key is None:
            raise TurbopufferError(
                "The api_key client option must be set either by passing api_key to the client or by setting the TURBOPUFFER_API_KEY environment variable"
            )
        self.api_key = api_key

        if region is None:
            region = os.environ.get("TURBOPUFFER_REGION")
        self.region = region

        self.default_namespace = default_namespace

        if base_url is None:
            base_url = os.environ.get("TURBOPUFFER_BASE_URL")
        if base_url is None:
            base_url = "https://{region}.turbopuffer.com"
        self.original_base_url = base_url

        has_region_placeholder = "{region}" in str(base_url)
        if has_region_placeholder:
            if region is None:
                raise TurbopufferError(
                    f"region is required, but not set (baseUrl has a {{region}} placeholder: {base_url})"
                )
            base_url = str(base_url).replace("{region}", region)
        elif region is not None:
            raise TurbopufferError(
                f"region is set, but would be ignored (baseUrl does not contain {{region}} placeholder: {base_url})"
            )

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
            compression=compression,
        )

        self.with_raw_response = AsyncTurbopufferWithRawResponse(self)
        self.with_streaming_response = AsyncTurbopufferWithStreamedResponse(self)

    def namespace(self, namespace: str) -> AsyncNamespace:
        """Create a namespace resource."""
        return AsyncNamespace(self.with_options(default_namespace=namespace))

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        region: str | None = None,
        default_namespace: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        compression: bool | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            region=region or self.region,
            default_namespace=default_namespace or self.default_namespace,
            base_url=base_url or self.original_base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            compression=compression if compression is not None else self.compression,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def namespaces(
        self,
        *,
        cursor: str | Omit = omit,
        page_size: int | Omit = omit,
        prefix: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[NamespaceSummary, AsyncNamespacePage[NamespaceSummary]]:
        """
        List namespaces.

        Args:
          cursor: Retrieve the next page of results.

          page_size: Limit the number of results per page.

          prefix: Retrieve only the namespaces that match the prefix.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.get_api_list(
            "/v1/namespaces",
            page=AsyncNamespacePage[NamespaceSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "page_size": page_size,
                        "prefix": prefix,
                    },
                    client_namespaces_params.ClientNamespacesParams,
                ),
            ),
            model=NamespaceSummary,
        )

    def _get_default_namespace_path_param(self) -> str:
        from_client = self.default_namespace
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing default_namespace argument; Please provide it at the client level, e.g. AsyncTurbopuffer(default_namespace='abcd') or per method."
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class TurbopufferWithRawResponse:
    _client: Turbopuffer

    def __init__(self, client: Turbopuffer) -> None:
        self._client = client
        self.namespaces = to_raw_response_wrapper(
            client.namespaces,
        )

    def namespace(self, namespace: str) -> NamespaceWithRawResponse:
        """Create a namespace resource."""
        return NamespaceWithRawResponse(self._client.with_options(default_namespace=namespace))


class AsyncTurbopufferWithRawResponse:
    _client: AsyncTurbopuffer

    def __init__(self, client: AsyncTurbopuffer) -> None:
        self._client = client
        self.namespaces = async_to_raw_response_wrapper(
            client.namespaces,
        )

    def namespace(self, namespace: str) -> AsyncNamespaceWithRawResponse:
        """Create a namespace resource."""
        return AsyncNamespaceWithRawResponse(self._client.with_options(default_namespace=namespace))


class TurbopufferWithStreamedResponse:
    _client: Turbopuffer

    def __init__(self, client: Turbopuffer) -> None:
        self._client = client
        self.namespaces = to_streamed_response_wrapper(
            client.namespaces,
        )

    def namespace(self, namespace: str) -> NamespaceWithStreamingResponse:
        """Create a namespace resource."""
        return NamespaceWithStreamingResponse(self._client.with_options(default_namespace=namespace))


class AsyncTurbopufferWithStreamedResponse:
    _client: AsyncTurbopuffer

    def __init__(self, client: AsyncTurbopuffer) -> None:
        self._client = client
        self.namespaces = async_to_streamed_response_wrapper(
            client.namespaces,
        )

    def namespace(self, namespace: str) -> AsyncNamespaceWithStreamingResponse:
        """Create a namespace resource."""
        return AsyncNamespaceWithStreamingResponse(self._client.with_options(default_namespace=namespace))


Client = Turbopuffer

AsyncClient = AsyncTurbopuffer
