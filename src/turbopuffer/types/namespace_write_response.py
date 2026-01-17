# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .id import ID
from .._models import BaseModel
from .write_billing import WriteBilling

__all__ = ["NamespaceWriteResponse"]


class NamespaceWriteResponse(BaseModel):
    """The response to a successful write request."""

    billing: WriteBilling
    """The billing information for a write request."""

    message: str
    """A message describing the result of the write request."""

    rows_affected: int
    """The number of rows affected by the write request."""

    status: Literal["OK"]
    """The status of the request."""

    deleted_ids: Optional[List[ID]] = None
    """The IDs of documents that were deleted.

    Only included when `return_affected_ids` is true and at least one document was
    deleted.
    """

    patched_ids: Optional[List[ID]] = None
    """The IDs of documents that were patched.

    Only included when `return_affected_ids` is true and at least one document was
    patched.
    """

    rows_deleted: Optional[int] = None
    """The number of rows deleted by the write request."""

    rows_patched: Optional[int] = None
    """The number of rows patched by the write request."""

    rows_remaining: Optional[bool] = None
    """Whether more documents match the filter for partial operations."""

    rows_upserted: Optional[int] = None
    """The number of rows upserted by the write request."""

    upserted_ids: Optional[List[ID]] = None
    """The IDs of documents that were upserted.

    Only included when `return_affected_ids` is true and at least one document was
    upserted.
    """
