# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .custom import Expr, GroupBy
from .._types import SequenceNotStr
from .limit_param import LimitParam
from .distance_metric import DistanceMetric
from .vector_encoding import VectorEncoding
from .include_attributes_param import IncludeAttributesParam

__all__ = ["NamespaceMultiQueryParams", "Query", "QueryLimit", "Consistency"]


class NamespaceMultiQueryParams(TypedDict, total=False):
    namespace: str

    queries: Required[Iterable[Query]]

    consistency: Consistency
    """The consistency level for a query."""

    rerank_by: object
    """How to combine the rows returned by each sub-query into a single ranked list."""

    vector_encoding: VectorEncoding
    """The encoding to use for vectors in the response."""


QueryLimit: TypeAlias = Union[int, LimitParam]


class Query(TypedDict, total=False):
    """Query, filter, full-text search and vector search documents."""

    aggregate_by: Dict[str, object]
    """
    Aggregations to compute over all documents in the namespace that match the
    filters.
    """

    compute_attributes: Dict[str, Expr]
    """Computes additional values on documents returned by a query.

    Each key is the name of the computed attribute; each value is an expression
    describing how to compute it.
    """

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    exclude_attributes: SequenceNotStr[str]
    """List of attribute names to exclude from the response.

    All other attributes will be included in the response.
    """

    filters: object
    """Exact filters for attributes to refine search results for.

    Think of it as a SQL WHERE clause.
    """

    group_by: Iterable[GroupBy]
    """
    Groups documents by the specified attributes (the "group key") before computing
    aggregates. Aggregates are computed separately for each group.
    """

    include_attributes: IncludeAttributesParam
    """Whether to include attributes in the response."""

    limit: QueryLimit
    """Limits the documents returned by a query."""

    rank_by: object
    """How to rank the documents in the namespace."""

    top_k: int
    """The number of results to return."""


class Consistency(TypedDict, total=False):
    """The consistency level for a query."""

    level: Literal["strong", "eventual"]
    """The query's consistency level.

    - `strong` - Strong consistency. Requires a round-trip to object storage to
      fetch the latest writes.
    - `eventual` - Eventual consistency. Does not require a round-trip to object
      storage, but may not see the latest writes.
    """
