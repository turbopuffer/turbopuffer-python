"""Test that Accept-Encoding header is set correctly based on compression setting."""

import pytest

from turbopuffer import Turbopuffer, AsyncTurbopuffer
from turbopuffer._models import FinalRequestOptions


def test_accept_encoding_with_compression_enabled():
    """When compression is enabled, Accept-Encoding should be 'gzip'."""
    client = Turbopuffer(api_key="test_key", region="use1", compression=True)

    # Build headers with compression enabled
    options = FinalRequestOptions.construct(method="get", url="/test")
    headers = client._build_headers(options)

    assert headers.get("Accept-Encoding") == "gzip"
    assert client.compression is True


def test_accept_encoding_with_compression_disabled():
    """When compression is disabled, Accept-Encoding should be 'identity'."""
    client = Turbopuffer(api_key="test_key", region="use1", compression=False)

    # Build headers with compression disabled
    options = FinalRequestOptions.construct(method="get", url="/test")
    headers = client._build_headers(options)

    assert headers.get("Accept-Encoding") == "identity"
    assert client.compression is False


def test_accept_encoding_custom_header_override():
    """Custom Accept-Encoding header should override default behavior."""
    client = Turbopuffer(api_key="test_key", region="use1", compression=True)

    # User provides custom Accept-Encoding header
    options = FinalRequestOptions.construct(
        method="get",
        url="/test",
        headers={"Accept-Encoding": "deflate"}
    )
    headers = client._build_headers(options)

    # Custom header should be preserved
    assert headers.get("Accept-Encoding") == "deflate"


@pytest.mark.asyncio
async def test_async_accept_encoding_with_compression_enabled():
    """When compression is enabled, Accept-Encoding should be 'gzip' for async client."""
    async with AsyncTurbopuffer(api_key="test_key", region="use1", compression=True) as client:
        # Build headers with compression enabled
        options = FinalRequestOptions.construct(method="get", url="/test")
        headers = client._build_headers(options)

        assert headers.get("Accept-Encoding") == "gzip"
        assert client.compression is True


@pytest.mark.asyncio
async def test_async_accept_encoding_with_compression_disabled():
    """When compression is disabled, Accept-Encoding should be 'identity' for async client."""
    async with AsyncTurbopuffer(api_key="test_key", region="use1", compression=False) as client:
        # Build headers with compression disabled
        options = FinalRequestOptions.construct(method="get", url="/test")
        headers = client._build_headers(options)

        assert headers.get("Accept-Encoding") == "identity"
        assert client.compression is False


def test_accept_encoding_with_options():
    """Test that Accept-Encoding header is correct when using with_options()."""
    client = Turbopuffer(api_key="test_key", region="use1", compression=True)

    # Create a new client with compression disabled
    client_no_compression = client.with_options(compression=False)

    options = FinalRequestOptions.construct(method="get", url="/test")
    headers = client_no_compression._build_headers(options)

    assert headers.get("Accept-Encoding") == "identity"
    assert client_no_compression.compression is False

    # Original client should still have gzip
    headers_original = client._build_headers(options)
    assert headers_original.get("Accept-Encoding") == "gzip"
    assert client.compression is True
