import asyncio
import time
import sys
from unittest import mock
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import requests
import aiohttp
import turbopuffer as tpuf
from turbopuffer import backend as tpuf_backend
from turbopuffer.error import APIError, raise_api_error


def mock_response_returning(status_code, reason):
    response = mock.Mock(spec=requests.Response)
    response.status_code = status_code
    # None of these values really matter, they're just accessed in Backend, so
    # they need to exist.
    response.url = tpuf.api_base_url
    response.reason = reason
    response.headers = {}
    response.request = mock.Mock(spec=requests.PreparedRequest)
    response.request.url = response.url
    response.raise_for_status = lambda: requests.Response.raise_for_status(response)
    return response


def setup_failing_async_response(status_code, reason):
    """Helper function to configure backend with failing async response"""
    # Create backend with test API key
    backend = tpuf_backend.Backend("fake_api_key")

    # Create a proper mock response with spec for better compatibility
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = status_code
    mock_response.ok = False
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.text = AsyncMock(return_value=reason)
    # This method will be called when we need to parse json response
    mock_response.json = AsyncMock(return_value={"status": "error", "error": reason})
    
    # Configure raise_for_status to raise the appropriate exception
    error = aiohttp.ClientResponseError(
        request_info=AsyncMock(),
        history=tuple(),
        status=status_code,
        message=reason,
        headers={}
    )
    mock_response.raise_for_status.side_effect = error

    # Create a proper context manager class
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return None

    # Create a session mock that returns our context manager
    mock_session = AsyncMock()
    mock_session.request = MagicMock(return_value=MockContextManager())
    mock_session.closed = False
    
    # Patch the _get_async_session method to return our mock session
    with patch.object(backend, '_get_async_session', AsyncMock(return_value=mock_session)):
        pass  # This applies the patch for the whole function scope
    
    return backend, mock_session.request


async def _test_500_retried_async():
    """Async implementation for the 500 error retry test"""
    # Create backend with test API key
    backend = tpuf_backend.Backend("fake_api_key")
    
    # Create mock response with internal server error
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 500
    mock_response.ok = False
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.text = AsyncMock(return_value="Internal Server Error")
    mock_response.json = AsyncMock(return_value={"status": "error", "error": "Internal Server Error"})
    
    # Configure raise_for_status to raise an appropriate exception
    error = aiohttp.ClientResponseError(
        request_info=AsyncMock(),
        history=tuple(),
        status=500,
        message="Internal Server Error",
        headers={}
    )
    mock_response.raise_for_status.side_effect = error
    
    # Create context manager
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return None
    
    # Create session
    mock_session = AsyncMock()
    mock_session.request = MagicMock(return_value=MockContextManager())
    mock_session.closed = False
    
    # Patching
    with patch.object(backend, '_get_async_session', AsyncMock(return_value=mock_session)):
        # Directly patch asyncio.sleep to count retries
        with patch.object(asyncio, 'sleep', AsyncMock()) as sleep:
            # We expect an API error when we make the request
            with pytest.raises(APIError):
                await backend.amake_api_request("vectors")
            
            # Since the 500 error should trigger retries, verify the sleep and request counts
            assert sleep.call_count == tpuf.max_retries - 1
            assert mock_session.request.call_count == tpuf.max_retries

def test_500_retried_async():
    """Synchronous wrapper for the async retry test"""
    asyncio.run(_test_500_retried_async())

# Helper function removed as we're using asyncio.run directly

def test_500_retried():
    """Test that 500 errors are properly retried in the sync API"""
    # Since the sync API now just calls the async API, we can reuse the async test
    asyncio.run(_test_500_retried_sync())
    
