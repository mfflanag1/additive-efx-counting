from pathlib import Path

from .audit_r3_singleton_compensated_anchor_uncrossing import run


def test_singleton_compensated_anchor_uncrossing_frontier():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "FOUR_EDGE_UNCROSSING_OR_BICRITERIA_CRITICAL_PACKET"
    assert result["edge_records_checked"] == 80
    assert result["minimal_crossing_calibrations_checked"] > 0
    assert all(row["total_edge_count"] <= 4 for row in result["edge_records"])
