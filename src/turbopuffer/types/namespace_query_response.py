# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .row import Row
from .._models import BaseModel
from .query_billing import QueryBilling
from .aggregation_group import AggregationGroup
from .query_performance import QueryPerformance

__all__ = ["NamespaceQueryResponse"]


class NamespaceQueryResponse(BaseModel):
    """The result of a query."""

    billing: QueryBilling
    """The billing information for a query."""

    performance: QueryPerformance
    """The performance information for a query."""

    aggregation_groups: Optional[List[AggregationGroup]] = None
    """
    One object per aggregation group, with its group key and the value of each
    requested aggregation. Only present when `aggregate_by` and `group_by` are both
    set.
    """

    aggregations: Optional[Dict[str, object]] = None
    """The value of each requested aggregation, keyed by its label.

    Only present when `aggregate_by` is set without `group_by`.
    """

    rows: Optional[List[Row]] = None
    """The documents that matched the query, ordered by `rank_by`.

    Only present when `rank_by` is set.
    """
