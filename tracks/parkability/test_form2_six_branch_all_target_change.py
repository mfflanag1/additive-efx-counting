from pathlib import Path

from .audit_form2_six_branch_all_target_change import run


def test_form2_six_branch_all_target_change():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "ALL_SIX_BRANCHES_CHANGE_ALL_FIVE_TARGETS"
    assert result["branch_count"] == 6
    assert all(row["all_targets_changed"] for row in result["branches"])
