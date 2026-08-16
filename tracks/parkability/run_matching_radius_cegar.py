#!/usr/bin/env python3
"""Exact CEGAR for bounded-radius EFX-matching augmentation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .anneal_matching_radius import parse_partition, radius_ball
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .search_strict_rank_trap import decode_rows
except ImportError:
    import core
    from anneal import atomic_json
    from anneal_matching_radius import parse_partition, radius_ball
    from audit_matching_augmentation import feasible_graph, matching_rank
    from search_strict_rank_trap import decode_rows


def run(
    *,
    n: int,
    m: int,
    source: tuple[tuple[int, ...], ...],
    radius: int,
    seed_paths: list[Path],
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
    smt2_path: Path,
) -> dict:
    solver = z3.SolverFor("QF_LRA")
    values = [
        [z3.Real(f"value_{agent}_{good}") for good in range(m)]
        for agent in range(n)
    ]
    for row in values:
        solver.add(*(value > 0 for value in row))
        solver.add(z3.Sum(*row) == 1)

    edge_cache: dict[
        tuple[tuple[tuple[int, ...], ...], int, int],
        z3.BoolRef,
    ] = {}

    def bundle_sum(
        agent: int,
        bundle: tuple[int, ...],
    ) -> z3.ArithRef:
        return z3.Sum(*(values[agent][good] for good in bundle))

    def edge(
        partition: tuple[tuple[int, ...], ...],
        agent: int,
        own_bundle: int,
    ) -> z3.BoolRef:
        key = partition, agent, own_bundle
        if key in edge_cache:
            return edge_cache[key]
        own = bundle_sum(agent, partition[own_bundle])
        comparisons = [
            own >= bundle_sum(
                agent,
                tuple(good for good in bundle if good != removed),
            )
            for target, bundle in enumerate(partition)
            if target != own_bundle
            for removed in bundle
        ]
        result = z3.Bool(
            f"edge_{len(edge_cache)}_agent_{agent}_bundle_{own_bundle}"
        )
        solver.add(result == z3.And(*comparisons))
        edge_cache[key] = result
        return result

    def matching_terms(
        partition: tuple[tuple[int, ...], ...],
        size: int,
    ):
        for agents in itertools.combinations(range(n), size):
            for bundles in itertools.permutations(range(n), size):
                yield z3.And(*(
                    edge(partition, agent, bundle)
                    for agent, bundle in zip(agents, bundles)
                ))

    solver.add(z3.Or(*matching_terms(source, n - 1)))
    solver.add(*(z3.Not(term) for term in matching_terms(source, n)))

    distances = radius_ball(source, radius)
    ball = sorted(distances)
    pool: list[tuple[tuple[int, ...], ...]] = []
    pool_set = set()

    def add_obstruction(partition: tuple[tuple[int, ...], ...]) -> None:
        if partition in pool_set:
            return
        solver.add(*(z3.Not(term) for term in matching_terms(partition, n)))
        pool.append(partition)
        pool_set.add(partition)

    for seed_path in seed_paths:
        raw = json.loads(seed_path.read_text())
        for raw_partition in raw.get("pool_partitions", []):
            partition = tuple(
                tuple(bundle)
                for bundle in raw_partition
            )
            if partition not in distances:
                raise ValueError("seed pool contains a partition outside the ball")
            add_obstruction(partition)
        seed_candidates = []
        if raw.get("values") is not None:
            seed_candidates.append(raw["values"])
        seed_candidates.extend(
            record["values"]
            for record in raw.get("trace", [])
            if record.get("values") is not None
        )
        for candidate in seed_candidates:
            seed_values = core.validate_values(
                candidate,
                expected_n=n,
                expected_m=m,
                lower=1,
            )
            for partition in ball:
                if matching_rank(feasible_graph(seed_values, partition)) == n:
                    add_obstruction(partition)

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    result_values = None
    reason_unknown = None
    solver_status = None
    for iteration in range(1, max_iterations + 1):
        solver.set(timeout=int(time_limit_s * 1000))
        solve_started = time.time()
        checked = solver.check()
        solve_seconds = time.time() - solve_started
        solver_status = str(checked)
        if checked == z3.unsat:
            status = "UNSAT_CANDIDATE"
            break
        if checked == z3.unknown:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        decoded = decode_rows(solver.model(), values)
        source_rank = matching_rank(feasible_graph(decoded, source))
        if source_rank != n - 1:
            raise AssertionError("decoded model lost the source rank")
        survivors = [
            partition
            for partition in ball
            if matching_rank(feasible_graph(decoded, partition)) == n
        ]
        trace.append({
            "iteration": iteration,
            "solve_seconds": solve_seconds,
            "pool_size_before": len(pool),
            "survivor_count": len(survivors),
            "survivor_count_by_distance": {
                str(distance): sum(
                    distances[partition] == distance
                    for partition in survivors
                )
                for distance in range(radius + 1)
            },
            "values": [list(row) for row in decoded],
        })
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"survivors={len(survivors)} solve={solve_seconds:.3f}s",
            flush=True,
        )
        if not survivors:
            status = "COUNTEREXAMPLE"
            result_values = decoded
            break
        for partition in survivors[:add_per_iteration]:
            add_obstruction(partition)

    formula = solver.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    return {
        "schema": "efx-matching-radius-cegar-v1",
        "status": status,
        "n": n,
        "m": m,
        "source_partition": [list(bundle) for bundle in source],
        "source_target_rank": n - 1,
        "transfer_radius": radius,
        "ball_partition_count": len(ball),
        "iterations": iteration,
        "pool_size": len(pool),
        "pool_partitions": [
            [list(bundle) for bundle in partition]
            for partition in pool
        ],
        "edge_variable_count": len(edge_cache),
        "elapsed_seconds": time.time() - started,
        "solver_status": solver_status,
        "reason_unknown": reason_unknown,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "trace": trace,
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=8)
    parser.add_argument("--source", required=True)
    parser.add_argument("--radius", type=int, default=3)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--add", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    if (
        args.radius < 1
        or args.add < 1
        or args.max_iterations < 1
        or args.time_limit < 0
    ):
        parser.error("search limits must be positive")
    source = parse_partition(args.source, args.n, args.m)
    result = run(
        n=args.n,
        m=args.m,
        source=source,
        radius=args.radius,
        seed_paths=args.seed,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
        smt2_path=args.smt2,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
