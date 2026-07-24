# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .highlight_fragment_by import HighlightFragmentBy
from .highlight_offset_units import HighlightOffsetUnits

__all__ = ["HighlightConfigParams"]


class HighlightConfigParams(TypedDict, total=False):
    """Additional (optional) parameters for the Highlight compute expression."""

    fragment_by: HighlightFragmentBy
    """How to split a text attribute into fragments for highlighting."""

    fragment_limit: int
    """The maximum number of fragments to return. Defaults to `3`."""

    include_offsets: HighlightOffsetUnits
    """The units to report highlighted fragment offsets in."""

    rank_fragments_by: object
    """
    How to rank candidate fragments within the attribute before selecting the top
    `fragment_limit`. Defaults to the query's `rank_by`.
    """
