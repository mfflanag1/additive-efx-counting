#!/usr/bin/env python3
"""Differential tests for the independent terminal CNF translation."""

from __future__ import annotations

import argparse
import contextlib
import io
import itertools
import json
import lzma
import os
import random
import tempfile
import time
from pathlib import Path

from pysat.solvers import Solver

try:
    from . import (
        independent,
        replay_terminal_cnf,
        run_cegar,
        terminal_cnf,
        verify_terminal_drat,
    )
except ImportError:
    import independent
    import replay_terminal_cnf
    import run_cegar
    import terminal_cnf
    import verify_terminal_drat


def pool_document(
    n: int,
    m: int,
    upper: int,
    triples: list[terminal_cnf.Triple],
) -> dict:
    return {
        "schema": terminal_cnf.POOL_SCHEMA,
        "property": terminal_cnf.PROPERTY,
        "n": n,
        "m": m,
        "lower": 1,
        "upper": upper,
        "symmetry": "none",
        "triples": [
            {
                "floater": triple.floater,
                "base_owner": list(triple.base_owner),
                "host": triple.host,
            }
            for triple in triples
        ],
    }


def solve_cnf(cnf: object) -> tuple[bool, list[int] | None]:
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        status = solver.solve()
        return status, solver.get_model() if status else None


def test_threshold_identity() -> int:
    checked = 0
    for upper in range(1, 5):
        for own_size in range(4):
            for target_size in range(4):
                for own in itertools.product(range(1, upper + 1), repeat=own_size):
                    for target in itertools.product(
                        range(1, upper + 1), repeat=target_size
                    ):
                        literal_sum = sum(
                            value >= threshold
                            for value in target
                            for threshold in range(2, upper + 1)
                        )
                        literal_sum += sum(
                            value < threshold
                            for value in own
                            for threshold in range(2, upper + 1)
                        )
                        encoded = literal_sum >= (
                            terminal_cnf.strict_sum_bound(upper, own_size, target_size)
                        )
                        direct = sum(target) > sum(own)
                        if encoded != direct:
                            raise AssertionError(
                                (
                                    upper,
                                    own,
                                    target,
                                    literal_sum,
                                    encoded,
                                    direct,
                                )
                            )
                        checked += 1
    return checked


def test_fixed_triple_cuts() -> int:
    checked = 0
    for flat in itertools.product((1, 2), repeat=4):
        values = [list(flat[:2]), list(flat[2:])]
        for floater in range(2):
            other = 1 - floater
            for owner in range(2):
                base_owner: list[int | None] = [None, None]
                base_owner[other] = owner
                for host in range(2):
                    triple = terminal_cnf.Triple(floater, tuple(base_owner), host)
                    document = pool_document(2, 2, 2, [triple])
                    _, triples = terminal_cnf.validate_pool_document(document)
                    cnf, _, _ = terminal_cnf.build_master(
                        document, triples, fixed_values=values
                    )
                    status, _ = solve_cnf(cnf)
                    literal = independent.is_parkable_triple(
                        values, floater, base_owner, host
                    )
                    translator_literal = terminal_cnf.triple_is_valid(values, triple)
                    if literal != translator_literal:
                        raise AssertionError("literal parkability predicates disagree")
                    if status == literal:
                        raise AssertionError(
                            (
                                "fixed triple cut mismatch",
                                values,
                                triple,
                                status,
                                literal,
                            )
                        )
                    checked += 1
    return checked


def matrix_4x8(case: int) -> list[list[int]]:
    generator = random.Random(2_000_033 * case + 17)
    return [[generator.randint(1, 4) for _ in range(8)] for _ in range(4)]


def triple_4x8(case: int, offset: int) -> terminal_cnf.Triple:
    generator = random.Random(3_000_017 * case + 101 * offset + 29)
    floater = generator.randrange(8)
    owner: list[int | None] = [generator.randrange(4) for _ in range(8)]
    owner[floater] = None
    return terminal_cnf.Triple(
        floater,
        tuple(owner),
        generator.randrange(4),
    )


