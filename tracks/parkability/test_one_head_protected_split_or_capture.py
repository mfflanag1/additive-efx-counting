from pathlib import Path

from .audit_one_head_protected_split_or_capture import run


ROOT = Path(__file__).resolve().parents[2]


def test_one_head_split_or_capture_algebra() -> None:
    result = run(ROOT)
    assert result["status"] == "EXACT_TWO_BUNDLE_SPLIT_OR_CAPTURE"
    assert all(result["symbolic_checks"].values())


def test_terminalized_countermodel_exercises_one_head_selector() -> None:
    result = run(ROOT)
    frozen = result["frozen_countermodel_replay"]
    assert len(frozen["raw_generic_blockers"]) > 1
    assert frozen["one_head_entry_premise"] is True
    assert frozen["blockers"] == ["a"]
    assert frozen["selector_record_count"] > 0
    assert frozen["paid_split_count"] >= frozen["efx_split_count"]
    assert frozen["complete_residual_return_fails"] is True
    assert frozen["complete_residual_source_value"] == "7/5"
    assert frozen["direct_source_floor_after_anchor_retaining_split"] == "7"
