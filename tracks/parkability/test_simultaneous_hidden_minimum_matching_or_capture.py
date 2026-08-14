from pathlib import Path

from .audit_simultaneous_hidden_minimum_matching_or_capture import run


def test_simultaneous_hidden_minimum_matching_or_capture():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "FOUR_OWNER_HALL_LIFT_TRICHOTOMY_EXHAUSTED"
    assert result["graph_count"] == (
        result["matching_count"] + result["deficient_count"]
    )
    assert result["maximum_unsafe_slot_count"] == 4
    assert all(result["checks"].values())
