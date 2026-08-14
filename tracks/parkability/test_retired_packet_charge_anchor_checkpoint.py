from pathlib import Path

from .audit_retired_packet_charge_anchor_checkpoint import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_charge_anchor_checkpoint_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "T_L_TIMES_NARROWED_TO_INDIVISIBLE_OR_ROOT_DOUBLE_ATOMIC_CUT"
    )
    assert result["all_unsafe_normalization_fan_closed"]
    assert result["birow_cut_scalar_realizable_inside_root_band"]
    assert result["remaining_separator_families"] == [
        "recipient_indivisible_whole_packet",
        "root_double_atomic_birow_cut",
    ]
    assert result["final_aggregate_separator"] == (
        "v_s(T)>=d implies v_h(T)>sigma+M_h(T) for every T subset K"
    )
    assert not result["full_T_L_times_theorem_closed"]
    assert not result["full_T_L_times_theorem_refuted"]
