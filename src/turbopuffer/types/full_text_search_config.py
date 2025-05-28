# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel
from .language import Language

__all__ = ["FullTextSearchConfig"]


class FullTextSearchConfig(BaseModel):
    case_sensitive: Optional[bool] = None
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

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
