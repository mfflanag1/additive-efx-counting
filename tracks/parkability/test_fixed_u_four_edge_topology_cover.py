from pathlib import Path

from .analyze_fixed_u_four_edge_topology_cover import analyze


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/fixed_u_rank_three_root_facing_support_edge_cegar.json"


def test_observed_profiles_need_nonpath_topology_family():
    result = analyze(SOURCE, 6)
    assert result["source_round_count"] == 7
    assert result["minimum_cover_status"] == "sat"
    assert result["minimum_cover_size"] == 3
    assert result["functional_topology_cover_status"] == "sat"
    assert result["functional_topology_cover_size"] == 3
    assert all(
        row["feasible_functional_topology_count"] > 0
        for row in result["profiles"]
    )
    assert result["hamiltonian_path_cover_status"] == "unsat"
    assert result["profiles"][6]["feasible_charity_hamiltonian_path_count"] == 0


def test_sharp_profile_has_exact_topology_census():
    result = analyze(SOURCE, 6)
    sharp = next(row for row in result["profiles"] if row["iteration"] == 1)
    assert sharp["minimum_edge_count"] == 4
    assert sharp["complete_efx_allocation_count"] == 33
    assert sharp["feasible_topology_count"] == 16
