# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .query_billing import QueryBilling

__all__ = ["WriteBilling"]


class WriteBilling(BaseModel):
    """The billing information for a write request."""

    billable_logical_bytes_written: int
    """The number of billable logical bytes written to the namespace."""

    query: Optional[QueryBilling] = None
    """The billing information for a query."""
