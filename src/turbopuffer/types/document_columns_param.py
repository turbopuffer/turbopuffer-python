# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .id_param import IDParam
from .vector_param import VectorParam

__all__ = ["DocumentColumnsParam"]


class DocumentColumnsParamTyped(TypedDict, total=False):
    id: Required[List[IDParam]]
    """The IDs of the documents."""

    vector: Union[List[VectorParam], Iterable[float], str]
    """The vector embeddings of the documents."""


DocumentColumnsParam: TypeAlias = Union[DocumentColumnsParamTyped, Dict[str, Iterable[object]]]
