# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .attribute_type import AttributeType
from .full_text_search_param import FullTextSearchParam

__all__ = ["AttributeSchemaParam"]


class AttributeSchemaParam(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: FullTextSearchParam
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: AttributeType
    """The data type of the attribute."""
