from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `turbopuffer.resources` module.

    This is used so that we can lazily import `turbopuffer.resources` only when
    needed *and* so that users can just import `turbopuffer` and reference `turbopuffer.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("turbopuffer.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
