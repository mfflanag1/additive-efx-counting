"""Audit the ITE-free complete-EFX formula and helper determinism."""

import z3

from .run_exact_response_linear_allocation_cegar import linear_complete_efx
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula


def test_linear_complete_efx_equals_tail_encoding():
    owners = ("r", "q", "d", "s")
    for size in range(1, 13):
        goods = tuple(f"g{index}" for index in range(size))
        allocation = {owner: [f"own_{owner}"] for owner in owners}
        allocation["q"] = list(goods)
        allocation["charity"] = []
        value = {
            (good, observer): z3.Real(f"v_{size}_{good}_{observer}")
            for good in (*goods, *(f"own_{owner}" for owner in owners))
            for observer in owners
        }
        old = allocation_formula(allocation, value, "complete_efx")
        new = linear_complete_efx(allocation, value)
        solver = z3.SolverFor("QF_LRA")
        solver.add(*(variable > 0 for variable in value.values()))
        solver.add(z3.Xor(old, new))
        assert solver.check() == z3.unsat
