# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ShardingConfig"]


class ShardingConfig(BaseModel):
    """
    Configuration for namespace sharding, which partitions a namespace's documents across multiple internal shards to scale indexing and query throughput beyond a single machine.
    Sharding can only be configured on a namespace's inaugural write, and cannot be added to or changed on an existing namespace.
    """

    num_shards: int
    """The number of shards to partition the namespace into."""
