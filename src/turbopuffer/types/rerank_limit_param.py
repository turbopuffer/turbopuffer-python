# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["RerankLimitParam"]


class RerankLimitParam(TypedDict, total=False):
    """Limits the total number of reranked documents returned."""

    total: Required[int]
    """Limits the total number of documents returned after reranking."""
