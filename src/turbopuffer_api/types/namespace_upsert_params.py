# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

from .document_row_param import DocumentRowParam

__all__ = [
    "NamespaceUpsertParams",
    "UpsertColumnar",
    "UpsertColumnarAttribute",
    "UpsertColumnarAttributeFullTextSearch",
    "UpsertColumnarAttributeFullTextSearchFullTextSearchConfig",
    "UpsertColumnarSchema",
    "UpsertColumnarSchemaFullTextSearch",
    "UpsertColumnarSchemaFullTextSearchFullTextSearchConfig",
    "UpsertRowBased",
    "UpsertRowBasedSchema",
    "UpsertRowBasedSchemaFullTextSearch",
    "UpsertRowBasedSchemaFullTextSearchFullTextSearchConfig",
    "CopyFromNamespace",
    "DeleteByFilter",
]


class UpsertColumnar(TypedDict, total=False):
    attributes: Dict[str, Iterable[UpsertColumnarAttribute]]
    """The attributes attached to each of the documents."""

    distance_metric: Literal["cosine_distance", "euclidean_squared"]
    """A function used to calculate vector similarity.

    - `cosine_distance` - Defined as `1 - cosine_similarity` and ranges from 0 to 2.
      Lower is better.
    - `euclidean_squared` - Defined as `sum((x - y)^2)`. Lower is better.
    """

    ids: List[Union[str, int]]
    """The IDs of the documents."""

    schema: Dict[str, Iterable[UpsertColumnarSchema]]
    """The schema of the attributes attached to the documents."""

    vectors: Iterable[Optional[Iterable[float]]]
    """Vectors describing each of the documents."""


class UpsertColumnarAttributeFullTextSearchFullTextSearchConfig(TypedDict, total=False):
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


UpsertColumnarAttributeFullTextSearch: TypeAlias = Union[
    bool, UpsertColumnarAttributeFullTextSearchFullTextSearchConfig
]


class UpsertColumnarAttribute(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: UpsertColumnarAttributeFullTextSearch
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]
    """The data type of the attribute."""


class UpsertColumnarSchemaFullTextSearchFullTextSearchConfig(TypedDict, total=False):
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


UpsertColumnarSchemaFullTextSearch: TypeAlias = Union[bool, UpsertColumnarSchemaFullTextSearchFullTextSearchConfig]


class UpsertColumnarSchema(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: UpsertColumnarSchemaFullTextSearch
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]
    """The data type of the attribute."""


class UpsertRowBased(TypedDict, total=False):
    distance_metric: Literal["cosine_distance", "euclidean_squared"]
    """A function used to calculate vector similarity.

    - `cosine_distance` - Defined as `1 - cosine_similarity` and ranges from 0 to 2.
      Lower is better.
    - `euclidean_squared` - Defined as `sum((x - y)^2)`. Lower is better.
    """

    schema: Dict[str, Iterable[UpsertRowBasedSchema]]
    """The schema of the attributes attached to the documents."""

    upserts: Iterable[DocumentRowParam]


class UpsertRowBasedSchemaFullTextSearchFullTextSearchConfig(TypedDict, total=False):
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


UpsertRowBasedSchemaFullTextSearch: TypeAlias = Union[bool, UpsertRowBasedSchemaFullTextSearchFullTextSearchConfig]


class UpsertRowBasedSchema(TypedDict, total=False):
    filterable: bool
    """Whether or not the attributes can be used in filters/WHERE clauses."""

    full_text_search: UpsertRowBasedSchemaFullTextSearch
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    type: Literal["string", "uint", "uuid", "bool", "[]string", "[]uint", "[]uuid"]
    """The data type of the attribute."""


class CopyFromNamespace(TypedDict, total=False):
    copy_from_namespace: str
    """The namespace to copy documents from."""


class DeleteByFilter(TypedDict, total=False):
    delete_by_filter: object


NamespaceUpsertParams: TypeAlias = Union[UpsertColumnar, UpsertRowBased, CopyFromNamespace, DeleteByFilter]
