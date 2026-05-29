# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EmbedParams"]


class EmbedParams(TypedDict, total=False):
    """Additional (optional) parameters for the Embed expression."""

    model: str
    """
    The model to use for embedding, overriding the model configured for the
    attribute.
    """
