# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .full_text_search_config import FullTextSearchConfig

__all__ = ["FullTextSearch"]

FullTextSearch: TypeAlias = Union[bool, FullTextSearchConfig]
