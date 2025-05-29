# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, TypeAlias

from .attribute_schema_config import AttributeSchemaConfig

__all__ = ["AttributeSchema"]

AttributeSchema: TypeAlias = Union[
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
    AttributeSchemaConfig,
]
