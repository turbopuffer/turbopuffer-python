# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .namespace_summary import NamespaceSummary

__all__ = ["ListNamespacesResponse"]


class ListNamespacesResponse(BaseModel):
    namespaces: Optional[List[NamespaceSummary]] = None
    """The list of namespaces."""

    next_cursor: Optional[str] = None
    """The cursor to use to retrieve the next page of results."""
