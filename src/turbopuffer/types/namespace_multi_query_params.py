# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, TypedDict

from .distance_metric import DistanceMetric

__all__ = ["NamespaceMultiQueryParams", "Consistency", "Query"]


class NamespaceMultiQueryParams(TypedDict, total=False):
    namespace: str

    consistency: Consistency
    """The consistency level for a query."""

    queries: Iterable[Query]

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


class Query(TypedDict, total=False):
    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    filters: object

    include_attributes: Union[bool, List[str]]
    """Whether to include attributes in the response."""

    rank_by: Union[
        Iterable[object],
        Iterable[object],
        Iterable[object],
        Iterable[object],
        Iterable[object],
        Iterable[object],
        Iterable[object],
    ]

    top_k: int
    """The number of results to return."""
