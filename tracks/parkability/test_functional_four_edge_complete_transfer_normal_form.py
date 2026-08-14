from .audit_functional_four_edge_complete_transfer_normal_form import run


def test_all_functional_four_edge_topologies_are_classified():
    result = run()
    assert result["status"] == "ALL_FUNCTIONAL_FOUR_EDGE_GRAPHS_CLASSIFIED"
    assert result["topology_count"] == 432
    assert result["class_counts"] == {
        "charity_connected_acyclic_branching": 232,
        "charity_fed_owner_cycle": 120,
        "charity_hamiltonian_path": 24,
        "disconnected_owner_cycle": 56,
    }


def test_hamiltonian_path_subfamily_has_expected_size():
    result = run()
    assert result["hamiltonian_path_count"] == 24
    assert all(
        len(record["weak_components"]) == 1 and not record["owner_cycles"]
        for record in result["records"]
        if record["class"] == "charity_hamiltonian_path"
    )
