# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import TypeAlias, TypedDict

from .id_param import IDParam
from .distance_metric import DistanceMetric
from .document_row_param import DocumentRowParam
from .attribute_schema_param import AttributeSchemaParam

__all__ = ["NamespaceUpsertParams", "UpsertColumnar", "UpsertRowBased", "CopyFromNamespace", "DeleteByFilter"]


class UpsertColumnar(TypedDict, total=False):
    attributes: Dict[str, Iterable[AttributeSchemaParam]]
    """The attributes attached to each of the documents."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    ids: List[IDParam]
    """The IDs of the documents."""

    schema: Dict[str, Iterable[AttributeSchemaParam]]
    """The schema of the attributes attached to the documents."""

    vectors: Iterable[Optional[Iterable[float]]]
    """Vectors describing each of the documents."""


class UpsertRowBased(TypedDict, total=False):
    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    schema: Dict[str, Iterable[AttributeSchemaParam]]
    """The schema of the attributes attached to the documents."""

    upserts: Iterable[DocumentRowParam]


class CopyFromNamespace(TypedDict, total=False):
    copy_from_namespace: str
    """The namespace to copy documents from."""


class DeleteByFilter(TypedDict, total=False):
    delete_by_filter: object


NamespaceUpsertParams: TypeAlias = Union[UpsertColumnar, UpsertRowBased, CopyFromNamespace, DeleteByFilter]