async def _test_500_retried_sync():
    """Async version of the sync retry test"""
    # Create backend with test API key
    backend = tpuf_backend.Backend("fake_api_key")
    
    # Create mock response with internal server error
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 500
    mock_response.ok = False
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.text = AsyncMock(return_value="Internal Server Error")
    mock_response.json = AsyncMock(return_value={"status": "error", "error": "Internal Server Error"})
    
    # Configure raise_for_status to raise an appropriate exception
    error = aiohttp.ClientResponseError(
        request_info=AsyncMock(),
        history=tuple(),
        status=500,
        message="Internal Server Error",
        headers={}
    )
    mock_response.raise_for_status.side_effect = error
    
    # Create context manager
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return None
    
    # Create session
    mock_session = AsyncMock()
    mock_session.request = MagicMock(return_value=MockContextManager())
    mock_session.closed = False
    
    # Patching
    with patch.object(backend, '_get_async_session', AsyncMock(return_value=mock_session)):
        # Directly patch asyncio.sleep to count retries
        with patch.object(asyncio, 'sleep', AsyncMock()) as sleep:
            # Use run_in_executor to call the sync API from async context
            loop = asyncio.get_event_loop()
            
            # We expect an API error when calling the sync version
            with pytest.raises(APIError):
                # Call the sync method which internally calls the async one
                await loop.run_in_executor(None, lambda: backend.make_api_request("vectors"))
            
            # Since we're using the same underlying amake_api_request, count should be the same
            assert sleep.call_count == tpuf.max_retries - 1
            assert mock_session.request.call_count == tpuf.max_retries


async def _test_429_retried_async():
    """Async implementation for 429 error retry test"""
    
    # Setup backend with failing response
    backend = tpuf_backend.Backend("fake_api_key")
    
    # Create a response mock with the appropriate async context manager methods
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 429
    mock_response.ok = False
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.text = AsyncMock(return_value="Too Many Requests")
    mock_response.json = AsyncMock(return_value={"status": "error", "error": "Rate limit exceeded"})
    
    # Set up the raise_for_status method to raise an appropriate exception
    error = aiohttp.ClientResponseError(
        request_info=AsyncMock(),
        history=tuple(),
        status=429,
        message="Too Many Requests",
        headers={}
    )
    mock_response.raise_for_status.side_effect = error
    
    # Create a proper context manager class
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return None
    
    # Create a session mock that returns our context manager
    mock_session = AsyncMock()
    mock_session.request = MagicMock(return_value=MockContextManager())
    mock_session.closed = False
    
    # Patch the _get_async_session method to return our mock
    with patch.object(backend, '_get_async_session', AsyncMock(return_value=mock_session)):
        # Patch asyncio.sleep to avoid waiting
        with patch.object(asyncio, 'sleep', AsyncMock(return_value=None)) as sleep:
            # Expect an APIError when we call make_api_request
            with pytest.raises(APIError):
                await backend.amake_api_request("namespaces", payload={})
            
            # Verify retry behavior
            assert sleep.call_count == tpuf.max_retries - 1
            assert mock_session.request.call_count == tpuf.max_retries
            
def test_429_retried_async():
    """Synchronous wrapper for the async 429 retry test"""
    asyncio.run(_test_429_retried_async())


def test_429_retried():
    """Test that 429 errors are properly retried in sync API which calls async"""
    # For the sync API, we can use the make_api_request method with the same setup
    asyncio.run(_test_429_retried_sync())
    
