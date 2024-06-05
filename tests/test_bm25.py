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
    ns.upsert({
        "ids": [1, 2, 3, 4],
        "vectors": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4]],
        "attributes": {
            "blabla": [
                "the fox is quick and brown",
                "fox jumped over the lazy dog",
                "the dog is lazy and brown",
                "walrus is slow and inferior"
            ]
        },
        "schema": schema
    })

    # Query with dict
    results = ns.query({
        "top_k": 10,
        "rank_by": ["blabla", "BM25", "fox jumping"]
    })
    assert [item.id for item in results] == [2, 1]

    # Upsert with positional args
    ns.upsert(
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

    # Upsert with named args
    ns.upsert(
        ids=[7],
        vectors=[[0.7,0.7]],
        attributes={ "blabla": [ "walruses can live up to 40 years" ] },
        schema=schema
    )

    # Query with named args (and combined ranking)
    results = ns.query(
        top_k=2,
        rank_by=["Sum", [["blabla", "BM25", "walrus tusk"], ["blabla", "BM25", "jumping fox"]]]
    )
    assert [item.id for item in results] == [2, 6]
