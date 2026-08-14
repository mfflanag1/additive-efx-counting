"""Audit the physical-minimum EFX encoding and master nonvacuity."""

import z3

from .run_exact_response_physical_minimum_cegar import (
    build_physical_master,
    linear_physical_efx,
    physical_tail,
)
from .run_fixed_u_full_packet_terminal_cegar import OWNERS, total


def test_linear_physical_efx_equals_role_minimum_tail():
    for size in range(1, 13):
        roles = tuple(f"g{index}" for index in range(size))
        allocation = {owner: [f"own_{owner}"] for owner in OWNERS}
        allocation["q"] = list(roles)
        allocation["charity"] = []
        all_roles = (*roles, *(f"own_{owner}" for owner in OWNERS))
        value = {
            (role, observer): z3.Real(f"t_{size}_{role}_{observer}")
            for role in all_roles
            for observer in OWNERS
        }
        minimum = {
            (role, observer): z3.Real(f"m_{size}_{role}_{observer}")
            for role in all_roles
            for observer in OWNERS
        }
        utility = {owner: total(value, owner, allocation[owner]) for owner in OWNERS}
        tail = physical_tail(minimum)
        nested = z3.And(*(
            utility[observer] >= tail(value, observer, allocation[target])
            for observer in OWNERS
            for target in OWNERS
            if observer != target
        ))
        direct = linear_physical_efx(allocation, value, minimum)
        solver = z3.SolverFor("QF_LRA")
        solver.add(*(
            z3.And(minimum[role, observer] > 0, minimum[role, observer] <= value[role, observer])
            for role in all_roles
            for observer in OWNERS
        ))
        solver.add(z3.Xor(nested, direct))
        assert solver.check() == z3.unsat


def test_physical_minimum_masters_are_nonvacuous():
    for form_index in (0, 2):
        solver, _, _ = build_physical_master(form_index)
        solver.set(timeout=10_000)
        assert solver.check() == z3.sat


def test_role_realizability_excludes_the_one_to_two_minimum_gap():
    solver, value, minimum = build_physical_master(0)
    role = "m"
    observer = "r"
    solver.add(minimum[role, observer] < value[role, observer])
    solver.add(value[role, observer] < 2 * minimum[role, observer])
    assert solver.check() == z3.unsat
