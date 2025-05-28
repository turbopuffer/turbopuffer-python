# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .full_text_search_config_param import FullTextSearchConfigParam

__all__ = ["FullTextSearchParam"]

FullTextSearchParam: TypeAlias = Union[bool, FullTextSearchConfigParam]
