import uuid
import turbopuffer as tpuf
import tests
import pytest
from datetime import datetime
from typing import List


def test_patches():
    ns = tpuf.Namespace(tests.test_prefix + 'patches')

    ns.write(
        upsert_rows=[
            {'id': 1, 'vector': [1, 1]},
            {'id': 2, 'vector': [2, 2]},
        ],
        distance_metric='euclidean_squared'
    )

    ns.write(
        patch_rows=[
            {'id': 1, 'a': 1},
            {'id': 2, 'b': 2},
        ],
    )

    ns.write(
        patch_rows=[
            {'id': 1, 'b': 1},
            {'id': 2, 'a': 2},
        ],
    )

    result = ns.query(rank_by=["id", "asc"], include_attributes=['a', 'b'], top_k=10)
    assert len(result.rows) == 2
    print(result.rows)
    assert result.rows[0].id == 1
    assert result.rows[0].attributes == {'a': 1, 'b': 1}
    assert result.rows[1].id == 2
    assert result.rows[1].attributes == {'a': 2, 'b': 2}

    ns.write(
        patch_columns={
            'id': [1, 2],
            'a': [11, 22],
            'c': [1, 2],
        },
    )

    result = ns.query(rank_by=["id", "asc"], include_attributes=['a', 'b', 'c'], top_k=10)
    assert len(result.rows) == 2
    assert result.rows[0].id == 1
    assert result.rows[0].attributes == {'a': 11, 'b': 1, 'c': 1}
    assert result.rows[1].id == 2
    assert result.rows[1].attributes == {'a': 22, 'b': 2, 'c': 2}
