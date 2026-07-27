#!/usr/bin/env python3
"""Differential tests for the exact parkability workbench."""

from __future__ import annotations

import contextlib
import hashlib
import io
import itertools
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from . import core, independent, master, run_cegar
except ImportError:
    import core
    import independent
    import master
    import run_cegar


ROOT = Path(__file__).resolve().parents[2]


def triple_key(triple: core.Triple) -> independent.Triple:
    return triple.floater, tuple(triple.base_owner), triple.host


def compare_enumerators(values: list[list[int]], label: str) -> int:
    base_first = independent.enumerate_base_first(values)
    completion_first = independent.enumerate_completion_first(values)
    if base_first != completion_first:
        raise AssertionError(f"{label}: independent enumeration orders disagree")

    optimized = [triple_key(triple) for triple in core.iter_parkable_triples(values)]
    repeated = [triple_key(triple) for triple in core.iter_parkable_triples(values)]
    if optimized != repeated:
        raise AssertionError(f"{label}: optimized enumeration is nondeterministic")
    if optimized != base_first:
        raise AssertionError(f"{label}: optimized and literal triple sets disagree")
    optimized_count = core.count_efx0_allocations(values)
    literal_count = independent.count_complete_efx0(values)
    if optimized_count != literal_count:
        raise AssertionError(f"{label}: optimized and literal complete counts disagree")

    for floater, owner, host in optimized:
        triple = core.Triple(floater, owner, host)
        if not core.triple_is_parkable(values, triple):
            raise AssertionError(f"{label}: enumerated triple failed core predicate")
        if not independent.is_parkable_triple(values, floater, owner, host):
            raise AssertionError(f"{label}: enumerated triple failed literal predicate")
    return len(optimized)


def test_literal_zero_semantics() -> None:
    values = [[0, 0], [1, 0]]
    if independent.is_complete_efx0(values, [0, 0]):
        raise AssertionError("zero-valued removed goods were not checked")
    base = (0, None)
    if not independent.is_removed_good_efx0(values, base, 1):
        raise AssertionError("controlled one-good base is not EFX0")
    triple = core.Triple(1, base, 0)
    if independent.is_parkable_triple(values, 1, base, 0):
        raise AssertionError("literal predicate accepted zero-sensitive parking")
    if core.triple_is_parkable(values, triple):
        raise AssertionError("core predicate accepted zero-sensitive parking")


def test_small_differential() -> tuple[int, int]:
    cases = [
        ("single_good", [[1], [0]]),
        ("zero_sensitive", [[0, 0], [1, 0]]),
        ("all_ones", [[1, 1, 1], [1, 1, 1]]),
    ]
    rng = random.Random(20260726)
    for n, m, repetitions in ((2, 2, 5), (2, 3, 5), (3, 3, 5), (3, 4, 5)):
        for index in range(repetitions):
            values = [[rng.randrange(5) for _ in range(m)] for _ in range(n)]
            cases.append((f"random_{n}_{m}_{index}", values))

    triple_total = 0
    for label, values in cases:
        triple_total += compare_enumerators(values, label)
    return len(cases), triple_total


