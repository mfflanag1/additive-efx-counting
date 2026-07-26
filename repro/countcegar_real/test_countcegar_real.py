#!/usr/bin/env python3
"""Differential regressions for the exact-real protected-slot master."""

from __future__ import annotations

import argparse
import contextlib
import io
import itertools
import json
import tempfile
from fractions import Fraction
from pathlib import Path

import z3

import countcegar_real


ROOT = Path(__file__).resolve().parents[2]


def is_efx0(values: list[list[int]], assignment: list[int]) -> bool:
    bundles = countcegar_real.bundles_of(assignment)
    for observer in range(countcegar_real.N):
        own = sum(values[observer][good] for good in bundles[observer])
        for removed_good, owner in enumerate(assignment):
            if observer == owner:
                continue
            target = sum(
                values[observer][good]
                for good in bundles[owner]
                if good != removed_good
            )
            if own < target:
                return False
    return True


def all_allocations() -> list[list[int]]:
    return [
        list(assignment)
        for assignment in itertools.product(
            range(countcegar_real.N), repeat=countcegar_real.M
        )
    ]


def check_fixed_case(
    values: list[list[int]],
    pool: list[list[int]],
    expected_sat: bool,
    formulation: str,
) -> None:
    master = countcegar_real.RealCountingMaster(
        formulation=formulation,
        symmetry=False,
        fixed_values=values,
    )
    for assignment in pool:
        master.add_allocation(assignment)
    status = master.solver.check()
    if (status == z3.sat) != expected_sat:
        raise AssertionError(
            (formulation, expected_sat, status, pool)
        )
    if status == z3.sat:
        decoded = master.decode_integer_values(master.solver.model())
        for assignment in all_allocations():
            if is_efx0(values, assignment) != is_efx0(decoded, assignment):
                raise AssertionError("rational-to-integer decode changed EFX0")


def test_fixed_master() -> int:
    matrices = {
        "all_ones": [[1] * countcegar_real.M for _ in range(countcegar_real.N)],
        "t47": json.loads((ROOT / "results/t47.json").read_text())["values"],
    }
    checked = 0
    allocations = all_allocations()
    for matrix_name, values in matrices.items():
        efx0 = [
            assignment
            for assignment in allocations
            if is_efx0(values, assignment)
        ]
        non_efx0 = [
            assignment
            for assignment in allocations
            if not is_efx0(values, assignment)
        ]
        if len(efx0) < 4 or not non_efx0:
            raise AssertionError(f"{matrix_name} lacks differential cases")
        cases = {
            "empty": ([], True),
            "three_efx0": (efx0[:3], True),
            "four_efx0": (efx0[:4], False),
            "non_efx0": (non_efx0[:4], True),
            "mixed": (efx0[:3] + non_efx0[:2], True),
        }
        for formulation in ("slots", "cardinality"):
            for pool, expected in cases.values():
                check_fixed_case(values, pool, expected, formulation)
                checked += 1
    return checked


def test_lex_margin() -> int:
    checked = 0
    for left in itertools.product(range(1, 4), repeat=2):
        for right in itertools.product(range(1, 4), repeat=2):
            solver = z3.SolverFor("QF_LRA")
            xs = [z3.Real(f"x_{checked}_{index}") for index in range(2)]
            ys = [z3.Real(f"y_{checked}_{index}") for index in range(2)]
            solver.add(
                *[variable == value for variable, value in zip(xs, left)],
                *[variable == value for variable, value in zip(ys, right)],
                countcegar_real.lex_margin_ge(xs, ys),
            )
            encoded = solver.check() == z3.sat
            direct = left >= right
            if encoded != direct:
                raise AssertionError((left, right, encoded, direct))
            checked += 1
    return checked


def test_doublelex_orbits() -> int:
    checked = 0
    row_permutations = list(itertools.permutations(range(2)))
    column_permutations = list(itertools.permutations(range(3)))
    for flat in itertools.product((1, 2), repeat=6):
        matrix = [flat[:3], flat[3:]]
        representative_exists = False
        for rows in row_permutations:
            for columns in column_permutations:
                permuted = [
                    [matrix[row][column] for column in columns]
                    for row in rows
                ]
                constraints = [
                    countcegar_real.lex_margin_ge(
                        list(map(z3.RealVal, permuted[0])),
                        list(map(z3.RealVal, permuted[1])),
                    )
                ]
                for column in range(2):
                    constraints.append(
                        countcegar_real.lex_margin_ge(
                            [
                                z3.RealVal(permuted[row][column])
                                for row in range(2)
                            ],
                            [
                                z3.RealVal(permuted[row][column + 1])
                                for row in range(2)
                            ],
                        )
                    )
                if z3.is_true(z3.simplify(z3.And(*constraints))):
                    representative_exists = True
                    break
            if representative_exists:
                break
        if not representative_exists:
            raise AssertionError(("DoubleLex orbit has no representative", matrix))
        checked += 1
    return checked


