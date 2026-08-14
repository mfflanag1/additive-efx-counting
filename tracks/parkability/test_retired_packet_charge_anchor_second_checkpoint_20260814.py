from .audit_retired_packet_charge_anchor_second_checkpoint_20260814 import run


def test_retired_packet_charge_anchor_second_checkpoint_20260814() -> None:
    result = run()
    assert result["status"] == (
        "SUPERSEDED_CONDITIONAL_GGS_FRONTIER_COLLISION_NOW_CLOSED"
    )
    assert result["nonroot_safe_whole_hit_closed"]
    assert not result["proper_donor_free_equality_closed"]
    assert result["root_packet_price_equality_closed"]
    assert not result["historical_supplier_return_admitted"]
    assert result["strict_clean_subpacket_release_admitted"]
    assert result["strict_atomwise_pool_dominance_unconditional"]
    assert result["signed_missing_base_support_fork_proved"]
    assert result["base_contained_exterior_sacrifice_admitted"]
    assert result["exterior_dominance_source_topology_reduced"]
    assert result["one_good_root_normal_form_proved"]
    assert result["global_exterior_supplier_star_admitted"]
    assert result["global_exterior_independent_integer_replay_passed"]
    assert result["base_containment_unconditional"]
    assert not result["signed_missing_base_return_required"]
    assert not result["multilabel_charge_branch_required"]
    assert result["unique_source_face_closed"]
    assert result["double_edge_two_source_face_closed"]
    assert result["cyclic_cross_completion_debt_proved"]
    assert not result["debt_cycle_release_compatible_pi_proved"]
    assert result["singleton_source_pair_closed"]
    assert result["forced_nonroot_GGS_cycle_proved"]
    assert result["off_good_profiles_remaining"] == 3
    assert not result["on_good_profiles_closed"]
    assert result["old_root_core_exterior_contradiction_proved"]
    assert result["full_T_L_times_theorem_closed"]
    assert not result["full_T_L_times_theorem_refuted"]
