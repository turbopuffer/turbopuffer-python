from typing import Iterator

import pytest
from turbopuffer import Turbopuffer


@pytest.fixture(scope="session")
def tpuf(request: pytest.FixtureRequest) -> Iterator[Turbopuffer]:
    strict = getattr(request, "param", True)
    if not isinstance(strict, bool):
        raise TypeError(f"Unexpected fixture parameter type {type(strict)}, expected {bool}")

    with Turbopuffer() as tpuf:
        yield tpuf