def test_full_size_fixed_cuts() -> tuple[int, int]:
    single_checks = 0
    pool_checks = 0
    for case in range(96):
        values = matrix_4x8(case)
        triple = triple_4x8(case, 0)
        document = pool_document(4, 8, 4, [triple])
        cnf, _, _ = terminal_cnf.build_master(document, [triple], fixed_values=values)
        status, _ = solve_cnf(cnf)
        literal = independent.is_parkable_triple(
            values,
            triple.floater,
            list(triple.base_owner),
            triple.host,
        )
        if literal != terminal_cnf.triple_is_valid(values, triple):
            raise AssertionError("full-size literal predicates disagree")
        if status == literal:
            raise AssertionError(("full-size fixed cut mismatch", case))
        single_checks += 1

    for case in range(48):
        values = matrix_4x8(case + 101)
        triples = list(
            dict.fromkeys(triple_4x8(case + 17, offset) for offset in range(4))
        )
        document = pool_document(4, 8, 4, triples)
        cnf, _, _ = terminal_cnf.build_master(document, triples, fixed_values=values)
        status, _ = solve_cnf(cnf)
        expected = all(
            not terminal_cnf.triple_is_valid(values, triple) for triple in triples
        )
        if status != expected:
            raise AssertionError(("full-size pool projection mismatch", case))
        pool_checks += 1
    return single_checks, pool_checks


def test_guard_boundaries() -> int:
    checked = 0
    for literal_count in range(6):
        for bound in range(-1, literal_count + 2):
            for truth_values in itertools.product((False, True), repeat=literal_count):
                encoder = terminal_cnf.CnfEncoder()
                literals = [
                    encoder.variable(f"literal_{index}")
                    for index in range(literal_count)
                ]
                guard = encoder.variable("guard")
                encoder.add_guarded_atleast(guard, literals, bound)
                encoder.cnf.append([guard])
                for literal, truth in zip(literals, truth_values):
                    encoder.cnf.append([literal if truth else -literal])
                status, _ = solve_cnf(encoder.cnf)
                expected = sum(truth_values) >= bound
                if status != expected:
                    raise AssertionError(
                        (
                            "guarded cardinality boundary mismatch",
                            literal_count,
                            bound,
                            truth_values,
                            status,
                            expected,
                        )
                    )
                checked += 1
    return checked


def expect_invalid(document: dict) -> None:
    try:
        terminal_cnf.validate_pool_document(document)
    except ValueError:
        return
    raise AssertionError("invalid terminal pool was accepted")


def test_schema() -> int:
    triple = terminal_cnf.Triple(0, (None, 0), 0)
    valid = pool_document(2, 2, 2, [triple])
    terminal_cnf.validate_pool_document(valid)

    extra = dict(valid)
    extra["note"] = "not in schema"
    expect_invalid(extra)

    wrong_symmetry = dict(valid)
    wrong_symmetry["symmetry"] = "double_lex"
    expect_invalid(wrong_symmetry)

    duplicate = json.loads(json.dumps(valid))
    duplicate["triples"].append(duplicate["triples"][0])
    expect_invalid(duplicate)

    wrong_null = json.loads(json.dumps(valid))
    wrong_null["triples"][0]["base_owner"] = [0, None]
    expect_invalid(wrong_null)

    boolean_owner = json.loads(json.dumps(valid))
    boolean_owner["triples"][0]["base_owner"][1] = True
    expect_invalid(boolean_owner)
    return 6


def crashing_worker(clauses: object, solver_name: str, output: object) -> None:
    del clauses, solver_name, output
    os._exit(17)


def sleeping_worker(clauses: object, solver_name: str, output: object) -> None:
    del clauses, solver_name, output
    time.sleep(5)


