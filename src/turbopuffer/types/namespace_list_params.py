# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["NamespaceListParams"]


class NamespaceListParams(TypedDict, total=False):
    cursor: str
    """Retrieve the next page of results."""

    page_size: int
    """Limit the number of results per page."""

    prefix: str
    """Retrieve only the namespaces that match the prefix."""
