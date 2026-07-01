# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel
from .attribute_type import AttributeType
from .attribute_embed import AttributeEmbed
from .distance_metric import DistanceMetric
from .full_text_search import FullTextSearch
from .sparse_distance_metric import SparseDistanceMetric

__all__ = ["AttributeSchemaConfig", "Ann", "AnnAnnConfig", "SparseKnn"]


class AnnAnnConfig(BaseModel):
    """Configuration options for ANN (Approximate Nearest Neighbor) indexing."""

    distance_metric: Optional[DistanceMetric] = None
    """A function used to calculate vector similarity."""

    late_interaction: Optional[bool] = None
    """Opt in to late-interaction (MUVERA) indexing.

    Only valid on fixed-dim `[][N]f32` vector array attributes, and is required to
    enable an ANN index on such attributes. Defaults to `false`.
    """


Ann: TypeAlias = Union[bool, AnnAnnConfig]


class SparseKnn(BaseModel):
    """Whether to create a sparse kNN index for the attribute.

    Requires the `{}f16` type.
    """

    distance_metric: SparseDistanceMetric
    """A function used to calculate sparse vector similarity."""


class AttributeSchemaConfig(BaseModel):
    """Detailed configuration for an attribute attached to a document."""

    type: AttributeType
    """The data type of the attribute.

    Valid values: string, int, uint, float, uuid, datetime, bool, []string, []int,
    []uint, []float, []uuid, []datetime, []bool, [DIMS]f16, [DIMS]f32, {}f16.
    """

    ann: Optional[Ann] = None
    """Whether to create an approximate nearest neighbor index for the attribute.

    Can be a boolean or a detailed configuration object.
    """

    embed: Optional[AttributeEmbed] = None
    """Whether to automatically embed this string attribute into a vector attribute.

    Can be a model name, a detailed configuration object, or `null` to remove an
    existing embedding configuration.
    """

    filterable: Optional[bool] = None
    """Whether or not the attributes can be used in filters."""

    full_text_search: Optional[FullTextSearch] = None
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    fuzzy: Optional[bool] = None
    """Whether to enable Fuzzy filters on this attribute."""

    glob: Optional[bool] = None
    """Whether to enable Glob filters on this attribute."""

    regex: Optional[bool] = None
    """Whether to enable Regex filters on this attribute."""

    sparse_knn: Optional[SparseKnn] = None
    """Whether to create a sparse kNN index for the attribute.

    Requires the `{}f16` type.
    """
