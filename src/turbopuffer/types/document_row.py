# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .id import ID
from .._models import BaseModel

__all__ = ["DocumentRow"]


class DocumentRow(BaseModel):
    id: Optional[ID] = None
    """An identifier for a document."""

    attributes: Optional[Dict[str, object]] = None
    """The attributes attached to the document."""

    vector: Optional[List[float]] = None
    """A vector describing the document."""
