from pathlib import Path

from .audit_mixed_cycle_decorated_head_localization import run


ROOT = Path(__file__).resolve().parents[2]


def test_terminal_blockers_are_at_most_two_decorated_heads() -> None:
    result = run(ROOT)
    assert result["status"] == "TERMINAL_BLOCKERS_LOCALIZED_TO_AT_MOST_TWO_DECORATED_HEADS"
    assert result["mixed_cycle_pattern_count"] == 14
    assert result["head_count_distribution"] == {"1": 12, "2": 2}
    assert result["anchored_pattern_count"] == 7
    assert result["maximum_terminal_blockers"] == 2


def test_localization_cancellation_is_symbolic() -> None:
    result = run(ROOT)
    assert all(result["symbolic_checks"].values())
    assert result["unique_two_head_topology"] == "cyclically alternating D,O,D,O"
