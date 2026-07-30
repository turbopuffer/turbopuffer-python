# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["RrfParams"]


class RrfParams(TypedDict, total=False):
    """Configuration options for RRF."""

    rank_constant: int
    """RRF rank constant (`k`). Must be greater than zero. Defaults to `60`."""

    weights: Iterable[float]
    """A positive weight for each subquery, in the same order as `queries`.

    The number of weights must match the number of subqueries. When omitted, every
    subquery has a weight of `1`.
    """
