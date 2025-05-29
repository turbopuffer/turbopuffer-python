# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .attribute_type_param import AttributeTypeParam
from .full_text_search_param import FullTextSearchParam

__all__ = ["AttributeSchemaConfigParam"]


class AttributeSchemaConfigParam(TypedDict, total=False):
    ann: bool
    """Whether to create an approximate nearest neighbor index for the attribute."""

    filterable: bool
    """Whether or not the attributes can be used in filters."""

    full_text_search: FullTextSearchParam
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: AttributeTypeParam
    """The data type of the attribute."""
