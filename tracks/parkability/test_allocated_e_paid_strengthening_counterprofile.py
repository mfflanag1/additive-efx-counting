from fractions import Fraction

from .audit_allocated_e_paid_strengthening_counterprofile import (
    complete_efx,
    desired_common_safe,
)


def test_exact_response_and_efx_primitives():
    owners = ("r", "q", "d", "s")
    values = {owner: {"x": Fraction(3, 5), "y": Fraction(3, 5)} for owner in owners}
    assert desired_common_safe(values, "r", ("x", "y"))
    allocation = {
        "r": ["x"], "q": ["y"], "d": [], "s": [], "charity": [],
    }
    assert complete_efx(values, allocation)
