# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr
from .id_param import IDParam
from .vector_param import VectorParam

__all__ = ["ColumnsParam"]


class ColumnsParam(TypedDict, total=False, extra_items=Iterable[object]):  # type: ignore[call-arg]
    """A list of documents in columnar format.

    Each key is a column name, mapped to an array of values for that column.
    """

    id: Required[SequenceNotStr[IDParam]]
    """The IDs of the documents."""

    vector: Union[SequenceNotStr[VectorParam], Iterable[float], str]
    """The vector embeddings of the documents."""
