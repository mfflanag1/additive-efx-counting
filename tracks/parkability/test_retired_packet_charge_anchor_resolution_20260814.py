from .audit_retired_packet_charge_anchor_resolution_20260814 import run


def test_retired_packet_charge_anchor_resolution_20260814() -> None:
    result = run()
    assert result["status"] == (
        "T_L_TIMES_COLLISION_CLOSED_BY_CONTROLLED_FLOOR_RESET"
    )
    assert result["holder_partition_exhaustive"]
    assert result["nonroot_whole_hit_closed"]
    assert result["root_whole_hit_closed"]
    assert result["root_scalar_contradiction_conditional"]
    assert result["root_supplier_star_floor_admission_proved"]
    assert result["strict_first_priority_floor_reset_admitted"]
    assert not result["old_later_floors_preserved"]
    assert not result["floor_reset_counts_as_progress"]
    assert result["root_packet_localized_to_old_anchor_critical_atoms"]
    assert result["root_off_anchor_atom_returns_closed"]
    assert result["root_noncritical_anchor_atom_returns_closed"]
    assert result["root_critical_anchor_packet_closed"]
    assert result["strict_capture_covered"]
    assert result["equality_critical_covered"]
    assert result["base_floor_source_inactive_covered"]
    assert result["release_compatibility_covered"]
    assert result["named_retired_packet_used"]
    assert result["retirement_supplier_used"]
    assert result["current_holder_used"]
    assert result["protected_floor_capture_used"]
    assert result["repeated_hitting_or_normalization_bypass_covered"]
    assert all(result["conditional_outcome_coverage"].values())
    assert result["root_interface_composition"]["supplier_star_floor_admission_proved"]
    assert all(result["root_interface_composition"].values())
    assert result["full_T_L_times_theorem_closed"]
    assert not result["parked_T_L_perp_closed"]
    assert not result["empty_ledger_T0_closed"]
    assert not result["GG_closed"]
    assert not result["four_agent_EFX_closed"]
