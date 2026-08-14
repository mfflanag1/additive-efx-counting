from pathlib import Path

from .audit_r3_singleton_source_root_compensated_direct_return import run


def test_r3_singleton_source_root_compensated_direct_return():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "DIRECT_RETURN_OR_ROOT_MARGIN_CHARITY_CAPTURE"
    assert result["signature_count"] == 26
    assert result["direct_four_edge_feasible"] == 10
    assert result["five_cell_union_feasible"] == 102
    assert result["root_payment_equivalence"]
