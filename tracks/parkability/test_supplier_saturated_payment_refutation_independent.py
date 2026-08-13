from pathlib import Path

from .audit_supplier_saturated_payment_refutation_independent import run


ROOT = Path(__file__).resolve().parents[2]


def test_independent_supplier_saturated_refutation_replay() -> None:
    result = run(ROOT)
    assert result["status"] == "INDEPENDENT_EXACT_REPLAY_PASSED"
    assert all(result["checks"].values())
    assert result["residual_assignment_count"] == 625
    assert result["residual_only_efx_payment_count"] == 0
    assert "does not import" in result["implementation_relation"]
