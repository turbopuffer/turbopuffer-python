# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import TypedDict

from .id_param import IDParam
from .attribute_schema_param import AttributeSchemaParam

__all__ = ["DocumentRowParam"]


class DocumentRowParam(TypedDict, total=False):
    id: IDParam
    """An identifier for a document."""

    attributes: Dict[str, AttributeSchemaParam]
    """The attributes attached to the document."""

    vector: Optional[Iterable[float]]
    """A vector describing the document."""
