from pathlib import Path

from .audit_anchor_trim_or_whole_target_response import run


ROOT = Path(__file__).resolve().parents[2]


def test_anchor_trim_or_whole_target_response_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "PROPER_RESPONSE_REDUCTION_VERIFIED_SUPERSEDED_BRANCHING"
    assert all(result["symbolic_checks"].values())
    assert result["support_record_count"] == 9
    assert result["proper_descent_count"] == 8
    assert result["whole_target_count"] == 1
    assert result["wall_derived_response_is_proper"]
