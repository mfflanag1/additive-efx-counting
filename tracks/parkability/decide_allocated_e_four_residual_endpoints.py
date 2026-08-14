#!/usr/bin/env python3
"""Decide four simplest complete residual endpoints in the allocated-E cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_fixed_u_full_packet_terminal_cegar import (
    OWNERS, RECIPIENTS, allocation_formula, fractions,
)


ENDPOINTS = (
    {"r": ["a0", "a1", "h"], "q": ["j", "k", "q0"],
     "d": ["m", "gq", "gr", "p"], "s": ["l", "e"], "charity": []},
    {"r": ["a0", "a1"], "q": ["j", "k", "q0"],
     "d": ["m", "gq", "gr", "h", "p"], "s": ["l", "e"], "charity": []},
    {"r": ["a0", "a1"], "q": ["j", "k", "q0"],
     "d": ["m", "gq", "gr", "p"], "s": ["l", "e", "h"], "charity": []},
    {"r": ["a0", "a1"], "q": ["j", "k", "q0"],
     "d": ["m", "gq", "gr", "h"], "s": ["l", "e", "p"], "charity": []},
)


def run(output, form_index, timeout_seconds, random_seed):
    solver, value = build_master(form_index)
    for allocation in ENDPOINTS:
        assert set(allocation) == set(RECIPIENTS)
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    started = time.monotonic()
    checked = solver.check()
    result = {
        "schema": "allocated-e-four-residual-endpoint-decision-v1",
        "status": str(checked),
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "endpoints": ENDPOINTS,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": time.monotonic() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact decision for four residual placements in the bounded "
            "allocated-E cell with complete self- and pairwise generalized "
            "PI exclusions. UNSAT is bounded only; SAT refutes only this "
            "four-endpoint selector."
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
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "form_index": result["form_index"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
