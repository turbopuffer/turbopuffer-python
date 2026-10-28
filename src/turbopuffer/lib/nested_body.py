from __future__ import annotations

from urllib.parse import parse_qs, urlsplit

from .._types import Body

# The API expects these overloads' parameters nested under a property of the write request, but the spec
# describes them at the top level of the body. The Rust SDK does the same with its `nest_body_params` option.
_NESTED_BODY_KEYS = {
    "branchFrom": "branch_from_namespace",
    "copyFrom": "copy_from_namespace",
    "startCopyFrom": "copy_from_namespace",
}


def nest_overload_body(url: str, json_data: Body | None) -> Body | None:
    """Nests an overloaded write request's body under the property the API expects."""
    overloads = parse_qs(urlsplit(url).query).get("stainless_overload")
    key = _NESTED_BODY_KEYS.get(overloads[0]) if overloads else None
    if key is None or json_data is None:
        return json_data
    return {key: json_data}
