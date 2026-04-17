# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .branch_from_namespace_params import BranchFromNamespaceParams

__all__ = ["NamespaceBranchFromParams"]


class NamespaceBranchFromParams(TypedDict, total=False):
    namespace: str

    branch_from_namespace: Required[BranchFromNamespaceParams]
    """The namespace to create an instant, copy-on-write clone of."""
