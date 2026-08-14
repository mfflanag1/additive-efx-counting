import z3

from .run_two_bare_closure_rank_three_cegar import build_master


def test_both_two_bare_exact_response_forms_are_excluded_by_generalized_self_pi():
    for form_index in (0, 2):
        solver, _ = build_master(form_index)
        solver.set(timeout=30_000)
        assert solver.check() == z3.unsat
