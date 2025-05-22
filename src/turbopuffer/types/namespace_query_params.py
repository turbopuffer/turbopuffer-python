# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .distance_metric import DistanceMetric
from .include_attributes_param import IncludeAttributesParam

__all__ = ["NamespaceQueryParams", "Consistency"]


class NamespaceQueryParams(TypedDict, total=False):
    namespace: str

    rank_by: Required[object]
    """How to rank the documents in the namespace."""

    top_k: Required[int]
    """The number of results to return."""

    consistency: Consistency
    """The consistency level for a query."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    filters: object
    """Exact filters for attributes to refine search results for.

    Think of it as a SQL WHERE clause.
    """

    include_attributes: IncludeAttributesParam
    """Whether to include attributes in the response."""

    vector_encoding: Literal["float", "base64"]
    """The encoding to use for vectors in the response."""


class Consistency(TypedDict, total=False):
    level: Literal["strong", "eventual"]
    """The query's consistency level.

    - `strong` - Strong consistency. Requires a round-trip to object storage to
      fetch the latest writes.
    - `eventual` - Eventual consistency. Does not require a round-trip to object
      storage, but may not see the latest writes.
    """