def test_basin1_regression() -> None:
    instance = json.loads((ROOT / "results" / "tb4.json").read_text())
    values = instance["values"]
    expected = [(3, (1, 1, 0, None, 3, 2, 2, 2), host) for host in range(4)] + [
        (5, (1, 1, 0, 2, 3, None, 2, 2), 2),
        (7, (1, 1, 0, 2, 3, 2, 2, None), 2),
    ]
    expected = sorted(expected)

    independent_base = independent.enumerate_base_first(values)
    independent_completion = independent.enumerate_completion_first(values)
    optimized = [triple_key(triple) for triple in core.iter_parkable_triples(values)]
    if independent_base != expected:
        raise AssertionError("basin-1 literal base-first regression changed")
    if independent_completion != expected:
        raise AssertionError("basin-1 literal completion-first regression changed")
    if optimized != expected:
        raise AssertionError("basin-1 optimized regression changed")

    limited = [
        triple_key(triple) for triple in core.iter_parkable_triples(values, limit=3)
    ]
    if limited != expected[:3]:
        raise AssertionError("triple enumeration limit is not a stable prefix")

    recorded_base = expected[0][1]
    base_detail = core.classify_base(values, 3, recorded_base)
    certificates = json.loads(
        (ROOT / "artifacts" / "generalized_parking" / "certificates.json").read_text()
    )
    certificate = next(
        record for record in certificates["witnesses"] if record["id"] == "n4_m8_basin1"
    )
    if base_detail["base_min_efx_slack"] != 3:
        raise AssertionError("basin-1 base EFX slack changed")
    if base_detail["parking_slack_matrix"] != certificate["parking_slack_matrix"]:
        raise AssertionError("basin-1 parking slack matrix changed")
    if base_detail["parkable_hosts"] != [0, 1, 2, 3]:
        raise AssertionError("basin-1 recorded base lost a parking")

    report = core.landscape(values, sample_limit=10)
    if not report["exhaustive"]:
        raise AssertionError("basin-1 landscape unexpectedly stopped early")
    if report["deletion_allocations_checked"] != 8 * 4**7:
        raise AssertionError("basin-1 deletion universe was not exhausted")
    if report["parkable_triple_count"] != 6:
        raise AssertionError("basin-1 parkable triple count changed")
    if report["complete_efx0_count"] != 4:
        raise AssertionError("basin-1 complete EFX0 count changed")
    if independent.count_complete_efx0(values) != 4:
        raise AssertionError("basin-1 literal complete EFX0 count changed")
    if (
        list(independent.count_removed_good_efx0_bases(values))
        != report["efx0_base_count_by_floater"]
    ):
        raise AssertionError("basin-1 literal deletion-base counts changed")
    if [
        core.validate_triple(raw, 4, 8).to_dict() for raw in report["triple_sample"]
    ] != [core.Triple(*triple).to_dict() for triple in expected]:
        raise AssertionError("basin-1 landscape sample changed")

    completions = {
        tuple(
            host if good == floater else owner for good, owner in enumerate(base_owner)
        )
        for floater, base_owner, host in expected
    }
    if len(completions) != 4:
        raise AssertionError("six basin-1 triples no longer encode four completions")

    invalid = core.Triple(0, (None, 0, 0, 0, 0, 0, 0, 0), 0)
    if core.triple_is_parkable(values, invalid):
        raise AssertionError("invalid basin-1 control passed the core predicate")
    if independent.is_parkable_triple(
        values, invalid.floater, invalid.base_owner, invalid.host
    ):
        raise AssertionError("invalid basin-1 control passed the literal predicate")


