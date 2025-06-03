# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Optional

from .id import ID
from .vector import Vector
from .._models import BaseModel

__all__ = ["Row"]


class Row(BaseModel):
    id: ID
    """An identifier for a document."""

    vector: Optional[Vector] = None
    """A vector embedding associated with a document."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
