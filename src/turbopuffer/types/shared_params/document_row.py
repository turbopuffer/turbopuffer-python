# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import TypeAlias, TypedDict

from .id import ID

__all__ = ["DocumentRow"]


class DocumentRowTyped(TypedDict, total=False):
    id: ID
    """An identifier for a document."""

    vector: Union[Iterable[float], str, None]
    """A vector describing the document."""


DocumentRow: TypeAlias = Union[DocumentRowTyped, Dict[str, object]]