def test_master_cuts() -> int:
    values = json.loads((ROOT / "results" / "tb4.json").read_text())["values"]
    triples = [
        core.Triple(3, (1, 1, 0, None, 3, 2, 2, 2), host) for host in range(4)
    ] + [
        core.Triple(5, (1, 1, 0, 2, 3, None, 2, 2), 2),
        core.Triple(7, (1, 1, 0, 2, 3, 2, 2, None), 2),
    ]
    for triple in triples:
        fixed = master.ParkabilityMaster(4, 8, 1, 60, fixed_values=values)
        if not fixed.add_triple(triple):
            raise AssertionError("fresh valid triple was treated as a duplicate")
        if fixed.add_triple(triple) or fixed.pool_size != 1:
            raise AssertionError("master triple deduplication failed")
        result = fixed.solve(time_limit_s=10)
        if result.status != "UNSAT":
            raise AssertionError(f"valid fixed triple cut returned {result.status}")

    invalid = core.Triple(0, (None, 0, 0, 0, 0, 0, 0, 0), 0)
    fixed = master.ParkabilityMaster(4, 8, 1, 60, fixed_values=values)
    fixed.add_triple(invalid)
    result = fixed.solve(time_limit_s=10)
    if result.status != "SAT":
        raise AssertionError(f"invalid fixed triple cut returned {result.status}")
    if result.values != tuple(tuple(row) for row in values):
        raise AssertionError("fixed-value master decoded a different matrix")

    tiny = master.ParkabilityMaster(2, 1, 1, 1)
    if tiny.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("empty tiny K=1 master is not SAT")
    only_matrix_triple = core.Triple(0, (None,), 0)
    if not independent.is_parkable_triple(
        [[1], [1]],
        only_matrix_triple.floater,
        only_matrix_triple.base_owner,
        only_matrix_triple.host,
    ):
        raise AssertionError("tiny K=1 control triple is not parkable")
    tiny.add_triple(only_matrix_triple)
    if tiny.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("tiny K=1 valid cut did not close the master")

    exhaustive = 0
    for flat in itertools.product((1, 2), repeat=4):
        small_values = [list(flat[:2]), list(flat[2:])]
        for floater in range(2):
            other = 1 - floater
            for owner in range(2):
                base_owner: list[int | None] = [None, None]
                base_owner[other] = owner
                for host in range(2):
                    triple = core.Triple(floater, tuple(base_owner), host)
                    expected_valid = independent.is_parkable_triple(
                        small_values,
                        floater,
                        base_owner,
                        host,
                    )
                    fixed = master.ParkabilityMaster(
                        2,
                        2,
                        1,
                        2,
                        fixed_values=small_values,
                    )
                    fixed.add_triple(triple)
                    encoded_valid = fixed.solve(time_limit_s=10).status == "UNSAT"
                    if encoded_valid != expected_valid:
                        raise AssertionError(
                            (
                                "fixed triple cut mismatch",
                                small_values,
                                triple,
                                expected_valid,
                            )
                        )
                    exhaustive += 1
    return len(triples) + 2 + exhaustive


def is_double_lex(values: list[list[int]]) -> bool:
    rows = [tuple(row) for row in values]
    columns = [
        tuple(values[observer][good] for observer in range(len(values)))
        for good in range(len(values[0]))
    ]
    return all(
        rows[index] >= rows[index + 1] for index in range(len(rows) - 1)
    ) and all(columns[index] >= columns[index + 1] for index in range(len(columns) - 1))


def test_double_lex() -> tuple[int, int]:
    encoded_cases = 0
    for flat in itertools.product((1, 2), repeat=4):
        values = [list(flat[:2]), list(flat[2:])]
        fixed = master.ParkabilityMaster(
            2, 2, 1, 2, symmetry="double_lex", fixed_values=values
        )
        encoded = fixed.solve(time_limit_s=10).status == "SAT"
        if encoded != is_double_lex(values):
            raise AssertionError(("DoubleLex encoding mismatch", values))
        encoded_cases += 1

    orbit_cases = 0
    for flat in itertools.product((1, 2), repeat=6):
        values = [list(flat[:3]), list(flat[3:])]
        representative = False
        for rows in itertools.permutations(range(2)):
            for columns in itertools.permutations(range(3)):
                permuted = [[values[row][good] for good in columns] for row in rows]
                if is_double_lex(permuted):
                    representative = True
                    break
            if representative:
                break
        if not representative:
            raise AssertionError(("DoubleLex orbit uncovered", values))
        orbit_cases += 1
    return encoded_cases, orbit_cases


