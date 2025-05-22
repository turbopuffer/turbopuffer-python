# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["NamespaceRecallParams"]


class NamespaceRecallParams(TypedDict, total=False):
    namespace: str

    filters: object
    """Filter by attributes. Same syntax as the query endpoint."""

    num: int
    """The number of searches to run."""

    queries: Iterable[float]
    """Use specific query vectors for the measurement.

    If omitted, sampled from the index.
    """

    top_k: int
    """Search for `top_k` nearest neighbors."""
