# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["QueryBilling"]


class QueryBilling(BaseModel):
    billable_logical_bytes_queried: int
    """The number of billable logical bytes queried from the namespace."""

    billable_logical_bytes_returned: int
    """The number of billable logical bytes returned from the query."""
