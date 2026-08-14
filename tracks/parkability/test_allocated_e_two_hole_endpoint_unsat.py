import z3

from .audit_allocated_e_two_hole_endpoint_unsat import (
    at_most_two_payment_holes,
    direct_atomic_efx,
)
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def test_direct_endpoint_formula_requires_efx_and_two_paid_owners():
    value = {(good, owner): z3.Real(f"twohole_{good}_{owner}")
             for good in GOODS for owner in OWNERS}
    allocation = {
        "r": ["a0", "a1"],
        "q": ["j", "k", "q0"],
        "d": ["h", "m", "gq", "gr", "p"],
        "s": ["l", "e"],
        "charity": [],
    }
    solver = z3.Solver()
    for owner in OWNERS:
        solver.add(z3.Sum(*(value[good, owner]
                           for good in ALLOCATED_E_BASE[owner])) == 1)
    solver.add(at_most_two_payment_holes(value, allocation))
    paid = []
    for owner in OWNERS:
        paid.append(z3.Sum(*(value[good, owner] for good in allocation[owner])) >= 1)
    solver.add(z3.Sum(*(z3.If(predicate, 1, 0) for predicate in paid)) <= 1)
    assert solver.check() == z3.unsat

    # The direct EFX formula includes every literal deletion comparison.
    solver = z3.Solver()
    solver.add(direct_atomic_efx(value, allocation))
    observer = "r"
    target = "q"
    own = z3.Sum(*(value[good, observer] for good in allocation[observer]))
    target_total = z3.Sum(*(value[good, observer] for good in allocation[target]))
    solver.add(own < target_total - value["j", observer])
    assert solver.check() == z3.unsat
