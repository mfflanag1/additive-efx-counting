#!/usr/bin/env python3

from pathlib import Path

from .audit_one_edge_charity_substitution_boundary import run


def test_exact_substitution_boundary():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == (
        "RESPONSE_CORE_SUBSTITUTION_REFUTED_GENERAL_FOUR_EDGE_SURVIVES"
    )
    checks = result["checks"]
    assert checks["corrected_nonself_owner_cycle_master_satisfied"]
    assert checks["one_edge_substitution_candidate_count"] == 12
    assert checks["one_edge_substitution_efx_count"] == 0
    assert checks["complete_efx_count_by_support_edges"] == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 20
    }
    assert checks["four_edge_topology_count"] == 11
