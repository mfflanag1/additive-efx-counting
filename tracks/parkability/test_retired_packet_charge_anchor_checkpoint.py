from pathlib import Path

from .audit_retired_packet_charge_anchor_checkpoint import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_charge_anchor_checkpoint_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "T_L_TIMES_NARROWED_TO_HOLDER_PRICE_OR_SAFE_PAYMENT_SEPARATOR"
    )
    assert result["all_unsafe_normalization_fan_closed"]
    assert result["remaining_separator_families"] == [
        "holder_price_separator",
        "safe_payment_normalization_wall",
    ]
    assert not result["full_T_L_times_theorem_closed"]
    assert not result["full_T_L_times_theorem_refuted"]

