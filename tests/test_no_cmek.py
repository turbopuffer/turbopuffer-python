import turbopuffer as tpuf
from turbopuffer.error import APIError
import tests


def test_no_cmek():
    ns = tpuf.Namespace(tests.test_prefix + 'no_cmek')

    try:
        ns.write(
            upsert_columns={
                "id": [1, 2],
                "vector": [[0.1, 0.1], [0.2, 0.2]],
            },
            distance_metric='cosine_distance',
            encryption={
                "cmek": {
                    "key_name": "mykey"
                }
            }
        )
        assert False, 'CMEK requires additional setup'
    except APIError as err:
        assert err.args[0].startswith('error (HTTP 400):')
