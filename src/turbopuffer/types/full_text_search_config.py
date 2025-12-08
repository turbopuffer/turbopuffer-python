# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .language import Language
from .tokenizer import Tokenizer

__all__ = ["FullTextSearchConfig"]


class FullTextSearchConfig(BaseModel):
    """Configuration options for full-text search."""

    ascii_folding: Optional[bool] = None
    """
    Whether to convert each non-ASCII character in a token to its ASCII equivalent,
    if one exists (e.g., à -> a). Defaults to `false` (i.e., no folding).
    """

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

    max_token_length: Optional[int] = None
    """Maximum length of a token in bytes.

    Tokens larger than this value during tokenization will be filtered out. Has to
    be between `1` and `254` (inclusive). Defaults to `39`.
    """

    remove_stopwords: Optional[bool] = None
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: Optional[bool] = None
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """

    tokenizer: Optional[Tokenizer] = None
    """The tokenizer to use for full-text search on an attribute.

    Defaults to `word_v3`.
    """