def test_isolated_solver() -> int:
    solved, reason = terminal_cnf.solve_with_timeout([[1]], "cadical195", 5)
    if reason is not None or solved is None or not solved["status"]:
        raise AssertionError("real isolated SAT solve failed")
    try:
        terminal_cnf.solve_with_timeout([[1]], "cadical195", 2, worker=crashing_worker)
    except RuntimeError as error:
        if "17" not in str(error):
            raise
    else:
        raise AssertionError("crashed solver child was not detected")
    solved, reason = terminal_cnf.solve_with_timeout(
        [[1]], "cadical195", 0.1, worker=sleeping_worker
    )
    if solved is not None or reason != "wall-clock timeout":
        raise AssertionError("solver wall-clock timeout was not detected")
    return 3


def run_cp_campaign(directory: Path, upper: int, add: int) -> tuple[dict, Path, Path]:
    pool_path = directory / f"k{upper}-pool.json"
    trace_path = directory / f"k{upper}-trace.jsonl"
    with contextlib.redirect_stdout(io.StringIO()):
        result = run_cegar.run(
            upper=upper,
            add_per_iteration=add,
            time_limit_s=30,
            workers=1,
            random_seed=1,
            symmetry="none",
            max_iterations=50,
            pool_path=pool_path,
            result_path=directory / f"k{upper}-cp.json",
            trace_path=trace_path,
        )
    if result["status"] != "UNSAT_CANDIDATE":
        raise AssertionError(f"K={upper} CP calibration did not close")
    return result, pool_path, trace_path


