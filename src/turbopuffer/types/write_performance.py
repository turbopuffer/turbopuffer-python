# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["WritePerformance"]


class WritePerformance(BaseModel):
    """The performance information for a write request."""

    server_total_ms: int
    """Request time measured on the server, in milliseconds."""
