# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Literal, Optional, overload
from typing_extensions import TypedDict

from .id import ID
from .vector import Vector
from .._models import BaseModel

__all__ = ["DocumentRow"]


# The `type: ignore` comment below is because mypy doesn't yet support the
# `extra_items` argument to `TypedDict`. Pyright does though.
# https://github.com/python/mypy/pull/18889
DocumentRowDict = TypedDict(  # type: ignore[misc]
    "DocumentRowDict",
    {
        "id": ID,
        "vector": Optional[Vector],
        "$dist": float,
    },
    total=False,
    extra_items=object,
)


class DocumentRow(BaseModel):
    id: ID
    """An identifier for a document."""

    vector: Optional[Vector] = None
    """A vector embedding associated with a document."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...

    @staticmethod
    def from_dict(values: DocumentRowDict) -> "DocumentRow":
        """Construct a `DocumentRow` from a dictionary of values."""
        return DocumentRow.construct(**values)

    @overload
    def __getitem__(self, key: Literal["id"]) -> ID: ...

    @overload
    def __getitem__(self, key: Literal["vector"]) -> Optional[Vector]: ...

    @overload
    def __getitem__(self, key: Literal["$dist"]) -> float: ...

    def __getitem__(self, key: str) -> object:
        return getattr(self, key)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __len__(self) -> int:
        extra_len = 0
        if self.model_extra is not None:
            extra_len = len(self.model_extra)
        return len(self.model_fields) + extra_len
