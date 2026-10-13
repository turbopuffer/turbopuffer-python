# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["RerankModelParams"]


class RerankModelParams(TypedDict, total=False):
    """Rerank retrieved candidates with a model."""

    attribute: Required[str]
    """The string attribute to score.

    Must be included in `include_attributes` in every query.
    """

    model: Required[str]
    """Which reranking model to use."""

    query: Required[str]
    """The query text to score each document against."""
