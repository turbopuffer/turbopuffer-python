# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .attribute_schema_config import AttributeSchemaConfig

__all__ = [
    "NamespaceMetadata",
    "Encryption",
    "EncryptionCmek",
    "EncryptionCmekCmek",
    "Index",
    "IndexStatus",
    "IndexUnionMember1",
]


class EncryptionCmekCmek(BaseModel):
    key_name: str
    """The name of the CMEK key in use."""


class EncryptionCmek(BaseModel):
    cmek: Optional[EncryptionCmekCmek] = None


Encryption: TypeAlias = Union[bool, EncryptionCmek]


class IndexStatus(BaseModel):
    status: Literal["up-to-date"]


class IndexUnionMember1(BaseModel):
    status: Literal["updating"]

    unindexed_bytes: int
    """
    The number of bytes in the namespace that are in the write-ahead log but have
    not yet been indexed.
    """


Index: TypeAlias = Union[IndexStatus, IndexUnionMember1]


class NamespaceMetadata(BaseModel):
    approx_logical_bytes: int
    """The approximate number of logical bytes in the namespace."""

    approx_row_count: int
    """The approximate number of rows in the namespace."""

    created_at: datetime
    """The timestamp when the namespace was created."""

    schema_: Dict[str, AttributeSchemaConfig] = FieldInfo(alias="schema")
    """The schema of the namespace."""

    updated_at: datetime
    """The timestamp when the namespace was last modified by a write operation."""

    encryption: Optional[Encryption] = None
    """
    Indicates that the namespace is encrypted with a customer-managed encryption key
    (CMEK).
    """

    index: Optional[Index] = None
