#!/usr/bin/env python3
"""Exact PI-free decision for the root/s/d three-edge fork family."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .run_allocated_e_selector_atom_cegar import run_selector, topology_allocations


TOPOLOGIES = (
    (("r", "d"), ("s", "d"), ("charity", "s")),
    (("r", "s"), ("s", "d"), ("charity", "d")),
    (("r", "s"), ("s", "d"), ("charity", "s")),
)


def selector_allocations():
    return topology_allocations(TOPOLOGIES)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=300)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    args = parser.parse_args()
    result = run_selector(
        output=args.output,
        topologies=TOPOLOGIES,
        resume=args.resume,
        timeout_seconds=args.timeout_seconds,
        random_seed=args.random_seed,
        maximum_iterations=args.maximum_iterations,
        maximum_families_per_round=args.maximum_families_per_round,
        schema="allocated-e-root-s-fork-cegar-v1",
        unsat_status="UNSAT_PI_OR_ROOT_S_FORK_EFX",
        sat_status="SAT_PI_FREE_NO_ROOT_S_FORK_EFX",
        claim_boundary=(
            "Exact twelve-good R3 decision for full generalized-PI-freeness "
            "versus complete EFX in the three root/s/d fork topologies seen "
            "across the preceding PI-free selector counterprofiles. UNSAT is "
            "bounded; SAT refutes only this fork family."
        ),
        source_path=Path(__file__),
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "core_atoms": result["distinct_core_atom_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["selector_allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
