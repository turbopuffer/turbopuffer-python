# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["NamespaceStartCopyFromResponse"]


class NamespaceStartCopyFromResponse(BaseModel):
    token: str
    """The token identifying the copy operation."""
