# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .document_columns import DocumentColumns

__all__ = ["NamespaceExportResponse"]


class NamespaceExportResponse(DocumentColumns):
    next_cursor: Optional[str] = None
    """The cursor to use to retrieve the next page of results."""
