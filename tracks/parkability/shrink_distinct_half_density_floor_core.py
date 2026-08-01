#!/usr/bin/env python3
"""Extract a partition core for the coarse-density floor theorem."""

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
    from .decide_distinct_half_density_floor import add_density_branch
    from .decide_distinct_half_pair_cover import (
        FAVORITE,
        N,
        favorite_pair_balanced_universe,
    )
    from .lra_master import ParkabilityLRAMaster
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_density_floor import add_density_branch
    from decide_distinct_half_pair_cover import (
        FAVORITE,
        N,
        favorite_pair_balanced_universe,
    )
    from lra_master import ParkabilityLRAMaster


SCHEMA = "distinct-half-density-floor-assumption-core-v1"


def add_guarded_obstruction(master, state, activation):
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


def run(output_path, timeout_s, minimize_core, core_passes):
    universe = favorite_pair_balanced_universe()
    master = ParkabilityLRAMaster(N, 9)
    add_density_branch(
        master,
        require_three_halves=True,
        require_residual_total=False,
        require_tail_seven=True,
    )
    activations = tuple(
        z3.Bool(f"density_floor_partition_{index}")
        for index in range(len(universe))
    )
    for state, activation in zip(universe, activations):
        add_guarded_obstruction(master, state, activation)
    master.solver.set(timeout=int(timeout_s * 1000))
    if minimize_core:
        master.solver.set("smt.core.minimize", True)
    started = time.time()
    active = activations
    status = master.solver.check(*active)
    pass_sizes = []
    for _ in range(core_passes):
        if status != z3.unsat:
            break
        core = set(master.solver.unsat_core())
        active = tuple(activation for activation in active if activation in core)
        pass_sizes.append(len(active))
        status = master.solver.check(*active)
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
    raw_partitions = [
        [list(bundle) for bundle in partition]
        for partition in selected
    ]
    result = {
        "schema": SCHEMA,
        "status": "UNSAT_CORE",
        "universe_size": len(universe),
        "core_size": len(selected),
        "elapsed_seconds": elapsed,
        "core_minimization": minimize_core,
        "core_pass_sizes": pass_sizes,
        "partitions": raw_partitions,
        "partition_sha256": hashlib.sha256(
            json.dumps(
                raw_partitions,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest(),
        "assumptions": {
            "strict_common_favorite": 0,
            "fixed_half_favorite_representatives": [1, 2, 3, 4],
            "at_least_three_residual_goods_above_one_half": True,
            "ordered_x5_x6_x7_above_favorite": True,
        },
        "interpretation": (
            "The selected favorite-pair balanced partitions suffice for "
            "the coarse-density owner-floor contradiction. This remains "
            "a proof-mining core, not an analytic proof."
        ),
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--minimize-core", action="store_true")
    parser.add_argument("--core-passes", type=int, default=1)
    args = parser.parse_args()
    if args.core_passes < 1:
        parser.error("core passes must be positive")
    result = run(
        args.output,
        args.timeout,
        args.minimize_core,
        args.core_passes,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
