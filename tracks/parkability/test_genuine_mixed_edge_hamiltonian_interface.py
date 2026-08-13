from pathlib import Path

from .audit_genuine_mixed_edge_hamiltonian_interface import run


ROOT = Path(__file__).resolve().parents[2]


def test_genuine_interface_reconstructs_kappa_branches() -> None:
    result = run(ROOT)
    assert result["status"] == "INTERFACE_RECONSTRUCTED_WITH_KAPPA_BRANCH"
    assert result["mixed_survivor_kappa"] == [1, 2, 3]
    assert result["one_decorated_path_count"] == 96
    assert result["one_decorated_closing_pivot_count"] == 288
    assert result["abstract_kappa2_countermodel"][
        "minimum_decorated_edges_in_rank4_matching"
    ] == 2


def test_genuine_interface_support_and_anchor_counts() -> None:
    result = run(ROOT)
    assert result["all_mixed_and_closing_supports_disjoint"]
    assert result["all_own_core_residual_pairs_disjoint"]
    assert result["prefix_membership_counts"] == {
        "mixed_inside_prefix": 144,
        "mixed_outside_prefix": 144,
    }
    assert result["anchored_nonanchor_mixed_location_count"] == 18
