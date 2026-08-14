from pathlib import Path

from .audit_whole_retired_packet_atomwise_criticality import run


ROOT = Path(__file__).resolve().parents[2]


def test_whole_retired_packet_atomwise_criticality_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "PROPER_PACKET_REDUCTION_OR_ATOMWISE_CRITICAL_SURVIVOR"
    )
    assert result["deletion_identity"]
    assert result["proper_candidate_below_margin"]
    assert result["capture_identity"]
    assert result["nonsingleton_implies_margin_at_most_deficit"]
    assert result["margin_above_deficit_forces_singleton"]
    assert result["general_charge"] == "(|K|-1)*mu <= d"
    assert not result["full_T_L_times_theorem_closed"]

