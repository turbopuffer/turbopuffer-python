import os
import sys

api_key = os.environ.get("TURBOPUFFER_API_KEY")
api_base_url = os.environ.get(
    "TURBOPUFFER_API_BASE_URL", "https://api.turbopuffer.com/v1"
)
upsert_batch_size = 10_000
max_retries = 6

try:
    import orjson  # extras = ["fast"]

    def dump_json_bytes(obj):
        return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY)

except ImportError:
    import json

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if "numpy" in sys.modules:
                if isinstance(obj, sys.modules["numpy"].integer):
                    return int(obj)
                elif isinstance(obj, sys.modules["numpy"].floating):
                    return float(obj)
                elif isinstance(obj, sys.modules["numpy"].ndarray):
                    return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    def dump_json_bytes(obj):
        return json.dumps(obj, cls=NumpyEncoder).encode()


from turbopuffer.error import APIError, AuthenticationError, TurbopufferError
from turbopuffer.namespace import Namespace, namespaces
from turbopuffer.query import FilterTuple, VectorQuery
from turbopuffer.vectors import VectorColumns, VectorResult, VectorRow
from turbopuffer.version import VERSION
