import z3

from .run_allocated_e_form0_role_split_pi_cegar import (
    OWNERS,
    PACKET,
    RESPONSE_CORE,
    add_anchor_charity_bypass_constraints,
    build_master,
    total,
)


def test_anchor_charity_bypass_branch_is_unsat():
    solver, value, present = build_master()
    rotated, allocations = add_anchor_charity_bypass_constraints(
        solver, value, present
    )
    solver.set(timeout=10_000)
    assert solver.check() == z3.unsat
    assert len(allocations) == len(OWNERS)
    assert set(RESPONSE_CORE["r"]) <= set(rotated["r"])
    assert not (set(RESPONSE_CORE["r"]) & set(rotated["q"]))
