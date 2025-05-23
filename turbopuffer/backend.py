import json
import re
import time
import traceback
import requests
import turbopuffer as tpuf
import gzip
from turbopuffer.error import AuthenticationError, raise_api_error
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

def clean_base_url(base_url: str) -> str:
    url = base_url.strip()

    if '://' not in url:
        url = f'https://{url}'

    if url.endswith(('/v1', '/v1/', '/')):
        url = re.sub('(/v1|/v1/|/)$', '', url)

    return url


class Backend:
    api_key: str
    base_url: str
    session: requests.Session

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, headers: Optional[dict] = None):
        if base_url is None:
            base_url = tpuf.api_base_url

        self.api_key = find_api_key(api_key)
        self.base_url = clean_base_url(base_url)
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': f'tpuf-python/{tpuf.VERSION} {requests.utils.default_headers()["User-Agent"]}',
        })

        if headers is not None:
            self.session.headers.update(headers)

    def __eq__(self, other):
        if isinstance(other, Backend):
            return self.api_key == other.api_key and self.base_url == other.base_url and self.headers == other.headers
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

        request = requests.Request(method or 'GET', self.base_url + '/'.join(args))

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
        timeouts = (tpuf.connect_timeout, tpuf.read_timeout)
        while retry_attempt < tpuf.max_retries:
            request_start = time.monotonic()
            try:
                # print(f'Sending request:', prepared.path_url, prepared.headers)
                response = self.session.send(prepared, allow_redirects=False, timeout=timeouts)
                performance['request_time'] = time.monotonic() - request_start
                # print(f'Request time (HTTP {response.status_code}):', performance['request_time'])

                if status_code_should_retry(response.status_code):
                    response.raise_for_status()

                server_timing_str = response.headers.get('Server-Timing', '')
                if len(server_timing_str) > 0:
                    match_cache = re.match(r'.*cache;hit_ratio=([\d\.]+);temperature=(\w+)', server_timing_str)
                    if match_cache:
                        try:
                            performance['cache_hit_ratio'] = float(match_cache.group(1))
                            performance['cache_temperature'] = match_cache.group(2)
                        except ValueError:
                            pass
                    match_exhaustive_search = re.match(r'.*exhaustive_search;count=([\d\.]+)', server_timing_str)
                    if match_exhaustive_search:
                        try:
                            performance['exhaustive_search_count'] = int(match_exhaustive_search.group(1))
                        except ValueError:
                            pass
                    match_processing = re.match(r'.*processing_time;dur=([\d\.]+)', server_timing_str)
                    if match_processing:
                        try:
                            # todo: update this to `processing_time`?
                            performance['server_time'] = float(match_processing.group(1)) / 1000.0
                        except ValueError:
                            pass
                    match_query_execution = re.match(r'.*query_execution_time;dur=([\d\.]+)', server_timing_str)
                    if match_query_execution:
                        try:
                            performance['query_execution_time'] = float(match_query_execution.group(1)) / 1000.0
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
                        raise_api_error(response.status_code, traceback.format_exception_only(err), response.text)

                    if response.ok:
                        performance['total_time'] = time.monotonic() - start
                        return dict(response.__dict__, **{
                            'content': content,
                            'performance': performance,
                        })
                    else:
                        raise_api_error(response.status_code, content.get('status', 'error'), content.get('error', ''))
                else:
                    raise_api_error(response.status_code, 'Server returned non-JSON response', response.text)
            except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as err:
                retry_attempt += 1
                # print(traceback.format_exc())
                if retry_attempt < tpuf.max_retries:
                    # print(f'Retrying request in {2 ** retry_attempt}s...')
                    time.sleep(2 ** retry_attempt)  # exponential falloff up to 64 seconds for 6 retries.
                else:
                    print(f'Request failed after {retry_attempt} attempts...')

                    if isinstance(err, requests.HTTPError):
                        raise_api_error(err.response.status_code,
                                   f'Request to {err.request.url} failed after {retry_attempt} attempts',
                                   str(err))
                    else:
                        raise

def status_code_should_retry(status_code: int) -> bool:
    return status_code >= 500 or status_code in (408, 409, 429)
