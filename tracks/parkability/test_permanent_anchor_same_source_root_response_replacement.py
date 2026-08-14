from pathlib import Path

from .audit_permanent_anchor_same_source_root_response_replacement import run


def test_permanent_anchor_same_source_root_response_replacement():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "SAME_SOURCE_PROGRESS_OR_TYPED_ROOT_CAPTURE"
    assert result["case_count"] == 30
    assert result["overflow_case_count"] == 2
    assert result["maximum_repaired_edge_count"] == 4
    assert result["response_implies_admissible"]
    assert result["strict_same_source_progress"]
    assert result["root_payment_equivalence"]
