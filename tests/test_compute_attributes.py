from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple, cast

import pytest

from turbopuffer.types import ComputeAttributes, NamespaceQueryParams
from turbopuffer._utils import maybe_transform
from turbopuffer.types.highlight_config_params import HighlightConfigParams

# An empty HighlightConfigParams (all fields optional) is valid for the
# HighlightWithConfig variant. Annotate it so it unifies with the union.
_empty_highlight_config: HighlightConfigParams = {}

# Each case: (variant name, ComputeAttributes value, expected JSON wire form).
#
# ComputeAttributes = Union[
#     ComputeAttributesVectorDist,           # ("vec", "VectorDist", [0.5])
#     ComputeAttributesHighlight,            # ("Highlight", "body")
#     ComputeAttributesHighlightWithConfig,  # ("Highlight", "body", {})  (3rd elem is HighlightConfigParams)
#     RankBy,                                # e.g. ("vec", "ANN", [0.5])
# ]
#
# The variants are positional tuples that serialize to JSON arrays on the wire.
CASES: List[Tuple[str, ComputeAttributes, List[Any]]] = [
    ("VectorDist", ("vec", "VectorDist", [0.5]), ["vec", "VectorDist", [0.5]]),
    ("Highlight", ("Highlight", "body"), ["Highlight", "body"]),
    ("HighlightWithConfig", ("Highlight", "body", _empty_highlight_config), ["Highlight", "body", {}]),
    ("RankBy", ("vec", "ANN", [0.5]), ["vec", "ANN", [0.5]]),
]


@pytest.mark.parametrize(("variant", "value", "expected_wire"), CASES)
def test_compute_attributes_serialization(variant: str, value: ComputeAttributes, expected_wire: List[Any]) -> None:
    """Every variant of the ComputeAttributes union serializes to its expected wire form."""
    body: NamespaceQueryParams = {
        "compute_attributes": {"my_attr": value},
        "top_k": 10,
    }

    transformed = cast(Dict[str, Any], maybe_transform(body, NamespaceQueryParams))
    serialized = transformed["compute_attributes"]["my_attr"]

    # The wire form is JSON, where tuples become arrays. Round-trip through JSON
    # to normalize tuples -> lists, then assert structural equality.
    assert json.loads(json.dumps(serialized)) == expected_wire, (
        f"variant {variant!r} serialized to {serialized!r}, expected {expected_wire!r}"
    )
