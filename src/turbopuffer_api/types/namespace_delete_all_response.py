# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["NamespaceDeleteAllResponse"]


class NamespaceDeleteAllResponse(BaseModel):
    status: Optional[Literal["ok"]] = None
    """The status of the request."""
