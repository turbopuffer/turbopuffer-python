# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .document_row_response import DocumentRowResponse

__all__ = ["NamespaceQueryResponse"]

NamespaceQueryResponse: TypeAlias = List[DocumentRowResponse]
