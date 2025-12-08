# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .query_param import QueryParam
from .vector_encoding import VectorEncoding

__all__ = ["NamespaceMultiQueryParams", "Consistency"]


class NamespaceMultiQueryParams(TypedDict, total=False):
    namespace: str

    queries: Required[Iterable[QueryParam]]

    consistency: Consistency
    """The consistency level for a query."""

    vector_encoding: VectorEncoding
    """The encoding to use for vectors in the response."""


class Consistency(TypedDict, total=False):
    """The consistency level for a query."""

    level: Literal["strong", "eventual"]
    """The query's consistency level.

    - `strong` - Strong consistency. Requires a round-trip to object storage to
      fetch the latest writes.
    - `eventual` - Eventual consistency. Does not require a round-trip to object
      storage, but may not see the latest writes.
    """
