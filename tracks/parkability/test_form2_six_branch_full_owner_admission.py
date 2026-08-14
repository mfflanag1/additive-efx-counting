from pathlib import Path

from .audit_form2_six_branch_full_owner_admission import run


def test_form2_six_branch_full_owner_admission():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "SIX_FOUR_EDGE_SPANNING_TREES"
    assert result["branch_count"] == 6
    assert all(row["spanning_tree"] for row in result["branches"])
