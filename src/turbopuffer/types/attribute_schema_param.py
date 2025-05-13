# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, TypeAlias, TypedDict

from .full_text_search_config_param import FullTextSearchConfigParam

__all__ = ["AttributeSchemaParam", "FullTextSearch"]

FullTextSearch: TypeAlias = Union[bool, FullTextSearchConfigParam]


class AttributeSchemaParam(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: FullTextSearch
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]
    """The data type of the attribute.

    - `string` - A string.
    - `uint` - An unsigned integer.
    - `uuid` - A UUID.
    - `bool` - A boolean.
    - `[]string` - An array of strings.
    - `[]uint` - An array of unsigned integers.
    - `[]uuid` - An array of UUIDs.
    """
