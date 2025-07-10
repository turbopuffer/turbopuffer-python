# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .attribute_schema_config import AttributeSchemaConfig

__all__ = ["NamespaceMetadata"]


class NamespaceMetadata(BaseModel):
    approx_logical_bytes: int
    """The approximate number of logical bytes in the namespace."""

    created_at: datetime
    """The timestamp when the namespace was created."""

    schema_: Dict[str, AttributeSchemaConfig] = FieldInfo(alias="schema")
    """The schema of the namespace."""
