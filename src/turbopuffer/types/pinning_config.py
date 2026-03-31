# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["PinningConfig"]


class PinningConfig(BaseModel):
    """Configuration for namespace pinning."""

    replicas: Optional[int] = None
    """The number of read replicas to provision. Defaults to 1 if not specified."""