def test_terminal_campaigns() -> tuple[int, str]:
    with tempfile.TemporaryDirectory(
        prefix="parkability-terminal-test-"
    ) as directory_name:
        directory = Path(directory_name)
        _, k1_pool, _ = run_cp_campaign(directory, upper=1, add=4)
        k1_snapshot = terminal_cnf.load_pool_snapshot(k1_pool)
        k1_cnf, _, _ = terminal_cnf.build_master(
            k1_snapshot.document, k1_snapshot.triples
        )
        if solve_cnf(k1_cnf)[0]:
            raise AssertionError("independent K=1 terminal master is SAT")

        cp_result, k2_pool, k2_trace = run_cp_campaign(directory, upper=2, add=32)
        if cp_result["pool_size"] == 0:
            raise AssertionError("K=2 calibration pool is empty")
        snapshot = terminal_cnf.load_pool_snapshot(k2_pool)
        cnf, value_bits, _ = terminal_cnf.build_master(
            snapshot.document, snapshot.triples
        )
        if solve_cnf(cnf)[0]:
            raise AssertionError("independent K=2 terminal master is SAT")

        prefix_document = json.loads(json.dumps(snapshot.document))
        trace_records = [
            json.loads(line) for line in k2_trace.read_text().splitlines() if line
        ]
        if not trace_records:
            raise AssertionError("K=2 calibration trace is empty")
        prefix_size = trace_records[-1]["pool_size_before"]
        prefix_document["triples"] = prefix_document["triples"][:prefix_size]
        _, prefix_triples = terminal_cnf.validate_pool_document(prefix_document)
        prefix_cnf, prefix_bits, _ = terminal_cnf.build_master(
            prefix_document, prefix_triples
        )
        prefix_status, prefix_model = solve_cnf(prefix_cnf)
        if not prefix_status or prefix_model is None:
            raise AssertionError("K=2 pool prefix is not SAT")
        prefix_values = terminal_cnf.decode_values(prefix_model, prefix_bits)
        model_check = terminal_cnf.verify_decoded_model(
            prefix_cnf,
            prefix_model,
            prefix_values,
            prefix_document,
            prefix_triples,
        )
        if not all(model_check.values()):
            raise AssertionError("decoded K=2 prefix model failed")
        prefix_dimacs = directory / "prefix.cnf"
        terminal_cnf.export_dimacs(prefix_cnf, prefix_dimacs)
        prefix_replay_path = directory / "prefix-replay.json"
        with contextlib.redirect_stdout(io.StringIO()):
            prefix_replay_exit = replay_terminal_cnf.run(
                argparse.Namespace(
                    dimacs=prefix_dimacs,
                    expect_sha256=terminal_cnf.sha256(prefix_dimacs),
                    solver="cadical195",
                    timeout_seconds=30.0,
                    result_out=prefix_replay_path,
                    expect="sat",
                )
            )
        prefix_replay = json.loads(prefix_replay_path.read_text())
        if (
            prefix_replay_exit != 0
            or prefix_replay["status"] != "SAT"
            or prefix_replay.get("model_verified") != {"all_dimacs_clauses": True}
            or not prefix_replay.get("model")
        ):
            raise AssertionError("cold SAT replay lacks a verified model")

        first_dimacs = directory / "first.cnf"
        second_dimacs = directory / "second.cnf"
        terminal_cnf.export_dimacs(cnf, first_dimacs)
        rebuilt, rebuilt_bits, _ = terminal_cnf.build_master(
            snapshot.document, snapshot.triples
        )
        terminal_cnf.export_dimacs(rebuilt, second_dimacs)
        first_hash = terminal_cnf.sha256(first_dimacs)
        if first_hash != terminal_cnf.sha256(second_dimacs):
            raise AssertionError("terminal DIMACS rebuild is not deterministic")
        if (
            first_hash
            != "fa7d72120474524f18bf2681c0cfbb7bd863ec01cbc1238d3b980f84f3f701ac"
        ):
            raise AssertionError(f"unexpected K=2 DIMACS regression hash: {first_hash}")
        if len(value_bits) != len(rebuilt_bits):
            raise AssertionError("rebuilt value-bit dimensions changed")

        result_path = directory / "terminal-result.json"
        with contextlib.redirect_stdout(io.StringIO()):
            exit_code = terminal_cnf.run(
                argparse.Namespace(
                    pool=k2_pool,
                    export=directory / "terminal.cnf",
                    result_out=result_path,
                    solver="cadical195",
                    timeout_seconds=30.0,
                    expect="unsat",
                )
            )
        result = json.loads(result_path.read_text())
        if (
            exit_code != 0
            or result["status"] != "UNSAT_SOLVER_RESULT"
            or result["solver"]["status"] != "UNSAT"
            or result["pool_sha256"] != cp_result["pool_sha256"]
        ):
            raise AssertionError("terminal K=2 result record is inconsistent")

        replay_path = directory / "replay.json"
        with contextlib.redirect_stdout(io.StringIO()):
            replay_exit = replay_terminal_cnf.run(
                argparse.Namespace(
                    dimacs=directory / "terminal.cnf",
                    expect_sha256=result["dimacs_sha256"],
                    solver="cadical195",
                    timeout_seconds=30.0,
                    result_out=replay_path,
                    expect="unsat",
                )
            )
        replay = json.loads(replay_path.read_text())
        if (
            replay_exit != 0
            or replay["status"] != "UNSAT_SOLVER_RESULT"
            or replay["dimacs_sha256"] != result["dimacs_sha256"]
        ):
            raise AssertionError("cold terminal replay is inconsistent")

        proof = directory / "dummy-proof.drat"
        proof.write_bytes(b"c hash-only wrapper calibration\n")
        compressed_proof = directory / "dummy-proof.drat.xz"
        with lzma.open(compressed_proof, "wb") as output:
            output.write(proof.read_bytes())
        proof_check_path = directory / "proof-hashes.json"
        with contextlib.redirect_stdout(io.StringIO()):
            proof_exit = verify_terminal_drat.run(
                argparse.Namespace(
                    dimacs=directory / "terminal.cnf",
                    terminal_result=result_path,
                    proof=compressed_proof,
                    result_out=proof_check_path,
                    expect_dimacs_sha256=result["dimacs_sha256"],
                    expect_proof_sha256=terminal_cnf.sha256(compressed_proof),
                    expect_uncompressed_sha256=terminal_cnf.sha256(proof),
                    expect_uncompressed_bytes=proof.stat().st_size,
                    checker="not-used-in-hash-only-mode",
                    timeout_seconds=1,
                    binary=True,
                    hash_only=True,
                )
            )
        proof_check = json.loads(proof_check_path.read_text())
        if (
            proof_exit != 0
            or proof_check["status"] != "HASHES_PASS"
            or proof_check["input"]["sha256"] != result["dimacs_sha256"]
            or proof_check["proof"]["uncompressed_sha256"] != terminal_cnf.sha256(proof)
        ):
            raise AssertionError("terminal proof hash record is inconsistent")
        try:
            verify_terminal_drat.require_hash(
                compressed_proof, "0" * 64, "proof source"
            )
        except ValueError:
            pass
        else:
            raise AssertionError("wrong proof hash was accepted")

        bad_terminal = json.loads(result_path.read_text())
        bad_terminal["dimacs_sha256"] = "0" * 64
        bad_terminal_path = directory / "bad-terminal.json"
        bad_terminal_path.write_text(json.dumps(bad_terminal))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                verify_terminal_drat.run(
                    argparse.Namespace(
                        dimacs=directory / "terminal.cnf",
                        terminal_result=bad_terminal_path,
                        proof=compressed_proof,
                        result_out=directory / "bad-chain.json",
                        expect_dimacs_sha256=None,
                        expect_proof_sha256=None,
                        expect_uncompressed_sha256=None,
                        expect_uncompressed_bytes=None,
                        checker="not-used-in-hash-only-mode",
                        expect_checker_sha256=None,
                        timeout_seconds=1,
                        binary=True,
                        hash_only=True,
                    )
                )
        except ValueError:
            pass
        else:
            raise AssertionError("mismatched terminal-result chain was accepted")

        corrupt_xz = directory / "corrupt-proof.drat.xz"
        corrupt_xz.write_bytes(b"not an xz stream")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                verify_terminal_drat.run(
                    argparse.Namespace(
                        dimacs=directory / "terminal.cnf",
                        terminal_result=result_path,
                        proof=corrupt_xz,
                        result_out=directory / "corrupt-xz.json",
                        expect_dimacs_sha256=None,
                        expect_proof_sha256=None,
                        expect_uncompressed_sha256=None,
                        expect_uncompressed_bytes=None,
                        checker="not-used-in-hash-only-mode",
                        expect_checker_sha256=None,
                        timeout_seconds=1,
                        binary=True,
                        hash_only=True,
                    )
                )
        except lzma.LZMAError:
            pass
        else:
            raise AssertionError("corrupt XZ proof was accepted")

        rejecting_checker = directory / "rejecting-checker"
        rejecting_checker.write_text(
            "#!/bin/sh\nprintf 'verification failed\\n'\nexit 0\n"
        )
        rejecting_checker.chmod(0o700)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                verify_terminal_drat.run(
                    argparse.Namespace(
                        dimacs=directory / "terminal.cnf",
                        terminal_result=result_path,
                        proof=proof,
                        result_out=directory / "rejected-proof.json",
                        expect_dimacs_sha256=None,
                        expect_proof_sha256=None,
                        expect_uncompressed_sha256=None,
                        expect_uncompressed_bytes=None,
                        checker=str(rejecting_checker),
                        expect_checker_sha256=terminal_cnf.sha256(rejecting_checker),
                        timeout_seconds=1,
                        binary=True,
                        hash_only=False,
                    )
                )
        except RuntimeError:
            pass
        else:
            raise AssertionError("checker output without VERIFIED was accepted")
        return 14, first_hash


def main() -> None:
    identity_checks = test_threshold_identity()
    fixed_cuts = test_fixed_triple_cuts()
    full_size_single, full_size_pools = test_full_size_fixed_cuts()
    guard_checks = test_guard_boundaries()
    schema_checks = test_schema()
    solver_checks = test_isolated_solver()
    campaign_checks, dimacs_hash = test_terminal_campaigns()
    print(
        "PASS parkability terminal CNF: "
        f"{identity_checks} threshold identities, "
        f"{fixed_cuts} fixed cuts, {guard_checks} guard checks, "
        f"{full_size_single} full-size cuts, "
        f"{full_size_pools} full-size pools, "
        f"{schema_checks} schema checks, "
        f"{solver_checks} isolated-solver checks, "
        f"{campaign_checks} campaign checks, "
        f"K=2 DIMACS {dimacs_hash[:16]}"
    )


if __name__ == "__main__":
    main()
