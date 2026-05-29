# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AttributeEmbedConfig"]


class AttributeEmbedConfig(BaseModel):
    """Configuration options for automatic embedding."""

    model: str
    """The model to use for embedding.

    See our documentation for a list of models supported in each region.
    """

    attribute: Optional[str] = None
    """The name of an existing vector attribute to store embeddings in.

    If omitted, turbopuffer will generate a computed vector attribute named
    `$embed_<attribute>`.
    """

    dims: Optional[int] = None
    """The dimensionality to embed at.

    If not set, will pick the default for this model. If you're storing embeddings
    in an existing attribute, this can be omitted, and may not be set to a value
    other than the dimensions of that attribute.
    """
