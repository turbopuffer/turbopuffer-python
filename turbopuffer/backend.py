import time
import traceback
import requests
import turbopuffer as tpuf
import gzip
from turbopuffer.error import TurbopufferError, AuthenticationError, APIError
from typing import Optional, List, Union
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

    def make_api_request(self, *args: List[str], method: Optional[str] = None, query: Optional[dict] = None, payload: Optional[Union[JSONSerializable, dict]] = None) -> dict:
        start = time.monotonic()
        if method is None and payload is not None: method = 'POST'
        request = requests.Request(method or 'GET', self.api_base_url + '/' + '/'.join(args))

        if query is not None:
            request.params = query

        if payload is not None:
            if isinstance(payload, JSONSerializable):
                # before = time.monotonic()
                dict_payload = payload.to_dict()
                # print('Dict time:', time.monotonic() - before)
                # before = time.monotonic()
                json_payload = tpuf.dump_json_bytes(dict_payload)
                # print('Json time:', time.monotonic() - before)
            elif isinstance(payload, dict):
                json_payload = tpuf.dump_json_bytes(payload)
            else:
                raise ValueError(f'Unsupported POST payload type: {type(payload)}')

            # before = time.monotonic()
            gzip_payload = gzip.compress(json_payload, compresslevel=1)
            # print(f'Gzip time ({len(json_payload) / 1024 / 1024} MiB json / {len(gzip_payload) / 1024 / 1024} MiB gzip):', time.monotonic() - before)

            request.headers.update({
                'Content-Type': 'application/json',
                'Content-Encoding': 'gzip',
            })
            request.data = gzip_payload

        prepared = self.session.prepare_request(request)

        retry_attempts = 0
        while retry_attempts < 3:
            # before = time.monotonic()
            try:
                # print(f'Sending request:', prepared.path_url, prepared.headers)
                response = self.session.send(prepared, allow_redirects=False)
                # print(f'Request time (HTTP {response.status_code}):', time.monotonic() - before)

                if response.status_code > 500:
                    response.raise_for_status()

                content_type = response.headers.get('Content-Type', 'text/plain')
                if content_type == 'application/json':
                    try:
                        content = response.json()
                    except json.JSONDecodeError as err:
                        raise APIError(response.status_code, traceback.format_exception_only(err), response.text)

                    if response.ok:
                        # print("Total request time:", time.monotonic() - start)
                        return content
                    else:
                        raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
                else:
                    raise APIError(response.status_code, 'Server returned non-JSON response', response.text)
            except requests.HTTPError:
                print(traceback.format_exc())
                print("retrying...")
                retry_attempts += 1
                time.sleep(2)
        print("Total request time (failed):", time.monotonic() - start)
        raise TurbopufferError('Failed after 3 retries')
