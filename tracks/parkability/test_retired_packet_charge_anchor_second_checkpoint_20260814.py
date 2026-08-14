from .audit_retired_packet_charge_anchor_second_checkpoint_20260814 import run


def test_retired_packet_charge_anchor_second_checkpoint_20260814() -> None:
    result = run()
    assert result["status"] == (
        "NONROOT_EQUALITY_CLOSED_ROOT_BASE_CONTAINED_OR_CHARGED"
    )
    assert result["nonroot_safe_whole_hit_closed"]
    assert not result["proper_donor_free_equality_closed"]
    assert result["root_packet_price_equality_closed"]
    assert not result["historical_supplier_return_admitted"]
    assert result["strict_clean_subpacket_release_admitted"]
    assert result["strict_atomwise_pool_dominance_unconditional"]
    assert result["signed_missing_base_support_fork_proved"]
    assert not result["full_T_L_times_theorem_closed"]
    assert not result["full_T_L_times_theorem_refuted"]
