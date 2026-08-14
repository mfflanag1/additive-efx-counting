import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_allocated_e_pi_payment_atom_cegar import CoreAtoms
from .run_generalized_pi_named_selector_cegar import generalized_pi_cut


def test_atomized_family_cut_is_formula_equivalent():
    solver, value = build_master(2)
    atomized_solver = z3.SolverFor("QF_LRA")
    atoms = CoreAtoms(atomized_solver, value)
    witness = {
        "edges": [
            {"source": "r", "desired_core": ["a0", "a1"]},
            {"source": "q", "desired_core": ["j", "k", "q0"]},
            {"source": "s", "desired_core": ["e", "l"]},
        ]
    }
    signature = tuple(sorted(
        (edge["source"], tuple(sorted(edge["desired_core"])))
        for edge in witness["edges"]
    ))
    atomized = atoms.cut(signature)
    inlined = generalized_pi_cut(value, witness)
    atomized_solver.add(z3.Xor(atomized, inlined))
    assert atomized_solver.check() == z3.unsat
    assert len(atoms.atoms) == 3


def test_repeated_core_is_defined_once():
    solver = z3.SolverFor("QF_LRA")
    _, value = build_master(0)
    atoms = CoreAtoms(solver, value)
    first = atoms.atom("d", ("j", "k", "q0"))
    second = atoms.atom("d", ("q0", "j", "k"))
    assert z3.eq(first, second)
    assert len(atoms.atoms) == 1
