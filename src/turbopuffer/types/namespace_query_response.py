# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional

from .._models import BaseModel

__all__ = ["NamespaceQueryResponse", "Vector"]


class Vector(BaseModel):
    id: Union[str, int, None] = None

    attributes: Optional[object] = None

    dist: Optional[float] = None
    """The distance (or relevance) score."""

    vector: Optional[List[float]] = None


class NamespaceQueryResponse(BaseModel):
    vectors: Optional[List[Vector]] = None
    """Array of search result objects."""
