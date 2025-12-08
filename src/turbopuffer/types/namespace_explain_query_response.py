# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["NamespaceExplainQueryResponse"]


class NamespaceExplainQueryResponse(BaseModel):
    """The response to a successful query explain."""

    plan_text: Optional[str] = None
    """The textual representation of the query plan."""
