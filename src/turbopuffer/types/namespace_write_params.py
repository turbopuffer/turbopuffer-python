# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import TypedDict

from .shared_params.id import ID
from .shared.distance_metric import DistanceMetric
from .shared_params.document_row import DocumentRow
from .shared_params.attribute_schema import AttributeSchema
from .shared_params.document_columns import DocumentColumns

__all__ = ["NamespaceWriteParams"]


class NamespaceWriteParams(TypedDict, total=False):
    namespace: str

    copy_from_namespace: str
    """The namespace to copy documents from."""

    delete_by_filter: object
    """The filter specifying which documents to delete."""

    deletes: List[ID]

    distance_metric: DistanceMetric
    """A function used to calculate vector similarity."""

    patch_columns: DocumentColumns
    """A list of documents in columnar format. The keys are the column names."""

    patch_rows: Iterable[DocumentRow]

    schema: Dict[str, AttributeSchema]
    """The schema of the attributes attached to the documents."""

    upsert_columns: DocumentColumns
    """A list of documents in columnar format. The keys are the column names."""

    upsert_rows: Iterable[DocumentRow]
