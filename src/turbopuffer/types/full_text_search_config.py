# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .language import Language
from .tokenizer import Tokenizer

__all__ = ["FullTextSearchConfig"]


class FullTextSearchConfig(BaseModel):
    b: Optional[float] = None
    """The `b` document length normalization parameter for BM25. Defaults to `0.75`."""

    case_sensitive: Optional[bool] = None
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

    k1: Optional[float] = None
    """The `k1` term saturation parameter for BM25. Defaults to `1.2`."""

    language: Optional[Language] = None
    """Describes the language of a text attribute. Defaults to `english`."""

    remove_stopwords: Optional[bool] = None
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: Optional[bool] = None
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """

    tokenizer: Optional[Tokenizer] = None
    """The tokenizer to use for full-text search on an attribute."""
