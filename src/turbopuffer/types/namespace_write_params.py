# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Required, TypedDict

from .id_param import IDParam
from .distance_metric import DistanceMetric
from .document_row_param import DocumentRowParam
from .attribute_schema_param import AttributeSchemaParam
from .document_columns_param import DocumentColumnsParam

__all__ = ["NamespaceWriteParams", "Encryption", "EncryptionCmek"]


class NamespaceWriteParams(TypedDict, total=False):
    namespace: str

    copy_from_namespace: str
    """The namespace to copy documents from."""

    delete_by_filter: object
    """The filter specifying which documents to delete."""

    deletes: List[IDParam]

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    encryption: Encryption
    """The encryption configuration for a namespace."""

    patch_columns: DocumentColumnsParam
    """A list of documents in columnar format. The keys are the column names."""

    patch_rows: Iterable[DocumentRowParam]

    schema: Dict[str, AttributeSchemaParam]
    """The schema of the attributes attached to the documents."""

    upsert_columns: DocumentColumnsParam
    """A list of documents in columnar format. The keys are the column names."""

    upsert_rows: Iterable[DocumentRowParam]


class EncryptionCmek(TypedDict, total=False):
    key_name: Required[str]
    """The identifier of the CMEK key to use for encryption.

    For GCP, the fully-qualified resource name of the key. For AWS, the ARN of the
    key.
    """


class Encryption(TypedDict, total=False):
    cmek: EncryptionCmek
