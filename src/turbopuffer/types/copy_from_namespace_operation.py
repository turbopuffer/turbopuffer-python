# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .copy_from_namespace_operation_result import CopyFromNamespaceOperationResult

__all__ = ["CopyFromNamespaceOperation", "Running", "Finished"]


class Running(BaseModel):
    start_time: datetime
    """The time at which the operation started."""

    status: Literal["running"]

    progress: Optional[str] = None
    """A freeform description of the operation's progress.

    May be absent, and its format may change.
    """


class Finished(BaseModel):
    finish_time: datetime
    """The time at which the operation finished."""

    result: CopyFromNamespaceOperationResult

    start_time: datetime
    """The time at which the operation started."""

    status: Literal["finished"]


CopyFromNamespaceOperation: TypeAlias = Annotated[Union[Running, Finished], PropertyInfo(discriminator="status")]
