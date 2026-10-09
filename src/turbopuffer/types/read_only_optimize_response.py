# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .write_billing import WriteBilling

__all__ = ["ReadOnlyOptimizeResponse"]


class ReadOnlyOptimizeResponse(BaseModel):
    """The response to a successful read-only optimize request."""

    status: Literal["OK", "ACCEPTED"]
    """
    `OK` if the namespace is optimized for a read-only workload, or `ACCEPTED` if
    the optimization is in progress.
    """

    billing: Optional[WriteBilling] = None
    """The billing information for a write request."""

    message: Optional[str] = None
