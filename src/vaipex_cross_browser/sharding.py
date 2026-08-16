from __future__ import annotations

from collections.abc import Iterable


def select_shard(
    node_ids: Iterable[str],
    shard_index: int,
    shard_total: int,
) -> tuple[str, ...]:
    """Select a stable, balanced, one-based shard from collected test IDs."""
    if shard_total < 1:
        raise ValueError("shard_total must be at least 1.")
    if shard_index < 1 or shard_index > shard_total:
        raise ValueError("shard_index must be between 1 and shard_total.")

    ordered_ids = sorted(node_ids)
    return tuple(
        node_id
        for ordinal, node_id in enumerate(ordered_ids)
        if ordinal % shard_total == shard_index - 1
    )
