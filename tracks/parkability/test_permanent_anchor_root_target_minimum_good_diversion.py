from pathlib import Path

from .audit_permanent_anchor_root_target_minimum_good_diversion import run


def test_permanent_anchor_root_target_minimum_good_diversion():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "THREE_EDGE_PROBE_OR_ITEMWISE_ROOT_CAPTURE"
    assert result["case_count"] == 9
    assert result["maximum_edge_count"] == 3
    assert result["root_payment_equivalence"]
    assert result["itemwise_capture"]
    assert result["source_strict"]
