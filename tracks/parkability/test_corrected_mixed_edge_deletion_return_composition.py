from pathlib import Path

from .audit_corrected_mixed_edge_deletion_return_composition import run


ROOT = Path(__file__).resolve().parents[2]


def test_corrected_composition_classifies_all_kappa1_cases() -> None:
    result = run(ROOT)
    assert result["status"] == "KAPPA1_REDUCED_TO_CROSS_DECORATED_EXCHANGE"
    assert result["case_count"] == 288
    assert result["case_counts"] == {
        "mixed_source_is_hole": 72,
        "two_special_cores": 216,
    }
    assert all(result["symbolic_checks"].values())


def test_cross_decorated_exchange_is_not_forced_locally() -> None:
    result = run(ROOT)
    witness = result["local_cross_decorated_separator"]
    assert witness["exchange_family_size"] == 8
    assert witness["feasible_exchange_count"] == 0
    assert witness["complete_pool_feasible_count"] == 89
    assert result["independent_open_branch"] == "kappa in {2,3} multi-decorated matching"
