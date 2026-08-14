from pathlib import Path

from .audit_permanent_anchor_two_source_root_response_topology_or_cross_capture import run


def test_permanent_anchor_two_source_root_response_topology_or_cross_capture():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "FOUR_EDGE_PAIR_OR_ROOT_OR_CROSS_CAPTURE"
    assert result["case_count"] == 96
    assert result["initial_four_edge_case_count"] == 76
    assert result["initial_overflow_case_count"] == 20
    assert result["irreducible_cross_case_count"] == 4
    assert result["root_payment_equivalence"]
    assert result["two_supplier_capture"]
