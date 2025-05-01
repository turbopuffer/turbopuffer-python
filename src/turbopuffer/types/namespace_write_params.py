# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .distance_metric import DistanceMetric
from .document_row_param import DocumentRowParam
from .attribute_schema_param import AttributeSchemaParam
from .document_columns_param import DocumentColumnsParam

__all__ = [
    "NamespaceWriteParams",
    "Operation",
    "OperationWriteDocuments",
    "OperationCopyFromNamespace",
    "OperationDeleteByFilter",
]


class NamespaceWriteParams(TypedDict, total=False):
    operation: Operation
    """Write documents."""


class OperationWriteDocuments(TypedDict, total=False):
    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    patch_columns: DocumentColumnsParam
    """A list of documents in columnar format. The keys are the column names."""

    patch_rows: Iterable[DocumentRowParam]

    schema: Dict[str, Iterable[AttributeSchemaParam]]
    """The schema of the attributes attached to the documents."""

    upsert_columns: DocumentColumnsParam
    """A list of documents in columnar format. The keys are the column names."""

    upsert_rows: Iterable[DocumentRowParam]


class OperationCopyFromNamespace(TypedDict, total=False):
    copy_from_namespace: Required[str]
    """The namespace to copy documents from."""


class OperationDeleteByFilter(TypedDict, total=False):
    delete_by_filter: Required[object]
    """The filter specifying which documents to delete."""


Operation: TypeAlias = Union[OperationWriteDocuments, OperationCopyFromNamespace, OperationDeleteByFilter]
