# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["LimitParam", "Per"]


class Per(TypedDict, total=False):
    """
    Limits the number of documents with the same value for a set of attributes (the "limit key") that can appear in the results.
    """

    attributes: Required[SequenceNotStr[str]]
    """The attributes to include in the limit key."""

    limit: Required[int]
    """The maximum number of documents to return for each value of the limit key."""


class LimitParam(TypedDict, total=False):
    """Limits the documents returned by a query."""

    total: Required[int]
    """Limits the total number of documents returned."""

    per: Per
    """
    Limits the number of documents with the same value for a set of attributes (the
    "limit key") that can appear in the results.
    """
