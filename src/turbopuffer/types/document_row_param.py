# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import TypeAlias, TypedDict

from .id_param import IDParam

__all__ = ["DocumentRowParam"]


class DocumentRowParamTyped(TypedDict, total=False):
    id: IDParam
    """An identifier for a document."""

    vector: Union[Iterable[float], str, None]
    """A vector describing the document."""


DocumentRowParam: TypeAlias = Union[DocumentRowParamTyped, Dict[str, object]]
