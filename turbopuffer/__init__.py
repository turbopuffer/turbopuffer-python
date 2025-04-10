import os
import sys
api_key = os.environ.get('TURBOPUFFER_API_KEY')
api_base_url = os.environ.get('TURBOPUFFER_API_BASE_URL', 'https://api.turbopuffer.com')
upsert_vectors_as_base64 = os.environ.get('TURBOPUFFER_UPSERT_VECTORS_AS_BASE64', 'true').lower() == 'true'
upsert_batch_size = 10_000
max_retries = 6
connect_timeout = 10 # seconds
read_timeout = 180 # seconds

try:
    import orjson  # extras = ["fast"]
    def dump_json_bytes(obj): return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY)
except ImportError:
    import json

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if 'numpy' in sys.modules:
                if isinstance(obj, sys.modules['numpy'].integer):
                    return int(obj)
                elif isinstance(obj, sys.modules['numpy'].floating):
                    return float(obj)
                elif isinstance(obj, sys.modules['numpy'].ndarray):
                    return obj.tolist()
            if isinstance(obj, VectorRow) or isinstance(obj, VectorColumns):
                # sanity check; should not be used in the v2 write api
                raise ValueError('Cannot serialize VectorRow or VectorColumns to JSON')
            return json.JSONEncoder.default(self, obj)

    def dump_json_bytes(obj): return json.dumps(obj, cls=NumpyEncoder).encode()

try:
    import pybase64  # extras = ["fast"]
    def b64encode_as_string(bytes): return pybase64.b64encode_as_string(bytes)
except ImportError:
    import base64
    def b64encode_as_string(bytes): return base64.b64encode(bytes).decode('utf-8')

from turbopuffer.version import VERSION
from turbopuffer.namespace import Namespace, namespaces, AttributeSchema, FullTextSearchParams
from turbopuffer.vectors import VectorColumns, VectorRow, VectorResult
from turbopuffer.query import VectorQuery, Filters, RankInput
from turbopuffer.error import TurbopufferError, AuthenticationError, APIError, NotFoundError
