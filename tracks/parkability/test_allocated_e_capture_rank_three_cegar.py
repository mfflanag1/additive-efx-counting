import z3

from .run_allocated_e_capture_rank_three_cegar import (
    ALLOCATED_E_BASE, build_master, linear_base_response,
    pairwise_closed_core_pi_free_constraints,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def test_allocated_e_is_not_unallocated_self_pi():
    assert "l" in ALLOCATED_E_BASE["d"]
    assert "l" not in ALLOCATED_E_BASE["charity"]
    assert "j" in ALLOCATED_E_BASE["q"]
    assert "j" not in ALLOCATED_E_BASE["charity"]


def test_allocated_e_capture_master_builds_both_forms():
    for form_index in (0, 2):
        solver, _ = build_master(form_index)
        assert len(solver.assertions()) > 10_000


def test_pairwise_closed_core_clause_count():
    value = {
        (good, owner): z3.Real(f"pair_{good}_{owner}")
        for good in GOODS for owner in OWNERS
    }
    assert len(pairwise_closed_core_pi_free_constraints(value)) == 11298


def test_linear_base_response_matches_reference_on_exact_samples():
    from .run_fixed_u_rank_three_relation_cegar import base_response
    value = {
        (good, owner): z3.Real(f"lin_{good}_{owner}")
        for good in GOODS for owner in OWNERS
    }
    for goods in (("a0",), ("a0", "a1"), ("j", "k", "q0"), ("h", "l", "e", "gr")):
        solver = z3.SolverFor("QF_LRA")
        solver.add(z3.Xor(
            base_response(value, "d", goods),
            linear_base_response(value, "d", goods),
        ))
        assert solver.check() == z3.unsat
