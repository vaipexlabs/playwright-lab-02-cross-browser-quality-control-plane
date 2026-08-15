import pytest

from vaipex_cross_browser.sharding import select_shard


def test_two_shards_are_balanced_and_complete() -> None:
    node_ids = [f"test_{index}" for index in range(7)]

    first = select_shard(node_ids, shard_index=1, shard_total=2)
    second = select_shard(node_ids, shard_index=2, shard_total=2)

    assert len(first) == 4
    assert len(second) == 3
    assert set(first).isdisjoint(second)
    assert set(first) | set(second) == set(node_ids)


def test_sharding_is_stable_when_collection_order_changes() -> None:
    node_ids = ["zeta", "alpha", "gamma", "beta"]

    assert select_shard(node_ids, 1, 2) == select_shard(reversed(node_ids), 1, 2)


@pytest.mark.parametrize(
    ("index", "total"),
    [(0, 2), (3, 2), (1, 0)],
)
def test_invalid_shard_contract_is_rejected(index: int, total: int) -> None:
    with pytest.raises(ValueError):
        select_shard(["test"], index, total)
