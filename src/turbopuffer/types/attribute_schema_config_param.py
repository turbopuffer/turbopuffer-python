# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from .attribute_type import AttributeType
from .distance_metric import DistanceMetric
from .attribute_embed_param import AttributeEmbedParam
from .full_text_search_param import FullTextSearchParam
from .sparse_distance_metric import SparseDistanceMetric

__all__ = ["AttributeSchemaConfigParam", "Ann", "AnnAnnConfig", "SparseKnn"]


class AnnAnnConfig(TypedDict, total=False):
    """Configuration options for ANN (Approximate Nearest Neighbor) indexing."""

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    late_interaction: bool
    """Opt in to late-interaction (MUVERA) indexing.

    Only valid on fixed-dim `[][N]f32` vector array attributes, and is required to
    enable an ANN index on such attributes. Defaults to `false`.
    """


Ann: TypeAlias = Union[bool, AnnAnnConfig]


class SparseKnn(TypedDict, total=False):
    """Whether to create a sparse kNN index for the attribute.

    Requires the `{}f16` type.
    """

    distance_metric: Required[SparseDistanceMetric]
    """A function used to calculate sparse vector similarity."""


class AttributeSchemaConfigParam(TypedDict, total=False):
    """Detailed configuration for an attribute attached to a document."""

    type: Required[AttributeType]
    """The data type of the attribute.

    Valid values: string, int, uint, float, uuid, datetime, bool, []string, []int,
    []uint, []float, []uuid, []datetime, []bool, [DIMS]f16, [DIMS]f32, {}f16.
    """

    ann: Ann
    """Whether to create an approximate nearest neighbor index for the attribute.

    Can be a boolean or a detailed configuration object.
    """

    embed: Optional[AttributeEmbedParam]
    """Whether to automatically embed this string attribute into a vector attribute.

    Can be a model name, a detailed configuration object, or `null` to remove an
    existing embedding configuration.
    """

    filterable: bool
    """Whether or not the attributes can be used in filters."""

    full_text_search: FullTextSearchParam
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    fuzzy: bool
    """Whether to enable Fuzzy filters on this attribute."""

    glob: bool
    """Whether to enable Glob filters on this attribute."""

    regex: bool
    """Whether to enable Regex filters on this attribute."""

    sparse_knn: SparseKnn
    """Whether to create a sparse kNN index for the attribute.

    Requires the `{}f16` type.
    """
