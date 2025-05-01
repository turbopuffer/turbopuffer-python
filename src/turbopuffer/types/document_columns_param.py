# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .id_param import IDParam

__all__ = ["DocumentColumnsParam"]


class DocumentColumnsParam(TypedDict, total=False):
    id: List[IDParam]
    """The IDs of the documents."""

    additional_properties: Annotated[Iterable[Dict[str, object]], PropertyInfo(alias="additionalProperties")]
    """The attributes attached to each of the documents."""
