from pathlib import Path

from .audit_two_creditor_retired_packet_split_or_hall_cut import run


ROOT = Path(__file__).resolve().parents[2]


def test_two_creditor_retired_packet_split_or_hall_cut() -> None:
    result = run(ROOT)
    assert result["status"] == "TWO_SIDED_PAYMENT_REDUCED_TO_EXACT_HALL_CUT"
    assert result["recipient_margin_identity"]
    assert result["recipient_floor_identity"]
    assert result["holder_margin_identity"]
    assert result["holder_floor_identity"]
    assert result["single_target_response_hits_only_proper_split"]
    assert result["scalar_models_verified"]
    assert len(result["scalar_joint_incompatibility_models"]) == 2
    assert result["terminal_branches"] == [
        "recipient_deficiency",
        "holder_deficiency",
        "joint_incompatibility",
    ]
    assert not result["full_T_L_times_theorem_closed"]
