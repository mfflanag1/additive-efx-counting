#!/usr/bin/env python3
"""Differential tests for the independent K=4 CNF literal-slot master."""

import argparse
import itertools
import json
import os
import platform
import shlex
import sys
import tempfile
import time
from pathlib import Path

import pysat
import z3
from pysat.solvers import Solver

import check_sat
import check_z3


ROOT = Path(__file__).resolve().parents[2]


def crashing_solver_worker(clauses, solver_name, output):
    del clauses, solver_name, output
    os._exit(17)


def sleeping_solver_worker(clauses, solver_name, output):
    del clauses, solver_name, output
    time.sleep(5)


def is_efx0_definition(values, assign):
    bundles = [[] for _ in range(check_sat.N)]
    for good, owner in enumerate(assign):
        bundles[owner].append(good)
    for observer in range(check_sat.N):
        own = sum(values[observer][good] for good in bundles[observer])
        for owner in range(check_sat.N):
            if owner == observer:
                continue
            target = sum(values[observer][good] for good in bundles[owner])
            for removed_good in bundles[owner]:
                if own < target - values[observer][removed_good]:
                    return False
    return True


def enumerate_efx0(values):
    return [
        list(assign)
        for assign in itertools.product(range(check_sat.N), repeat=check_sat.M)
        if is_efx0_definition(values, assign)
    ]


def test_strong_envy_identity():
    checked = 0
    for own_size in range(check_sat.M):
        for target_size in range(check_sat.M - own_size):
            bound = 4 * own_size - target_size + 1
            own_bundles = itertools.combinations_with_replacement(
                range(1, check_sat.K + 1), own_size
            )
            for own in own_bundles:
                for target in itertools.combinations_with_replacement(
                    range(1, check_sat.K + 1), target_size
                ):
                    threshold_sum = sum(
                        value >= threshold
                        for value in target
                        for threshold in check_sat.THRESHOLDS
                    )
                    threshold_sum += sum(
                        value < threshold
                        for value in own
                        for threshold in check_sat.THRESHOLDS
                    )
                    direct = sum(target) > sum(own)
                    encoded = threshold_sum >= bound
                    if direct != encoded:
                        raise AssertionError(
                            (
                                own_size,
                                target_size,
                                own,
                                target,
                                threshold_sum,
                                bound,
                            )
                        )
                    checked += 1
    return checked


def threshold_assumptions(bits, values):
    return [
        variable if value >= threshold else -variable
        for value, coordinate in zip(values, bits)
        for threshold, variable in zip(check_sat.THRESHOLDS, coordinate)
    ]


def test_doublelex_comparator():
    encoder = check_sat.CnfEncoder()
    left = []
    right = []
    for side, sequence in (("left", left), ("right", right)):
        for index in range(2):
            bits = [
                encoder.variable(f"{side}_{index}_ge_{threshold}")
                for threshold in check_sat.THRESHOLDS
            ]
            encoder.add_threshold_domain(bits)
            sequence.append(bits)
    encoder.add_lex_ge(left, right, "differential_lex")

    checked = 0
    with Solver(
        name="cadical195", bootstrap_with=encoder.cnf.clauses
    ) as solver:
        for left_values in itertools.product(range(1, 5), repeat=2):
            for right_values in itertools.product(range(1, 5), repeat=2):
                assumptions = threshold_assumptions(left, left_values)
                assumptions.extend(
                    threshold_assumptions(right, right_values)
                )
                encoded = solver.solve(assumptions=assumptions)
                direct = left_values >= right_values
                if encoded != direct:
                    raise AssertionError(
                        (left_values, right_values, encoded, direct)
                    )
                checked += 1
    return checked


def cnf_status(values, pool):
    cnf, _, _, _ = check_sat.build_master(pool, fixed_values=values)
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        return solver.solve()


def fix_z3_values(solver, variables, values, encoding):
    for observer in range(check_sat.N):
        for good in range(check_sat.M):
            value = values[observer][good]
            if encoding == "lia":
                solver.add(variables[observer][good] == value)
            else:
                solver.add(variables[observer][good][value - 1])


def z3_status(builder, encoding, values, pool):
    solver, variables, _ = builder(check_sat.K, pool)
    solver.set(timeout=30000)
    fix_z3_values(solver, variables, values, encoding)
    status = solver.check()
    if status == z3.unknown:
        raise AssertionError(
            f"{builder.__name__} returned unknown: {solver.reason_unknown()}"
        )
    return status == z3.sat


