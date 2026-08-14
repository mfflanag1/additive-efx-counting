from pathlib import Path

from .audit_retired_packet_charge_anchor_gate import run


ROOT = Path(__file__).resolve().parents[2]


def test_retired_packet_charge_anchor_gate_replays() -> None:
    result = run(ROOT)
    assert result["status"] == "RECIPIENT_CAPTURE_DOES_NOT_PAY_HOLDER_GATE_OPEN"
    assert result["capture_identity"]
    assert result["holder_payment_identity"]
    assert result["strict_capture_cross_row_countermodel"]["mu"] == "2"
    assert result["equality_critical_cross_row_countermodel"]["mu"] == "0"
    assert result["indivisible_whole_packet_deadlock"]["packet_atoms"] == 1
    assert result["indivisible_whole_packet_deadlock"]["recipient_requires_packet"]
    assert result["root_band_cross_row_countermodel"] == {
        "x": "10",
        "delta": "4",
        "root_target": "14",
        "response": "5",
        "complement": "9",
        "coexists_with_strict_recipient_capture": True,
    }
    assert result["base_floor_debt_countermodel"] == {
        "base": "10",
        "current": "13",
        "old_core": "11",
        "decorated_threshold": "12",
    }
    assert result["release_closure_countermodel"]["outside_suppliers"] == [3]
    assert not result["full_T_L_times_theorem_refuted"]
