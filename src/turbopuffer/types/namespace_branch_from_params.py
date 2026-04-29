# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["NamespaceBranchFromParams"]


class NamespaceBranchFromParams(TypedDict, total=False):
    namespace: str

    source_namespace: Required[str]
    """The namespace to create an instant, copy-on-write clone of."""
