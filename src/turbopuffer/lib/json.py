from typing import Any


def _serialize_pydantic(obj: Any) -> Any:
    import pydantic

    from .._compat import model_dump

    if isinstance(obj, pydantic.BaseModel):
        return model_dump(obj, exclude_unset=True, mode="json")
    raise TypeError


try:
    import orjson

    loads = orjson.loads

    def dumps(obj: Any) -> bytes:
        return orjson.dumps(obj, default=_serialize_pydantic)

except ImportError:
    import json
    from datetime import datetime
    from typing_extensions import override

    loads = json.loads

    def dumps(obj: Any) -> bytes:
        return json.dumps(obj, cls=_CustomEncoder).encode()

    class _CustomEncoder(json.JSONEncoder):
        @override
        def default(self, o: Any) -> Any:
            if isinstance(o, datetime):
                return o.isoformat()
            return _serialize_pydantic(o)