def test_pool_and_runner() -> int:
    with tempfile.TemporaryDirectory(prefix="parkability-test-") as directory:
        root = Path(directory)
        pool_path = root / "pool.json"
        trace_path = root / "trace.jsonl"
        result_path = root / "result.json"
        with contextlib.redirect_stdout(io.StringIO()):
            result = run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=result_path,
                trace_path=trace_path,
            )
        if result["status"] != "UNSAT_CANDIDATE":
            raise AssertionError("K=1 runner smoke did not close")
        if result["iterations"] != 2 or result["pool_size"] != 4:
            raise AssertionError("K=1 runner smoke changed")
        pool_bytes = pool_path.read_bytes()
        if result["pool_sha256"] != hashlib.sha256(pool_bytes).hexdigest():
            raise AssertionError("result does not bind the pool bytes")
        if (
            result["trace_sha256"]
            != hashlib.sha256(trace_path.read_bytes()).hexdigest()
        ):
            raise AssertionError("result does not bind the trace bytes")
        triples = run_cegar.load_pool(pool_path, 1, "none")
        if len(triples) != 4:
            raise AssertionError("saved K=1 pool did not replay")
        try:
            run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=root / "stale-trace-result.json",
                trace_path=trace_path,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("existing session trace was accepted")

        resumed_path = root / "resumed.json"
        with contextlib.redirect_stdout(io.StringIO()):
            resumed = run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=resumed_path,
                trace_path=None,
            )
        if (
            resumed["status"] != "UNSAT_CANDIDATE"
            or resumed["iterations"] != 1
            or resumed["pool_sha256"] != result["pool_sha256"]
        ):
            raise AssertionError("K=1 resumed terminal result changed")

        duplicate_path = root / "duplicate.json"
        duplicate = run_cegar.pool_document(triples, 1, "none")
        duplicate["triples"].append(duplicate["triples"][0])
        duplicate_path.write_text(json.dumps(duplicate))
        try:
            run_cegar.load_pool(duplicate_path, 1, "none")
        except ValueError:
            pass
        else:
            raise AssertionError("duplicate pool triple was accepted")

        wrong_box_path = root / "wrong-box.json"
        wrong_box = run_cegar.pool_document(triples, 1, "none")
        wrong_box["upper"] = 2
        wrong_box_path.write_text(json.dumps(wrong_box))
        try:
            run_cegar.load_pool(wrong_box_path, 1, "none")
        except ValueError:
            pass
        else:
            raise AssertionError("pool from a different box was accepted")

        extra_field_path = root / "extra-field.json"
        extra_field = run_cegar.pool_document(triples, 1, "none")
        extra_field["note"] = "not part of the schema"
        extra_field_path.write_text(json.dumps(extra_field))
        try:
            run_cegar.load_pool(extra_field_path, 1, "none")
        except ValueError:
            pass
        else:
            raise AssertionError("extra pool field was accepted")

        try:
            run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=pool_path,
                trace_path=None,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("aliased pool and result paths were accepted")
    return 7


def test_evaluator_cli() -> int:
    with tempfile.TemporaryDirectory(prefix="parkability-evaluate-") as directory:
        output = Path(directory) / "landscape.json"
        details = Path(directory) / "bases.jsonl"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tracks" / "parkability" / "evaluate.py"),
                str(ROOT / "results" / "tb4.json"),
                "--output",
                str(output),
                "--details",
                str(details),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(output.read_text())
        detail_bytes = details.read_bytes()
        if result["details"]["records"] != 167:
            raise AssertionError("evaluator detail record count changed")
        if result["details"]["sha256"] != hashlib.sha256(detail_bytes).hexdigest():
            raise AssertionError("evaluator output does not bind details")
        if detail_bytes.count(b"\n") != result["efx0_base_count"]:
            raise AssertionError("evaluator details are incomplete")
    return 3


def main() -> None:
    test_literal_zero_semantics()
    cases, triples = test_small_differential()
    test_basin1_regression()
    master_cases = test_master_cuts()
    double_lex_cases, orbit_cases = test_double_lex()
    runner_cases = test_pool_and_runner()
    evaluator_cases = test_evaluator_cli()
    print(
        f"PASS parkability differential: {cases} small matrices, "
        f"{triples} small triples, basin-1 exact regression, "
        f"{master_cases} master cases, {double_lex_cases} DoubleLex encodings, "
        f"{orbit_cases} DoubleLex orbits, {runner_cases} runner cases, "
        f"{evaluator_cases} evaluator cases"
    )


if __name__ == "__main__":
    main()
