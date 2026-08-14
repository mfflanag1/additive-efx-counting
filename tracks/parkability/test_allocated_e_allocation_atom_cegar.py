from fractions import Fraction

import z3

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .run_allocated_e_allocation_atom_cegar import (
    AllocationAtoms,
    canonical,
    complete_menu,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, allocation_formula


def test_complete_menu_is_exact_and_duplicate_free():
    menu = complete_menu()
    assert len(menu) == 93_480
    assert len({canonical(allocation) for allocation in menu}) == len(menu)


def test_lazy_atom_is_formula_equivalent_on_exact_profile():
    value = {
        (good, owner): z3.Real(f"test_all_{good}_{owner}")
        for good in GOODS for owner in OWNERS
    }
    values = {
        owner: {good: Fraction(index + 1, 17) for index, good in enumerate(GOODS)}
        for owner in OWNERS
    }
    allocation = complete_menu()[1234]
    solver = z3.SolverFor("QF_LRA")
    for owner in OWNERS:
        for good in GOODS:
            solver.add(value[good, owner] == z3.RealVal(str(values[owner][good])))
    atoms = AllocationAtoms(solver, value)
    forbidden = atoms.forbid(allocation)
    expected = complete_efx(values, allocation)
    solver.push()
    solver.add(forbidden if expected else z3.Not(forbidden))
    assert solver.check() == z3.unsat
    solver.pop()
    solver.push()
    solver.add(allocation_formula(allocation, value, "complete_efx") != z3.Not(forbidden))
    assert solver.check() == z3.unsat
