# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .language import Language

__all__ = ["FullTextSearchConfigParam"]


class FullTextSearchConfigParam(TypedDict, total=False):
    case_sensitive: bool
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

    language: Language
    """Describes the language of a text attribute. Defaults to `english`."""

    remove_stopwords: bool
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: bool
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """
