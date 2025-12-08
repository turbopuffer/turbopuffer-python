# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .attribute_type import AttributeType
from .distance_metric import DistanceMetric
from .full_text_search_param import FullTextSearchParam

__all__ = ["AttributeSchemaConfigParam", "Ann", "AnnAnnConfig"]


class AnnAnnConfig(TypedDict, total=False):
    """Configuration options for ANN (Approximate Nearest Neighbor) indexing."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""


Ann: TypeAlias = Union[bool, AnnAnnConfig]


class AttributeSchemaConfigParam(TypedDict, total=False):
    """Detailed configuration for an attribute attached to a document."""

    type: Required[AttributeType]
    """The data type of the attribute.

    Valid values: string, int, uint, float, uuid, datetime, bool, []string, []int,
    []uint, []float, []uuid, []datetime, []bool, [DIMS]f16, [DIMS]f32.
    """

    ann: Ann
    """Whether to create an approximate nearest neighbor index for the attribute.

    Can be a boolean or a detailed configuration object.
    """

    filterable: bool
    """Whether or not the attributes can be used in filters."""

    full_text_search: FullTextSearchParam
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    regex: bool
    """Whether to enable Regex filters on this attribute."""
