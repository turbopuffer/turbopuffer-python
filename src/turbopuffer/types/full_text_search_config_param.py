# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .language import Language
from .tokenizer import Tokenizer

__all__ = ["FullTextSearchConfigParam"]


class FullTextSearchConfigParam(TypedDict, total=False):
    """Configuration options for full-text search."""

    ascii_folding: bool
    """
    Whether to convert each non-ASCII character in a token to its ASCII equivalent,
    if one exists (e.g., à -> a). Defaults to `false` (i.e., no folding).
    """

    b: float
    """The `b` document length normalization parameter for BM25. Defaults to `0.75`."""

    case_sensitive: bool
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

    k1: float
    """The `k1` term saturation parameter for BM25. Defaults to `1.2`."""

    language: Language
    """Describes the language of a text attribute. Defaults to `english`."""

    max_token_length: int
    """Maximum length of a token in bytes.

    Tokens larger than this value during tokenization will be filtered out. Has to
    be between `1` and `254` (inclusive). Defaults to `39`.
    """

    remove_stopwords: bool
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: bool
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """

    tokenizer: Tokenizer
    """The tokenizer to use for full-text search on an attribute.

    Defaults to `word_v3`.
    """
