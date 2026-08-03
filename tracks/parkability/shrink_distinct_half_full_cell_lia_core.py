#!/usr/bin/env python3
"""Extract a Z3 assumption core from a bounded full-cell partition pool."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_distinct_half_hall_layers import add_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import add_no_full_hall_cell
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import add_no_full_hall_cell


SCHEMA = "distinct-half-full-cell-lia-assumption-core-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    output: Path,
    smt2: Path,
    source: Path,
    cap: int,
    time_limit: float,
    minimize_core: bool,
):
    payload = json.loads(source.read_text())
    if payload.get("cap") != cap or payload.get("solver_status") not in {
        "INFEASIBLE",
        "unsat",
    }:
        raise ValueError("source is not a compatible infeasible cap result")
    raw_partitions = payload.get("core_partitions")
    if raw_partitions is None:
        raise ValueError("source does not contain core_partitions")
    partitions = tuple(
        tuple(tuple(bundle) for bundle in partition)
        for partition in raw_partitions
    )
    universe = set(favorite_pair_balanced_universe())
    if len(partitions) != len(set(partitions)) or not set(partitions) <= universe:
        raise AssertionError("invalid source partition pool")

    master = ParkabilityLRAMaster(N, M, integer_upper=cap)
    add_branch(master, None, threshold_encoding="sorting")
    for agent in range(N - 1):
        master.solver.add(
            master.values[agent][FAVORITE]
            >= master.values[agent + 1][FAVORITE]
        )
    for good in range(5, M - 1):
        master.solver.add(master.values[0][good] >= master.values[0][good + 1])
    full_cell_encoding = add_no_full_hall_cell(master)

    guards = []
    partition_by_guard = {}
    for position, partition in enumerate(partitions):
        guard = z3.Bool(f"core_partition_{position}")
        master.add_partition_obstruction(partition, activation=guard)
        guards.append(guard)
        partition_by_guard[str(guard)] = partition

    master.solver.set(timeout=int(time_limit * 1000))
    if minimize_core:
        master.solver.set("core.minimize", True)
    started = time.time()
    status = master.solver.check(*guards)
    elapsed = time.time() - started
    extracted = ()
    if status == z3.unsat:
        extracted = tuple(
            partition_by_guard[str(guard)] for guard in master.solver.unsat_core()
        )

    formula = master.to_smt2().rstrip()
    if not formula.endswith("(check-sat)"):
        raise AssertionError("unexpected Z3 SMT2 trailer")
    formula = formula[: -len("(check-sat)")]
    formula += "(check-sat-assuming (" + " ".join(map(str, guards)) + "))\n"
    smt2.parent.mkdir(parents=True, exist_ok=True)
    smt2.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": (
            "ASSUMPTION_CORE_EXTRACTED"
            if extracted
            else "MASTER_UNKNOWN"
            if status == z3.unknown
            else str(status)
        ),
        "solver_status": str(status),
        "reason_unknown": (
            master.solver.reason_unknown() if status == z3.unknown else None
        ),
        "solver": "Z3",
        "solver_version": z3.get_version_string(),
        "cap": cap,
        "source": str(source),
        "source_sha256": sha256(source),
        "pool_size": len(partitions),
        "core_size": len(extracted),
        "core_partitions": [
            [list(bundle) for bundle in partition] for partition in extracted
        ],
        "full_cell_encoding": full_cell_encoding,
        "universal_threshold_encoding": "sorting",
        "symmetry_breaking": [
            "nonincreasing favorite values by agent",
            "nonincreasing agent-0 values on goods 5..8",
        ],
        "elapsed_seconds": elapsed,
        "time_limit_seconds": time_limit,
        "core_minimization": minimize_core,
        "smt2_path": str(smt2),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "warning": "The returned Z3 assumption core is sufficient, not minimal.",
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    parser.add_argument("--minimize-core", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.smt2,
        args.source,
        args.cap,
        args.time_limit,
        args.minimize_core,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
