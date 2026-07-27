#!/usr/bin/env python3
"""Independent threshold-CNF checker for a terminal parkability pool."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing
import os
import platform
import queue
import shlex
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pysat
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


POOL_SCHEMA = "parkable-deletion-pool-v1"
PROPERTY = "zero_parkable_deletion_triples"


@dataclass(frozen=True, order=True)
class Triple:
    floater: int
    base_owner: tuple[int | None, ...]
    host: int


@dataclass(frozen=True)
class PoolSnapshot:
    document: dict
    triples: tuple[Triple, ...]
    contents_sha256: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    encoded = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_pool_document(raw: object) -> tuple[dict, tuple[Triple, ...]]:
    if not isinstance(raw, dict):
        raise ValueError("pool must be a JSON object")
    fields = {
        "schema",
        "property",
        "n",
        "m",
        "lower",
        "upper",
        "symmetry",
        "triples",
    }
    if set(raw) != fields:
        raise ValueError(
            f"pool fields differ from the exact schema: {sorted(set(raw) ^ fields)}"
        )
    if raw["schema"] != POOL_SCHEMA or raw["property"] != PROPERTY:
        raise ValueError("unexpected pool schema or property")
    n = raw["n"]
    m = raw["m"]
    lower = raw["lower"]
    upper = raw["upper"]
    if (
        type(n) is not int
        or n < 2
        or type(m) is not int
        or m < 1
        or type(lower) is not int
        or type(upper) is not int
        or lower != 1
        or upper < lower
    ):
        raise ValueError("invalid pool dimensions or value interval")
    if raw["symmetry"] != "none":
        raise ValueError("terminal certification requires symmetry 'none'")
    if not isinstance(raw["triples"], list):
        raise ValueError("pool triples must be a JSON list")

    triples = []
    for index, record in enumerate(raw["triples"]):
        if not isinstance(record, dict) or set(record) != {
            "floater",
            "base_owner",
            "host",
        }:
            raise ValueError(f"invalid triple object at index {index}")
        floater = record["floater"]
        host = record["host"]
        owner = record["base_owner"]
        if type(floater) is not int or not 0 <= floater < m:
            raise ValueError(f"invalid floater at triple index {index}")
        if type(host) is not int or not 0 <= host < n:
            raise ValueError(f"invalid host at triple index {index}")
        if not isinstance(owner, list) or len(owner) != m:
            raise ValueError(f"invalid base_owner at triple index {index}")
        for good, assigned in enumerate(owner):
            if good == floater:
                if assigned is not None:
                    raise ValueError(f"floater is assigned at triple index {index}")
            elif type(assigned) is not int or not 0 <= assigned < n:
                raise ValueError(f"invalid base owner at triple index {index}")
        triples.append(Triple(floater, tuple(owner), host))
    if len(triples) != len(set(triples)):
        raise ValueError("pool contains duplicate triples")
    return raw, tuple(triples)


def load_pool_snapshot(path: Path) -> PoolSnapshot:
    contents = path.read_bytes()
    document, triples = validate_pool_document(json.loads(contents))
    return PoolSnapshot(
        document=document,
        triples=triples,
        contents_sha256=hashlib.sha256(contents).hexdigest(),
    )


def bundles_of(triple: Triple, n: int) -> tuple[tuple[int, ...], ...]:
    bundles: list[list[int]] = [[] for _ in range(n)]
    for good, owner in enumerate(triple.base_owner):
        if owner is not None:
            bundles[owner].append(good)
    return tuple(tuple(bundle) for bundle in bundles)


def strict_sum_bound(upper: int, own_size: int, target_size: int) -> int:
    """Threshold-literal bound equivalent to target sum > own sum."""
    return upper * own_size - target_size + 1


class CnfEncoder:
    def __init__(self) -> None:
        self.vpool = IDPool()
        self.cnf = CNF()

    def variable(self, name: str) -> int:
        return self.vpool.id(name)

    def add_threshold_domain(self, bits: Sequence[int]) -> None:
        for lower, higher in zip(bits, bits[1:]):
            self.cnf.append([-higher, lower])

    def add_guarded_atleast(
        self, guard: int, literals: Sequence[int], bound: int
    ) -> None:
        if bound <= 0:
            return
        if bound > len(literals):
            self.cnf.append([-guard])
            return
        encoded = CardEnc.atleast(
            lits=list(literals),
            bound=bound,
            vpool=self.vpool,
            encoding=EncType.seqcounter,
        )
        for clause in encoded.clauses:
            self.cnf.append([-guard, *clause])


def validate_fixed_values(
    values: Sequence[Sequence[int]], n: int, m: int, lower: int, upper: int
) -> tuple[tuple[int, ...], ...]:
    if (
        not isinstance(values, (list, tuple))
        or len(values) != n
        or any(not isinstance(row, (list, tuple)) or len(row) != m for row in values)
    ):
        raise ValueError("fixed values have the wrong dimensions")
    normalized = []
    for row in values:
        normalized_row = []
        for value in row:
            if type(value) is not int or not lower <= value <= upper:
                raise ValueError("fixed value lies outside the pool interval")
            normalized_row.append(value)
        normalized.append(tuple(normalized_row))
    return tuple(normalized)


def build_master(
    document: dict,
    triples: Sequence[Triple],
    fixed_values: Sequence[Sequence[int]] | None = None,
) -> tuple[
    CNF,
    list[list[list[int]]],
    IDPool,
]:
    n = document["n"]
    m = document["m"]
    lower = document["lower"]
    upper = document["upper"]
    thresholds = tuple(range(lower + 1, upper + 1))
    encoder = CnfEncoder()
    values = [
        [
            [
                encoder.variable(f"value_{observer}_{good}_ge_{threshold}")
                for threshold in thresholds
            ]
            for good in range(m)
        ]
        for observer in range(n)
    ]
    for row in values:
        for bits in row:
            encoder.add_threshold_domain(bits)

    def add_violation(
        triple_index: int,
        family: str,
        observer: int,
        own_bundle: Sequence[int],
        target_remainder: Sequence[int],
        suffix: str,
    ) -> int:
        witness = encoder.variable(f"triple_{triple_index}_{family}_{suffix}_violation")
        literals = [bit for good in target_remainder for bit in values[observer][good]]
        literals.extend(-bit for good in own_bundle for bit in values[observer][good])
        encoder.add_guarded_atleast(
            witness,
            literals,
            strict_sum_bound(upper, len(own_bundle), len(target_remainder)),
        )
        return witness

    for triple_index, triple in enumerate(triples):
        bundles = bundles_of(triple, n)
        violations = []
        for observer in range(n):
            for target in range(n):
                if observer == target:
                    continue
                for removed in bundles[target]:
                    remainder = tuple(
                        good for good in bundles[target] if good != removed
                    )
                    violations.append(
                        add_violation(
                            triple_index,
                            "base",
                            observer,
                            bundles[observer],
                            remainder,
                            (f"observer_{observer}_target_{target}_remove_{removed}"),
                        )
                    )

        enlarged = bundles[triple.host] + (triple.floater,)
        for observer in range(n):
            if observer == triple.host:
                continue
            for removed in enlarged:
                remainder = tuple(good for good in enlarged if good != removed)
                violations.append(
                    add_violation(
                        triple_index,
                        "parking",
                        observer,
                        bundles[observer],
                        remainder,
                        (f"observer_{observer}_host_{triple.host}_remove_{removed}"),
                    )
                )
        if not violations:
            raise ValueError(f"triple {triple_index} has no EFX inequalities")
        encoder.cnf.append(violations)

    if fixed_values is not None:
        fixed = validate_fixed_values(fixed_values, n, m, lower, upper)
        for observer in range(n):
            for good in range(m):
                value = fixed[observer][good]
                for threshold, bit in zip(thresholds, values[observer][good]):
                    encoder.cnf.append([bit if value >= threshold else -bit])

    encoder.cnf.nv = max(encoder.cnf.nv, encoder.vpool.top)
    return encoder.cnf, values, encoder.vpool


def decode_values(
    model: Sequence[int],
    value_bits: Sequence[Sequence[Sequence[int]]],
) -> tuple[tuple[int, ...], ...]:
    assignment = {abs(literal): literal > 0 for literal in model}
    decoded = []
    for row in value_bits:
        decoded_row = []
        for bits in row:
            decoded_row.append(1 + sum(assignment.get(bit, False) for bit in bits))
        decoded.append(tuple(decoded_row))
    return tuple(decoded)


def literal_efx0(
    values: Sequence[Sequence[int]],
    assignment: Sequence[int | None],
    floater: int | None,
) -> bool:
    n = len(values)
    bundles = [
        [good for good, owner in enumerate(assignment) if owner == target]
        for target in range(n)
    ]
    if floater is not None and assignment[floater] is not None:
        raise ValueError("base assignment does not omit its floater")
    for observer in range(n):
        own = sum(values[observer][good] for good in bundles[observer])
        for target in range(n):
            if observer == target:
                continue
            target_total = sum(values[observer][good] for good in bundles[target])
            for removed in bundles[target]:
                if own < target_total - values[observer][removed]:
                    return False
    return True


def triple_is_valid(values: Sequence[Sequence[int]], triple: Triple) -> bool:
    if not literal_efx0(values, triple.base_owner, triple.floater):
        return False
    completion = list(triple.base_owner)
    completion[triple.floater] = triple.host
    return literal_efx0(values, completion, None)


def verify_decoded_model(
    cnf: CNF,
    model: Sequence[int],
    values: Sequence[Sequence[int]],
    document: dict,
    triples: Sequence[Triple],
) -> dict:
    assignment = {abs(literal): literal > 0 for literal in model}
    clauses_valid = all(
        any(assignment.get(abs(literal), False) == (literal > 0) for literal in clause)
        for clause in cnf.clauses
    )
    invalid_triples = all(not triple_is_valid(values, triple) for triple in triples)
    return {
        "all_dimacs_clauses": clauses_valid,
        "symmetry_free": document["symmetry"] == "none",
        "all_pool_triples_invalid": invalid_triples,
    }


def solve_formula(clauses: Sequence[Sequence[int]], solver_name: str) -> dict:
    with Solver(name=solver_name, bootstrap_with=clauses, use_timer=True) as solver:
        status = solver.solve()
        return {
            "status": status,
            "model": solver.get_model() if status else None,
            "backend": type(solver.solver).__name__,
            "statistics": solver.accum_stats(),
            "solver_cpu_seconds": solver.time(),
        }


def solve_worker(
    clauses: Sequence[Sequence[int]], solver_name: str, output: object
) -> None:
    try:
        output.put(
            {
                "ok": True,
                "result": solve_formula(clauses, solver_name),
            }
        )
    except BaseException as error:
        output.put(
            {
                "ok": False,
                "error_type": type(error).__name__,
                "error": str(error),
            }
        )


def solve_with_timeout(
    clauses: Sequence[Sequence[int]],
    solver_name: str,
    timeout_seconds: float,
    worker: object = solve_worker,
) -> tuple[dict | None, str | None]:
    methods = multiprocessing.get_all_start_methods()
    context = multiprocessing.get_context("fork" if "fork" in methods else methods[0])
    output = context.Queue(maxsize=1)
    process = context.Process(target=worker, args=(clauses, solver_name, output))

    def reap(force: bool) -> None:
        if force and process.is_alive():
            process.terminate()
        process.join(timeout=2)
        if process.is_alive():
            process.kill()
            process.join(timeout=2)
        if process.is_alive():
            raise RuntimeError("solver child could not be stopped")

    try:
        process.start()
        deadline = None if timeout_seconds == 0 else time.monotonic() + timeout_seconds
        while True:
            remaining = None if deadline is None else deadline - time.monotonic()
            if remaining is not None and remaining <= 0:
                reap(force=True)
                return None, "wall-clock timeout"
            try:
                payload = output.get(
                    timeout=(0.25 if remaining is None else min(0.25, remaining))
                )
                break
            except queue.Empty:
                if process.is_alive():
                    continue
                reap(force=False)
                try:
                    payload = output.get(timeout=0.25)
                except queue.Empty as error:
                    raise RuntimeError(
                        "solver child exited without a result "
                        f"(exit code {process.exitcode})"
                    ) from error
                break
        reap(force=False)
        if not payload["ok"]:
            raise RuntimeError(f"{payload['error_type']}: {payload['error']}")
        return payload["result"], None
    except BaseException:
        if process.pid is not None:
            reap(force=True)
        raise
    finally:
        if process.pid is not None and process.is_alive():
            reap(force=True)
        output.close()
        output.join_thread()


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def export_dimacs(cnf: CNF, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        cnf.to_file(str(temporary))
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def run(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    source_path = Path(__file__).resolve()
    source_hash = sha256(source_path)
    snapshot = load_pool_snapshot(args.pool)
    document = snapshot.document

    build_started = time.perf_counter()
    cnf, value_bits, vpool = build_master(document, snapshot.triples)
    build_seconds = time.perf_counter() - build_started
    export_dimacs(cnf, args.export)
    dimacs_hash = sha256(args.export)

    solve_started = time.perf_counter()
    solved, unknown_reason = solve_with_timeout(
        cnf.clauses, args.solver, args.timeout_seconds
    )
    solve_seconds = time.perf_counter() - solve_started
    if sha256(args.pool) != snapshot.contents_sha256:
        raise RuntimeError("pool changed during terminal checking")
    if sha256(args.export) != dimacs_hash:
        raise RuntimeError("DIMACS changed during terminal checking")
    if sha256(source_path) != source_hash:
        raise RuntimeError("terminal encoder source changed during checking")

    if solved is None:
        solver_status = "UNKNOWN"
        status = "UNKNOWN"
    else:
        solver_status = "SAT" if solved["status"] else "UNSAT"
        status = "SAT" if solved["status"] else "UNSAT_SOLVER_RESULT"
    result = {
        "schema": "parkability-terminal-cnf-result-v1",
        "status": status,
        "target_claim": (
            "the bounded valuation box has no matrix with zero "
            "parkable deletion triples"
        ),
        "n": document["n"],
        "m": document["m"],
        "lower": document["lower"],
        "upper": document["upper"],
        "symmetry": document["symmetry"],
        "pool_path": str(args.pool.resolve()),
        "pool_sha256": snapshot.contents_sha256,
        "pool_canonical_sha256": canonical_sha256(document),
        "pool_size": len(snapshot.triples),
        "encoding": {
            "implementation": (
                "independent monotone-threshold CNF with no CP-SAT imports"
            ),
            "value_bits_per_entry": document["upper"] - 1,
            "strict_inequalities": (
                "guarded sequential-counter cardinality constraints"
            ),
            "triple_cut": "base-not-EFX0 OR parked-completion-not-EFX0",
        },
        "variables": cnf.nv,
        "named_and_auxiliary_variables": vpool.top,
        "clauses": len(cnf.clauses),
        "dimacs_path": str(args.export.resolve()),
        "dimacs_sha256": dimacs_hash,
        "dimacs_bytes": args.export.stat().st_size,
        "solver": {
            "status": solver_status,
            "requested": args.solver,
            "backend": solved["backend"] if solved else None,
            "timeout_seconds": args.timeout_seconds,
            "statistics": solved["statistics"] if solved else None,
            "cpu_seconds": (solved["solver_cpu_seconds"] if solved else None),
        },
        "seconds": {
            "build": round(build_seconds, 6),
            "solve_wall": round(solve_seconds, 6),
            "total": round(time.perf_counter() - started, 6),
        },
        "command": shlex.join(sys.argv),
        "source_sha256": source_hash,
        "environment": {
            "python": platform.python_version(),
            "python_sat": pysat.__version__,
            "platform": platform.platform(),
        },
    }
    if unknown_reason is not None:
        result["reason_unknown"] = unknown_reason
    if solver_status == "SAT":
        values = decode_values(solved["model"], value_bits)
        model_check = verify_decoded_model(
            cnf,
            solved["model"],
            values,
            document,
            snapshot.triples,
        )
        if not all(model_check.values()):
            raise RuntimeError("decoded SAT model failed semantic validation")
        result["values"] = [list(row) for row in values]
        result["model_verified"] = model_check
    atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2), flush=True)
    if args.expect is not None and solver_status.lower() != args.expect:
        return 1
    return 2 if solver_status == "UNKNOWN" else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--result-out", type=Path, required=True)
    parser.add_argument(
        "--solver",
        choices=("cadical195", "kissat404"),
        default="cadical195",
    )
    parser.add_argument("--timeout-seconds", type=float, default=0)
    parser.add_argument("--expect", choices=("sat", "unsat", "unknown"))
    args = parser.parse_args()
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds < 0:
        parser.error("timeout-seconds must be finite and nonnegative")
    paths = [
        args.pool.resolve(),
        args.export.resolve(),
        args.result_out.resolve(),
    ]
    if len(paths) != len(set(paths)):
        parser.error("pool, DIMACS, and result paths must be distinct")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
