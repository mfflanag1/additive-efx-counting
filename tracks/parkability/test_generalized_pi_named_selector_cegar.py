import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .run_generalized_pi_named_selector_cegar import generalized_pi_cut


ROOT = Path(__file__).resolve().parents[2]


def test_generalized_pi_cut_excludes_independent_exact_witness():
    profile = json.loads((
        ROOT / "results" / "two_survivor_named_topology_form0_pi_free_decision.json"
    ).read_text())
    witness = json.loads((
        ROOT / "results" / "two_survivor_named_topology_form0_pi_free_generalized_pi.json"
    ).read_text())["witness"]
    value = {
        (good, owner): z3.Real(f"cut_{good}_{owner}")
        for good in GOODS for owner in OWNERS
    }
    solver = z3.SolverFor("QF_LRA")
    for owner in OWNERS:
        for good in GOODS:
            amount = Fraction(profile["values"][owner][good])
            solver.add(value[good, owner] == z3.RealVal(amount.numerator) / amount.denominator)
    solver.add(generalized_pi_cut(value, witness))
    assert solver.check() == z3.unsat
