import turbopuffer as tpuf
from turbopuffer.error import APIError
import tests


def test_no_encryption():
    ns = tpuf.Namespace(tests.test_prefix + 'no_encryption')

    try:
        ns.upsert(
            {
                'ids': [1, 2],
                'vectors': [[0.1, 0.1], [0.2, 0.2]],
            },
            distance_metric='cosine_distance',
            encryption={
                'cmek': {
                    'key_name': 'mykey'
                }
            }
        )
        assert False, 'Using encryption is only available as part of enterprise offerings.'
    except APIError as err:
        assert err.args == ('error (HTTP 400): 💔 CMEK is not currently enabled in this cluster',)
