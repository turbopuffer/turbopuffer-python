# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import TypeAlias, TypedDict

from .id import ID

__all__ = ["DocumentColumns"]


class DocumentColumnsTyped(TypedDict, total=False):
    id: List[ID]
    """The IDs of the documents."""


DocumentColumns: TypeAlias = Union[DocumentColumnsTyped, Dict[str, Iterable[object]]]