def test_fractional_lex_scaling() -> None:
    left = [z3.RealVal(3) / 2, z3.RealVal(1)]
    right = [z3.RealVal(1), z3.RealVal(100)]
    if z3.is_true(z3.simplify(countcegar_real.lex_margin_ge(left, right))):
        raise AssertionError("subunit lex gap unexpectedly passed unit margin")
    scaled_left = [2 * value for value in left]
    scaled_right = [2 * value for value in right]
    if not z3.is_true(
        z3.simplify(
            countcegar_real.lex_margin_ge(scaled_left, scaled_right)
        )
    ):
        raise AssertionError("global scaling did not restore unit lex margin")


def test_rational_integerization() -> None:
    weights = [
        [1, 2, 3, 4, 5, 6, 7],
        [2, 3, 5, 7, 11, 13, 17],
        [1, 1, 2, 3, 5, 8, 13],
        [3, 4, 4, 6, 9, 10, 15],
    ]
    rational_rows = [
        [Fraction(100 * value, sum(row)) for value in row]
        for row in weights
    ]
    master = countcegar_real.RealCountingMaster(symmetry=False)
    for observer, row in enumerate(rational_rows):
        for good, value in enumerate(row):
            master.solver.add(
                master.values[observer][good]
                == z3.Q(value.numerator, value.denominator)
            )
    if master.solver.check() != z3.sat:
        raise AssertionError("controlled rational master is not SAT")
    decoded = master.decode_integer_values(master.solver.model())
    allocations = all_allocations()
    for assignment in allocations:
        rational_efx = is_efx0(rational_rows, assignment)
        integer_efx = is_efx0(decoded, assignment)
        if rational_efx != integer_efx:
            raise AssertionError("rowwise integerization changed EFX0")


def test_fresh_cegar_cut() -> int:
    values = json.loads((ROOT / "results/t47.json").read_text())["values"]
    efx0 = [
        assignment
        for assignment in all_allocations()
        if is_efx0(values, assignment)
    ]
    if len(efx0) != 4:
        raise AssertionError("t47 is no longer an exact count-four control")
    checked = 0
    for formulation in ("slots", "cardinality"):
        master = countcegar_real.RealCountingMaster(
            formulation=formulation,
            symmetry=False,
            fixed_values=values,
        )
        for assignment in efx0[:3]:
            master.add_allocation(assignment)
        if master.solver.check() != z3.sat:
            raise AssertionError("three-control CEGAR prefix is not SAT")
        decoded = master.decode_integer_values(master.solver.model())
        candidate = countcegar_real.enumerate_all(
            countcegar_real.N,
            countcegar_real.M,
            decoded,
            collect=4,
        )
        known = {tuple(assignment) for assignment in master.pool}
        fresh = [
            assignment
            for assignment in candidate["examples_efx0"]
            if tuple(assignment) not in known
        ]
        if not fresh:
            raise AssertionError("four-allocation candidate produced no fresh cut")
        master.add_allocation(fresh[0])
        if master.solver.check() != z3.unsat:
            raise AssertionError("fourth control cut did not close fixed master")
        checked += 1
    return checked


