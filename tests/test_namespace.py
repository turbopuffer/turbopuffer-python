from unittest import mock
import requests
import tests
import turbopuffer as tpuf

base_url = "https://gcp-us-east4.turbopuffer.com"

def mock_response_returning(status_code, reason):
    response = mock.Mock(spec=requests.Response)
    response.status_code = status_code
    response.reason = reason
    response.headers = {'Content-Type': 'application/json'}
    response.request = mock.Mock(spec=requests.PreparedRequest)
    response.request.url = base_url
    response.json.return_value = {"status": "OK"}
    return response

def test_namespace_base_url():
    ns_name = tests.test_prefix + "namespace_base_url"
    ns = tpuf.Namespace(ns_name, base_url=base_url)

    with mock.patch.object(ns.backend.session, "send", return_value=mock_response_returning(200, "OK")) as mock_send:
        ns.upsert([
            {'id': 1, 'vector': [0.1, 0.1]},
            {'id': 2, 'vector': [0.2, 0.2], 'attributes': {'test_name': 'namespace'}},
        ], distance_metric='euclidean_squared')

        assert mock_send.called, "Expected the backend session send method to be called"

        args, _ = mock_send.call_args
        request = args[0]
        expected_url = base_url + "/v1/namespaces/" + ns_name
        assert request.url == expected_url
