import json
import re
import time
import traceback
import requests
import turbopuffer as tpuf
import gzip
from turbopuffer.error import AuthenticationError, APIError
from typing import Optional, List


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

    def __eq__(self, other):
        if isinstance(other, Backend):
            return self.api_key == other.api_key and self.api_base_url == other.api_base_url
        else:
            return False

    def make_api_request(self,
                         *args: List[str],
                         method: Optional[str] = None,
                         query: Optional[dict] = None,
                         payload: Optional[dict] = None) -> dict:
        start = time.monotonic()
        if method is None and payload is not None:
            method = 'POST'
        request = requests.Request(method or 'GET', self.api_base_url + '/' + '/'.join(args))

        if query is not None:
            request.params = query

        performance = dict()
        if payload is not None:
            payload_start = time.monotonic()
            if isinstance(payload, dict):
                json_payload = tpuf.dump_json_bytes(payload)
                performance['json_time'] = time.monotonic() - payload_start
            elif isinstance(payload, bytes):
                json_payload = payload
            else:
                raise ValueError(f'Unsupported POST payload type: {type(payload)}')

            gzip_start = time.monotonic()
            gzip_payload = gzip.compress(json_payload, compresslevel=1)
            performance['gzip_time'] = time.monotonic() - gzip_start
            if len(gzip_payload) > 0:
                performance['gzip_ratio'] = len(json_payload) / len(gzip_payload)

            request.headers.update({
                'Content-Type': 'application/json',
                'Content-Encoding': 'gzip',
            })
            request.data = gzip_payload

        prepared = self.session.prepare_request(request)

        retry_attempt = 0
        while retry_attempt < tpuf.max_retries:
            request_start = time.monotonic()
            try:
                # print(f'Sending request:', prepared.path_url, prepared.headers)
                response = self.session.send(prepared, allow_redirects=False)
                performance['request_time'] = time.monotonic() - request_start
                # print(f'Request time (HTTP {response.status_code}):', performance['request_time'])

                if response.status_code > 500:
                    response.raise_for_status()

                server_timing_str = response.headers.get('Server-Timing', '')
                if len(server_timing_str) > 0:
                    match_processing = re.match(r'.*processing_time;dur=([\d\.]+)', server_timing_str)
                    if match_processing:
                        try:
                            performance['server_time'] = float(match_processing.group(1)) / 1000.0
                        except ValueError:
                            pass
                    match_exhaustive = re.match(r'.*exhaustive_search_count;count=([\d\.]+)', server_timing_str)
                    if match_exhaustive:
                        try:
                            performance['exhaustive_search_count'] = int(match_exhaustive.group(1))
                        except ValueError:
                            pass

                if method == 'HEAD':
                    return dict(response.__dict__, **{
                        'performance': performance,
                    })

                content_type = response.headers.get('Content-Type', 'text/plain')
                if content_type == 'application/json':
                    try:
                        content = response.json()
                    except json.JSONDecodeError as err:
                        raise APIError(response.status_code, traceback.format_exception_only(err), response.text)

                    if response.ok:
                        performance['total_time'] = time.monotonic() - start
                        return dict(response.__dict__, **{
                            'content': content,
                            'performance': performance,
                        })
                    else:
                        raise APIError(response.status_code, content.get('status', 'error'), content.get('error', ''))
                else:
                    raise APIError(response.status_code, 'Server returned non-JSON response', response.text)
            except requests.HTTPError as http_err:
                retry_attempt += 1
                # print(traceback.format_exc())
                if retry_attempt < tpuf.max_retries:
                    # print(f'Retrying request in {2 ** retry_attempt}s...')
                    time.sleep(2 ** retry_attempt)  # exponential falloff up to 64 seconds for 6 retries.
                else:
                    print(f'Request failed after {retry_attempt} attempts...')
                    raise APIError(http_err.response.status_code,
                                   f'Request to {http_err.request.url} failed after {retry_attempt} attempts',
                                   str(http_err))
