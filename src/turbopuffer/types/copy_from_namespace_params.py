# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["CopyFromNamespaceParams", "CopyFromNamespaceConfig"]


class CopyFromNamespaceConfig(TypedDict, total=False):
    source_namespace: Required[str]
    """The namespace to copy documents from."""

    source_api_key: str
    """(Optional) An API key for the organization containing the source namespace"""

    source_region: str
    """(Optional) The region of the source namespace."""


CopyFromNamespaceParams: TypeAlias = Union[str, CopyFromNamespaceConfig]
