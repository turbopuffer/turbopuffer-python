from typing import Iterator, AsyncIterator

import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer


@pytest.fixture(scope="session")
def tpuf() -> Iterator[Turbopuffer]:
    with Turbopuffer(region="gcp-us-central1") as tpuf:
        yield tpuf


@pytest.fixture(scope="session")
async def async_tpuf() -> AsyncIterator[AsyncTurbopuffer]:
    yield AsyncTurbopuffer(region="gcp-us-central1")
