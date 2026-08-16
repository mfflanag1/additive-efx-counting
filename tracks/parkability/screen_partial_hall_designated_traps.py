#!/usr/bin/env python3
"""Screen the 102 designated pair traps against a strengthened radius-five master."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_designated_pair_trap import (
        SELECTED_PARTITIONS,
        designated_bundle,
    )
    from .decide_partial_hall_radius_one import candidate_partitions, integerize
    from .decide_partial_hall_utilitarian_local import local_rivals
    from .run_partial_hall_utilitarian_local_cegar import improving_local_rivals
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_designated_pair_trap import (
        SELECTED_PARTITIONS,
        designated_bundle,
    )
    from decide_partial_hall_radius_one import candidate_partitions, integerize
    from decide_partial_hall_utilitarian_local import local_rivals
    from run_partial_hall_utilitarian_local_cegar import improving_local_rivals


def run(
    source: Path,
    output: Path,
    timeout_seconds: int,
    only_partition_index: int | None = None,
    only_pair: tuple[int, int] | None = None,
) -> dict:
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.from_file(str(source))
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    floater = 8
    moves = list(candidate_partitions(base, floater))
    templates = local_rivals(base, floater, 9, 5)
    values = [[z3.Real(f"v_{agent}_{good}") for good in range(9)] for agent in range(4)]
    cells = [
        (partition_index, pair)
        for partition_index in SELECTED_PARTITIONS
        for pair in itertools.combinations(range(4), 2)
        if (only_partition_index is None or partition_index == only_partition_index)
        and (only_pair is None or pair == only_pair)
    ]
    records = []
    counts = Counter()
    started = time.time()
    for partition_index, pair in cells:
        move = moves[partition_index]
        designated = designated_bundle(move)
        witness = z3.And(
                *(
                    z3.Bool(f"edge_{partition_index}_{agent}_{designated}")
                    for agent in pair
                ),
                *(
                    z3.Not(z3.Bool(f"edge_{partition_index}_{agent}_{bundle}"))
                    for agent in pair
                    for bundle in range(4)
                    if bundle != designated
                )
        )
        solver.push()
        solver.add(witness)
        verdict = solver.check()
        record = {
                "partition_index": partition_index,
                "floater_host": move["floater_host"],
                "moved_good": move["moved_good"],
                "move_source": move["move_source"],
                "move_destination": move["move_destination"],
                "designated_bundle": designated,
                "deficient_agents": list(pair),
                "solver_verdict": str(verdict),
        }
        if verdict == z3.sat:
            integer_values = integerize(solver.model(), values)
            _, improving = improving_local_rivals(integer_values, base, templates)
            record["values"] = integer_values
            record["improving_radius_five_rival_count"] = len(improving)
            record["best_improving_rival"] = improving[0] if improving else None
        elif verdict == z3.unknown:
            record["solver_reason_unknown"] = solver.reason_unknown()
        counts[str(verdict)] += 1
        records.append(record)
        solver.pop()
        print(
            f"trap={len(records)}/{len(cells)} partition={partition_index} pair={pair} "
            f"verdict={verdict}",
            flush=True,
        )
    artifact = {
        "schema": "partial-hall-designated-trap-screen-v1",
        "status": "SCREENED",
        "meaning": (
            "UNSAT cells are exact exclusions under the supplied strengthened "
            "master. SAT cells are candidates requiring new radius-five "
            "blockers; UNKNOWN cells are inconclusive."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "timeout_seconds_per_cell": timeout_seconds,
        "only_partition_index": only_partition_index,
        "only_pair": list(only_pair) if only_pair is not None else None,
        "cell_count": len(records),
        "verdict_counts": dict(counts),
        "elapsed_seconds": round(time.time() - started, 6),
        "records": records,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=5)
    parser.add_argument("--only-partition-index", type=int)
    parser.add_argument("--only-pair", type=int, nargs=2, metavar=("AGENT_A", "AGENT_B"))
    args = parser.parse_args()
    only_pair = tuple(args.only_pair) if args.only_pair is not None else None
    print(
        json.dumps(
            run(
                args.source,
                args.output,
                args.timeout_seconds,
                args.only_partition_index,
                only_pair,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
