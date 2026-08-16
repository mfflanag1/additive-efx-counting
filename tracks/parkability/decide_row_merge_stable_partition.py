#!/usr/bin/env python3
"""Decide whether row-merge endpoints can have disjoint EFX partitions."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import z3

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_row_merge_interpolation import path_audit
    from .audit_row_merge_single_wall_radius import graph, matching_count
    from .core import iter_unlabeled_nonempty_partitions
    from .decide_row_merge_single_wall_radius import (
        N,
        as_fraction,
        edge_matrix,
        has_matching_expression,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_row_merge_interpolation import path_audit
    from audit_row_merge_single_wall_radius import graph, matching_count
    from core import iter_unlabeled_nonempty_partitions
    from decide_row_merge_single_wall_radius import (
        N,
        as_fraction,
        edge_matrix,
        has_matching_expression,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "row-merge-stable-partition-lra-v1"


def primitive_values(model, rows):
    values = []
    for row in rows:
        fractions = tuple(as_fraction(model, value) for value in row)
        denominator = math.lcm(*(value.denominator for value in fractions))
        integers = [int(value * denominator) for value in fractions]
        divisor = math.gcd(*integers)
        values.append(tuple(value // divisor for value in integers))
    return tuple(values)


def endpoint_partition_census(values, moving, base):
    merged = [list(row) for row in values]
    merged[moving] = list(merged[base])
    target_support = set()
    merged_support = set()
    target_allocations = 0
    merged_allocations = 0
    for partition in iter_unlabeled_nonempty_partitions(N, len(values[0])):
        target_count = matching_count(graph(values, partition))
        merged_count = matching_count(graph(merged, partition))
        if target_count:
            target_support.add(partition)
            target_allocations += target_count
        if merged_count:
            merged_support.add(partition)
            merged_allocations += merged_count
    return {
        "target_endpoint_partition_count": len(target_support),
        "merged_endpoint_partition_count": len(merged_support),
        "shared_endpoint_partition_count": len(target_support & merged_support),
        "target_endpoint_allocation_count": target_allocations,
        "merged_endpoint_allocation_count": merged_allocations,
    }


def run(result_path, smt2_path, m, moving, base, time_limit):
    if result_path.exists() or smt2_path.exists():
        raise ValueError("result and SMT2 paths must be new")
    if m < N or moving == base or not 0 <= moving < N or not 0 <= base < N:
        raise ValueError("m >= 4 and distinct valid moving/base agents required")
    partitions = tuple(iter_unlabeled_nonempty_partitions(N, m))
    master = ParkabilityLRAMaster(N, m)
    solver = master.solver
    target_rows = master.values
    merged_rows = tuple(
        target_rows[base] if agent == moving else target_rows[agent]
        for agent in range(N)
    )
    target_support = []
    merged_support = []
    for index, partition in enumerate(partitions):
        target_edges = edge_matrix(
            solver, target_rows, partition, f"target_partition_{index}"
        )
        merged_edges = edge_matrix(
            solver, merged_rows, partition, f"merged_partition_{index}"
        )
        target_has = z3.Bool(f"target_partition_{index}_supports")
        merged_has = z3.Bool(f"merged_partition_{index}_supports")
        solver.add(target_has == has_matching_expression(target_edges))
        solver.add(merged_has == has_matching_expression(merged_edges))
        solver.add(z3.Not(z3.And(target_has, merged_has)))
        target_support.append(target_has)
        merged_support.append(merged_has)
    solver.add(z3.Or(*target_support))
    solver.add(z3.Or(*merged_support))
    smt2_path.write_text(solver.to_smt2())
    formula_sha256 = hashlib.sha256(smt2_path.read_bytes()).hexdigest()

    solver.set(timeout=int(time_limit * 1000))
    started = time.time()
    status = solver.check()
    elapsed = time.time() - started
    reason_unknown = solver.reason_unknown() if status == z3.unknown else None
    values = None
    census = None
    interpolation = None
    if status == z3.sat:
        values = primitive_values(solver.model(), target_rows)
        census = endpoint_partition_census(values, moving, base)
        if (
            census["shared_endpoint_partition_count"] != 0
            or census["target_endpoint_allocation_count"]
            != independent.count_complete_efx0(values)
        ):
            raise AssertionError("the exact endpoint census rejected the model")
        interpolation = path_audit(values, moving, base)
        if interpolation["stable_partition"] is not None:
            raise AssertionError("the model unexpectedly has a stable partition")

    result = {
        "schema": SCHEMA,
        "status": (
            "NO_STABLE_PARTITION_FOUND"
            if status == z3.sat
            else "UNSAT_CANDIDATE"
            if status == z3.unsat
            else "UNKNOWN"
        ),
        "claim_boundary": (
            "A SAT result refutes fixed-partition row-merge coverage, not EFX "
            "existence or row-merge continuation with changing partitions. "
            "An UNSAT result applies only to the recorded item count."
        ),
        "n": N,
        "m": m,
        "moving_agent": moving,
        "base_agent": base,
        "partition_count": len(partitions),
        "time_limit_seconds": time_limit,
        "elapsed_seconds": elapsed,
        "solver_status": str(status),
        "reason_unknown": reason_unknown,
        "smt2_path": str(smt2_path),
        "smt2_sha256": formula_sha256,
        "values": [list(row) for row in values] if values is not None else None,
        "endpoint_census": census,
        "interpolation_audit": interpolation,
    }
    atomic_json(result_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=7)
    parser.add_argument("--moving", type=int, default=3)
    parser.add_argument("--base", type=int, default=2)
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.result,
        args.smt2,
        args.m,
        args.moving,
        args.base,
        args.time_limit,
    )


if __name__ == "__main__":
    main()
