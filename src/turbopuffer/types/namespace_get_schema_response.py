# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .full_text_search_config import FullTextSearchConfig

__all__ = [
    "NamespaceGetSchemaResponse",
    "NamespaceGetSchemaResponseItem",
    "NamespaceGetSchemaResponseItemFullTextSearch",
]

NamespaceGetSchemaResponseItemFullTextSearch: TypeAlias = Union[bool, FullTextSearchConfig]


class NamespaceGetSchemaResponseItem(BaseModel):
    filterable: Optional[bool] = None
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: Optional[NamespaceGetSchemaResponseItemFullTextSearch] = None
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Optional[Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]] = None
    """The data type of the attribute.

    - `string` - A string.
    - `uint` - An unsigned integer.
    - `uuid` - A UUID.
    - `bool` - A boolean.
    - `[]string` - An array of strings.
    - `[]uint` - An array of unsigned integers.
    """


NamespaceGetSchemaResponse: TypeAlias = Dict[str, List[NamespaceGetSchemaResponseItem]]
