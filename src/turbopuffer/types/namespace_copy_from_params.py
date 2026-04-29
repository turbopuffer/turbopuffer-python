# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["NamespaceCopyFromParams"]


class NamespaceCopyFromParams(TypedDict, total=False):
    namespace: str

    source_namespace: Required[str]
    """The namespace to copy documents from."""

    source_api_key: str
    """(Optional) An API key for the organization containing the source namespace"""

    source_region: str
    """(Optional) The region of the source namespace."""
