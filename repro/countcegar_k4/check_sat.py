#!/usr/bin/env python3
"""Independent CNF checker/exporter for the counting-CEGAR K=4 master."""

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
from pathlib import Path

import pysat
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N, M, K, SLOTS = 4, 7, 4, 3
THRESHOLDS = (2, 3, 4)
ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_sha256(value):
    encoded = (json.dumps(value, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_pool(raw):
    if not isinstance(raw, list):
        raise ValueError("pool must be a JSON list")
    unique = []
    seen = set()
    for index, assign in enumerate(raw):
        if (
            not isinstance(assign, list)
            or len(assign) != M
            or any(
                type(owner) is not int or not 0 <= owner < N
                for owner in assign
            )
        ):
            raise ValueError(f"invalid allocation at pool index {index}")
        key = tuple(assign)
        if key not in seen:
            seen.add(key)
            unique.append(assign)
    return raw, unique


def load_pool_snapshot(path):
    contents = path.read_bytes()
    raw, unique = validate_pool(json.loads(contents))
    return raw, unique, hashlib.sha256(contents).hexdigest()


def load_pool(path):
    raw, unique, _ = load_pool_snapshot(path)
    return raw, unique


def validate_fixed_values(values):
    if (
        not isinstance(values, list)
        or len(values) != N
        or any(not isinstance(row, list) or len(row) != M for row in values)
        or any(
            type(value) is not int or not 1 <= value <= K
            for row in values
            for value in row
        )
    ):
        raise ValueError("fixed values must be a 4x7 integer matrix over [1,4]")


class CnfEncoder:
    def __init__(self):
        self.vpool = IDPool()
        self.cnf = CNF()

    def variable(self, name):
        return self.vpool.id(name)

    def add_threshold_domain(self, bits):
        self.cnf.append([-bits[1], bits[0]])
        self.cnf.append([-bits[2], bits[1]])

    def add_lex_ge(self, xs, ys, name):
        if len(xs) != len(ys) or not xs:
            raise ValueError("lexicographic sequences must have equal positive length")
        equal = self.variable(f"{name}_equal")
        greater = [
            self.variable(f"{name}_greater_{index}")
            for index in range(len(xs))
        ]
        self.cnf.append([equal, *greater])

        for left, right in zip(xs, ys):
            for xbit, ybit in zip(left, right):
                self.cnf.append([-equal, -xbit, ybit])
                self.cnf.append([-equal, xbit, -ybit])

        for index, branch in enumerate(greater):
            for prefix in range(index):
                for xbit, ybit in zip(xs[prefix], ys[prefix]):
                    self.cnf.append([-branch, -xbit, ybit])
                    self.cnf.append([-branch, xbit, -ybit])
            witnesses = []
            for threshold, (xbit, ybit) in zip(
                THRESHOLDS, zip(xs[index], ys[index])
            ):
                witness = self.variable(
                    f"{name}_greater_{index}_threshold_{threshold}"
                )
                witnesses.append(witness)
                self.cnf.append([-witness, branch])
                self.cnf.append([-witness, xbit])
                self.cnf.append([-witness, -ybit])
            self.cnf.append([-branch, *witnesses])

    def add_exactly_one(self, literals):
        self.cnf.append(list(literals))
        for left in range(len(literals)):
            for right in range(left + 1, len(literals)):
                self.cnf.append([-literals[left], -literals[right]])

    def add_guarded_atleast(self, guard, literals, bound):
        if bound <= 0:
            return
        if bound > len(literals):
            self.cnf.append([-guard])
            return
        encoded = CardEnc.atleast(
            lits=literals,
            bound=bound,
            vpool=self.vpool,
            encoding=EncType.seqcounter,
        )
        for clause in encoded.clauses:
            self.cnf.append([-guard, *clause])


def build_master(pool, fixed_values=None):
    encoder = CnfEncoder()
    values = [
        [
            [
                encoder.variable(f"v_{observer}_{good}_ge_{threshold}")
                for threshold in THRESHOLDS
            ]
            for good in range(M)
        ]
        for observer in range(N)
    ]
    for row in values:
        for bits in row:
            encoder.add_threshold_domain(bits)

    slots = [
        [
            [
                encoder.variable(f"slot_{slot}_{good}_owner_{owner}")
                for owner in range(N)
            ]
            for good in range(M)
        ]
        for slot in range(SLOTS)
    ]
    for slot in slots:
        for owners in slot:
            encoder.add_exactly_one(owners)

    for observer in range(N - 1):
        encoder.add_lex_ge(
            values[observer],
            values[observer + 1],
            f"row_lex_{observer}_{observer + 1}",
        )
    for good in range(M - 1):
        encoder.add_lex_ge(
            [values[observer][good] for observer in range(N)],
            [values[observer][good + 1] for observer in range(N)],
            f"column_lex_{good}_{good + 1}",
        )

    for allocation_index, assign in enumerate(pool):
        bundles = [[] for _ in range(N)]
        for good, owner in enumerate(assign):
            bundles[owner].append(good)
        disjuncts = []
        for removed_good, owner in enumerate(assign):
            target_remainder = [
                good for good in bundles[owner] if good != removed_good
            ]
            for observer in range(N):
                if observer == owner:
                    continue
                witness = encoder.variable(
                    f"pool_{allocation_index}_remove_{removed_good}"
                    f"_observer_{observer}_strong_envy"
                )
                disjuncts.append(witness)
                own_bundle = bundles[observer]
                literals = [
                    bit
                    for good in target_remainder
                    for bit in values[observer][good]
                ]
                literals.extend(
                    -bit
                    for good in own_bundle
                    for bit in values[observer][good]
                )
                bound = 4 * len(own_bundle) - len(target_remainder) + 1
                encoder.add_guarded_atleast(witness, literals, bound)

        for slot_index, slot in enumerate(slots):
            match = encoder.variable(
                f"pool_{allocation_index}_matches_slot_{slot_index}"
            )
            disjuncts.append(match)
            for good, owner in enumerate(assign):
                encoder.cnf.append([-match, slot[good][owner]])
        encoder.cnf.append(disjuncts)

    if fixed_values is not None:
        validate_fixed_values(fixed_values)
        for observer in range(N):
            for good in range(M):
                value = fixed_values[observer][good]
                for threshold, bit in zip(
                    THRESHOLDS, values[observer][good]
                ):
                    encoder.cnf.append([bit if value >= threshold else -bit])

    encoder.cnf.nv = max(encoder.cnf.nv, encoder.vpool.top)
    return encoder.cnf, values, slots, encoder.vpool


def decode_model(model, values, slots):
    assignment = {}
    for literal in model:
        assignment[abs(literal)] = literal > 0

    def truth(variable):
        if variable not in assignment:
            raise ValueError(f"solver model omitted variable {variable}")
        return assignment[variable]

    matrix = [
        [
            1 + sum(truth(bit) for bit in values[observer][good])
            for good in range(M)
        ]
        for observer in range(N)
    ]
    decoded_slots = []
    for slot in slots:
        decoded = []
        for owner_bits in slot:
            owners = [
                owner
                for owner, variable in enumerate(owner_bits)
                if truth(variable)
            ]
            if len(owners) != 1:
                raise ValueError("solver model violates slot one-hot domain")
            decoded.append(owners[0])
        decoded_slots.append(decoded)
    return matrix, decoded_slots, assignment


def is_doublelex(values):
    rows = [tuple(row) for row in values]
    columns = [
        tuple(values[observer][good] for observer in range(N))
        for good in range(M)
    ]
    return all(rows[index] >= rows[index + 1] for index in range(N - 1)) and all(
        columns[index] >= columns[index + 1] for index in range(M - 1)
    )


def has_strong_envy(values, assign):
    bundles = [[] for _ in range(N)]
    for good, owner in enumerate(assign):
        bundles[owner].append(good)
    for removed_good, owner in enumerate(assign):
        target_remainder = [
            good for good in bundles[owner] if good != removed_good
        ]
        for observer in range(N):
            if observer == owner:
                continue
            own_value = sum(
                values[observer][good] for good in bundles[observer]
            )
            target_value = sum(
                values[observer][good] for good in target_remainder
            )
            if target_value > own_value:
                return True
    return False


def verify_decoded_model(cnf, model_assignment, values, slots, pool):
    clauses_valid = all(
        any(
            model_assignment.get(abs(literal), False) == (literal > 0)
            for literal in clause
        )
        for clause in cnf.clauses
    )
    master_valid = is_doublelex(values) and all(
        has_strong_envy(values, assign) or assign in slots for assign in pool
    )
    return clauses_valid, master_valid


def solve_formula(clauses, solver_name):
    with Solver(
        name=solver_name, bootstrap_with=clauses, use_timer=True
    ) as solver:
        backend = type(solver.solver).__name__
        status = solver.solve()
        model = solver.get_model() if status else None
        try:
            statistics = solver.accum_stats()
        except NotImplementedError:
            statistics = None
        return {
            "status": status,
            "model": model,
            "backend": backend,
            "statistics": statistics,
            "solver_cpu_seconds": solver.time(),
        }


def solve_worker(clauses, solver_name, output):
    try:
        output.put({"ok": True, "result": solve_formula(clauses, solver_name)})
    except BaseException as error:
        output.put(
            {
                "ok": False,
                "error_type": type(error).__name__,
                "error": str(error),
            }
        )


def solve_with_timeout(
    clauses, solver_name, timeout_seconds, worker=solve_worker
):
    if timeout_seconds == 0:
        return solve_formula(clauses, solver_name), None

    methods = multiprocessing.get_all_start_methods()
    context = multiprocessing.get_context(
        "fork" if "fork" in methods else methods[0]
    )
    output = context.Queue(maxsize=1)
    process = context.Process(
        target=worker, args=(clauses, solver_name, output)
    )
    try:
        process.start()
        deadline = time.monotonic() + timeout_seconds
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                process.terminate()
                process.join()
                return None, "wall-clock timeout"
            try:
                payload = output.get(timeout=min(0.25, remaining))
                break
            except queue.Empty:
                if process.is_alive():
                    continue
                process.join()
                try:
                    payload = output.get(timeout=0.25)
                    break
                except queue.Empty as error:
                    raise RuntimeError(
                        "solver child exited without a result "
                        f"(exit code {process.exitcode})"
                    ) from error
        process.join()
        if not payload["ok"]:
            raise RuntimeError(
                f'{payload["error_type"]}: {payload["error"]}'
            )
        return payload["result"], None
    except BaseException:
        if process.pid is not None:
            if process.is_alive():
                process.terminate()
            process.join()
        raise
    finally:
        output.close()
        output.join_thread()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(value, handle, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def run(args):
    started = time.perf_counter()
    load_started = time.perf_counter()
    raw, pool, pool_hash = load_pool_snapshot(args.pool)
    load_seconds = time.perf_counter() - load_started

    build_started = time.perf_counter()
    cnf, values, slots, vpool = build_master(pool)
    build_seconds = time.perf_counter() - build_started

    args.export.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.export))
    dimacs_hash = sha256(args.export)

    solve_started = time.perf_counter()
    solved, unknown_reason = solve_with_timeout(
        cnf.clauses, args.solver, args.timeout_seconds
    )
    solve_seconds = time.perf_counter() - solve_started
    if sha256(args.pool) != pool_hash:
        raise RuntimeError("pool file changed during the check")
    if solved is None:
        status = "UNKNOWN"
    else:
        status = "SAT" if solved["status"] else "UNSAT"

    result = {
        "schema": 1,
        "status": status,
        "claim": (
            "every 4x7 additive valuation matrix over {1,2,3,4} has at "
            "least four EFX0 allocations"
        ),
        "encoding": {
            "formulation": "independent CNF literal-slot master",
            "values": "v = 1 + [v>=2] + [v>=3] + [v>=4]",
            "symmetry": "exact row-and-column DoubleLex",
            "slots": 3,
            "strong_envy": (
                "guarded sequential-counter cardinality encodings"
            ),
        },
        "solver": {
            "requested": args.solver,
            "backend": solved["backend"] if solved else None,
            "timeout_seconds": args.timeout_seconds,
            "timeout_mechanism": (
                "isolated child process with wall-clock termination"
                if args.timeout_seconds
                else None
            ),
            "statistics": solved["statistics"] if solved else None,
            "cpu_seconds": solved["solver_cpu_seconds"] if solved else None,
        },
        "K": K,
        "raw_pool_size": len(raw),
        "unique_pool_size": len(pool),
        "duplicates_dropped": len(raw) - len(pool),
        "pool_path": str(args.pool),
        "pool_sha256": pool_hash,
        "deduplicated_pool_sha256": json_sha256(pool),
        "variables": cnf.nv,
        "named_and_auxiliary_variables": vpool.top,
        "clauses": len(cnf.clauses),
        "dimacs_path": str(args.export),
        "dimacs_sha256": dimacs_hash,
        "dimacs_bytes": args.export.stat().st_size,
        "seconds": {
            "load_pool": round(load_seconds, 6),
            "build": round(build_seconds, 6),
            "solve_wall": round(solve_seconds, 6),
            "total": round(time.perf_counter() - started, 6),
        },
        "command": shlex.join(sys.argv),
        "environment": {
            "python": platform.python_version(),
            "python_sat": pysat.__version__,
            "platform": platform.platform(),
        },
    }
    if unknown_reason:
        result["reason_unknown"] = unknown_reason
    if status == "SAT":
        matrix, decoded_slots, assignment = decode_model(
            solved["model"], values, slots
        )
        clauses_valid, master_valid = verify_decoded_model(
            cnf, assignment, matrix, decoded_slots, pool
        )
        if not clauses_valid or not master_valid:
            raise RuntimeError("SAT model failed independent semantic validation")
        result["values"] = matrix
        result["slots"] = decoded_slots
        result["model_verified"] = {
            "all_dimacs_clauses": clauses_valid,
            "doublelex_and_literal_master": master_valid,
        }

    atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2), flush=True)
    if args.expect and status.lower() != args.expect:
        return 1
    return 2 if status == "UNKNOWN" else 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pool",
        type=Path,
        default=ROOT / "results/countpool_K4_complete.json",
    )
    parser.add_argument(
        "--solver",
        choices=["cadical195", "kissat404"],
        default="cadical195",
    )
    parser.add_argument("--timeout-seconds", type=float, default=0)
    parser.add_argument(
        "--export",
        type=Path,
        default=ROOT / "results/countcegar_K4_sat.cnf",
    )
    parser.add_argument(
        "--result-out",
        type=Path,
        default=ROOT / "results/countcegar_K4_sat.json",
    )
    parser.add_argument("--expect", choices=["sat", "unsat", "unknown"])
    args = parser.parse_args()
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds < 0:
        parser.error("timeout-seconds must be finite and nonnegative")
    resolved = [
        args.pool.resolve(),
        args.export.resolve(),
        args.result_out.resolve(),
    ]
    if len(set(resolved)) != len(resolved):
        parser.error("pool, DIMACS export, and result JSON paths must differ")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
