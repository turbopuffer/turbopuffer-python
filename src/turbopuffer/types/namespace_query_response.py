# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .document_row import DocumentRow
from .query_billing import QueryBilling
from .query_performance import QueryPerformance

__all__ = ["NamespaceQueryResponse"]


class NamespaceQueryResponse(BaseModel):
    billing: QueryBilling
    """The billing information for a query."""

    performance: QueryPerformance
    """The performance information for a query."""

    aggregations: Optional[Dict[str, object]] = None

    rows: Optional[List[DocumentRow]] = None
