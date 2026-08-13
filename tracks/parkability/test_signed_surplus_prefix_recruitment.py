from pathlib import Path

from .audit_signed_surplus_prefix_recruitment import run


ROOT = Path(__file__).resolve().parents[2]


def test_prefix_recruitment_is_finite_and_disjoint() -> None:
    result = run(ROOT)
    assert result["status"] == "RECRUITMENT_WELL_FOUNDED_POOL_SEPARATOR_SUPERSEDED"
    assert result["case_count"] == 1344
    assert result["maximum_strict_prefix_extensions"] == 3
    assert all(result["symbolic_checks"].values())
    assert all(record["physical_disjointness"] for record in result["records"])
    assert all(record["anchor_target_support_preserved"] for record in result["records"])


def test_archived_pool_countermodel_misses_terminal_premises() -> None:
    result = run(ROOT)
    witness = result["superseded_local_separator"]
    assert witness["census_family_size"] == 262144
    assert witness["census_feasible_count"] == 0
    assert witness["old_observer_utility"] == "11"
    assert witness["old_observer_decorated_threshold"] == "12"
    assert witness["old_observer_prepaid"] is False
    assert witness["hole_owner_utility_on_P"] == "12"
    assert witness["hole_owner_decorated_threshold"] == "8"
    assert witness["hole_row_separator"] is False


def test_response_order_classification() -> None:
    result = run(ROOT)
    assert result["response_pair_counts_by_prefix"] == {
        "0": {"backward": 3, "forward": 0},
        "1": {"backward": 5, "forward": 1},
        "2": {"backward": 6, "forward": 3},
        "3": {"backward": 6, "forward": 6},
    }
