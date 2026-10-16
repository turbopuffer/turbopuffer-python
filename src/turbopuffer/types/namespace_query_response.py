# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .row import Row
from .._models import BaseModel
from .query_billing import QueryBilling
from .aggregation_group import AggregationGroup
from .query_performance import QueryPerformance

__all__ = ["NamespaceQueryResponse"]


class NamespaceQueryResponse(BaseModel):
    """The result of a query.

    With `aggregate_by`, `aggregations` maps each aggregation's label to its value. With `group_by` as well, `aggregation_groups` holds one object per group instead, with its group key and the value of each aggregation.
    """

    billing: QueryBilling
    """The billing information for a query."""

    performance: QueryPerformance
    """The performance information for a query."""

    aggregation_groups: Optional[List[AggregationGroup]] = None

    aggregations: Optional[Dict[str, object]] = None

    rows: Optional[List[Row]] = None
    """The documents that matched the query, ordered by `rank_by`.

    Only present when `rank_by` is set.
    """
