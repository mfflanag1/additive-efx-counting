from pathlib import Path

from .audit_retired_packet_selector_collision_normalization import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_selector_collision_normalization_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "COLLISION_NORMALIZED_TO_LEDGER_FREE_PROGRESS_ROOT_OR_TL_STAR"
    assert result["capture_inequality"]
    assert result["capture_packet_positive"]
    assert result["weak_floor_equality_critical"]
    assert result["minimality_protected_floor_safety_step"]
    assert result["current_safety_requires_current_floor"]
    assert result["exact_repeat_route_count"] == 1
    assert result["history_only_progress_forbidden"]
    assert result["equality_without_typed_handoff_routes_to_TL_star"]
    assert result["ledger_free_exact_response_repeat_routes_to_TL_star"]
    assert result["specialized_handoff_requires_exact_premises"]
    assert result["no_silent_reuse"]
