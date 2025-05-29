# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel
from .write_billing import WriteBilling

__all__ = ["NamespaceWriteResponse"]


class NamespaceWriteResponse(BaseModel):
    billing: WriteBilling
    """The billing information for a write request."""

    message: str
    """A message describing the result of the write request."""

    rows_affected: int
    """The number of rows affected by the write request."""

    status: Literal["OK"]
    """The status of the request."""
