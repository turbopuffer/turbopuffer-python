# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, Literal, Optional, overload
from typing_extensions import TypedDict

from pydantic import Field as FieldInfo

from .id import ID
from .vector import Vector
from .._models import BaseModel

__all__ = ["Row"]


# The `type: ignore` comment below is because mypy doesn't yet support the
# `extra_items` argument to `TypedDict`. Pyright does though.
# https://github.com/python/mypy/pull/18889
RowDict = TypedDict(  # type: ignore[misc]
    "RowDict",
    {
        "id": ID,
        "vector": Optional[Vector],
        "$dist": float,
    },
    total=False,
    extra_items=object,
)


class Row(BaseModel):
    """A single document, in a row-based format."""

    id: ID
    """An identifier for a document."""

    vector: Optional[Vector] = None
    """A vector embedding associated with a document."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]

    @staticmethod
    def from_dict(values: RowDict) -> "Row":
        """Construct a `Row` from a dictionary of values."""
        return Row.construct(**values)

    @overload
    def __getitem__(self, key: Literal["id"]) -> ID: ...

    @overload
    def __getitem__(self, key: Literal["vector"]) -> Optional[Vector]: ...

    @overload
    def __getitem__(self, key: Literal["$dist"]) -> float: ...

    @overload
    def __getitem__(self, key: str) -> object: ...

    def __getitem__(self, key: str) -> object:
        return getattr(self, key)

    @overload
    def __setitem__(self, key: Literal["id"], value: ID) -> None: ...

    @overload
    def __setitem__(self, key: Literal["vector"], value: Optional[Vector]) -> None: ...

    @overload
    def __setitem__(self, key: Literal["$dist"], value: float) -> None: ...

    @overload
    def __setitem__(self, key: str, value: object) -> None: ...

    def __setitem__(self, key: str, value: object) -> None:
        setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __len__(self) -> int:
        extra_len = 0
        if self.model_extra is not None:
            extra_len = len(self.model_extra)
        return len(Row.model_fields) + extra_len
