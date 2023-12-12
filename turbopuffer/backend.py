import requests
import turbopuffer
import json
import gzip
from turbopuffer.error import TurbopufferError, AuthenticationError, APIError
from typing import Optional
from dataclass_wizard import JSONSerializable

def find_api_key(api_key: Optional[str] = None) -> str:
    import turbopuffer
    if api_key is not None:
        return api_key
    elif turbopuffer.api_key is not None:
        return turbopuffer.api_key
    else:
        raise AuthenticationError("No turbopuffer API key was provided.\n"
            "Set the TURBOPUFFER_API_KEY environment variable, "
            "or pass `api_key=` when creating a Namespace.")


def make_api_request(*args: list[str], api_key: Optional[str] = None, method: Optional[str] = None, cursor: Optional[str] = None, payload: Optional[dict] = None) -> dict:
    s = requests.Session()
    s.headers.update({
        'Authorization': f'Bearer {find_api_key(api_key)}',
        'User-Agent': f'turbopuffer-python/{turbopuffer.VERSION} {requests.utils.default_headers()["User-Agent"]}'
    })

    request_uri = turbopuffer.api_base_uri + '/' + '/'.join(args)
    try:
        if payload is None and (method is None or method == 'GET'):
            if cursor is not None:
                params = {'cursor': cursor}
            else:
                params = None
            response = s.get(request_uri, params=params)
        elif payload is not None and (method is None or method == 'POST'):
            if isinstance(payload, JSONSerializable):
                json_payload = payload.to_json()
                print('Posting:', json_payload)
                response = s.post(request_uri, headers={
                    'Content-Type': 'application/json',
                    'Content-Encoding': 'gzip',
                },
                data=gzip.compress(json_payload.encode()))
            else:
                raise ValueError(f'Unsupported POST payload type: {type(payload).name}')
        elif payload is None and method == 'DELETE':
            response = s.delete(request_uri)
        else:
            raise TurbopufferError(f'Method not implemented: {method}')

        content_type = response.headers.get('Content-Type', 'text/plain')
        if content_type == 'application/json':
            content = response.json()
            if response.ok:
                return content
            else:
                raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
        else:
            raise APIError(response.status_code, 'invalid_response', response.text)
    except json.decoder.JSONDecodeError as err:
        raise TurbopufferError(err)