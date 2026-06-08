# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .fuzzy_max_edit_distance_param import FuzzyMaxEditDistanceParam

__all__ = ["FuzzyParams"]


class FuzzyParams(TypedDict, total=False):
    """Additional parameters for the Fuzzy filter."""

    max_edit_distance: Required[Iterable[FuzzyMaxEditDistanceParam]]
    """Maximum edit distance allowed at each query length.

    Queries shorter than the first threshold return no matches.
    """

    case_sensitive: bool
    """Whether searching with Fuzzy filter is case-sensitive.

    Defaults to `true` (i.e. case-sensitive).
    """