def differential_cases():
    matrices = {
        "all_ones": [[1] * check_sat.M for _ in range(check_sat.N)],
        "staircase": [
            [4, 4, 4, 3, 3, 2, 1],
            [4, 4, 3, 3, 2, 2, 1],
            [4, 3, 3, 2, 2, 1, 1],
            [3, 3, 2, 2, 1, 1, 1],
        ],
    }
    formulations = {
        "lia_slots": (check_z3.build_lia_master, "lia"),
        "lia_cardinality": (
            check_z3.build_lia_cardinality_master,
            "lia",
        ),
        "pb_slots": (check_z3.build_pb_master, "pb"),
        "pb_cardinality": (
            check_z3.build_pb_cardinality_master,
            "pb",
        ),
    }
    records = []
    for matrix_name, values in matrices.items():
        if not check_sat.is_doublelex(values):
            raise AssertionError(f"{matrix_name} is not DoubleLex")
        efx0 = enumerate_efx0(values)
        non_efx0 = [
            list(assign)
            for assign in itertools.product(
                range(check_sat.N), repeat=check_sat.M
            )
            if not is_efx0_definition(values, assign)
        ][:4]
        if len(efx0) < 4 or len(non_efx0) < 4:
            raise AssertionError(f"{matrix_name} lacks test allocations")
        cases = {
            "empty": [],
            "three_efx0": efx0[:3],
            "four_efx0": efx0[:4],
            "non_efx0_only": non_efx0,
            "three_efx0_plus_non_efx0": efx0[:3] + non_efx0[:2],
        }
        for case_name, pool in cases.items():
            distinct_efx0 = {
                tuple(assign)
                for assign in pool
                if is_efx0_definition(values, assign)
            }
            expected = len(distinct_efx0) <= check_sat.SLOTS
            statuses = {"definition": expected, "cnf_slots": cnf_status(values, pool)}
            for formulation, (builder, encoding) in formulations.items():
                statuses[formulation] = z3_status(
                    builder, encoding, values, pool
                )
            if any(status != expected for status in statuses.values()):
                raise AssertionError(
                    (matrix_name, case_name, expected, statuses)
                )
            records.append(
                {
                    "matrix": matrix_name,
                    "case": case_name,
                    "pool_size": len(pool),
                    "distinct_efx0_in_pool": len(distinct_efx0),
                    "expected_sat": expected,
                    "statuses": statuses,
                }
            )
    return records


def test_pool_loader_and_dimacs():
    with tempfile.TemporaryDirectory() as directory:
        directory = Path(directory)
        allocation = [0, 0, 1, 1, 2, 2, 3]
        pool_path = directory / "pool.json"
        pool_path.write_text(json.dumps([allocation, allocation]) + "\n")
        raw, unique = check_sat.load_pool(pool_path)
        if len(raw) != 2 or unique != [allocation]:
            raise AssertionError("pool deduplication failed")

        bad_path = directory / "bad.json"
        bad_path.write_text(json.dumps([[False, 0, 1, 1, 2, 2, 3]]) + "\n")
        try:
            check_sat.load_pool(bad_path)
        except ValueError:
            pass
        else:
            raise AssertionError("boolean owner passed strict pool validation")

        first, _, _, _ = check_sat.build_master(unique)
        second, _, _, _ = check_sat.build_master(unique)
        first_path = directory / "first.cnf"
        second_path = directory / "second.cnf"
        first.to_file(str(first_path))
        second.to_file(str(second_path))
        if check_sat.sha256(first_path) != check_sat.sha256(second_path):
            raise AssertionError("DIMACS export is not deterministic")
        return {
            "raw_pool_size": len(raw),
            "unique_pool_size": len(unique),
            "dimacs_sha256": check_sat.sha256(first_path),
        }


def test_isolated_solver_process():
    solved, reason = check_sat.solve_with_timeout(
        [[1]], "cadical195", 5.0
    )
    if reason is not None or solved["status"] is not True:
        raise AssertionError((solved, reason))

    started = time.monotonic()
    try:
        check_sat.solve_with_timeout(
            [[1]],
            "cadical195",
            5.0,
            worker=crashing_solver_worker,
        )
    except RuntimeError as error:
        elapsed = time.monotonic() - started
        if "exit code 17" not in str(error) or elapsed >= 2:
            raise AssertionError((str(error), elapsed))
    else:
        raise AssertionError("crashed solver child was not detected")

    timeout_started = time.monotonic()
    timed_out, reason = check_sat.solve_with_timeout(
        [[1]],
        "cadical195",
        0.1,
        worker=sleeping_solver_worker,
    )
    timeout_elapsed = time.monotonic() - timeout_started
    if (
        timed_out is not None
        or reason != "wall-clock timeout"
        or timeout_elapsed >= 2
    ):
        raise AssertionError((timed_out, reason, timeout_elapsed))
    return {
        "successful_backend": solved["backend"],
        "crash_exit_code": 17,
        "crash_detected_within_seconds": round(elapsed, 6),
        "timeout_reason": reason,
        "timeout_detected_within_seconds": round(timeout_elapsed, 6),
    }


def run(args):
    started = time.perf_counter()
    identity_checks = test_strong_envy_identity()
    lex_checks = test_doublelex_comparator()
    loader = test_pool_loader_and_dimacs()
    isolated_process = test_isolated_solver_process()
    cases = differential_cases()
    source_paths = {
        "check_sat": Path(check_sat.__file__).resolve(),
        "check_z3": Path(check_z3.__file__).resolve(),
        "differential_test": Path(__file__).resolve(),
    }
    result = {
        "schema": 1,
        "status": "PASS",
        "test": (
            "independent CNF against direct definitions and four Z3 "
            "master formulations"
        ),
        "strong_envy_identity_checks": identity_checks,
        "lexicographic_comparator_checks": lex_checks,
        "differential_cases": cases,
        "pool_and_dimacs_checks": loader,
        "isolated_solver_process": isolated_process,
        "seconds": round(time.perf_counter() - started, 6),
        "command": shlex.join(sys.argv),
        "source_sha256": {
            name: check_sat.sha256(path)
            for name, path in source_paths.items()
        },
        "environment": {
            "python": platform.python_version(),
            "python_sat": pysat.__version__,
            "z3": z3.get_version_string(),
            "platform": platform.platform(),
        },
    }
    check_sat.atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2))
    return 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_sat_differential.json",
    )
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
