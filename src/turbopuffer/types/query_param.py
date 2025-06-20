# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from .distance_metric import DistanceMetric
from .include_attributes_param import IncludeAttributesParam

__all__ = ["QueryParam"]


class QueryParam(TypedDict, total=False):
    aggregate_by: Dict[str, object]
    """
    Aggregations to compute over all documents in the namespace that match the
    filters.
    """

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    filters: object
    """Exact filters for attributes to refine search results for.

    Think of it as a SQL WHERE clause.
    """

    include_attributes: IncludeAttributesParam
    """Whether to include attributes in the response."""

    rank_by: object
    """How to rank the documents in the namespace."""

    top_k: int
    """The number of results to return."""
