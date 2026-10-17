import gzip
import json
from io import BytesIO
from typing import Any, Optional
from unittest.mock import Mock

import httpx
import pytest

urllib3 = pytest.importorskip("urllib3")

from turbopuffer import Turbopuffer
from turbopuffer.lib.vector import b64decode_vector
from turbopuffer.lib.transport_urllib3 import Urllib3Transport


@pytest.mark.parametrize("compression", [None, False, True])
@pytest.mark.parametrize("large", [False, True])
def test_urllib3_respects_compression(
    compression: Optional[bool], large: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    transport = Urllib3Transport()
    pool_request = Mock(
        return_value=urllib3.HTTPResponse(
            body=BytesIO(b"{}"), status=200, preload_content=False
        )
    )
    monkeypatch.setattr(transport._pool, "request", pool_request)
    options: dict[str, Any] = (
        {} if compression is None else {"compression": compression}
    )
    with Turbopuffer(
        api_key="test-key",
        base_url="https://api.example.test",
        http_client=httpx.Client(transport=transport),
        **options,
    ) as client:
        client.namespace("test").write(
            upsert_rows=[{"id": 1, "vector": [0.1] * (1024 if large else 1)}]
        )

    sent = pool_request.call_args.kwargs
    expected_compressed = compression is True and large
    assert (sent["headers"].get("Content-Encoding") == "gzip") is expected_compressed
    body = gzip.decompress(sent["body"]) if expected_compressed else sent["body"]
    assert b64decode_vector(
        json.loads(body)["upsert_rows"][0]["vector"]
    ) == pytest.approx([0.1] * (1024 if large else 1))
    assert int(sent["headers"]["Content-Length"]) == len(sent["body"])
