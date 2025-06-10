# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..lib.performance import ClientPerformance

__all__ = ["QueryPerformance"]


class QueryPerformance(ClientPerformance):
    approx_namespace_size: int
    """the approximate number of documents in the namespace."""

    cache_hit_ratio: float
    """The ratio of cache hits to total cache lookups."""

    cache_temperature: str
    """A qualitative description of the cache hit ratio (`hot`, `warm`, or `cold`)."""

    exhaustive_search_count: int
    """The number of unindexed documents processed by the query."""

    query_execution_ms: int
    """
    Request time measured on the server, excluding time spent waiting due to the
    namespace concurrency limit.
    """

    server_total_ms: int
    """
    Request time measured on the server, including time spent waiting for other
    queries to complete if the namespace was at its concurrency limit.
    """
