# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["NamespaceRetrieveResponse"]


class NamespaceRetrieveResponse(BaseModel):
    approx_count: Optional[int] = None

    dimensions: Optional[int] = None

    name: Optional[str] = None
