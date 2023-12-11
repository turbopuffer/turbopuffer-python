import requests
import turbopuffer
import json
from turbopuffer.api import read_api_key
from turbopuffer.error import TurbopufferError, APIError
from typing import Optional

def make_request(*args: list[str], api_key: Optional[str] = None, method: Optional[str] = None, payload: Optional[dict] = None):
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {read_api_key(api_key)}"})

    request_uri = turbopuffer.api_base_uri + '/' + '/'.join(args)
    try:
        if payload is None and (method is None or method == 'GET'):
            response = s.get(request_uri)
            content = response.json()
            if response.ok:
                return content
            else:
                raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
        elif payload is not None and (method is None or method == 'POST'):
            response = s.post(request_uri, json=payload)
            content = response.json()
            if response.ok:
                return content
            else:
                raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
        elif payload is None and method == 'DELETE':
            response = s.delete(request_uri)
            content = response.json()
            if response.ok:
                return content
            else:
                raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
        else:
            raise TurbopufferError(f'Method not implemented: {method}')
    except json.decoder.JSONDecodeError as err:
        raise TurbopufferError(err)