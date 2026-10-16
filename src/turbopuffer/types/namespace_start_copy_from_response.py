# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["NamespaceStartCopyFromResponse"]


class NamespaceStartCopyFromResponse(BaseModel):
    """The response to a successful request to start a copy."""

    token: str
    """The token identifying the copy operation."""
