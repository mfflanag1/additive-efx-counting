import z3

from .decide_allocated_e_seven_endpoint_packet_lift import (
    endpoint_efx,
    tail,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, allocation_formula


def test_packet_tail_specializes_to_atomic_tail():
    value = {(piece, observer): z3.Real(f"sp_v_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    least = {(piece, observer): value[piece, observer]
             for piece in GOODS for observer in OWNERS}
    from .run_fixed_u_full_packet_terminal_cegar import tail as atomic_tail
    for observer in OWNERS:
        for pieces in (("a0",), ("a0", "a1"), ("j", "k", "q0")):
            solver = z3.Solver()
            solver.add(tail(value, least, observer, pieces) != atomic_tail(value, observer, pieces))
            assert solver.check() == z3.unsat


def test_endpoint_formula_specializes_to_atomic_complete_efx():
    allocation = {
        "r": ["a0", "a1"], "q": ["j", "k", "q0"],
        "d": ["h", "m", "gq", "gr", "p"], "s": ["l", "e"],
        "charity": [],
    }
    value = {(piece, observer): z3.Real(f"ef_v_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    least = {(piece, observer): value[piece, observer]
             for piece in GOODS for observer in OWNERS}
    solver = z3.Solver()
    solver.add(
        endpoint_efx(value, least, allocation)
        != allocation_formula(allocation, value, "complete_efx")
    )
    assert solver.check() == z3.unsat
