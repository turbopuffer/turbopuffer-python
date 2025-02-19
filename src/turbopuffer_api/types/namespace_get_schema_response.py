# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "NamespaceGetSchemaResponse",
    "NamespaceGetSchemaResponseItem",
    "NamespaceGetSchemaResponseItemFullTextSearch",
    "NamespaceGetSchemaResponseItemFullTextSearchFullTextSearchConfig",
]


class NamespaceGetSchemaResponseItemFullTextSearchFullTextSearchConfig(BaseModel):
    case_sensitive: Optional[bool] = None
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

    language: Optional[
        Literal[
            "arabic",
            "danish",
            "dutch",
            "english",
            "finnish",
            "french",
            "german",
            "greek",
            "hungarian",
            "italian",
            "norwegian",
            "portuguese",
            "romanian",
            "russian",
            "spanish",
            "swedish",
            "tamil",
            "turkish",
        ]
    ] = None
    """The language of the text. Defaults to `english`."""

    remove_stopwords: Optional[bool] = None
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: Optional[bool] = None
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """


NamespaceGetSchemaResponseItemFullTextSearch: TypeAlias = Union[
    bool, NamespaceGetSchemaResponseItemFullTextSearchFullTextSearchConfig
]


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
    """The data type of the attribute."""


NamespaceGetSchemaResponse: TypeAlias = Dict[str, List[NamespaceGetSchemaResponseItem]]
