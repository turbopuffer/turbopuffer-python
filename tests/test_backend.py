import pytest
import requests
import time
import turbopuffer as tpuf
from turbopuffer import backend as tpuf_backend
from unittest import mock


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


def test_500_retried():
    backend = tpuf_backend.Backend("fake_api_key")
    backend.session.send = mock.MagicMock()
    backend.session.send.return_value = mock_response_returning(500, 'Internal Error')

    with mock.patch.object(time, 'sleep', return_value=None) as sleep:
        with pytest.raises(tpuf.error.APIError):
            backend.make_api_request('namespaces', payload={})
        assert sleep.call_count == tpuf.max_retries - 1


def test_429_retried():
    backend = tpuf_backend.Backend("fake_api_key")
    backend.session.send = mock.MagicMock()
    backend.session.send.return_value = mock_response_returning(429, 'Too Many Requests')

    with mock.patch.object(time, 'sleep', return_value=None) as sleep:
        with pytest.raises(tpuf.error.APIError):
            backend.make_api_request('namespaces', payload={})
        assert sleep.call_count == tpuf.max_retries - 1
