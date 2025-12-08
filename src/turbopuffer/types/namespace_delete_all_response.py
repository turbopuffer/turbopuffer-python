# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["NamespaceDeleteAllResponse"]


class NamespaceDeleteAllResponse(BaseModel):
    """The response to a successful namespace deletion request."""

    status: Literal["OK"]
    """The status of the request."""
