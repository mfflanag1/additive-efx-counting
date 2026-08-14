from pathlib import Path

from .audit_permanent_anchor_nonroot_three_placement_response_transfer import run


def test_permanent_anchor_nonroot_three_placement_response_transfer():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "DISJOINT_RESPONSE_GIVES_FOUR_EDGE_PROBE_OR_ROOT_CAPTURE"
    assert result["case_count"] == 33
    assert result["maximum_edge_count"] == 4
    assert result["root_payment_equivalence"]
    assert result["response_source_strict"]
