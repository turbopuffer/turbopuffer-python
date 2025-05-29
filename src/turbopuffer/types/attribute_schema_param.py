# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .attribute_type import AttributeType
from .attribute_schema_config_param import AttributeSchemaConfigParam

__all__ = ["AttributeSchemaParam"]

AttributeSchemaParam: TypeAlias = Union[AttributeType, AttributeSchemaConfigParam]
