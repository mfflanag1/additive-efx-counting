#!/usr/bin/env python3
"""Extract an assumption core for the distinct-half owner-floor theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import (
        FAVORITE,
        N,
        add_branch_constraints,
        favorite_pair_balanced_universe,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import (
        FAVORITE,
        N,
        add_branch_constraints,
        favorite_pair_balanced_universe,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "distinct-half-floor-assumption-core-v1"


def add_guarded_obstruction(master, state, activation) -> None:
    for matching in itertools.permutations(range(N)):
        master.solver.add(
            z3.Implies(
                activation,
                z3.Or(
                    *(
                        master._sum(observer, state[matching[observer]])
                        < master.values[observer][FAVORITE]
                        for observer in range(N)
                    )
                ),
            )
        )


def run(output_path: Path, timeout_s: float, minimize_core: bool) -> dict:
    universe = favorite_pair_balanced_universe()
    master = ParkabilityLRAMaster(N, 9)
    add_branch_constraints(master)
    activations = tuple(
        z3.Bool(f"floor_partition_{index}")
        for index in range(len(universe))
    )
    for state, activation in zip(universe, activations):
        add_guarded_obstruction(master, state, activation)
    master.solver.set(timeout=int(timeout_s * 1000))
    if minimize_core:
        master.solver.set("smt.core.minimize", True)
    started = time.time()
    status = master.solver.check(*activations)
    elapsed = time.time() - started
    if status != z3.unsat:
        result = {
            "schema": SCHEMA,
            "status": str(status).upper(),
            "reason_unknown": master.solver.reason_unknown(),
            "universe_size": len(universe),
            "elapsed_seconds": elapsed,
        }
        atomic_json(output_path, result)
        return result
    core = set(master.solver.unsat_core())
    selected = tuple(
        state
        for state, activation in zip(universe, activations)
        if activation in core
    )
    result = {
        "schema": SCHEMA,
        "status": "UNSAT_CORE",
        "universe_size": len(universe),
        "core_size": len(selected),
        "elapsed_seconds": elapsed,
        "core_minimization": minimize_core,
        "partitions": [
            [list(bundle) for bundle in partition]
            for partition in selected
        ],
        "partition_sha256": hashlib.sha256(
            json.dumps(
                [
                    [list(bundle) for bundle in partition]
                    for partition in selected
                ],
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest(),
        "interpretation": (
            "The selected favorite-pair balanced partitions suffice for "
            "the matching-clause QF_LRA owner-floor contradiction. The "
            "assumption core is not guaranteed inclusion-minimal."
        ),
    }
    atomic_json(output_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--minimize-core", action="store_true")
    args = parser.parse_args()
    result = run(args.output, args.timeout, args.minimize_core)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
