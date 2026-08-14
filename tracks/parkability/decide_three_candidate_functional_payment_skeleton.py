#!/usr/bin/env python3
"""Decide the three-candidate functional payment skeleton in R2/R3."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .decide_two_survivor_named_topology_family import (
    allocations_supported_by, canonical, serialize_values,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, total, fractions
from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master


TOPOLOGIES = {
    0: (
        (("charity", "q"), ("q", "r"), ("r", "d")),
        (("charity", "r"), ("r", "q"), ("q", "d")),
        (("charity", "d"), ("q", "r"), ("r", "q")),
    ),
    2: (
        (("charity", "s"), ("s", "q"), ("q", "r"), ("r", "d")),
        (("charity", "r"), ("r", "s"), ("s", "q"), ("q", "d")),
        (("charity", "d"), ("q", "r"), ("s", "q"), ("r", "s")),
    ),
}


def paid_formula(allocation, value):
    return z3.And(*(
        total(value, owner, allocation[owner]) >= 1 for owner in OWNERS
    ))


def run(output, form_index, timeout_seconds, random_seed):
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    seen = set()
    counts = []
    started = time.monotonic()
    for topology in TOPOLOGIES[form_index]:
        before = len(seen)
        for allocation in allocations_supported_by(topology):
            key = canonical(allocation)
            if key in seen:
                continue
            seen.add(key)
            solver.add(z3.Not(paid_formula(allocation, value)))
        counts.append(len(seen) - before)
    build_seconds = time.monotonic() - started
    status = solver.check()
    result = {
        "schema": "three-candidate-functional-payment-skeleton-decision-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": "R2_TWO_CYCLE" if form_index == 0 else "R3_THREE_CYCLE",
        "topologies": [[list(edge) for edge in t] for t in TOPOLOGIES[form_index]],
        "new_allocation_counts_by_topology": counts,
        "distinct_allocation_count": len(seen),
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "build_seconds": build_seconds,
        "solve_seconds": time.monotonic() - started - build_seconds,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "direct payment-only decision for three functional topologies in one "
            "corrected exact-response twelve-atom cell. UNSAT is a bounded payment "
            "theorem, not EFX and not cap-free. SAT refutes only this payment menu."
        ),
    }
    if status == z3.sat:
        result["values"] = serialize_values(fractions(solver.model(), value))
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.timeout_seconds, args.random_seed)
    print(json.dumps({key: result[key] for key in (
        "status", "form_name", "distinct_allocation_count",
        "build_seconds", "solve_seconds",
    )}, indent=2))


if __name__ == "__main__":
    main()
