import z3

from .decide_allocated_e_seven_endpoint_paid_strengthening import (
    owner_paid_endpoint,
    payment_hole_bounded_endpoint,
)
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def test_owner_paid_endpoint_requires_efx_and_every_base_floor():
    value = {(good, owner): z3.Real(f"paid_{good}_{owner}")
             for good in GOODS for owner in OWNERS}
    allocation = {
        "r": ["a0", "a1"],
        "q": ["j", "k", "q0"],
        "d": ["h", "m", "gq", "gr", "p"],
        "s": ["l", "e"],
        "charity": [],
    }
    predicate = owner_paid_endpoint(value, allocation)
    solver = z3.Solver()
    for owner in OWNERS:
        for good in GOODS:
            solver.add(value[good, owner] > 0)
        solver.add(z3.Sum(*(value[good, owner]
                           for good in ALLOCATED_E_BASE[owner])) == 1)
    solver.add(predicate, z3.Sum(*(value[good, "r"] for good in allocation["r"])) < 1)
    assert solver.check() == z3.unsat


def test_single_hole_endpoint_excludes_two_underpaid_owners():
    value = {(good, owner): z3.Real(f"hole_{good}_{owner}")
             for good in GOODS for owner in OWNERS}
    allocation = {
        "r": ["a0", "a1"],
        "q": ["j", "k", "q0"],
        "d": ["h", "m", "gq", "gr", "p"],
        "s": ["l", "e"],
        "charity": [],
    }
    predicate = payment_hole_bounded_endpoint(value, allocation, 1)
    solver = z3.Solver()
    for owner in OWNERS:
        for good in GOODS:
            solver.add(value[good, owner] > 0)
        solver.add(z3.Sum(*(value[good, owner]
                           for good in ALLOCATED_E_BASE[owner])) == 1)
    solver.add(predicate)
    solver.add(z3.Sum(*(value[good, "r"] for good in allocation["r"])) < 1)
    solver.add(z3.Sum(*(value[good, "q"] for good in allocation["q"])) < 1)
    assert solver.check() == z3.unsat


def test_hole_bound_can_require_named_paid_owners():
    value = {(good, owner): z3.Real(f"named_{good}_{owner}")
             for good in GOODS for owner in OWNERS}
    allocation = {
        "r": ["a0", "a1"],
        "q": ["j", "k", "q0"],
        "d": ["h", "m", "gq", "gr", "p"],
        "s": ["l", "e"],
        "charity": [],
    }
    predicate = payment_hole_bounded_endpoint(
        value, allocation, 2, required_paid_owners=("q", "s"),
    )
    solver = z3.Solver()
    for owner in OWNERS:
        for good in GOODS:
            solver.add(value[good, owner] > 0)
        solver.add(z3.Sum(*(value[good, owner]
                           for good in ALLOCATED_E_BASE[owner])) == 1)
    solver.add(predicate)
    solver.add(z3.Sum(*(value[good, "q"] for good in allocation["q"])) < 1)
    assert solver.check() == z3.unsat
