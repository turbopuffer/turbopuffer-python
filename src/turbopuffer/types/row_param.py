# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .id_param import IDParam
from .vector_param import VectorParam

__all__ = ["RowParam"]


class RowParamTyped(TypedDict, total=False):
    id: Required[IDParam]
    """An identifier for a document."""

    vector: VectorParam
    """A vector embedding associated with a document."""


RowParam: TypeAlias = Union[RowParamTyped, Dict[str, object]]
