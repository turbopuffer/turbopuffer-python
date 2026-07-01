# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ShardingConfigParam"]


class ShardingConfigParam(TypedDict, total=False):
    """
    Configuration for namespace sharding, which partitions a namespace's documents across multiple internal shards to scale indexing and query throughput beyond a single machine.
    Sharding can only be configured on a namespace's inaugural write, and cannot be added to or changed on an existing namespace.
    """

    num_shards: Required[int]
    """The number of shards to partition the namespace into."""
