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

    aggregations: Optional[Dict[str, object]] = None

    rows: Optional[List[Row]] = None
