# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, List, Union, Optional

from .id import ID
from ..._models import BaseModel

__all__ = ["DocumentRow"]


class DocumentRow(BaseModel):
    id: Optional[ID] = None
    """An identifier for a document."""

    vector: Union[List[float], str, None] = None
    """A vector describing the document."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
