# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["OperationError", "Detail"]


class Detail(BaseModel):
    """The response to an unsuccessful request."""

    error: str
    """The error message."""

    status: Literal["error"]
    """The status of the request."""


class OperationError(BaseModel):
    detail: Detail
    """The response to an unsuccessful request."""

    status_code: int
    """The HTTP status code of the operation's error."""
