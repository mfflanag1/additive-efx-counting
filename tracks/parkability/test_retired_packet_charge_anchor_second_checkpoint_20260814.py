from .audit_retired_packet_charge_anchor_second_checkpoint_20260814 import run


def test_retired_packet_charge_anchor_second_checkpoint_20260814() -> None:
    result = run()
    assert result["status"] == (
        "ROOT_REDUCED_TO_ONE_GOOD_ON_OFF_SOURCE_DEBT_OR_CHARGE"
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
    assert not result["full_T_L_times_theorem_closed"]
    assert not result["full_T_L_times_theorem_refuted"]
