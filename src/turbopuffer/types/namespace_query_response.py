# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .document_row_with_score import DocumentRowWithScore

__all__ = ["NamespaceQueryResponse"]

NamespaceQueryResponse: TypeAlias = List[DocumentRowWithScore]
