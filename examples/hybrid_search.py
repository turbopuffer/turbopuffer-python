import turbopuffer as tpuf


# Converts a search result set to a dict of ID -> rank
def results_to_ranks(results):
    return {item.id: rank for rank, item in enumerate(results, start=1)}

# Fuses two search result sets together into one
# Uses reciprocal rank fusion
def rank_fusion(bm25_results, vector_results, k=60):
    # Compute the ranks of all docs
    bm25_ranks = results_to_ranks(bm25_results)
    vector_ranks = results_to_ranks(vector_results)

    print("bm25_ranks:", bm25_ranks)
    print("vector ranks", vector_ranks)

    # Get all the unique document IDs
    doc_ids = set(bm25_ranks.keys()).union(set(vector_ranks.keys()))

    # Calculate the RRF score for each document
    scores = {}
    for doc_id in doc_ids:
        score = 0.0
        if doc_id in bm25_ranks:
            score += 1.0 / (k + bm25_ranks[doc_id])
        if doc_id in vector_ranks:
            score += 1.0 / (k + vector_ranks[doc_id])
        scores[doc_id] = score

    # Fuse the results together and return
    fused_results = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [{"id": doc_id, "score": score} for doc_id, score in fused_results]


def main():
    ns = tpuf.Namespace("tpuf_python_hybrid_search")
    try:
        ns.delete_all()  # For cleaning up from previous runs
    except tpuf.NotFoundError:
        pass

    # Upsert 10 documents, containing both vectors and text
    # Whale facts from: https://www.natgeokids.com/uk/discover/animals/sea-life/10-blue-whale-facts/
    ns.upsert(
        {
            "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "vectors": [
                [0.1, 0.1],
                [0.2, 0.2],
                [0.3, 0.3],
                [0.4, 0.4],
                [0.5, 0.5],
                [0.6, 0.6],
                [0.7, 0.7],
                [0.8, 0.8],
                [0.9, 0.9],
                [1.0, 1.0],
            ],
            "attributes": {
                "text": [
                    "blue whales can grow to over 30m long",
                    "pretty much everything about the blue whale is massive",
                    "blue whales can be found in all oceans, except for the arctic",
                    "blue whales eat tiny shrimp-like crustaceans called krill",
                    "to communicate with each other, blue whales make a series of super loud vocal sounds",
                    "blah",
                    "blah",
                    "blah",
                    "blah",
                    "blah",
                ]
            },
            "schema": {
                "text": {
                    "type": "?string",
                    "bm25": {
                        "language": "english",
                        "stemming": True,
                        "case_sensitive": False,
                        "remove_stopwords": True,
                    },
                },
            },
            "distance_metric": "euclidean_squared",
        }
    )
    print("upsert documents successfully")
    print("")

    # First, do query w/ BM25 full-text search
    bm25_results = ns.query({"top_k": 10, "rank_by": ("text", "BM25", "blue whale")})
    print(
        "search results for 'blue whale':",
        [(item.id, item.dist) for item in bm25_results],
    )
    print("")

    # Now, we also do a query with a vector
    vector_results = ns.query(
        top_k=10, vector=[1.0, 1.0], distance_metric="euclidean_squared"
    )
    print(
        "search results for [1.0, 1.0]:",
        [(item.id, item.dist) for item in vector_results],
    )
    print("")

    # Fuse the results with Reciprocal rank fusion (RRF)
    fused_results = rank_fusion(bm25_results, vector_results)
    print("")
    print("fused results:", fused_results)


if __name__ == "__main__":
    main()
