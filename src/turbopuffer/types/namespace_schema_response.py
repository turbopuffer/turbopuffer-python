# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from typing_extensions import TypeAlias

from .attribute_schema_config import AttributeSchemaConfig

__all__ = ["NamespaceSchemaResponse"]

NamespaceSchemaResponse: TypeAlias = Dict[str, AttributeSchemaConfig]
