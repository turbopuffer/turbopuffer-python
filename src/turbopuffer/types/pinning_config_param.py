# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PinningConfigParam"]


class PinningConfigParam(TypedDict, total=False):
    """Configuration for namespace pinning."""

    replicas: int
    """The number of read replicas to provision. Defaults to 1 if not specified."""
