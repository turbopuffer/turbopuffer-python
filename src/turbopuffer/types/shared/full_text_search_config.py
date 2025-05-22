# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["FullTextSearchConfig"]


class FullTextSearchConfig(BaseModel):
    case_sensitive: Optional[bool] = None
    """Whether searching is case-sensitive.

    Defaults to `false` (i.e. case-insensitive).
    """

    language: Optional[
        Literal[
            "arabic",
            "danish",
            "dutch",
            "english",
            "finnish",
            "french",
            "german",
            "greek",
            "hungarian",
            "italian",
            "norwegian",
            "portuguese",
            "romanian",
            "russian",
            "spanish",
            "swedish",
            "tamil",
            "turkish",
        ]
    ] = None
    """The language of the text. Defaults to `english`."""

    remove_stopwords: Optional[bool] = None
    """Removes common words from the text based on language.

    Defaults to `true` (i.e. remove common words).
    """

    stemming: Optional[bool] = None
    """Language-specific stemming for the text.

    Defaults to `false` (i.e., do not stem).
    """
