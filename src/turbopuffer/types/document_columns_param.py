# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable, Optional
from typing_extensions import TypedDict

from .id_param import IDParam

__all__ = ["DocumentColumnsParam"]


class DocumentColumnsParam(TypedDict, total=False):
    attributes: Dict[str, Iterable[object]]
    """The attributes attached to each of the documents."""

    ids: List[IDParam]
    """The IDs of the documents."""

    vectors: Iterable[Optional[Iterable[float]]]
    """Vectors describing each of the documents."""
