# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from .attribute_schema_param import AttributeSchemaParam

__all__ = ["NamespaceUpdateSchemaParams"]


class NamespaceUpdateSchemaParams(TypedDict, total=False):
    namespace: str

    schema: Dict[str, AttributeSchemaParam]
    """The desired schema for the namespace."""
