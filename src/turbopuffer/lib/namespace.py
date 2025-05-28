from __future__ import annotations

from typing import TYPE_CHECKING, Protocol
from typing_extensions import override

from ..resources import namespaces

if TYPE_CHECKING:
    from .._client import Turbopuffer, AsyncTurbopuffer


class NamespaceProtocol(Protocol):
    _client: Turbopuffer | AsyncTurbopuffer
    id: str


class NamespaceMixin:
    @property
    def id(self: NamespaceProtocol) -> str:
        assert self._client.default_namespace is not None
        return self._client.default_namespace

    @override
    def __str__(self: NamespaceProtocol) -> str:
        return f"tpuf-namespace:{self.id}"


class Namespace(namespaces.NamespacesResource, NamespaceMixin):
    def __init__(self, client: Turbopuffer) -> None:
        super().__init__(client)


class NamespaceWithRawResponse(namespaces.NamespacesResourceWithRawResponse, NamespaceMixin):
    def __init__(self, client: Turbopuffer) -> None:
        super().__init__(namespaces.NamespacesResource(client))


class NamespaceWithStreamingResponse(namespaces.NamespacesResourceWithStreamingResponse, NamespaceMixin):
    def __init__(self, client: Turbopuffer) -> None:
        super().__init__(namespaces.NamespacesResource(client))


class AsyncNamespace(namespaces.AsyncNamespacesResource, NamespaceMixin):
    def __init__(self, client: AsyncTurbopuffer) -> None:
        super().__init__(client)


class AsyncNamespaceWithRawResponse(namespaces.AsyncNamespacesResourceWithRawResponse, NamespaceMixin):
    def __init__(self, client: AsyncTurbopuffer) -> None:
        super().__init__(namespaces.AsyncNamespacesResource(client))


class AsyncNamespaceWithStreamingResponse(namespaces.AsyncNamespacesResourceWithStreamingResponse, NamespaceMixin):
    def __init__(self, client: AsyncTurbopuffer) -> None:
        super().__init__(namespaces.AsyncNamespacesResource(client))
