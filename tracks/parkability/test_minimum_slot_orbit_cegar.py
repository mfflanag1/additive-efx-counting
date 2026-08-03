from pathlib import Path

import pytest
import z3

try:
    from .decide_threshold_hall_local_gradient import (
        eligible as nested_eligible,
        threshold as nested_threshold,
    )
    from .run_minimum_slot_orbit_cegar import (
        eligible,
        owner_cores_dominate_floater,
        owner_cores_dominate_predecessor_tokens,
        pair_hall_cross_row_core_clauses,
        run,
        theta_upper_bound,
        threshold_terms,
    )
    from .split_minimum_slot_literal_cubes import run as split_literal_cubes
    from .decide_minimum_slot_literal_cube_cover import run as decide_literal_cubes
    from .audit_minimum_slot_diagonal_topology_union import (
        canonical_key,
        template_record,
    )
    from .run_minimum_slot_orbit_cegar import relabeled_state_orbit
except ImportError:
    from decide_threshold_hall_local_gradient import (
        eligible as nested_eligible,
        threshold as nested_threshold,
    )
    from run_minimum_slot_orbit_cegar import (
        eligible,
        owner_cores_dominate_floater,
        owner_cores_dominate_predecessor_tokens,
        pair_hall_cross_row_core_clauses,
        run,
        theta_upper_bound,
        threshold_terms,
    )
    from split_minimum_slot_literal_cubes import run as split_literal_cubes
    from decide_minimum_slot_literal_cube_cover import run as decide_literal_cubes
    from audit_minimum_slot_diagonal_topology_union import (
        canonical_key,
        template_record,
    )
    from run_minimum_slot_orbit_cegar import relabeled_state_orbit


def assert_equivalent(left, right):
    solver = z3.Solver()
    solver.add(z3.Xor(left, right))
    assert solver.check() == z3.unsat


def test_literal_threshold_expansions_are_exact():
    row = [z3.Real(f"x_{good}") for good in range(9)]
    bound = z3.Real("bound")
    for bundle in ((0,), (0, 1), (0, 1, 2)):
        nested = nested_threshold(row, bundle)
        terms = threshold_terms(row, bundle)
        assert_equivalent(bound >= nested, z3.And(*(bound >= term for term in terms)))
        assert_equivalent(bound < nested, z3.Or(*(bound < term for term in terms)))


def test_literal_theta_upper_bound_is_exact():
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    bound = z3.Real("theta_bound")
    for bundles in (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0,), (1, 2), (3, 4), (5, 6, 7)),
    ):
        nested = z3.Sum(
            *(nested_threshold(values[owner], bundles[owner]) for owner in range(4))
        )
        assert_equivalent(
            nested <= bound,
            theta_upper_bound(values, bundles, bound),
        )


def test_literal_eligibility_is_exact():
    values = [
        [z3.Real(f"w_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    bundles = ((0, 1), (2, 3), (4, 5), (6, 7))
    assert_equivalent(
        nested_eligible(values, bundles, 8),
        eligible(values, bundles, 8),
    )


def test_owner_cores_dominate_floater_gate():
    values = [
        [z3.Real(f"d_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    gate = owner_cores_dominate_floater(values)
    for owner, core in enumerate((0, 2, 4, 6)):
        solver = z3.Solver()
        solver.add(gate, values[owner][core] < values[owner][8])
        assert solver.check() == z3.unsat


def test_owner_cores_dominate_predecessor_tokens_gate():
    values = [
        [z3.Real(f"p_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    gate = owner_cores_dominate_predecessor_tokens(values)
    for owner, core in enumerate((0, 2, 4, 6)):
        predecessor_token = (2 * owner - 1) % 8
        solver = z3.Solver()
        solver.add(gate, values[owner][predecessor_token] > values[owner][core])
        assert solver.check() == z3.unsat


def test_pair_hall_cross_row_core_clause_gate():
    values = [
        [z3.Real(f"c_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    gate = pair_hall_cross_row_core_clauses(values)
    solver = z3.Solver()
    solver.add(
        gate,
        values[0][0] < values[0][3],
        values[2][2] > values[2][3] + values[2][4],
    )
    assert solver.check() == z3.unsat
    solver = z3.Solver()
    solver.add(
        gate,
        values[3][1] > values[3][3] + values[3][6],
        values[0][1] + values[0][4] < values[0][3] + values[0][8],
    )
    assert solver.check() == z3.unsat


def test_tracked_assertions_cannot_be_exported_as_standalone_smt2(tmp_path):
    with pytest.raises(
        ValueError,
        match="standalone SMT2 output requires untracked assertions",
    ):
        run(
            tmp_path / "result.json",
            timeout_seconds=1,
            max_iterations=1,
            seed=None,
            relabeling_mode="none",
            completion_batch_size=1,
            smt2_output=Path(tmp_path / "formula.smt2"),
            track_unsat_core=True,
        )


def test_core_minimization_requires_tracking(tmp_path):
    with pytest.raises(
        ValueError,
        match="UNSAT-core minimization requires tracked assertions",
    ):
        run(
            tmp_path / "result.json",
            timeout_seconds=1,
            max_iterations=1,
            seed=None,
            relabeling_mode="none",
            completion_batch_size=1,
            minimize_unsat_core=True,
        )


def test_core_dominance_modes_are_mutually_exclusive(tmp_path):
    with pytest.raises(
        ValueError,
        match="core-dominance assumption and refutation mode are mutually exclusive",
    ):
        run(
            tmp_path / "result.json",
            timeout_seconds=1,
            max_iterations=1,
            seed=None,
            relabeling_mode="none",
            completion_batch_size=1,
            base_owner_cores_dominate_floater=True,
            refute_base_owner_core_below_floater=1,
        )


def test_literal_cube_cover_closes_unsat_source(tmp_path):
    source = tmp_path / "source.smt2"
    source.write_text(
        "(set-logic QF_LRA)\n"
        "(declare-fun v_0_0 () Real)\n"
        "(assert (> v_0_0 0))\n"
        "(assert (<= v_0_0 0))\n"
        "(check-sat)\n"
    )
    manifest = tmp_path / "manifest.json"
    split = split_literal_cubes(
        source,
        tmp_path / "branches",
        manifest,
        depth=2,
        timeout_seconds=1,
    )
    assert split["status"] == "EXACT_CUBE_COVER"
    decision = decide_literal_cubes(
        manifest,
        tmp_path / "decision.json",
        timeout_seconds=1,
        workers=1,
        solver_profile="qf_lra",
    )
    assert decision["status"] == "SOURCE_UNSAT"


def test_diagonal_topology_template_is_cyclically_canonical():
    state = {"floater": 8, "masks": (3, 12, 80, 160)}
    keys = {
        canonical_key(
            {"floater": mapped["floater"], "masks": mapped["masks"]}
        )
        for mapped in relabeled_state_orbit(state, "cyclic")
    }
    assert len(keys) == 1
    record = template_record(keys.pop(), member_count=4)
    assert record["moved_goods"] == 2
    assert record["transfer_support_size"] == 2
    assert record["bundle_shape"] == [2, 2, 2, 2]
