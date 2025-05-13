# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import TypeAlias, TypedDict

from .id_param import IDParam

__all__ = ["DocumentColumnsParam"]


class DocumentColumnsParamTyped(TypedDict, total=False):
    id: List[IDParam]
    """The IDs of the documents."""


DocumentColumnsParam: TypeAlias = Union[DocumentColumnsParamTyped, Dict[str, Iterable[Dict[str, object]]]]
