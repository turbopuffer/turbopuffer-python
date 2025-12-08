# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["NamespaceSummary"]


class NamespaceSummary(BaseModel):
    """A summary of a namespace."""

    id: str
    """The namespace ID."""
