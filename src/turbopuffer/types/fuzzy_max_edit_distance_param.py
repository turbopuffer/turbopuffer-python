# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FuzzyMaxEditDistanceParam"]


class FuzzyMaxEditDistanceParam(TypedDict, total=False):
    """An edit distance threshold for the Fuzzy filter."""

    distance: Required[int]
    """The maximum edit distance to allow."""

    min_query_chars: Required[int]
    """Minimum number of characters in a query where this distance applies.

    Must be at least 3 · (distance + 1).
    """
