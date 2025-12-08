# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["Bm25ClauseParams"]


class Bm25ClauseParams(TypedDict, total=False):
    """Additional (optional) parameters for a single BM25 query clause."""

    last_as_prefix: bool
    """Whether to treat the last token in the query input as a literal prefix."""
