import os
from typing import Iterator, AsyncIterator

import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer

# If the base URL contains a {region} placeholder, use gcp-us-central1.
region = None
if "{region}" in os.getenv("TURBOPUFFER_BASE_URL", "{region}"):
    region = "gcp-us-central1"


@pytest.fixture(scope="session")
def tpuf() -> Iterator[Turbopuffer]:
    with Turbopuffer(region=region) as tpuf:
        yield tpuf


@pytest.fixture(scope="session")
async def async_tpuf() -> AsyncIterator[AsyncTurbopuffer]:
    async with AsyncTurbopuffer(region=region) as client:
        yield client
