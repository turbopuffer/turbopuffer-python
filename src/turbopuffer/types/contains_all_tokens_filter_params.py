# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ContainsAllTokensFilterParams"]


class ContainsAllTokensFilterParams(TypedDict, total=False):
    """Additional (optional) parameters for the ContainsAllTokens filter."""

    last_as_prefix: bool
    """Whether to treat the last token in the query input as a literal prefix."""
