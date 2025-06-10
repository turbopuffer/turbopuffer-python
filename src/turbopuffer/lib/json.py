from typing import Any

try:
    import orjson

    loads = orjson.loads

    def dumps(obj: Any) -> bytes:
        return orjson.dumps(obj)

except ImportError:
    import json

    loads = json.loads

    def dumps(obj: Any) -> bytes:
        return json.dumps(obj).encode()
