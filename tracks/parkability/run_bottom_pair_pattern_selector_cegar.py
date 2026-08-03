#!/usr/bin/env python3
"""Exact CEGAR for the 20 bottom-pair multiplicity patterns."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        favorite_pair_universe,
        full_hall_cells,
    )
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from decide_two_pair_bottom_cross_conversion import add_bottom_orders
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_full_cell_cegar import (
        add_no_full_hall_cell,
        favorite_pair_universe,
        full_hall_cells,
    )
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import (
        add_universal_threshold_failure_cardinal,
        audit_threshold_failure,
    )


SCHEMA = "bottom-pair-pattern-selector-cegar-v1"
N = 4
M = 9
FAVORITE = 0

# Canonical loopless multigraphs with four edges, edge multiplicity at most
# two, and no isolated vertices. Vertex labels are shifted by one when used
# as residual-good labels.
CANONICAL_PATTERNS = (
    ((0, 1), (0, 1), (0, 2), (0, 2)),
    ((0, 1), (0, 1), (0, 2), (0, 3)),
    ((0, 1), (0, 1), (0, 2), (1, 2)),
    ((0, 1), (0, 1), (0, 2), (1, 3)),
    ((0, 1), (0, 1), (0, 2), (2, 3)),
    ((0, 1), (0, 1), (0, 2), (3, 4)),
    ((0, 1), (0, 1), (2, 3), (2, 3)),
    ((0, 1), (0, 1), (2, 3), (2, 4)),
    ((0, 1), (0, 1), (2, 3), (4, 5)),
    ((0, 1), (0, 2), (0, 3), (0, 4)),
    ((0, 1), (0, 2), (0, 3), (1, 2)),
    ((0, 1), (0, 2), (0, 3), (1, 4)),
    ((0, 1), (0, 2), (0, 3), (4, 5)),
    ((0, 1), (0, 2), (1, 2), (3, 4)),
    ((0, 1), (0, 2), (1, 3), (2, 3)),
    ((0, 1), (0, 2), (1, 3), (2, 4)),
    ((0, 1), (0, 2), (1, 3), (4, 5)),
    ((0, 1), (0, 2), (3, 4), (3, 5)),
    ((0, 1), (0, 2), (3, 4), (5, 6)),
    ((0, 1), (2, 3), (4, 5), (6, 7)),
)


def goods_pattern(index: int):
    if index not in range(len(CANONICAL_PATTERNS)):
        raise ValueError("bottom-pair pattern index is out of range")
    return tuple(
        tuple(vertex + 1 for vertex in edge)
        for edge in CANONICAL_PATTERNS[index]
    )


def multiplicity_signature(pattern):
    counts = {}
    for edge in pattern:
        counts[edge] = counts.get(edge, 0) + 1
    return tuple(sorted(counts.values(), reverse=True))


def select_obstructions(survivors, limit, selection):
    count = min(limit, len(survivors))
    if selection == "first":
        return survivors[:count]
    if selection == "spread":
        if count == 1:
            return survivors[:1]
        return tuple(
            survivors[index * (len(survivors) - 1) // (count - 1)]
            for index in range(count)
        )
    raise ValueError("unknown obstruction selection")


def run(
    result_path: Path,
    formula_path: Path,
    pattern_index: int,
    time_limit: float,
    max_iterations: int,
    add_per_iteration: int,
    seed_paths: tuple[Path, ...],
    obstruction_encoding: str = "matching_clauses",
    obstruction_selection: str = "first",
):
    pattern = goods_pattern(pattern_index)
    selected_pairs = tuple(dict.fromkeys(pattern))
    universe = tuple(favorite_pair_universe("all"))

    master = ParkabilityLRAMaster(N, M)
    master.add_strict_favorite_pattern((FAVORITE,) * N)
    add_universal_threshold_failure_cardinal(master)
    for agent, lows in enumerate(pattern):
        add_bottom_orders(master, lows, (agent,))
    selected_cell_encoding = add_no_full_hall_cell(
        master, low_pairs=selected_pairs
    )

    pool = set()
    seed_sources = []
    for seed_path in seed_paths:
        payload = json.loads(seed_path.read_text())
        raw_values = payload.get("values")
        if raw_values is None and payload.get("trace"):
            raw_values = payload["trace"][-1]["values"]
        values = core.validate_values(
            raw_values, expected_n=N, expected_m=M, lower=1
        )
        pool.update(supported_partitions(values, list(universe)))
        seed_sources.append(
            {
                "path": str(seed_path),
                "sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
            }
        )
    for partition in sorted(pool):
        master.add_partition_obstruction(
            partition, encoding=obstruction_encoding
        )
    seeded_pool_size = len(pool)

    trace = []
    status = "ITERATION_LIMIT"
    raw_status = None
    reason_unknown = None
    terminal_values = None
    started = time.time()
    iteration = 0
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit)
        raw_status = solved.raw_status
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break

        values = core.validate_values(
            solved.values, expected_n=N, expected_m=M, lower=1
        )
        audit_threshold_failure(values)
        for agent, lows in enumerate(pattern):
            residual = tuple(
                good for good in range(1, M) if good not in lows
            )
            if any(
                values[agent][low] > values[agent][good]
                for low in lows
                for good in residual
            ):
                raise AssertionError("model lost a selected bottom pair")
        all_full_cells = full_hall_cells(values)
        if any(list(lows) in all_full_cells for lows in selected_pairs):
            raise AssertionError("model gained a selected full Hall cell")

        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(pool),
                "favorite_pair_efx_survivors": len(survivors),
                "full_hall_cells": all_full_cells,
                "values": [list(row) for row in values],
            }
        )
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"survivors={len(survivors)} full_cells={len(all_full_cells)}",
            flush=True,
        )
        if not survivors:
            status = "SELECTED_BOTTOM_CELL_COUNTEREXAMPLE"
            terminal_values = values
            break
        for partition in select_obstructions(
            survivors, add_per_iteration, obstruction_selection
        ):
            master.add_partition_obstruction(
                partition, encoding=obstruction_encoding
            )
            pool.add(partition)

    formula = master.to_smt2()
    formula_path.parent.mkdir(parents=True, exist_ok=True)
    formula_path.write_text(formula)
    terminal_full_cells = (
        full_hall_cells(terminal_values)
        if terminal_values is not None
        else None
    )
    result = {
        "schema": SCHEMA,
        "status": status,
        "solver_status": raw_status,
        "reason_unknown": reason_unknown,
        "pattern_index": pattern_index,
        "pattern_count": len(CANONICAL_PATTERNS),
        "agent_bottom_pairs": [list(edge) for edge in pattern],
        "distinct_selected_bottom_pairs": [
            list(edge) for edge in selected_pairs
        ],
        "multiplicity_signature": list(multiplicity_signature(pattern)),
        "selected_cell_encoding": selected_cell_encoding,
        "favorite_pair_partition_count": len(universe),
        "obstruction_encoding": obstruction_encoding,
        "obstruction_selection": obstruction_selection,
        "seed_sources": seed_sources,
        "seeded_pool_size": seeded_pool_size,
        "pool_size": len(pool),
        "add_per_iteration": add_per_iteration,
        "max_iterations": max_iterations,
        "iterations": iteration,
        "time_limit_seconds_per_solve": time_limit,
        "elapsed_seconds": time.time() - started,
        "trace": trace,
        "values": (
            [list(row) for row in terminal_values]
            if terminal_values is not None
            else None
        ),
        "full_hall_cells": terminal_full_cells,
        "literal_complete_efx_count": (
            independent.count_complete_efx0(terminal_values)
            if terminal_values is not None
            else None
        ),
        "smt2_path": str(formula_path),
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
        "claim_boundary": (
            "UNSAT for all 20 patterns, followed by independent proof "
            "checking, would force a full Hall cell among the four selected "
            "bottom pairs whenever no pair is bottom-two for three agents. "
            "A SAT endpoint refutes only this selected-cell strengthening if "
            "another Hall cell or another EFX shape survives."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--pattern-index", type=int, required=True)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--add", type=int, default=64)
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument(
        "--encoding",
        choices=(
            "matching_clauses",
            "inline_matching_clauses",
            "hall_selectors",
        ),
        default="matching_clauses",
    )
    parser.add_argument(
        "--selection", choices=("first", "spread"), default="first"
    )
    args = parser.parse_args()
    if (
        args.time_limit <= 0
        or args.max_iterations < 1
        or args.add < 1
    ):
        parser.error("invalid search limits")
    result = run(
        args.result,
        args.formula,
        args.pattern_index,
        args.time_limit,
        args.max_iterations,
        args.add,
        tuple(args.seed),
        args.encoding,
        args.selection,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
