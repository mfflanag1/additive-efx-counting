from pathlib import Path

from .audit_branch_tree_base_cancellation_closed_union import run


def test_branch_tree_base_cancellation_closed_union():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "CLOSED_UNION_EQUIVALENCE_EXHAUSTED"
    assert result["whole_return_shortcut_counterexample"][
        "whole_return_packet_count"
    ] == 0
