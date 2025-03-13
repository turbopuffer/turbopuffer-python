# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, TypedDict

from .distance_metric import DistanceMetric

__all__ = ["NamespaceQueryParams", "Consistency"]


class NamespaceQueryParams(TypedDict, total=False):
    consistency: Consistency
    """The consistency level for a query."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    filters: object
    """Exact filters for attributes to refine search results for.

    Think of it as a SQL WHERE clause.
    """

    include_attributes: Union[bool, List[str]]
    """Whether to include attributes in the response."""

    include_vectors: bool
    """Whether to return vectors for the search results.

    Vectors are large and slow to deserialize on the client, so use this option only
    if you need them.
    """

    rank_by: object
    """The attribute to rank the results by. Cannot be specified with `vector`."""

    top_k: int
    """The number of results to return."""

    vector: Iterable[float]
    """
    A vector to search for. It must have the same number of dimensions as the
    vectors in the namespace. Cannot be specified with `rank_by`.
    """


class Consistency(TypedDict, total=False):
    level: Literal["strong", "eventual"]
    """The query's consistency level.

    - `strong` - Strong consistency. Requires a round-trip to object storage to
      fetch the latest writes.
    - `eventual` - Eventual consistency. Does not require a round-trip to object
      storage, but may not see the latest writes.
    """
