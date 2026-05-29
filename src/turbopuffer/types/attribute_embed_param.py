# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .attribute_embed_config_param import AttributeEmbedConfigParam

__all__ = ["AttributeEmbedParam"]

AttributeEmbedParam: TypeAlias = Union[str, AttributeEmbedConfigParam]
