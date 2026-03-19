# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["BranchFromNamespaceParams", "BranchFromNamespaceConfig"]


class BranchFromNamespaceConfig(TypedDict, total=False):
    source_namespace: Required[str]
    """The namespace to create an instant, copy-on-write clone of."""


BranchFromNamespaceParams: TypeAlias = Union[str, BranchFromNamespaceConfig]
