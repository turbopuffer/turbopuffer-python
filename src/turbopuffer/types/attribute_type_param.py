# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, TypeAlias

__all__ = ["AttributeTypeParam"]

AttributeTypeParam: TypeAlias = Union[
    Literal["string", "uint", "uuid", "bool", "datetime", "[]string", "[]uint", "[]uuid", "[]datetime"], str
]
