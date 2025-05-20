# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["NamespaceExportParams"]


class NamespaceExportParams(TypedDict, total=False):
    namespace: str

    cursor: str
    """Retrieve the next page of results."""
