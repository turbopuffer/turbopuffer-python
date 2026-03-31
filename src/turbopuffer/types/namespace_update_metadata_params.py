# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import TypeAlias, TypedDict

from .pinning_config_param import PinningConfigParam

__all__ = ["NamespaceUpdateMetadataParams", "Pinning"]


class NamespaceUpdateMetadataParams(TypedDict, total=False):
    namespace: str

    pinning: Optional[Pinning]
    """Configuration for namespace pinning.

    - Missing field: no change to pinning configuration
    - `null` or `false`: explicitly remove pinning
    - `true`: enable pinning with default configuration
    - Object: set pinning configuration
    """


Pinning: TypeAlias = Union[bool, PinningConfigParam]
