# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, TypedDict

__all__ = ["NamespaceQueryParams", "Consistency"]


class NamespaceQueryParams(TypedDict, total=False):
    consistency: Consistency
    """Consistency level for the query."""

    distance_metric: Literal["cosine_distance", "euclidean_squared"]
    """Required if a query vector is provided."""

    filters: Union[Iterable[object], object]
    """Filters to narrow down search results (e.g., attribute conditions)."""

    include_attributes: Union[List[str], bool]
    """A list of attribute names to return or `true` to include all attributes."""

    include_vectors: bool
    """Whether to include the stored vectors in the response."""

    rank_by: List[str]
    """
    Parameter to order results (either BM25 for full-text search or attribute-based
    ordering).
    """

    top_k: int
    """Number of results to return."""

    vector: Iterable[float]
    """The query vector."""


class Consistency(TypedDict, total=False):
    level: Literal["strong", "eventual"]
