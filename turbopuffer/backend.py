import time
import traceback
import requests
import turbopuffer as tpuf
import json
import gzip
from turbopuffer.error import TurbopufferError, AuthenticationError, APIError
from typing import Optional, List
from dataclass_wizard import JSONSerializable

def find_api_key(api_key: Optional[str] = None) -> str:
    if api_key is not None:
        return api_key
    elif tpuf.api_key is not None:
        return tpuf.api_key
    else:
        raise AuthenticationError("No turbopuffer API key was provided.\n"
            "Set the TURBOPUFFER_API_KEY environment variable, "
            "or pass `api_key=` when creating a Namespace.")

class Backend:
    api_key: str
    api_base_url: str
    session: requests.Session

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = find_api_key(api_key)
        self.api_base_url = tpuf.api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': f'tpuf-python/{tpuf.VERSION} {requests.utils.default_headers()["User-Agent"]}',
        })

    def make_api_request(self, *args: List[str], method: Optional[str] = None, query: Optional[dict] = None, payload: Optional[dict] = None) -> dict:
        start = time.monotonic()
        if method is None and payload is not None: method = 'POST'
        request = requests.Request(method or 'GET', self.api_base_url + '/' + '/'.join(args))

        if query is not None:
            request.params = query

        if payload is not None:
            try:
                if isinstance(payload, JSONSerializable):
                    # before = time.monotonic()
                    json_payload = payload.to_json()
                    # print('Json time:', time.monotonic() - before)
                    # before = time.monotonic()
                    gzip_payload = gzip.compress(json_payload.encode(), compresslevel=1)
                    # print(f'Gzip time ({len(json_payload) / 1024 / 1024} MiB json / {len(gzip_payload) / 1024 / 1024} MiB gzip):', time.monotonic() - before)

                    request.headers.update({
                        'Content-Type': 'application/json',
                        'Content-Encoding': 'gzip',
                    })
                    request.data = gzip_payload
                else:
                    raise ValueError(f'Unsupported POST payload type: {type(payload)}')
            except json.decoder.JSONDecodeError as err:
                raise TurbopufferError(err)

        prepared = self.session.prepare_request(request)

        retry_attempts = 0
        while retry_attempts < 3:
            # before = time.monotonic()
            try:
                # print(f'Sending request:', prepared.path_url, prepared.headers)
                response = self.session.send(prepared, allow_redirects=False)
                # print(f'Request time (HTTP {response.status_code}):', time.monotonic() - before)

                content_type = response.headers.get('Content-Type', 'text/plain')
                if content_type == 'application/json':
                    content = response.json()
                    if response.ok:
                        # print("Total request time:", time.monotonic() - start)
                        return content
                    else:
                        raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
                else:
                    raise requests.HTTPError('invalid_response', response.text, request=prepared, response=response)
            except json.JSONDecodeError:
                print(traceback.format_exc())
                raise requests.HTTPError('invalid_response', response.text, request=prepared, response=response)
            except requests.HTTPError:
                print(traceback.format_exc())
                print("retrying...")
                retry_attempts += 1
                time.sleep(2)
        print("Total request time (failed):", time.monotonic() - start)
        raise TurbopufferError('Failed after 3 retries')
