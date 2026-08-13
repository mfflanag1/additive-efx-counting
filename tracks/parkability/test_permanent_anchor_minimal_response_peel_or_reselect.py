from pathlib import Path

from .audit_permanent_anchor_minimal_response_peel_or_reselect import run
from .audit_permanent_anchor_minimal_response_peel_or_reselect_independent import run as run_independent


ROOT = Path(__file__).resolve().parents[2]


def test_permanent_anchor_minimal_response_peel_or_reselect_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "PERMANENT_ANCHOR_RECURRENCE_RESOLVED_BY_OUTCOMES_3_OR_4"
    assert result["branch_exhaustion"]
    assert result["high_response_reselection_above_base"]
    assert result["low_response_peel_keeps_root_above_pre_floor"]
    assert result["root_pays_safe_peeled_target_after_utility_drop"]
    assert result["proper_response_gives_strict_support_partition"]
    assert result["physical_peel_partition_valid"]
    assert result["retired_support_strictly_grows"]


def test_permanent_anchor_minimal_response_peel_or_reselect_independent() -> None:
    result = run_independent(ROOT)
    assert result["status"] == "INDEPENDENT_EXACT_PEEL_OR_RESELECT_REPLAY_PASSED"
    assert result["high_reselection_integer_cases"] > 0
    assert result["low_paid_peel_integer_cases"] > 0
    assert result["proper_support_cases"] == 14
    assert result["mixed_support_cases"] == 8
    assert result["anchor_only_support_cases"] == 3
