# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional

from pydantic import Field as FieldInfo

from .id import ID
from .._models import BaseModel

__all__ = ["DocumentRow"]


class DocumentRow(BaseModel):
    id: Optional[ID] = None
    """An identifier for a document."""

    additional_properties: Optional[object] = FieldInfo(alias="additionalProperties", default=None)
    """The attributes attached to the document."""

    vector: Union[List[float], str, None] = None
    """A vector describing the document."""
