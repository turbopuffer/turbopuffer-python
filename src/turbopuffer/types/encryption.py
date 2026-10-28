# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["Encryption", "CustomerManaged", "Default"]


class CustomerManaged(BaseModel):
    """Encrypt the namespace with a customer-managed encryption key (CMEK)."""

    key_name: str
    """The identifier of the CMEK key to use for encryption.

    For GCP, the fully-qualified resource name of the key. For AWS, the ARN of the
    key.
    """

    mode: Literal["customer-managed"]

    encryption_context: Optional[Dict[str, str]] = None
    """The AWS KMS encryption context to send with every request that uses the key.

    Only supported on AWS, and must be enabled for your organization. Keys may not
    start with `tpuf:` or `aws:`.
    """


class Default(BaseModel):
    """Use the default server-side encryption (SSE)."""

    mode: Literal["default"]


Encryption: TypeAlias = Union[CustomerManaged, Default]
