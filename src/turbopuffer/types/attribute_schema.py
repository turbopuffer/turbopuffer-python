# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .full_text_search_config import FullTextSearchConfig

__all__ = ["AttributeSchema", "FullTextSearch"]

FullTextSearch: TypeAlias = Union[bool, FullTextSearchConfig]


class AttributeSchema(BaseModel):
    filterable: Optional[bool] = None
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: Optional[FullTextSearch] = None
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Optional[Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]] = None
    """The data type of the attribute."""
