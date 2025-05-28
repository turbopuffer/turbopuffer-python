# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .attribute_type import AttributeType
from .full_text_search_config_param import FullTextSearchConfigParam

__all__ = ["AttributeSchemaParam"]


class AttributeSchemaParam(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: FullTextSearchConfigParam
    """Configuration options for full-text search."""

    type: AttributeType
    """The data type of the attribute."""
