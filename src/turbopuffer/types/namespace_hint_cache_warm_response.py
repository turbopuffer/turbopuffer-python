# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["NamespaceHintCacheWarmResponse"]


class NamespaceHintCacheWarmResponse(BaseModel):
    status: Literal["OK"]
    """The status of the request."""

    message: Optional[str] = None
