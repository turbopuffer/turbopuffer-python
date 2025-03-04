import turbopuffer as tpuf
import tests


def test_bm25():
    ns = tpuf.Namespace(tests.test_prefix + "bm25")

    schema = {
        "blabla": {
            "type": "string",
            "bm25": {
                "language": "english",
                "stemming": True,
                "case_sensitive": False,
                "remove_stopwords": True,
            },
        }
    }

    # Upsert with dict
    ns.upsert(
        {
            "ids": [1, 2, 3, 4],
            "vectors": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
            "attributes": {
                "blabla": [
                    "the fox is quick and brown",
                    "fox jumped over the lazy dog",
                    "the dog is lazy and brown",
                    "walrus is slow and inferior",
                ],
                "fact_id": ["a", "b", "c", "d"],
            },
            "schema": schema,
        }
    )

    # Query with dict
    results = ns.query({"top_k": 10, "rank_by": ("blabla", "BM25", "fox jumping")})
    assert [item.id for item in results] == [2, 1]

    # Upsert with positional args
    ns.upsert(
        [5, 6],
        [[0.5, 0.5], [0.6, 0.6]],
        {
            "blabla": [
                "Male Pacific walruses can be over 3.6m long and weigh over 1500kg",
                "Female walruses have tusks too",
            ],
            "fact_id": ["e", "f"],
        },
        schema,
    )

    # Upsert with named args
    ns.upsert(
        ids=[7],
        vectors=[[0.7, 0.7]],
        attributes={"blabla": ["walruses can live up to 40 years"], "fact_id": ["g"]},
        schema=schema,
    )

    # Query with named args (and combined ranking)
    results = ns.query(
        top_k=2,
        rank_by=(
            "Sum",
            [("blabla", "BM25", "walrus tusk"), ("blabla", "BM25", "jumping fox")],
        ),
        filters=("fact_id", "NotEq", "z"),
    )
    assert [item.id for item in results] == [2, 6]

    # Upsert with row-based upsert format
    ns.upsert(
        [
            tpuf.VectorRow(
                id=8,
                vector=[0.8, 0.8],
                attributes={
                    "blabla": "row based upsert format is cool",
                    "fact_id": "h",
                },
            ),
        ],
        schema=schema,
    )

    # Upsert with the dict format
    ns.upsert(
        [
            {
                "id": 9,
                "vector": [0.9, 0.9],
                "attributes": {
                    "blabla": "dict format of row based upsert also works, but isn't typed as well",
                    "fact_id": "i",
                },
            },
        ],
        schema=schema,
    )

    # Query to make sure the new row(s) is there
    results = ns.query(
        {
            "top_k": 10,
            "rank_by": ["blabla", "BM25", "row based upsert"],
        }
    )
    assert [item.id for item in results] == [8, 9]


def test_bm25_product_operator():
    ns = tpuf.Namespace(tests.test_prefix + "bm25_product_operator")

    try:
        ns.delete_all()
    except tpuf.NotFoundError:
        pass

    schema = {
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
    ns.upsert(
        [
            tpuf.VectorRow(
                id=1,
                vector=[0.1, 0.1],
                attributes={
                    "title": "the quick brown fox",
                    "content": "jumped over the lazy dog",
                },
            ),
            tpuf.VectorRow(
                id=2,
                vector=[0.2, 0.2],
                attributes={
                    "title": "the lazy dog",
                    "content": "is brown",
                },
            ),
        ],
        schema=schema,
    )

    # Try out a bunch of query variations
    queries: list[tpuf.RankInput] = [
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
            [
                0.5,
                (
                    "Sum",
                    [
                        ("Product", (0.5, ("title", "BM25", "quick brown"))),
                        ("content", "BM25", "brown"),
                    ],
                ),
            ],
        ),
    ]

    for query in queries:
        results = ns.query(
            rank_by=query,
            top_k=10,
        )
        assert len(results) > 0
