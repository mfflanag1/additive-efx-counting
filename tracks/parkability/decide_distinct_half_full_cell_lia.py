#!/usr/bin/env python3
"""Independent QF_LIA replay of a bounded full-Hall-cell CEGAR core."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_hall_layers import add_branch
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        full_hall_cells,
    )
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_hall_layers import add_branch
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        full_hall_cells,
    )
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-lia-replay-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reconstruct_pool(source_path, universe):
    payload = json.loads(source_path.read_text())
    if payload.get("schema") != "distinct-half-full-cell-cpsat-cegar-v1":
        raise ValueError("expected a full-cell CP-SAT CEGAR source")
    seed_supported = set()
    for source in payload["seed_sources"]:
        path = Path(source["path"])
        if sha256(path) != source["sha256"]:
            raise AssertionError("seed source hash changed")
        seed_supported.update(
            supported_partitions(load_values(path), list(universe))
        )
    pool = (
        set(seed_supported)
        if payload["seed_mode"] == "union"
        else set(universe).difference(seed_supported)
    )
    trace_counts = []
    for record in payload["trace"]:
        values = core.validate_values(
            record["values"], expected_n=N, expected_m=M, lower=1
        )
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError("source trace has a full Hall cell")
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        if (
            record["pool_size_before"] != len(pool)
            or record["favorite_pair_efx_survivors"] != len(survivors)
        ):
            raise AssertionError("source trace replay changed")
        trace_counts.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])
    if len(pool) != payload["pool_size"]:
        raise AssertionError("source pool size changed")
    return payload, pool, trace_counts


def run(result_path, smt2_path, source_path, core_path, cap, time_limit):
    universe = tuple(favorite_pair_balanced_universe())
    source, pool, trace_counts = reconstruct_pool(source_path, universe)
    if source["cap"] != cap:
        raise ValueError("source cap does not match requested cap")
    core_source = None
    if core_path is not None:
        core_payload = json.loads(core_path.read_text())
        if (
            core_payload.get("schema")
            != "distinct-half-full-cell-cpsat-assumption-core-v1"
            or core_payload.get("cap") != cap
            or core_payload.get("solver_status") != "INFEASIBLE"
        ):
            raise ValueError("invalid CP-SAT core source")
        pool = {
            tuple(tuple(bundle) for bundle in partition)
            for partition in core_payload["core_partitions"]
        }
        core_source = {
            "path": str(core_path),
            "sha256": sha256(core_path),
        }

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
    for partition in universe:
        if partition in pool:
            master.add_partition_obstruction(partition)

    started = time.time()
    solved = master.solve(time_limit_s=time_limit)
    formula = master.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    values = solved.values
    if values is not None:
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError("decoded model violates no-full-cell formula")
        if supported_partitions(values, list(pool)):
            raise AssertionError("decoded model violates a pooled obstruction")
    result = {
        "schema": SCHEMA,
        "status": (
            "FINITE_CAP_UNSAT_CANDIDATE"
            if solved.status == "UNSAT"
            else "SAT_RELAXATION"
            if solved.status == "SAT"
            else "MASTER_UNKNOWN"
        ),
        "solver_status": solved.raw_status,
        "reason_unknown": solved.reason_unknown,
        "cap": cap,
        "n": N,
        "m": M,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "source_trace_survivor_counts": trace_counts,
        "core_source": core_source,
        "pool_size": len(pool),
        "favorite_pair_partition_count": len(universe),
        "full_hall_cell_forbidden": True,
        "full_cell_encoding": full_cell_encoding,
        "universal_threshold_encoding": "sorting",
        "symmetry_breaking": [
            "nonincreasing favorite values by agent",
            "nonincreasing agent-0 values on goods 5..8",
        ],
        "elapsed_seconds": time.time() - started,
        "time_limit_seconds": time_limit,
        "values": [list(row) for row in values] if values is not None else None,
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "interpretation": (
            "UNSAT independently corroborates only the finite integer cap "
            "and pooled full-cell dichotomy. It is not a real-valued or "
            "general additive-EFX theorem."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--core", type=Path)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=600)
    args = parser.parse_args()
    if args.cap < 2 or args.time_limit <= 0:
        parser.error("invalid replay parameters")
    result = run(
        args.result,
        args.smt2,
        args.source,
        args.core,
        args.cap,
        args.time_limit,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
