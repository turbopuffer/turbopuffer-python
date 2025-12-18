# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .row import Row
from .._models import BaseModel

__all__ = ["NamespaceRecallResponse", "GroundTruth"]


class GroundTruth(BaseModel):
    nearest_neighbors: List[Row]
    """The true nearest neighbors with their distances and vectors."""

    query_vector: List[float]
    """The query vector used for this search."""


class NamespaceRecallResponse(BaseModel):
    """The response to a successful cache warm request."""

    avg_ann_count: float
    """
    The average number of documents retrieved by the approximate nearest neighbor
    searches.
    """

    avg_exhaustive_count: float
    """The average number of documents retrieved by the exhaustive searches."""

    avg_recall: float
    """The average recall of the queries."""

    ground_truth: Optional[List[GroundTruth]] = None
    """Ground truth data including query vectors and true nearest neighbors.

    Only included when include_ground_truth is true.
    """
