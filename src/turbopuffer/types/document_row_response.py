# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .document_row import DocumentRow

__all__ = ["DocumentRowResponse"]


class DocumentRowResponse(DocumentRow):
    dist: Optional[float] = None
    """
    For vector search, the distance between the query vector and the document
    vector. For BM25 full-text search, the score of the document. Not present for
    other types of queries.
    """
