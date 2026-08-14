from pathlib import Path

from .audit_strict_root_incoming_cell_diversion_or_capture import run


def test_strict_root_incoming_cell_diversion_or_capture():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "NONINCREASING_EDGE_PROBE_OR_CELL_CAPTURE"
    assert result["checked_graph_count"] > 1000
    assert result["maximum_before_edges"] == 4
    assert result["maximum_after_edges"] == 4
    assert result["edge_count_never_increases"]
    assert result["root_payment_equivalence"]
    assert result["recipient_strict"]
