#!/usr/bin/env python3
"""Decide the dynamic three-edge capture topologies found after residual no-go."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .decide_two_survivor_named_topology_family import allocations_supported_by, canonical
from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula, fractions


TOPOLOGIES = (
    (("charity", "q"), ("d", "q"), ("q", "d")),
    (("charity", "q"), ("d", "s"), ("q", "d")),
    (("charity", "q"), ("d", "r"), ("q", "d")),
    (("charity", "q"), ("d", "r"), ("r", "d")),
    (("charity", "q"), ("q", "r"), ("r", "d")),
    (("charity", "d"), ("d", "r"), ("r", "d")),
    (("charity", "q"), ("q", "d"), ("q", "r")),
    (("charity", "d"), ("d", "q"), ("q", "d")),
)


def run(output, form_index, timeout_seconds, random_seed):
    solver, value = build_master(form_index)
    seen = set()
    counts = []
    for topology in TOPOLOGIES:
        before = len(seen)
        for allocation in allocations_supported_by(topology):
            key = canonical(allocation)
            if key in seen:
                continue
            seen.add(key)
            solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
        counts.append(len(seen) - before)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    started = time.monotonic()
    checked = solver.check()
    result = {
        "schema": "allocated-e-dynamic-capture-topology-decision-v1",
        "status": str(checked),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "topologies": [[list(edge) for edge in topology] for topology in TOPOLOGIES],
        "new_allocation_counts_by_topology": counts,
        "distinct_allocation_count": len(seen),
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact bounded decision for the eight dynamic three-edge capture "
            "topologies harvested from the hardened residual counterprofile, "
            "under complete self-/pair-PI exclusions."
        ),
    }
    if checked == z3.sat:
        values = fractions(solver.model(), value)
        result["values"] = {
            owner: {good: str(amount) for good, amount in row.items()}
            for owner, row in values.items()
        }
    elif checked == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "form_index": result["form_index"],
        "allocations": result["distinct_allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
