# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .attribute_type import AttributeType
from .full_text_search_config import FullTextSearchConfig

__all__ = ["AttributeSchema"]


class AttributeSchema(BaseModel):
    filterable: Optional[bool] = None
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: Optional[FullTextSearchConfig] = None
    """Configuration options for full-text search."""

    type: Optional[AttributeType] = None
    """The data type of the attribute."""
