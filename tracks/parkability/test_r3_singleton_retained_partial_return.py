from pathlib import Path

from .audit_r3_singleton_retained_partial_return import run


def test_r3_singleton_retained_partial_return():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "PARTIAL_RETURN_OR_ROOT_MARGIN_CAPTURE"
    assert result["response_signature_count"] == 26
    assert result["signatures_with_four_edge_partial_return"] == 21
    assert len(result["obstruction_signatures"]) == 5
    assert result["root_payment_equivalence"]
