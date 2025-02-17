# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["NamespaceSummary"]


class NamespaceSummary(BaseModel):
    id: Optional[str] = None
    """The namespace ID."""
