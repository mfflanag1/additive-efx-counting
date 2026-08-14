from pathlib import Path

from .audit_external_hall_finite_decision_nonvacuity import run


def test_external_hall_nonvacuity_audit():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "LEGACY_FULL_PI_MENU_DECISION_VACUOUS"
    assert all(
        not form["menu_theorem_nonvacuous_under_full_pi"]
        for form in result["forms"].values()
    )
