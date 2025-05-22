# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["NamespaceRecallResponse"]


class NamespaceRecallResponse(BaseModel):
    avg_ann_count: float
    """
    The average number of documents retrieved by the approximate nearest neighbor
    searches.
    """

    avg_exhaustive_count: float
    """The average number of documents retrieved by the exhaustive searches."""

    avg_recall: float
    """The average recall of the queries."""
