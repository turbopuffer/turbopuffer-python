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
        assert False, 'Using CMEK is only available as part of enterprise offerings.'
    except APIError as err:
        assert err.args == ('error (HTTP 400): 💔 CMEK is not currently enabled in this cluster',)
