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
    "DocumentsWrite",
    "DocumentsCopyFromNamespace",
    "DocumentsDeleteByFilter",
]


class NamespaceUpsertParams(TypedDict, total=False):
    documents: Documents
    """Write documents."""


class DocumentsWrite(TypedDict, total=False):
    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    schema: Dict[str, Iterable[AttributeSchemaParam]]
    """The schema of the attributes attached to the documents."""

    upsert_columns: DocumentColumnsParam
    """A list of documents in columnar format. The keys are the column names."""

    upsert_rows: Iterable[DocumentRowParam]


class DocumentsCopyFromNamespace(TypedDict, total=False):
    copy_from_namespace: Required[str]
    """The namespace to copy documents from."""


class DocumentsDeleteByFilter(TypedDict, total=False):
    delete_by_filter: Required[object]
    """The filter specifying which documents to delete."""


Documents: TypeAlias = Union[DocumentsWrite, DocumentsCopyFromNamespace, DocumentsDeleteByFilter, object]
