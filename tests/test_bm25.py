import uuid
import turbopuffer as tpuf
import tests


def test_bm25():
    ns = tpuf.Namespace(tests.test_prefix + 'bm25')

    schema = {
        "blabla": {
            "type": "?string",
            "bm25": {
                "language": "english",
                "stemming": True,
                "case_sensitive": False,
                "remove_stopwords": True,
            }
        }
    }

    # Upsert with dict
    ns.async_upsert({
        "ids": [1, 2, 3, 4],
        "vectors": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
        "attributes": {
            "blabla": [
                "the fox is quick and brown",
                "fox jumped over the lazy dog",
                "the dog is lazy and brown",
                "walrus is slow and inferior"
            ]
        }
    }, schema=schema)

    # Query with dict
    results = ns.query({
        "top_k": 10,
        "rank_by": ["blabla", "BM25", "fox jumping"]
    })
    print("results", results)
    assert [item.id for item in results] == [2, 1]

    # Upsert with positional args
    ns.async_upsert(
        [5, 6],
        [[0.5, 0.5], [0.6, 0.6]],
        {
            "blabla": [
                "Male Pacific walruses can be over 3.6m long and weigh over 1500kg",
                "Female walruses have tusks too"
            ]
        },
        schema
    )


test_bm25()
