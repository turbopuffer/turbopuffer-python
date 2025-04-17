# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .id_param import IDParam

__all__ = ["DocumentRowParam"]


class DocumentRowParam(TypedDict, total=False):
    id: IDParam
    """An identifier for a document."""

    additional_properties: Annotated[object, PropertyInfo(alias="additionalProperties")]
    """The attributes attached to the document."""

    vector: Union[Iterable[float], str, None]
    """A vector describing the document."""
