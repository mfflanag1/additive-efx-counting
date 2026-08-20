"""Equivalence smoke tests for the fixed-U master solver pipelines."""

import pytest
import z3

from .decide_fixed_u_cut_pool_normal_forms import MODES, solver_for_mode


@pytest.mark.parametrize("mode", MODES)
def test_every_mode_preserves_a_mixed_boolean_linear_sat_formula(mode):
    x, y = z3.Reals("x y")
    p = z3.Bool("p")
    formula = z3.And(
        x > 0, y > 0, x + y == 1,
        z3.If(p, x, y) >= z3.RealVal("1/2"),
        z3.Or(p, x < y),
    )
    solver = solver_for_mode(mode, 5, 0)
    solver.add(formula)
    assert solver.check() == z3.sat


@pytest.mark.parametrize("mode", MODES)
def test_every_mode_preserves_a_mixed_boolean_linear_unsat_formula(mode):
    x = z3.Real("ux")
    p = z3.Bool("up")
    formula = z3.And(
        z3.If(p, x, -x) > 0,
        z3.If(p, x, -x) <= 0,
    )
    solver = solver_for_mode(mode, 5, 0)
    solver.add(formula)
    assert solver.check() == z3.unsat

