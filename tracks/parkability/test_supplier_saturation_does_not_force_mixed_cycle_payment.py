from pathlib import Path

from .audit_supplier_saturation_does_not_force_mixed_cycle_payment import run


ROOT = Path(__file__).resolve().parents[2]


def test_exact_anchored_mixed_cycle_refutes_residual_payment() -> None:
    result = run(ROOT)
    assert result["status"] == "GENERIC_SUPPLIER_SATURATED_PAYMENT_IMPLICATION_REFUTED"
    assert result["supplier_closure"] == ["r", "q", "a", "b"]
    assert result["permanent_anchor_retained"] is True
    assert result["blocked_observer_threshold"] == "12"
    assert result["blocked_observer_full_residual_value"] == "57/5"
    assert result["residual_assignment_count"] == 625
    assert result["residual_only_efx_payment_count"] == 0


def test_failure_localizes_at_decorated_head() -> None:
    result = run(ROOT)
    assert result["row_cancellation_forces_incoming_over_outgoing"] is True
    assert "decorated-head exchange" in result["smallest_missing_operation"]
