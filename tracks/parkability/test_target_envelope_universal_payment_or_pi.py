from pathlib import Path

from .audit_target_envelope_universal_payment_or_pi import run


ROOT = Path(__file__).resolve().parents[2]


def test_target_envelope_universal_payment_or_pi_replays() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "ONE_TARGET_HAS_UNIVERSAL_EXTERNAL_PAYER_OR_SUPPLIED_PI"
    )
    assert result["selector_nonempty_from_current_safety"]
    assert result["safe_packet_pays_every_target_response"]
    assert result["unsafe_reversal_below_envelope"]
    assert result["all_unsafe_source_assignments_checked"] == 324
    assert result["all_unsafe_supplier_cycles"] == 324
    assert not result["full_T_L_times_theorem_closed"]

