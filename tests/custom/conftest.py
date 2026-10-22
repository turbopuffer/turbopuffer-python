import os
from typing import Iterator, AsyncIterator

import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer

# If the base URL contains a {region} placeholder, use gcp-us-central1.
region = None
if "{region}" in os.getenv("TURBOPUFFER_BASE_URL", "{region}"):
    region = "gcp-us-central1"


def require_api_key() -> None:
    """Skip a live API test when no API key is available.

    PRs from forks don't get repository secrets, so their CI runs only mocked
    tests, and a maintainer runs the live tests with the "Live tests" workflow
    instead. Anywhere else in CI a missing key is a misconfiguration, so fail
    rather than skip silently.
    """
    if os.getenv("TURBOPUFFER_API_KEY"):
        return
    if os.getenv("GITHUB_ACTIONS") == "true" and os.getenv("GITHUB_EVENT_NAME") != "pull_request":
        pytest.fail("TURBOPUFFER_API_KEY must be set to run live API tests in CI")
    pytest.skip("live API test requires TURBOPUFFER_API_KEY")


@pytest.fixture(scope="session")
def tpuf() -> Iterator[Turbopuffer]:
    require_api_key()
    with Turbopuffer(region=region) as tpuf:
        yield tpuf


@pytest.fixture(scope="session")
async def async_tpuf() -> AsyncIterator[AsyncTurbopuffer]:
    require_api_key()
    async with AsyncTurbopuffer(region=region) as client:
        yield client
