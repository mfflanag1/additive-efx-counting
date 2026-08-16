#!/usr/bin/env python3
"""Extract a deletion-irreducible core for the pair-deficiency gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import (
        candidate_partitions,
        eligible_constraints,
    )
    from .partial_hall_factored_master import (
        adjacency_constraints,
        hall_witnesses_by_size,
    )
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import (
        candidate_partitions,
        eligible_constraints,
    )
    from partial_hall_factored_master import (
        adjacency_constraints,
        hall_witnesses_by_size,
    )


def run(
    output: Path,
    smt2: Path,
    timeout_seconds: int,
    minimization_timeout_seconds: int,
) -> dict:
    n, m = 4, 9
    base = ((6, 7), (1, 2, 3), (0, 4), (5,))
    floater = 8
    values = [[z3.Real(f"v_{agent}_{good}") for good in range(m)] for agent in range(n)]
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    tracked = []

    def track(kind: str, expression, **record) -> None:
        label = z3.Bool(f"track_{len(tracked)}")
        solver.add(z3.Implies(label, expression))
        tracked.append((label, {"kind": kind, **record}))

    for agent, row in enumerate(values):
        track("row_normalization", z3.Sum(*row) == 1, agent=agent)
        track("row_nonnegativity", z3.And(*(entry >= 0 for entry in row)), agent=agent)
    for index, formula in enumerate(eligible_constraints(values, base, floater)):
        track("base_eligibility", formula, constraint_index=index, formula=str(formula))

    partitions = list(candidate_partitions(base, floater))
    for partition_index, move in enumerate(partitions):
        partition_edges = []
        for agent in range(n):
            agent_edges = []
            for bundle in range(n):
                edge = z3.Bool(f"edge_{partition_index}_{agent}_{bundle}")
                solver.add(
                    edge
                    == z3.And(
                        *adjacency_constraints(values[agent], move["partition"], bundle)
                    )
                )
                agent_edges.append(edge)
            partition_edges.append(tuple(agent_edges))
        groups = hall_witnesses_by_size(tuple(partition_edges))
        hall_failure = z3.Or(*(witness for group in groups[1:] for witness in group))
        no_pair_deficiency = z3.Not(z3.Or(*groups[1]))
        metadata = {
            "partition_index": partition_index,
            "floater_host": move["floater_host"],
            "moved_good": move["moved_good"],
            "move_source": move["move_source"],
            "move_destination": move["move_destination"],
            "partition": [list(bundle) for bundle in move["partition"]],
        }
        track("hall_failure", hall_failure, **metadata)
        track("no_pair_deficiency", no_pair_deficiency, **metadata)

    labels = [label for label, _ in tracked]
    verdict = solver.check(*labels)
    if verdict != z3.unsat:
        raise RuntimeError(f"expected UNSAT pair-deficiency gate, got {verdict}")
    core = list(solver.unsat_core())
    initial_core_size = len(core)
    print(f"initial_unsat_core_size={initial_core_size}", flush=True)
    solver.set(timeout=minimization_timeout_seconds * 1000)
    unknown_deletions = 0
    changed = True
    while changed:
        changed = False
        for label in tuple(core):
            trial = [item for item in core if item is not label]
            trial_verdict = solver.check(*trial)
            if trial_verdict == z3.unsat:
                core = trial
                changed = True
                print(f"core_size={len(core)}", flush=True)
            elif trial_verdict == z3.unknown:
                unknown_deletions += 1
    core_names = {str(label) for label in core}
    records = [record for label, record in tracked if str(label) in core_names]

    replay = z3.Solver()
    replay.add(*(solver.assertions()))
    replay.add(*core)
    if replay.check() != z3.unsat:
        raise RuntimeError("minimized core failed standalone replay")
    smt2.write_text(replay.to_smt2())
    artifact = {
        "schema": "partial-hall-pair-deficiency-core-v1",
        "status": "UNSAT",
        "meaning": (
            "The bounded-deletion tracked core proves that an eligible fixed-"
            "cell radius-one Hall obstruction cannot avoid a two-agent, one-"
            "neighbor deficient set in every candidate move. The core is "
            "deletion-irreducible only when every deletion query was decided."
        ),
        "candidate_partition_count": len(partitions),
        "tracked_constraint_count": len(tracked),
        "initial_unsat_core_size": initial_core_size,
        "unsat_core_size": len(records),
        "bounded_deletion_unsat_core": records,
        "deletion_irreducible": unknown_deletions == 0,
        "unknown_deletion_checks": unknown_deletions,
        "timeout_seconds": timeout_seconds,
        "minimization_timeout_seconds": minimization_timeout_seconds,
        "smt2": str(smt2),
        "smt2_sha256": hashlib.sha256(smt2.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--minimization-timeout-seconds", type=int, default=10)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.output,
                args.smt2,
                args.timeout_seconds,
                args.minimization_timeout_seconds,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
