from typing import Any

try:
    import orjson

    loads = orjson.loads

    def dumps(obj: Any) -> bytes:
        return orjson.dumps(obj)

except ImportError:
    import json
    from datetime import datetime
    from typing_extensions import override

    loads = json.loads

    def dumps(obj: Any) -> bytes:
        return json.dumps(obj, cls=_DateTimeEncoder).encode()

    class _DateTimeEncoder(json.JSONEncoder):
        @override
        def default(self, o: Any) -> Any:
            if isinstance(o, datetime):
                return o.isoformat()
            return super().default(o)
