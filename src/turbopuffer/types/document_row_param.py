# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .id_param import IDParam

__all__ = ["DocumentRowParam"]


class DocumentRowParamTyped(TypedDict, total=False):
    id: Required[IDParam]
    """An identifier for a document."""

    vector: Union[Iterable[float], str]
    """A vector embedding associated with a document."""


DocumentRowParam: TypeAlias = Union[DocumentRowParamTyped, Dict[str, object]]
