from pathlib import Path

from .audit_r3_later_source_root_preserving_star import run


def test_later_source_star_is_four_edge_or_captures_root_margin():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "FOUR_EDGE_OR_FULL_ROOT_MARGIN_CAPTURE"
    assert result["edge_records_checked"] == 20
    assert all(row["total_edge_count"] <= 4 for row in result["edge_records"])
