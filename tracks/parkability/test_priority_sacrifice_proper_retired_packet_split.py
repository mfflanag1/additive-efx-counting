from pathlib import Path

from .audit_priority_sacrifice_proper_retired_packet_split import run


ROOT = Path(__file__).resolve().parents[2]


def test_priority_sacrifice_proper_retired_packet_split() -> None:
    result = run(ROOT)
    assert result["status"] == "SACRIFICE_SPLIT_ROUTES_TO_PROGRESS_OR_PROTECTED_CUT"
    assert result["recipient_floor_identity"]
    assert result["strict_recipient_indivisibility_atom"]
    assert result["single_target_response_hits_only_proper_packet"]
    assert not result["holder_payment_required"]
    assert result["remaining_branches"] == [
        "recipient_indivisible_whole_packet",
        "root_or_protected_holder_birow_cut",
    ]
    assert not result["full_T_L_times_theorem_closed"]
