# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["AttributeType"]

AttributeType: TypeAlias = Literal[
    "string", "uint", "uuid", "bool", "datetime", "[]string", "[]uint", "[]uuid", "[]datetime"
]
