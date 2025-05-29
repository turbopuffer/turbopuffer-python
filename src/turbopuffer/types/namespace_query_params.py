# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, TypedDict

from .custom import Filter, AggregateBy
from .distance_metric import DistanceMetric
from .vector_encoding import VectorEncoding
from .include_attributes_param import IncludeAttributesParam

__all__ = ["NamespaceQueryParams", "Consistency"]


class NamespaceQueryParams(TypedDict, total=False):
    namespace: str

    aggregate_by: Dict[str, AggregateBy]
    """
    Aggregations to compute over all documents in the namespace that match the
    filters.
    """

    consistency: Consistency
    """The consistency level for a query."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    filters: Filter
    """Exact filters for attributes to refine search results for.

    Think of it as a SQL WHERE clause.
    """

    include_attributes: IncludeAttributesParam
    """Whether to include attributes in the response."""

    rank_by: object
    """How to rank the documents in the namespace."""

    top_k: int
    """The number of results to return."""

    vector_encoding: VectorEncoding
    """The encoding to use for vectors in the response."""


class Consistency(TypedDict, total=False):
    level: Literal["strong", "eventual"]
    """The query's consistency level.

    - `strong` - Strong consistency. Requires a round-trip to object storage to
      fetch the latest writes.
    - `eventual` - Eventual consistency. Does not require a round-trip to object
      storage, but may not see the latest writes.
    """