async def _test_429_retried_sync():
    """Test async function for the sync API that internally calls async"""
    # Same setup as the async test
    backend = tpuf_backend.Backend("fake_api_key")
    
    # Create mock response
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 429
    mock_response.ok = False
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.text = AsyncMock(return_value="Too Many Requests")
    mock_response.json = AsyncMock(return_value={"status": "error", "error": "Rate limit exceeded"})
    
    # Set up exception
    error = aiohttp.ClientResponseError(
        request_info=AsyncMock(),
        history=tuple(),
        status=429,
        message="Too Many Requests",
        headers={}
    )
    mock_response.raise_for_status.side_effect = error
    
    # Context manager
    class MockContextManager:
        async def __aenter__(self):
            return mock_response
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return None
    
    # Session
    mock_session = AsyncMock()
    mock_session.request = MagicMock(return_value=MockContextManager())
    mock_session.closed = False
    
    # Patch
    with patch.object(backend, '_get_async_session', AsyncMock(return_value=mock_session)):
        with patch.object(asyncio, 'sleep', AsyncMock(return_value=None)) as sleep:
            # Use the sync API which calls the async API internally
            with pytest.raises(APIError):
                # Use run_in_executor to call sync from async
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, lambda: backend.make_api_request("namespaces", payload={}))
            
            # Verify
            assert sleep.call_count == tpuf.max_retries - 1
            assert mock_session.request.call_count == tpuf.max_retries


def test_custom_headers():
    """Test that custom headers are properly passed to sync sessions"""
    # Since we mock the find_api_key function, no API key errors will occur
    with patch.object(tpuf_backend, 'find_api_key', return_value='fake_api_key'):
        backend = tpuf_backend.Backend(headers={"foo": "bar"})
        # Test sync session headers
        assert backend.session.headers["foo"] == "bar"
        
        # Test that namespace correctly passes headers to backend
        ns = tpuf.Namespace("fake_namespace", headers={"foo": "bar"})
        assert ns.backend.session.headers["foo"] == "bar"
        
        # Test headers are stored in the backend for later async session creation
        assert backend.headers == {"foo": "bar"}


async def _test_custom_headers_async():
    """Async implementation for testing custom headers in async contexts"""
    # Mock the find_api_key to avoid auth errors
    with patch.object(tpuf_backend, 'find_api_key', return_value='fake_api_key'):
        # Create backend with custom headers
        backend = tpuf_backend.Backend(headers={"foo": "bar"})
        assert backend.headers == {"foo": "bar"}
        
        # Create a mock session to be returned by ClientSession
        mock_session = AsyncMock()
        mock_session.closed = False
        
        # Mock the ClientSession constructor
        with patch('aiohttp.ClientSession', return_value=mock_session) as mock_client_session:
            # Call the method that creates the session
            await backend._get_async_session()
            
            # Verify ClientSession was called with headers
            mock_client_session.assert_called_once()
            call_kwargs = mock_client_session.call_args.kwargs
            assert 'headers' in call_kwargs
            assert 'foo' in call_kwargs['headers']
            assert call_kwargs['headers']['foo'] == 'bar'
        
        # Test with AsyncNamespace
        with patch.object(tpuf, 'api_key', 'fake_api_key'):
            ns = tpuf.AsyncNamespace("fake_namespace", headers={"foo": "bar"})
            assert ns.backend.headers == {"foo": "bar"}
            
def test_custom_headers_async():
    """Synchronous wrapper for async headers test"""
    asyncio.run(_test_custom_headers_async())

# Remove redundant test that uses run_async_test helper


def test_backend_eq():
    """Test that backend equality checks work correctly"""
    # Mock find_api_key to avoid auth errors
    with patch.object(tpuf_backend, 'find_api_key', return_value='fake_api_key'):
        backend = tpuf_backend.Backend(headers={"foo": "bar"})
    
        # Different headers should not be equal
        with patch.object(tpuf_backend, 'find_api_key', return_value='fake_api_key'):
            backend2 = tpuf_backend.Backend(headers={"foo": "notbar"})
            assert backend != backend2
    
        # Same api key and headers should be equal
        with patch.object(tpuf_backend, 'find_api_key', return_value='fake_api_key'):
            backend2 = tpuf_backend.Backend(headers={"foo": "bar"})
            assert backend == backend2
    
        # Different api key should not be equal
        with patch.object(tpuf_backend, 'find_api_key', return_value='fake_api_key2'):
            backend2 = tpuf_backend.Backend("fake_api_key2", headers={"foo": "bar"})
            assert backend != backend2
