from pathlib import Path

from .audit_form2_all_target_change_exact_repeat_rank_no_go import run


def test_form2_all_target_change_exact_repeat_rank_no_go():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACT_REPEAT_DOES_NOT_FORCE_RANK_FOUR"
    assert result["support_edge_count"] == 4
    assert result["all_five_targets_changed"]
    assert result["maximum_response_matching_rank"] == 3
