# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .id_param import IDParam
from .distance_metric import DistanceMetric
from .document_row_param import DocumentRowParam
from .full_text_search_config_param import FullTextSearchConfigParam

__all__ = [
    "NamespaceUpsertParams",
    "UpsertColumnar",
    "UpsertColumnarSchema",
    "UpsertColumnarSchemaFullTextSearch",
    "UpsertRowBased",
    "UpsertRowBasedSchema",
    "UpsertRowBasedSchemaFullTextSearch",
    "CopyFromNamespace",
    "DeleteByFilter",
]


class UpsertColumnar(TypedDict, total=False):
    distance_metric: Required[DistanceMetric]
    """A function used to calculate vector similarity."""

    attributes: Dict[str, Iterable[Dict[str, object]]]
    """The attributes attached to each of the documents."""

    ids: List[IDParam]
    """The IDs of the documents."""

    schema: Dict[str, Iterable[UpsertColumnarSchema]]
    """The schema of the attributes attached to the documents."""

    vectors: Iterable[Optional[Iterable[float]]]
    """Vectors describing each of the documents."""


UpsertColumnarSchemaFullTextSearch: TypeAlias = Union[bool, FullTextSearchConfigParam]


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
    """The data type of the attribute.

    - `string` - A string.
    - `uint` - An unsigned integer.
    - `uuid` - A UUID.
    - `bool` - A boolean.
    - `[]string` - An array of strings.
    - `[]uint` - An array of unsigned integers.
    """


class UpsertRowBased(TypedDict, total=False):
    distance_metric: Required[DistanceMetric]
    """A function used to calculate vector similarity."""

    upserts: Required[Iterable[DocumentRowParam]]

    schema: Dict[str, Iterable[UpsertRowBasedSchema]]
    """The schema of the attributes attached to the documents."""


UpsertRowBasedSchemaFullTextSearch: TypeAlias = Union[bool, FullTextSearchConfigParam]


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
    """The data type of the attribute.

    - `string` - A string.
    - `uint` - An unsigned integer.
    - `uuid` - A UUID.
    - `bool` - A boolean.
    - `[]string` - An array of strings.
    - `[]uint` - An array of unsigned integers.
    """


class CopyFromNamespace(TypedDict, total=False):
    copy_from_namespace: Required[str]
    """The namespace to copy documents from."""


class DeleteByFilter(TypedDict, total=False):
    delete_by_filter: Required[object]


NamespaceUpsertParams: TypeAlias = Union[UpsertColumnar, UpsertRowBased, CopyFromNamespace, DeleteByFilter]
