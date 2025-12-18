# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel
from .attribute_type import AttributeType
from .distance_metric import DistanceMetric
from .full_text_search import FullTextSearch

__all__ = ["AttributeSchemaConfig", "Ann", "AnnAnnConfig"]


class AnnAnnConfig(BaseModel):
    """Configuration options for ANN (Approximate Nearest Neighbor) indexing."""

    distance_metric: Optional[DistanceMetric] = None
    """A function used to calculate vector similarity."""


Ann: TypeAlias = Union[bool, AnnAnnConfig]


class AttributeSchemaConfig(BaseModel):
    """Detailed configuration for an attribute attached to a document."""

    type: AttributeType
    """The data type of the attribute.

    Valid values: string, int, uint, float, uuid, datetime, bool, []string, []int,
    []uint, []float, []uuid, []datetime, []bool, [DIMS]f16, [DIMS]f32.
    """

    ann: Optional[Ann] = None
    """Whether to create an approximate nearest neighbor index for the attribute.

    Can be a boolean or a detailed configuration object.
    """

    filterable: Optional[bool] = None
    """Whether or not the attributes can be used in filters."""

    full_text_search: Optional[FullTextSearch] = None
    """Whether this attribute can be used as part of a BM25 full-text search.

    Requires the `string` or `[]string` type, and by default, BM25-enabled
    attributes are not filterable. You can override this by setting
    `filterable: true`.
    """

    regex: Optional[bool] = None
    """Whether to enable Regex filters on this attribute."""
