# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .._types import Omit, SequenceNotStr
from .id_param import IDParam
from .row_param import RowParam
from ..types.custom import Filter
from .columns_param import ColumnsParam
from .distance_metric import DistanceMetric
from .attribute_schema_param import AttributeSchemaParam

__all__ = [
    "NamespaceWriteParams",
    "CopyFromNamespace",
    "CopyFromNamespaceCopyFromNamespaceConfig",
    "Encryption",
    "EncryptionCmek",
    "PatchByFilter",
]


class NamespaceWriteParams(TypedDict, total=False):
    namespace: str

    copy_from_namespace: CopyFromNamespace
    """The namespace to copy documents from."""

    delete_by_filter: Union[Filter, Omit]
    """The filter specifying which documents to delete."""

    delete_by_filter_allow_partial: bool
    """Allow partial completion when filter matches too many documents."""

    delete_condition: Union[Filter, Omit]
    """
    A condition evaluated against the current value of each document targeted by a
    delete write. Only documents that pass the condition are deleted.
    """

    deletes: SequenceNotStr[IDParam]

    disable_backpressure: bool
    """Disables write throttling (HTTP 429 responses) during high-volume ingestion."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    encryption: Encryption
    """The encryption configuration for a namespace."""

    patch_by_filter: PatchByFilter
    """The patch and filter specifying which documents to patch."""

    patch_by_filter_allow_partial: bool
    """Allow partial completion when filter matches too many documents."""

    patch_columns: ColumnsParam
    """A list of documents in columnar format.

    Each key is a column name, mapped to an array of values for that column.
    """

    patch_condition: Union[Filter, Omit]
    """
    A condition evaluated against the current value of each document targeted by a
    patch write. Only documents that pass the condition are patched.
    """

    patch_rows: Iterable[RowParam]

    schema: Dict[str, AttributeSchemaParam]
    """The schema of the attributes attached to the documents."""

    upsert_columns: ColumnsParam
    """A list of documents in columnar format.

    Each key is a column name, mapped to an array of values for that column.
    """

    upsert_condition: Union[Filter, Omit]
    """
    A condition evaluated against the current value of each document targeted by an
    upsert write. Only documents that pass the condition are upserted.
    """

    upsert_rows: Iterable[RowParam]


class CopyFromNamespaceCopyFromNamespaceConfig(TypedDict, total=False):
    source_namespace: Required[str]
    """The namespace to copy documents from."""

    source_api_key: str
    """An API key for the organization containing the source namespace"""

    source_region: str
    """The region of the source namespace."""


CopyFromNamespace: TypeAlias = Union[str, CopyFromNamespaceCopyFromNamespaceConfig]


class EncryptionCmek(TypedDict, total=False):
    key_name: Required[str]
    """The identifier of the CMEK key to use for encryption.

    For GCP, the fully-qualified resource name of the key. For AWS, the ARN of the
    key.
    """


class Encryption(TypedDict, total=False):
    """The encryption configuration for a namespace."""

    cmek: EncryptionCmek


class PatchByFilter(TypedDict, total=False):
    """The patch and filter specifying which documents to patch."""

    filters: Required[Filter]
    """Filter by attributes. Same syntax as the query endpoint."""

    patch: Required[Dict[str, object]]
