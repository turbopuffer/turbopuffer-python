# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from .shared_params.attribute_schema import AttributeSchema

__all__ = ["NamespaceUpdateSchemaParams"]


class NamespaceUpdateSchemaParams(TypedDict, total=False):
    namespace: str

    schema: Dict[str, AttributeSchema]
    """The desired schema for the namespace."""
