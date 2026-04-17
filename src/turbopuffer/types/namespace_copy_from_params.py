# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .copy_from_namespace_params import CopyFromNamespaceParams

__all__ = ["NamespaceCopyFromParams"]


class NamespaceCopyFromParams(TypedDict, total=False):
    namespace: str

    copy_from_namespace: Required[CopyFromNamespaceParams]
    """The namespace to copy documents from."""
