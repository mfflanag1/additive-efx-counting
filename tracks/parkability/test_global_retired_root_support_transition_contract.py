from pathlib import Path

from .audit_global_retired_root_support_transition_contract import run


ROOT = Path(__file__).resolve().parents[2]


def test_global_retired_root_support_transition_contract_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "CONTRACT_AND_G0_G10_COVERAGE_VERIFIED"
    assert result["g_states_covered"] == [f"G{i}" for i in range(11)]
    assert len(result["cross_cutting_operations"]) == 8
    assert result["physical_anchor_label_excludes_current_floor"]
    assert result["retired_support_persists_across_floor_changes"]
    assert result["no_collision_T_star_requires_complete_pool_audit"]
    assert all(result["scalar_checks"].values())
    assert result["collision_interface"] == "resolved_by_selector_collision_normalization"
