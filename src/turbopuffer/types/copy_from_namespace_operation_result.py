# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .._models import BaseModel
from .write_result import WriteResult
from .operation_error import OperationError

__all__ = ["CopyFromNamespaceOperationResult", "Success", "Error"]


class Success(BaseModel):
    success: WriteResult
    """The copy succeeded, with the result of its write."""


class Error(BaseModel):
    error: OperationError
    """The copy failed, with its error."""


CopyFromNamespaceOperationResult: TypeAlias = Union[Success, Error]
