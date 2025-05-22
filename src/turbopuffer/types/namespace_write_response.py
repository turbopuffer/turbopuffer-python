# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["NamespaceWriteResponse", "Billing", "BillingQuery"]


class BillingQuery(BaseModel):
    billable_logical_bytes_queried: int
    """The number of billable logical bytes queried from the namespace."""

    billable_logical_bytes_returned: int
    """The number of billable logical bytes returned from the query."""


class Billing(BaseModel):
    billable_logical_bytes_written: int
    """The number of billable logical bytes written to the namespace."""

    query: Optional[BillingQuery] = None
    """The billing information for a query."""


class NamespaceWriteResponse(BaseModel):
    billing: Billing

    message: str
    """A message describing the result of the write request."""

    rows_affected: int
    """The number of rows affected by the write request."""

    status: Literal["OK"]
    """The status of the request."""
