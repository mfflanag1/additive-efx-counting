#!/usr/bin/env python3
"""Decide the four-topology functional cover in each exact response form.

The menu was mined as a minimum functional topology cover of all 25 profiles
in the frozen corrected exact-response CEGAR census.  This script tests the
menu universally over the corresponding twelve-atom necessary-premise cell,
with unrestricted packets along each allowed edge.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from .decide_two_survivor_named_topology_family import (
        allocations_supported_by, canonical, serialize_values,
    )
    from .run_fixed_u_full_packet_terminal_cegar import allocation_formula, fractions
    from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
except ImportError:
    from decide_two_survivor_named_topology_family import (
        allocations_supported_by, canonical, serialize_values,
    )
    from run_fixed_u_full_packet_terminal_cegar import allocation_formula, fractions
    from run_fixed_u_rank_three_relation_cegar import build_rank_three_master


FUNCTIONAL_COVER_TOPOLOGIES = (
    (("charity", "d"), ("d", "s"), ("q", "r"), ("r", "q")),
    (("charity", "q"), ("q", "d"), ("r", "s"), ("s", "r")),
    (("charity", "s"), ("d", "r"), ("q", "d"), ("r", "q")),
    (("charity", "s"), ("d", "r"), ("r", "d"), ("s", "q")),
)


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
    for topology in FUNCTIONAL_COVER_TOPOLOGIES:
        before = len(seen)
        for allocation in allocations_supported_by(topology):
            key = canonical(allocation)
            if key in seen:
                continue
            seen.add(key)
            solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
        counts.append(len(seen) - before)
    build_seconds = time.monotonic() - started
    status = solver.check()
    result = {
        "schema": "exact-response-functional-four-topology-cover-decision-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": "R2_TWO_CYCLE" if form_index == 0 else "R3_THREE_CYCLE",
        "topologies": [
            [list(edge) for edge in topology]
            for topology in FUNCTIONAL_COVER_TOPOLOGIES
        ],
        "new_allocation_counts_by_topology": counts,
        "distinct_allocation_count": len(seen),
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "build_seconds": build_seconds,
        "solve_seconds": time.monotonic() - started - build_seconds,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "universal decision for the empirically minimum four-topology "
            "functional cover in one corrected exact-response twelve-atom cell. "
            "SAT refutes this menu but not the unrestricted four-edge theorem; "
            "UNSAT proves only the bounded-atom menu theorem."
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
    print(json.dumps({
        key: result[key] for key in (
            "status", "form_name", "distinct_allocation_count",
            "build_seconds", "solve_seconds",
        )
    }, indent=2))


if __name__ == "__main__":
    main()
