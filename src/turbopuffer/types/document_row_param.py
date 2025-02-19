# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

__all__ = ["DocumentRowParam", "Attributes", "AttributesFullTextSearch", "AttributesFullTextSearchFullTextSearchConfig"]


class AttributesFullTextSearchFullTextSearchConfig(TypedDict, total=False):
    case_sensitive: bool
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

    language: Literal[
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
    """The language of the text. Defaults to `english`."""

    remove_stopwords: bool
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: bool
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """


AttributesFullTextSearch: TypeAlias = Union[bool, AttributesFullTextSearchFullTextSearchConfig]


class Attributes(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: AttributesFullTextSearch
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]
    """The data type of the attribute."""


class DocumentRowParam(TypedDict, total=False):
    id: Union[str, int]
    """An identifier for a document."""

    attributes: Dict[str, Attributes]
    """The attributes attached to the document."""

    vector: Optional[Iterable[float]]
    """A vector describing the document."""
