# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .id_param import IDParam
from .vector_param import VectorParam

__all__ = ["RowParam"]


class RowParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """A single document, in a row-based format."""

    id: Required[IDParam]
    """An identifier for a document."""

    vector: VectorParam
    """A vector embedding associated with a document."""
