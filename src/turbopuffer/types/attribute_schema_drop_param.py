# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AttributeSchemaDropParam"]


class AttributeSchemaDropParam(TypedDict, total=False):
    """Drops the attribute from the namespace.

    Cannot be combined with other schema settings.
    """

    drop: Required[bool]
    """Must be `true`."""
