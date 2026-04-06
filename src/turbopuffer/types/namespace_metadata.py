# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .pinning_config import PinningConfig
from .attribute_schema_config import AttributeSchemaConfig

__all__ = [
    "NamespaceMetadata",
    "Encryption",
    "EncryptionSse",
    "EncryptionCmek",
    "EncryptionCmekCmek",
    "Index",
    "IndexIndexUpToDate",
    "IndexIndexUpdating",
    "Pinning",
    "PinningStatus",
]


class EncryptionSse(BaseModel):
    sse: bool
    """Always true. Indicates that the namespace is encrypted with SSE."""


class EncryptionCmekCmek(BaseModel):
    key_name: str
    """The name of the CMEK key in use."""


class EncryptionCmek(BaseModel):
    """
    Indicates that the namespace is encrypted with a customer-managed encryption key (CMEK).
    """

    cmek: EncryptionCmekCmek


Encryption: TypeAlias = Union[EncryptionSse, EncryptionCmek]


class IndexIndexUpToDate(BaseModel):
    status: Literal["up-to-date"]


class IndexIndexUpdating(BaseModel):
    status: Literal["updating"]

    unindexed_bytes: int
    """
    The number of bytes in the namespace that are in the write-ahead log but have
    not yet been indexed.
    """


Index: TypeAlias = Union[IndexIndexUpToDate, IndexIndexUpdating]


class PinningStatus(BaseModel):
    """Operational status for a pinned namespace."""

    ready_replicas: int
    """The number of replicas that are warm and serving traffic."""

    updated_at: datetime
    """The timestamp of the latest pinning status snapshot."""

    utilization: float
    """
    Aggregate utilization for the pinned namespace, reported as a value between 0.0
    and 1.0.
    """


class Pinning(PinningConfig):
    """
    Configuration for namespace pinning, along with the current status of the pinned namespace.
    """

    status: Optional[PinningStatus] = None
    """Operational status for a pinned namespace."""


class NamespaceMetadata(BaseModel):
    """Metadata about a namespace."""

    approx_logical_bytes: int
    """The approximate number of logical bytes in the namespace."""

    approx_row_count: int
    """The approximate number of rows in the namespace."""

    created_at: datetime
    """The timestamp when the namespace was created."""

    encryption: Encryption
    """
    Indicates that the namespace is encrypted with a customer-managed encryption key
    (CMEK).
    """

    index: Index

    schema_: Dict[str, AttributeSchemaConfig] = FieldInfo(alias="schema")
    """The schema of the namespace."""

    updated_at: datetime
    """The timestamp when the namespace was last modified by a write operation."""

    pinning: Optional[Pinning] = None
    """
    Configuration for namespace pinning, along with the current status of the pinned
    namespace.
    """