def test_pool_validation() -> None:
    assignment = [0, 0, 1, 1, 2, 2, 3]
    if countcegar_real.validate_pool([assignment, assignment]) != [assignment]:
        raise AssertionError("pool deduplication failed")
    master = countcegar_real.RealCountingMaster(symmetry=False)
    master.add_allocation(assignment)
    assignment[0] = 3
    if master.pool[0][0] != 0:
        raise AssertionError("master retained a mutable caller pool reference")
    for bad in (
        [[False, 0, 1, 1, 2, 2, 3]],
        [[0, 0, 1]],
        [[0, 0, 1, 1, 2, 2, 4]],
    ):
        try:
            countcegar_real.validate_pool(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid pool passed: {bad}")


def test_trace_state() -> None:
    with tempfile.TemporaryDirectory() as directory:
        trace = Path(directory) / "trace.jsonl"
        if countcegar_real.load_trace_state(trace) != (0, None, None):
            raise AssertionError("missing trace did not decode as empty")
        records = [
            {"pool_size": 4, "pool_sha256": "a" * 64},
            {
                "pool_size": 7,
                "pool_sha256": "b" * 64,
                "invocation_id": "test",
                "cumulative_round": 2,
            },
        ]
        trace.write_text(
            "\n".join(json.dumps(record) for record in records) + "\n"
        )
        if countcegar_real.load_trace_state(trace) != (2, 7, "b" * 64):
            raise AssertionError("trace terminal state was decoded incorrectly")
        trace.write_text('{"pool_size": 7')
        try:
            countcegar_real.load_trace_state(trace)
        except ValueError:
            pass
        else:
            raise AssertionError("truncated trace passed validation")


def test_run_provenance() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        seed = root / "seed.json"
        pool = root / "pool.json"
        result = root / "result.json"
        trace = root / "trace.jsonl"
        export = root / "master.smt2"
        seed.write_text("[]\n")
        arguments = argparse.Namespace(
            seed_pool=seed,
            pool_out=pool,
            result_out=result,
            trace_out=trace,
            export=export,
            formulation="slots",
            add=4,
            timeout_ms=10000,
            max_rounds=1,
            resume=False,
            no_symmetry=True,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            status = countcegar_real.run(arguments)
        if status != 2:
            raise AssertionError("controlled run did not checkpoint")
        first = json.loads(result.read_text())
        first_trace = json.loads(trace.read_text())
        if (
            first["checked_pool_size"] != 0
            or first["cuts_added_after_last_check"] != 4
            or first["export_formula_checked"] is not False
            or first["export_formula_stage"] != "post_cut_pool"
            or first_trace["cumulative_round"] != 1
            or first_trace["invocation_round"] != 1
        ):
            raise AssertionError("controlled run provenance fields are wrong")
        exported_formula = export.read_text()
        exported_pool = json.loads(pool.read_text())
        if any(
            f"pool_{index}_matches_slot_2" not in exported_formula
            for index in range(len(exported_pool))
        ) or f"pool_{len(exported_pool)}_matches_slot_2" in exported_formula:
            raise AssertionError("checkpoint export is not the post-cut master")

        arguments.resume = True
        with contextlib.redirect_stdout(io.StringIO()):
            status = countcegar_real.run(arguments)
        if status != 2:
            raise AssertionError("controlled resume did not checkpoint")
        second = json.loads(result.read_text())
        trace_records = [
            json.loads(line) for line in trace.read_text().splitlines()
        ]
        if (
            second["prior_trace_records"] != 1
            or second["checked_pool_size"] != 4
            or trace_records[-1]["cumulative_round"] != 2
            or trace_records[0]["invocation_id"]
            == trace_records[1]["invocation_id"]
        ):
            raise AssertionError("controlled resume provenance fields are wrong")
        tampered_pool = json.loads(pool.read_text())
        tampered_pool.pop()
        pool.write_text(json.dumps(tampered_pool, indent=2) + "\n")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                countcegar_real.run(arguments)
        except ValueError:
            pass
        else:
            raise AssertionError("resume accepted a trace/pool mismatch")


def test_variable_master() -> None:
    for formulation in ("slots", "cardinality"):
        master = countcegar_real.RealCountingMaster(
            formulation=formulation,
            symmetry=True,
        )
        if master.solver.check() != z3.sat:
            raise AssertionError(f"empty {formulation} master is not SAT")
        values = master.decode_integer_values(master.solver.model())
        if any(value <= 0 for row in values for value in row):
            raise AssertionError("decoded a nonpositive matrix")


def main() -> None:
    test_pool_validation()
    test_trace_state()
    test_run_provenance()
    lex_checks = test_lex_margin()
    orbit_checks = test_doublelex_orbits()
    test_fractional_lex_scaling()
    fixed_checks = test_fixed_master()
    test_rational_integerization()
    cegar_checks = test_fresh_cegar_cut()
    test_variable_master()
    print(
        "PASS exact-real master differential: "
        f"{lex_checks} lex cases, {orbit_checks} DoubleLex orbits, "
        f"{fixed_checks} fixed-master cases, {cegar_checks} CEGAR refinements"
    )


if __name__ == "__main__":
    main()
