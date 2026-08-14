from pathlib import Path

from .audit_r3_represented_star_double_absorption import run


def test_double_absorption_has_two_owner_edges_plus_charity():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACT_TWO_OWNER_EDGE_DOUBLE_ABSORPTION"
    assert result["records_checked"] == 24
    assert all(row["total_edge_count"] == 3 for row in result["records"])
