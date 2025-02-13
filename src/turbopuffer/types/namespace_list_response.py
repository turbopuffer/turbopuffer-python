# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["NamespaceListResponse", "NamespaceListResponseItem"]


class NamespaceListResponseItem(BaseModel):
    approx_count: Optional[int] = None

    dimensions: Optional[int] = None

    name: Optional[str] = None


NamespaceListResponse: TypeAlias = List[NamespaceListResponseItem]
