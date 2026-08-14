from pathlib import Path

from .audit_r3_singleton_retained_incoming_cell_return import run


def test_r3_singleton_retained_incoming_cell_return():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "ALL_SUPPORT_SIGNATURES_HAVE_RETURN_OR_ROOT_CAPTURE"
    assert result["presence_pattern_count"] == 8
    assert result["all_patterns_have_candidate"]
    assert result["all_candidates_at_most_four_edges"]
    assert result["root_payment_equivalence"]
    assert result["singleton_owner_strict"]
