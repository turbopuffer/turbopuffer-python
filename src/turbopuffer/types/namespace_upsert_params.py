# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .distance_metric import DistanceMetric
from .document_row_param import DocumentRowParam
from .attribute_schema_param import AttributeSchemaParam
from .document_columns_param import DocumentColumnsParam

__all__ = [
    "NamespaceUpsertParams",
    "Documents",
    "DocumentsUpsertColumnar",
    "DocumentsUpsertRowBased",
    "DocumentsCopyFromNamespace",
    "DocumentsDeleteByFilter",
]


class NamespaceUpsertParams(TypedDict, total=False):
    documents: Documents
    """Upsert documents in columnar format."""


class DocumentsUpsertColumnar(DocumentColumnsParam):
    distance_metric: Required[DistanceMetric]
    """A function used to calculate vector similarity."""

    schema: Dict[str, Iterable[AttributeSchemaParam]]
    """The schema of the attributes attached to the documents."""


class DocumentsUpsertRowBased(TypedDict, total=False):
    distance_metric: Required[DistanceMetric]
    """A function used to calculate vector similarity."""

    upserts: Required[Iterable[DocumentRowParam]]

    schema: Dict[str, Iterable[AttributeSchemaParam]]
    """The schema of the attributes attached to the documents."""


class DocumentsCopyFromNamespace(TypedDict, total=False):
    copy_from_namespace: Required[str]
    """The namespace to copy documents from."""


class DocumentsDeleteByFilter(TypedDict, total=False):
    delete_by_filter: Required[object]
    """The filter specifying which documents to delete."""


Documents: TypeAlias = Union[
    DocumentsUpsertColumnar, DocumentsUpsertRowBased, DocumentsCopyFromNamespace, DocumentsDeleteByFilter
]
