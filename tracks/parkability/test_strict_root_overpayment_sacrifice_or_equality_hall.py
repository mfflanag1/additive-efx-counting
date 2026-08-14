from pathlib import Path

from .audit_strict_root_overpayment_sacrifice_or_equality_hall import run


ROOT = Path(__file__).resolve().parents[2]


def test_strict_root_overpayment_sacrifice_or_equality_hall() -> None:
    result = run(ROOT)
    assert result["status"] == (
        "JOINT_HALL_REDUCED_TO_ROOT_DEFICIENCY_OR_EXACT_EQUALITY"
    )
    assert result["root_margin_identity"]
    assert result["strict_root_overpayment_equivalence"]
    assert result["exact_root_payment_equivalence"]
    assert result["remaining_root_branches"] == [
        "root_payment_family_empty",
        "all_surviving_root_payments_exact",
    ]
    assert not result["full_T_L_times_theorem_closed"]

