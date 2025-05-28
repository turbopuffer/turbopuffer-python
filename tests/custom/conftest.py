from typing import Iterator

import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer


@pytest.fixture(scope="session")
def tpuf() -> Iterator[Turbopuffer]:
    with Turbopuffer() as tpuf:
        yield tpuf


@pytest.fixture(scope="session")
def async_tpuf() -> Iterator[AsyncTurbopuffer]:
    yield AsyncTurbopuffer()
