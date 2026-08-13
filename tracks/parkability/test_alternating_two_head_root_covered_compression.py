from pathlib import Path

from .audit_alternating_two_head_root_covered_compression import run


ROOT = Path(__file__).resolve().parents[2]


def test_alternating_two_head_root_covered_compression_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "TWO_HEAD_HALL_REDUCED_TO_ROOT_COVERED_COMPRESSION"
    assert result["anchored_topology"]["root_is_head"]
    assert result["graph_census"]["deficient_relation_count"] == 860
    assert result["graph_census"]["all_deficient_graphs_have_root_covered_maximum_matching"]
    assert set(result["graph_census"]["rank_distribution"]) == {"2", "3"}


def test_rank_two_and_three_wall_localization() -> None:
    result = run(ROOT)
    assert all(result["rank_three_wall_check"].values())
    assert all(result["rank_two_wall_check"].values())

