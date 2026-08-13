from pathlib import Path

from .audit_paid_response_path_core_rotation import run


ROOT = Path(__file__).resolve().parents[2]


def test_path_core_rotation_replays_frozen_audit() -> None:
    result = run(ROOT)
    assert result["status"] == "CORE_SUPPORTED_REDUCED_TO_ONE_ENDPOINT_EXCHANGE"
    assert result["outcome_counts"] == {
        "internally_supplied_segment_cycle": 3,
        "rank_four": 2,
        "endpoint_hole_core_exchange": 1,
    }
    assert result["unique_survivor"]["target_position"] == 1
    assert result["unique_survivor"]["source_position"] == 3


def test_both_referee_witnesses_escape_by_rotation() -> None:
    result = run(ROOT)
    assert all(
        replay["efx"] for replay in result["frozen_witness_replays"].values()
    )
