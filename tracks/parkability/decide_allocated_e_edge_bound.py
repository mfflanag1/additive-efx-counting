#!/usr/bin/env python3
"""Direct edge-bound decision for the allocated-E captured-support cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .decide_fixed_u_rank_three_four_edge_complete_efx import allocations_with_at_most_edges
from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_fixed_u_full_packet_terminal_cegar import (
    OWNERS, SUPPORT_STATE, allocation_formula, fractions,
)


def run(output, form_index, edge_bound, timeout_seconds, random_seed):
    solver, value = build_master(form_index)
    count = 0
    for allocation in allocations_with_at_most_edges(edge_bound, SUPPORT_STATE):
        if any(not allocation[owner] for owner in OWNERS):
            continue
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
        count += 1
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    started = time.monotonic()
    checked = solver.check()
    result = {
        "schema": "allocated-e-direct-edge-bound-decision-v1",
        "status": str(checked),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "edge_bound": edge_bound,
        "allocation_count": count,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Direct exhaustive edge-bound decision in the repaired twelve-good "
            "cell with complete generalized self- and pair-PI exclusions. UNSAT "
            "is bounded only; SAT is an edge-bound selector counterprofile, not "
            "a full saturated countermodel."
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
    parser.add_argument("--edge-bound", type=int, choices=range(5), required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.edge_bound,
        args.timeout_seconds, args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "form_index": result["form_index"],
        "edge_bound": result["edge_bound"],
        "allocations": result["allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
