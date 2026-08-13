from pathlib import Path

from .audit_residual_essential_path_core_topup import run


ROOT = Path(__file__).resolve().parents[2]


def test_residual_essential_response_reduction() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "ALL_RESPONSES_REDUCED_TO_TARGET_COMPENSATION_OR_CORE_ROTATION"
    )
    assert all(result["symbolic_checks"].values())
    assert result["order_outcomes_after_target_payment"] == {
        "endpoint_hole_core_exchange": 1,
        "internally_supplied_segment_cycle": 3,
        "rank_four": 2,
    }
