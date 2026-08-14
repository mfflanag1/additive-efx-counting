from pathlib import Path

from .audit_complete_holder_price_pool_reversal_or_underpayment import run


ROOT = Path(__file__).resolve().parents[2]


def test_complete_holder_price_pool_reversal_or_underpayment_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "HOLDER_GATE_REDUCED_TO_PAYMENT_RESPONSE_OR_AGGREGATE_UNDERPAYMENT"
    )
    assert result["complete_pool_underpayment_blocks_every_subpacket"]
    assert result["price_crossing_selector_nonempty"]
    assert result["safe_crossing_packet_pays_holder"]
    assert result["unsafe_reversal_below_holder_price"]
    assert result["remaining_separator"] == (
        "max_{R in compatible modes} v_h(R) < p_h"
    )
    assert not result["full_T_L_times_theorem_closed"]
