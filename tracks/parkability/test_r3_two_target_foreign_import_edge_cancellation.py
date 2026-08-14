from pathlib import Path

from .audit_r3_two_target_foreign_import_edge_cancellation import run


def test_r3_two_target_foreign_import_edge_cancellation():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACT_FIVE_INDICATOR_EDGE_CRITERION"
    assert result["signature_count"] == 208
    assert result["four_edge_feasible"] == 69
    assert result["four_edge_feasible_with_foreign_support"] == 53
    assert result["foreign_margin_capture"]
