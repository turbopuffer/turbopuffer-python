from __future__ import annotations

from typing import TYPE_CHECKING

from ..resources import namespaces

if TYPE_CHECKING:
    from .._client import Turbopuffer, AsyncTurbopuffer

class Namespace(namespaces.NamespacesResource):
    def __init__(self, client: Turbopuffer) -> None:
        super().__init__(client)

class AsyncNamespace(namespaces.AsyncNamespacesResource):
    def __init__(self, client: AsyncTurbopuffer) -> None:
        super().__init__(client)
