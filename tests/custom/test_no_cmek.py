import turbopuffer
from turbopuffer import Turbopuffer
from tests.custom import test_prefix


def test_no_cmek(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "no_cmek")

    try:
        ns.write(
            upsert_columns={
                "id": [1, 2],
                "vector": [[0.1, 0.1], [0.2, 0.2]],
            },
            distance_metric="cosine_distance",
            encryption={"cmek": {"key_name": "mykey"}},
        )
        raise AssertionError("CMEK requires additional setup")
    except turbopuffer.BadRequestError as err:
        assert "Malformed Cloud KMS crypto key: mykey" in err.message
