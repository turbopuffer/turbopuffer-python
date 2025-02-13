# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["NamespaceUpsertParams", "Variant0", "Variant1", "Variant1Upsert"]


class Variant0(TypedDict, total=False):
    distance_metric: Required[Literal["cosine_distance", "euclidean_squared"]]
    """The function used to calculate vector similarity."""

    ids: Required[List[Union[int, str]]]
    """Array of document IDs (unsigned 64-bit integers, UUIDs, or strings)."""

    vectors: Required[Iterable[Optional[Iterable[float]]]]
    """Array of vectors.

    Each vector is an array of numbers. Use `null` to delete a document.
    """

    attributes: Dict[str, Iterable[object]]
    """Object mapping attribute names to arrays of attribute values."""

    copy_from_namespace: str
    """Copy all documents from another namespace into this one."""

    schema: object
    """Manually specify the schema for the documents."""


class Variant1(TypedDict, total=False):
    upserts: Required[Iterable[Variant1Upsert]]
    """Array of document operations in row-based format."""


class Variant1Upsert(TypedDict, total=False):
    id: Required[Union[int, str]]
    """Document ID."""

    attributes: object
    """Object mapping attribute names to values."""

    vector: Optional[Iterable[float]]
    """Document vector. Use `null` to indicate deletion."""


NamespaceUpsertParams: TypeAlias = Union[Variant0, Variant1]
