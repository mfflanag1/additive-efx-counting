from pathlib import Path

from .audit_general_mixed_edge_deletion_return_composition import run


ROOT = Path(__file__).resolve().parents[2]


def test_general_composition_covers_every_mixed_kappa() -> None:
    result = run(ROOT)
    assert result["status"] == "ALL_KAPPA_SCALAR_REDUCTION_POOL_WITNESS_NOT_TERMINAL"
    assert result["mixed_interface_case_count"] == 1008
    assert result["counts_by_kappa"] == {"1": 288, "2": 432, "3": 288}
    assert all(result["symbolic_checks"].values())


def test_general_composition_tracks_special_pool_sizes() -> None:
    result = run(ROOT)
    assert result["participant_count_distribution"] == {
        "2": 216,
        "3": 576,
        "4": 216,
    }
    assert result["smallest_terminal"] == "signed-surplus predecessor-prefix recruitment"
    separator = result["local_selected_pool_separator"]
    assert separator["family_size"] == 262144
    assert separator["feasible_count"] == 0
    assert result["post_residual_premise_checks"] == {
        "old_observer_prepaid": False,
        "hole_row_separator": False,
    }
