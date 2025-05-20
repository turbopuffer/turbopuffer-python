# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .document_row import DocumentRow

__all__ = ["NamespaceMultiQueryResponse", "Result"]


class Result(BaseModel):
    aggregations: Optional[List[Dict[str, object]]] = None

    rows: Optional[List[DocumentRow]] = None


class NamespaceMultiQueryResponse(BaseModel):
    results: List[Result]
