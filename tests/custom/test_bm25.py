import pytest

import turbopuffer
from turbopuffer import Turbopuffer
from tests.custom import test_prefix
from turbopuffer.types import RankBy, AttributeSchemaParam, FullTextSearchConfigParam, AttributeSchemaConfigParam


def test_bm25(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "bm25")

    schema: dict[str, AttributeSchemaParam] = {
        "blabla": AttributeSchemaConfigParam(
            type="string",
            full_text_search=FullTextSearchConfigParam(
                language="english",
                stemming=True,
                case_sensitive=False,
                remove_stopwords=True,
            ),
        ),
    }

    # Upsert with dict
    ns.write(
        upsert_columns={
            "id": [1, 2, 3, 4],
            "vector": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
            "blabla": [
                "the fox is quick and brown",
                "fox jumped over the lazy dog",
                "the dog is lazy and brown",
                "walrus is slow and inferior",
            ],
            "fact_id": ["a", "b", "c", "d"],
        },
        distance_metric="euclidean_squared",
        schema=schema,
    )

    # Query with dict
    result = ns.query(top_k=10, rank_by=("blabla", "BM25", "fox jumping"))
    assert result.rows is not None
    assert [item.id for item in result.rows] == [2, 1]

    # Upsert with named args
    ns.write(
        upsert_columns={
            "id": [7],
            "vector": [[0.7, 0.7]],
            "blabla": ["walruses can live up to 40 years"],
            "fact_id": ["g"],
        },
        schema=schema,
    )

    # Query with named args (and combined ranking)
    result = ns.query(
        top_k=2,
        rank_by=(
            "Sum",
            [("blabla", "BM25", "walrus tusk"), ("blabla", "BM25", "jumping fox")],
        ),
        filters=("fact_id", "NotEq", "z"),
    )
    assert result.rows is not None
    assert [item.id for item in result.rows] == [2, 4]

    # Upsert with row-based upsert format
    ns.write(
        upsert_rows=[
            {
                "id": 8,
                "vector": [0.8, 0.8],
                "blabla": "row based upsert format is cool",
                "fact_id": "h",
            },
            {
                "id": 9,
                "vector": [0.9, 0.9],
                "blabla": "dict format of row based upsert also works, but isn't typed as well",
                "fact_id": "i",
            },
        ],
        schema=schema,
    )

    # Query to make sure the new row(s) is there
    result = ns.query(
        top_k=10,
        rank_by=("blabla", "BM25", "row based upsert"),
    )
    assert result.rows is not None
    assert [item.id for item in result.rows] == [8, 9]


def test_bm25_product_operator(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "bm25_product_operator")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    schema: dict[str, AttributeSchemaParam] = {
        "title": {
            "type": "string",
            "full_text_search": True,
        },
        "content": {
            "type": "string",
            "full_text_search": True,
        },
    }

    # Upsert a few docs
    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1, 0.1],
                "title": "the quick brown fox",
                "content": "jumped over the lazy dog",
            },
            {
                "id": 2,
                "vector": [0.2, 0.2],
                "title": "the lazy dog",
                "content": "is brown",
            },
        ],
        distance_metric="euclidean_squared",
        schema=schema,
    )

    # Try out a bunch of query variations
    queries: list[RankBy] = [
        ("Product", (0.5, ("title", "BM25", "quick brown"))),
        ("Product", (("title", "BM25", "quick brown"), 0.5)),
        (
            "Sum",
            [
                ("Product", (0.5, ("title", "BM25", "quick brown"))),
                ("content", "BM25", "brown"),
            ],
        ),
        (
            "Product",
            (
                0.5,
                (
                    "Sum",
                    [
                        ("Product", (0.5, ("title", "BM25", "quick brown"))),
                        ("content", "BM25", "brown"),
                    ],
                ),
            ),
        ),
    ]

    for query in queries:
        result = ns.query(
            rank_by=query,
            top_k=10,
        )
        assert result.rows is not None
        assert len(result.rows) > 0


def test_bm25_ContainsAllTokens(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "bm25_ContainsAllTokens")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "vector": [0.1, 0.1],
                "text": "Walruses are large marine mammals with long tusks and whiskers",
            }
        ],
        schema={
            "text": {
                "type": "string",
                "full_text_search": {
                    "stemming": True,
                },
            },
        },
        distance_metric="cosine_distance",
    )

    result = ns.query(
        rank_by=("text", "BM25", "walrus whisker"),
        filters=("text", "ContainsAllTokens", "marine mammals"),
        top_k=10,
    )
    assert result.rows is not None
    assert len(result.rows) == 1

    missing = ns.query(
        rank_by=("text", "BM25", "walrus whisker"),
        filters=("text", "ContainsAllTokens", "marine mammals short"),
        top_k=10,
    )
    assert missing.rows is not None
    assert len(missing.rows) == 0


def test_bm25_pre_tokenized_array(tpuf: Turbopuffer):
    ns = tpuf.namespace(test_prefix + "bm25_pre_tokenized_array")

    try:
        ns.delete_all()
    except turbopuffer.NotFoundError:
        pass

    schema: dict[str, AttributeSchemaParam] = {
        "content": AttributeSchemaConfigParam(
            type="[]string",
            full_text_search=FullTextSearchConfigParam(
                tokenizer="pre_tokenized_array",
            ),
        ),
    }

    ns.write(
        upsert_rows=[
            {
                "id": 1,
                "content": ["jumped", "over", "the", "lazy", "dog"],
            },
            {
                "id": 2,
                "content": ["the", "lazy", "dog", "is", "brown"],
            },
        ],
        schema=schema,
    )

    result = ns.query(
        rank_by=("content", "BM25", ["jumped"]),
        top_k=10,
    )
    assert result.rows is not None
    assert len(result.rows) == 1
    assert result.rows[0].id == 1

    result = ns.query(
        rank_by=("content", "BM25", ["dog"]),
        top_k=10,
    )
    assert result.rows is not None
    assert len(result.rows) == 2

    with pytest.raises(
        turbopuffer.APIError, match=r"""invalid input \\'jumped\\' for rank_by field "content", expecting \[\]string"""
    ):
        # Query must be an array.
        ns.query(
            rank_by=("content", "BM25", "jumped"),
            top_k=10,
        )
