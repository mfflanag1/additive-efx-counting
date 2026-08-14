from pathlib import Path

from .audit_recipient_topup_retired_packet_split_or_cut import run


ROOT = Path(__file__).resolve().parents[2]


def test_recipient_topup_retired_packet_split_or_cut() -> None:
    result = run(ROOT)
    assert result["status"] == "RECIPIENT_INDIVISIBILITY_REDUCED_TO_TOPUP_CUT"
    assert result["topup_margin_identity"]
    assert result["topup_floor_identity"]
    assert result["whole_packet_replacement_threshold"]
    assert result["indivisible_retained_packet_has_positive_price"]
    assert result["topup_multiplicity_charge"]
    assert result["single_target_response_hits_only_proper_split"]
    assert not result["full_T_L_times_theorem_closed"]
