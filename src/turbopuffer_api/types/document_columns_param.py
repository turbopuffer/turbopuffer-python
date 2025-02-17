# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, TypeAlias, TypedDict

__all__ = [
    "DocumentColumnsParam",
    "Attribute",
    "AttributeFullTextSearch",
    "AttributeFullTextSearchFullTextSearchConfig",
]


class AttributeFullTextSearchFullTextSearchConfig(TypedDict, total=False):
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


AttributeFullTextSearch: TypeAlias = Union[bool, AttributeFullTextSearchFullTextSearchConfig]


class Attribute(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: AttributeFullTextSearch
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]
    """The data type of the attribute."""


class DocumentColumnsParam(TypedDict, total=False):
    attributes: Dict[str, Iterable[Attribute]]
    """The attributes attached to each of the documents."""

    ids: List[Union[str, int]]
    """The IDs of the documents."""

    vectors: Iterable[Union[float, Iterable[float], None]]
    """Vectors describing each of the documents."""
