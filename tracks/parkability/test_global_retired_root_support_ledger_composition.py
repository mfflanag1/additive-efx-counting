from pathlib import Path

from .audit_global_retired_root_support_ledger_composition import run
from .audit_global_retired_root_support_ledger_composition_independent import run as run_independent


ROOT = Path(__file__).resolve().parents[2]


def test_global_retired_root_support_ledger_composition_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "T_L_TIMES_CLOSED_T0_AND_T_L_PERP_OPEN"
    )
    assert result["g_states_covered"] == [f"G{i}" for i in range(11)]
    assert len(result["cross_cutting_operations_covered"]) == 8
    assert all(result["physical_label_floor_separation"].values())
    assert len(result["finite_component_argument"]) == 6
    assert all(result["scalar_collision_checks"].values())
    assert all(result["collision_normalization_checks"].values())
    assert result["historical_typed_terminal"] == (
        "T^dagger = T_0^* dot-union T_L^*"
    )
    assert result["surviving_terminal"] == "T_0^* dot-union T_{L,perp}^*"
    assert result["pre_ledger_terminal"] == "T_0^*"
    assert result["post_ledger_terminal"] == "T_L^*"
    assert result["post_ledger_terminal_subtypes"] == [
        "T_{L,perp}^*", "T_{L,times}^*"
    ]
    assert result["closed_post_ledger_subtypes"] == ["T_{L,times}^*"]
    assert result["collision_T_L_times_closed"]
    assert result["collision_T_L_times_controlled_floor_reset_admitted"]
    assert result["collision_T_L_times_conditional_scalar_contradiction"]
    assert result["collision_T_L_times_root_packet_localized_to_critical_old_anchor"]
    assert not result["parked_T_L_perp_closed"]
    assert result["no_collision_terminal_guard"]
    assert result["augmented_generic_T_star_strictly_narrowed"]
    assert not result["generic_empty_ledger_T_star_closed"]
    assert not result["gg_closed"]


def test_global_retired_root_support_ledger_composition_independent() -> None:
    result = run_independent(ROOT)
    assert result["status"] == "INDEPENDENT_SIGNED_STATE_AND_NORMALIZATION_REPLAY_PASSED"
    assert result["allocations"] == 125
    assert result["signed_reconstruction_pairs"] == 15625
    assert result["normalization_cases"] == 125000
    assert result["retired_transfer_collision_cases"] > 0
    assert result["failed_floor_capture_cases"] > 0
    assert result["weak_floor_equality_critical_cases"] > 0
    assert result["nonempty_ledger_collision_free_proposal_cases"] > 0
    assert result["physical_conservation"]
    assert result["signed_reconstruction_injective"]
