from pathlib import Path

from .audit_retired_packet_birow_split_or_cut import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_birow_split_or_cut_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "PROPER_PACKET_REDUCTION_OR_EXACT_BIROW_CUT"
    assert result["recipient_floor_identity"]
    assert result["recipient_margin_identity"]
    assert result["holder_floor_identity"]
    assert result["full_packet_blocked_by_aggregate_underpayment"]
    assert result["recipient_critical_good_exceeds_strict_margin"]
    assert result["equality_capture_has_no_proper_recipient_feasible_packet"]
    assert result["single_target_response_cannot_reassemble_split_packet"]
    assert not result["full_T_L_times_theorem_closed"]
