# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DecayParams"]


class DecayParams(TypedDict, total=False):
    """Additional parameters for the Decay operator."""

    exponent: float
    """An exponent that helps further control the shape of the Decay function."""

    midpoint: object
    """The midpoint of the Decay operator."""
