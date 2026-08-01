#!/usr/bin/env python3
"""Extract a CaDiCaL assumption core from a cap-5 threshold CNF pool."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from pathlib import Path

from pysat.solvers import Solver

try:
    from .anneal import atomic_json
    from .terminal_distinct_half_full_cell_cnf import build
except ImportError:
    from anneal import atomic_json
    from terminal_distinct_half_full_cell_cnf import build


SCHEMA = "distinct-half-full-cell-threshold-cnf-assumption-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    source_path: Path,
    output: Path,
    cap: int,
    order: str,
    random_seed: int,
    deletion_shrink: bool,
    allow_cap_extension: bool,
):
    source = json.loads(source_path.read_text())
    source_cap = source.get("cap")
    if (
        not source.get("core_partitions")
        or (
            source_cap != cap
            and not (
                allow_cap_extension
                and isinstance(source_cap, int)
                and cap > source_cap
            )
        )
    ):
        raise ValueError("source is not a compatible partition core")
    ordered_source = dict(source)
    raw_partitions = list(source["core_partitions"])
    if order == "reverse":
        raw_partitions.reverse()
    elif order == "random":
        random.Random(random_seed).shuffle(raw_partitions)
    elif order != "original":
        raise ValueError("unknown partition order")
    ordered_source["core_partitions"] = raw_partitions
    encoder, partitions, full_cell_encoding = build(
        ordered_source, cap, partition_assumptions=True
    )
    guards = encoder.partition_guards
    if len(guards) != len(partitions):
        raise AssertionError("partition guard count changed")
    partition_by_guard = dict(zip(guards, partitions))
    started = time.time()
    with Solver(
        name="cadical195",
        bootstrap_with=encoder.cnf.clauses,
        use_timer=True,
    ) as solver:
        satisfiable = solver.solve(assumptions=guards)
        raw_core = () if satisfiable else tuple(solver.get_core() or ())
        current = [
            guard for guard in guards if guard in {abs(item) for item in raw_core}
        ]
        deletion_trace = []
        if not satisfiable and deletion_shrink:
            for guard in tuple(current):
                if guard not in current:
                    continue
                candidate = [item for item in current if item != guard]
                candidate_satisfiable = solver.solve(assumptions=candidate)
                deletion_trace.append(
                    {
                        "tested_guard": guard,
                        "pool_size_before": len(current),
                        "without_guard_status": (
                            "SAT" if candidate_satisfiable else "UNSAT"
                        ),
                    }
                )
                if not candidate_satisfiable:
                    failed = {abs(item) for item in solver.get_core() or ()}
                    current = [item for item in candidate if item in failed]
        statistics = solver.accum_stats()
        cpu_seconds = solver.time()
        backend = type(solver.solver).__name__
    elapsed = time.time() - started
    if satisfiable or not raw_core:
        raise AssertionError("expected an unsatisfiable assumption formula")
    core_guards = set(current)
    if not core_guards <= set(guards):
        raise AssertionError("solver returned an unknown assumption")
    core_partitions = tuple(
        partition_by_guard[guard] for guard in guards if guard in core_guards
    )
    result = {
        "schema": SCHEMA,
        "status": "ASSUMPTION_CORE_EXTRACTED",
        "solver_status": "UNSAT",
        "solver": "CaDiCaL",
        "backend": backend,
        "cap": cap,
        "source_cap": source_cap,
        "cap_extension": cap != source_cap,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "pool_size": len(partitions),
        "partition_order": order,
        "random_seed": random_seed if order == "random" else None,
        "deletion_shrink": deletion_shrink,
        "deletion_trace": deletion_trace,
        "core_size": len(core_partitions),
        "core_partitions": [
            [list(bundle) for bundle in partition]
            for partition in core_partitions
        ],
        "variables": encoder.cnf.nv,
        "clauses": len(encoder.cnf.clauses),
        "full_cell_encoding": full_cell_encoding,
        "statistics": statistics,
        "cpu_seconds": cpu_seconds,
        "elapsed_seconds": elapsed,
        "warning": (
            "The returned core is deletion-minimal for the recorded order."
            if deletion_shrink
            else "The returned failed-assumption core is sufficient, not minimal."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument(
        "--order", choices=("original", "reverse", "random"), default="original"
    )
    parser.add_argument("--random-seed", type=int, default=20260731)
    parser.add_argument("--deletion-shrink", action="store_true")
    parser.add_argument("--allow-cap-extension", action="store_true")
    args = parser.parse_args()
    result = run(
        args.source,
        args.output,
        args.cap,
        args.order,
        args.random_seed,
        args.deletion_shrink,
        args.allow_cap_extension,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
