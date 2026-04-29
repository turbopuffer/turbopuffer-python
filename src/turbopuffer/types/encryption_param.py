# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["EncryptionParam", "CustomerManaged", "Default"]


class CustomerManaged(TypedDict, total=False):
    """Encrypt the namespace with a customer-managed encryption key (CMEK)."""

    key_name: Required[str]
    """The identifier of the CMEK key to use for encryption.

    For GCP, the fully-qualified resource name of the key. For AWS, the ARN of the
    key.
    """

    mode: Required[Literal["customer-managed"]]


class Default(TypedDict, total=False):
    """Use the default server-side encryption (SSE)."""

    mode: Required[Literal["default"]]


EncryptionParam: TypeAlias = Union[CustomerManaged, Default]
