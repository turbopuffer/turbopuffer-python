# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["WritePerformance"]


class WritePerformance(BaseModel):
    """The performance information for a write request."""

    server_total_ms: int
    """Request time measured on the server, in milliseconds."""

    embedding_ms: Optional[int] = None
    """Time spent embedding text, in milliseconds.

    Only set when using a native embedding model.
    """

    embedding_tokens: Optional[int] = None
    """The number of tokens embedded. Only set when using a native embedding model."""
