from pathlib import Path

from .audit_permanent_anchor_root_target_bilateral_compensator_frontier import run


def test_permanent_anchor_root_target_bilateral_compensator_frontier():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACT_FOUR_EDGE_BILATERAL_FRONTIER_OR_TWO_ROW_SEPARATOR"
    assert result["case_count"] == 30
    assert result["four_edge_case_count"] == 28
    assert result["overflow_case_count"] == 2
    assert result["maximum_feasible_edge_count"] == 4
    assert result["root_payment_equivalence"]
    assert result["source_strict_equivalence"]
    assert result["maximizer_propagation"]
    assert result["empty_compensator_packet_wall"]
    assert result["full_swap_source_strict"]
    assert result["full_swap_direct_safety_equivalence"]
    assert result["local_separator_witness"]["response_desired"]
    assert result["local_separator_witness"]["successful_admissible_pairs"] == 0
