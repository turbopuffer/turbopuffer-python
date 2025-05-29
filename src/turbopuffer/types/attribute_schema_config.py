# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .attribute_type import AttributeType
from .full_text_search import FullTextSearch

__all__ = ["AttributeSchemaConfig"]


class AttributeSchemaConfig(BaseModel):
    ann: Optional[bool] = None
    """Whether to create an approximate nearest neighbor index for the attribute."""

    filterable: Optional[bool] = None
    """Whether or not the attributes can be used in filters."""

    full_text_search: Optional[FullTextSearch] = None
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Optional[AttributeType] = None
    """The data type of the attribute.

    Valid values: string, int, uint, uuid, datetime, bool, []string, []int, []uint,
    []uuid, []datetime, [DIMS]f16, [DIMS]f32.
    """
