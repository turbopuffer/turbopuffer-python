# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, TypeAlias

from .attribute_schema_config_param import AttributeSchemaConfigParam

__all__ = ["AttributeSchemaParam"]

AttributeSchemaParam: TypeAlias = Union[
    Literal["string"],
    Literal["uint"],
    Literal["uuid"],
    Literal["bool"],
    Literal["datetime"],
    Literal["[]string"],
    Literal["[]uint"],
    Literal["[]uuid"],
    Literal["[]datetime"],
    str,
    AttributeSchemaConfigParam,
]
