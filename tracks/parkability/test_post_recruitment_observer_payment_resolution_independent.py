from fractions import Fraction
from pathlib import Path

from .audit_post_recruitment_observer_payment_resolution_independent import run


ROOT = Path(__file__).resolve().parents[2]


def test_post_recruitment_payment_objective_is_exactly_refuted() -> None:
    result = run(ROOT)
    assert result["status"] == "POST_RECRUITMENT_PAYMENT_OBJECTIVE_EXACTLY_REFUTED"
    generic = result["generic_payment_refutation"]
    assert generic["residual_assignment_count"] == 625
    assert generic["efx_all_paid_count"] == 0
    assert generic["supplier_closure"] == ["r", "q", "a", "b"]
    assert generic["permanent_anchor_retained"]


def test_anchor_case_is_independently_refuted_and_handoff_is_feasible() -> None:
    result = run(ROOT)
    anchor = result["anchor_case_refutation"]
    assert anchor["a_after_Rq"] == "5"
    assert anchor["a_after_complete_pool"] == "11"
    assert anchor["anchor_response_disjoint"]
    assert anchor["sacrifice_handoff_partitions_pool"]
    assert Fraction(anchor["root_anchor_response_value"]) > Fraction(anchor["root_base"])
