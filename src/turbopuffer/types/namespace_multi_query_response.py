# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .row import Row
from .._models import BaseModel
from .query_billing import QueryBilling
from .aggregation_group import AggregationGroup
from .query_performance import QueryPerformance

__all__ = ["NamespaceMultiQueryResponse", "Result"]


class Result(BaseModel):
    aggregation_groups: Optional[List[AggregationGroup]] = None

    aggregations: Optional[Dict[str, object]] = None

    rows: Optional[List[Row]] = None


class NamespaceMultiQueryResponse(BaseModel):
    """The result of a multi-query."""

    billing: QueryBilling
    """The billing information for a query."""

    performance: QueryPerformance
    """The performance information for a query."""

    results: List[Result]
