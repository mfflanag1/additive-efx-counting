#!/usr/bin/env python3
"""Search exact LRA for a strict local maximum of EFX-matching rank."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from math import gcd
from pathlib import Path

import z3

try:
    from . import core
    from .audit_matching_augmentation import (
        feasible_graph,
        matching_rank,
        transfer_neighbors,
    )
except ImportError:
    import core
    from audit_matching_augmentation import (
        feasible_graph,
        matching_rank,
        transfer_neighbors,
    )


def decode_rows(
    model: z3.ModelRef,
    variables: list[list[z3.ArithRef]],
) -> tuple[tuple[int, ...], ...]:
    rows = []
    for variable_row in variables:
        fractions = []
        for variable in variable_row:
            value = model.eval(variable, model_completion=True)
            fractions.append(
                Fraction(value.numerator_as_long(), value.denominator_as_long())
            )
        denominator = 1
        for value in fractions:
            denominator = (
                denominator * value.denominator
                // gcd(denominator, value.denominator)
            )
        row = [int(value * denominator) for value in fractions]
        divisor = 0
        for value in row:
            divisor = gcd(divisor, value)
        rows.append(tuple(value // divisor for value in row))
    return tuple(rows)


def parse_partition(raw: str, n: int, m: int) -> tuple[tuple[int, ...], ...]:
    bundles = tuple(
        tuple(int(good) for good in bundle.split(",") if good)
        for bundle in raw.split("/")
    )
    canonical = tuple(sorted(tuple(sorted(bundle)) for bundle in bundles))
    if (
        len(canonical) != n
        or any(not bundle for bundle in canonical)
        or sorted(good for bundle in canonical for good in bundle)
        != list(range(m))
    ):
        raise ValueError("partition must cover every good once in n nonempty bundles")
    return canonical


def run(
    n: int,
    m: int,
    source: tuple[tuple[int, ...], ...],
    radius: int,
    neighbor_max_rank: int,
    timeout_s: float,
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
        comparisons = []
        for target, bundle in enumerate(partition):
            if target == own_bundle:
                continue
            for removed in bundle:
                comparisons.append(
                    own
                    >= bundle_sum(
                        agent,
                        tuple(good for good in bundle if good != removed),
                    )
                )
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
    ball = set()
    frontier = {source}
    for _ in range(radius):
        frontier = {
            neighbor
            for partition in frontier
            for neighbor in transfer_neighbors(partition)
            if neighbor != source and neighbor not in ball
        }
        ball.update(frontier)
    neighbors = sorted(ball)
    for neighbor in neighbors:
        solver.add(*(
            z3.Not(term)
            for term in matching_terms(neighbor, neighbor_max_rank + 1)
        ))

    started = time.time()
    solver.set(timeout=int(timeout_s * 1000))
    status = solver.check()
    elapsed = time.time() - started
    formula = solver.to_smt2()
    base = {
        "schema": "efx-matching-strict-rank-trap-v1",
        "n": n,
        "m": m,
        "source_partition": [list(bundle) for bundle in source],
        "source_target_rank": n - 1,
        "neighbor_maximum_rank": neighbor_max_rank,
        "transfer_radius": radius,
        "neighbor_count": len(neighbors),
        "edge_variable_count": len(edge_cache),
        "elapsed_seconds": elapsed,
        "solver_status": str(status),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "smt2": formula,
    }
    if status == z3.sat:
        decoded = decode_rows(solver.model(), values)
        source_rank = matching_rank(feasible_graph(decoded, source))
        neighbor_ranks = {
            str([list(bundle) for bundle in neighbor]): matching_rank(
                feasible_graph(decoded, neighbor)
            )
            for neighbor in neighbors
        }
        if (
            source_rank != n - 1
            or max(neighbor_ranks.values(), default=0) > neighbor_max_rank
        ):
            raise AssertionError("decoded strict trap failed exact replay")
        return {
            **base,
            "status": "COUNTEREXAMPLE",
            "values": [list(row) for row in decoded],
            "source_rank": source_rank,
            "neighbor_rank_histogram": {
                str(rank): count
                for rank, count in sorted(
                    {
                        rank: list(neighbor_ranks.values()).count(rank)
                        for rank in set(neighbor_ranks.values())
                    }.items()
                )
            },
        }
    return {
        **base,
        "status": "UNSAT_CANDIDATE" if status == z3.unsat else "UNKNOWN",
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=8)
    parser.add_argument(
        "--partition",
        default="0,1/2,4/3/5,6,7",
        help="slash-separated bundles of comma-separated goods",
    )
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--neighbor-max-rank", type=int)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path)
    args = parser.parse_args()
    if args.radius < 1:
        parser.error("radius must be positive")
    neighbor_max_rank = (
        args.n - 2
        if args.neighbor_max_rank is None
        else args.neighbor_max_rank
    )
    if not 0 <= neighbor_max_rank < args.n:
        parser.error("neighbor maximum rank must lie in 0..n-1")
    source = parse_partition(args.partition, args.n, args.m)
    result = run(
        args.n,
        args.m,
        source,
        args.radius,
        neighbor_max_rank,
        args.timeout,
    )
    if args.smt2 is not None:
        args.smt2.parent.mkdir(parents=True, exist_ok=True)
        args.smt2.write_text(result.pop("smt2"))
        result["smt2_path"] = str(args.smt2.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
