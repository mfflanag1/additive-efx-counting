from pathlib import Path

from .audit_nonroot_singleton_retired_packet_isolation_descent import run


ROOT = Path(__file__).resolve().parents[2]


def test_nonroot_singleton_retired_packet_isolation_descent() -> None:
    result = run(ROOT)
    assert result["status"] == "SINGLETON_ISOLATION_WALLS_VERIFIED_ADMISSION_OPEN"
    assert result["singleton_deletion_threshold"] == 0
    assert result["singleton_target_walls"] == []
    assert not result["test_allocation_responses_intersect_singleton"]
    assert not result["collision_hitting_multiplicity_strictly_reduced"]
    assert not result["admissible_transition_proved"]
    assert result["remaining_direct_branch"] == "singleton_isolation_transition_admission"
    assert not result["full_T_L_times_theorem_closed"]
