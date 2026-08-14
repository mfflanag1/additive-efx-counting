#!/usr/bin/env python3
"""Extract a minimized assumption core for the two-hole endpoint theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .audit_allocated_e_all_allocation_unsat import collect
from .decide_allocated_e_seven_endpoint_paid_strengthening import (
    payment_hole_bounded_endpoint,
)
from .run_allocated_e_capture_rank_three_cegar import build_master, linear_base_response


ROOT = Path(__file__).resolve().parents[2]


def run(pi_source: Path, core_source: Path, output: Path,
        timeout_seconds: int, random_seed: int,
        required_paid_owners: tuple[str, ...] = ()):
    pi_source = pi_source.resolve()
    core_source = core_source.resolve()
    _, signature_map, _ = collect(pi_source)
    signatures = tuple(sorted(signature_map))
    core_payload = json.loads(core_source.read_text())
    allocations = tuple(core_payload["allocations"])

    solver, value = build_master(2)
    solver.set(
        timeout=timeout_seconds * 1000,
        random_seed=random_seed,
        **{"core.minimize": True},
    )
    assumptions = []
    metadata = {}
    for index, signature in enumerate(signatures):
        atom = z3.Bool(f"twohole_pi_{index}")
        clause = z3.Or(*(
            z3.Not(linear_base_response(value, source, tuple(pieces)))
            for source, pieces in signature
        ))
        solver.add(z3.Implies(atom, clause))
        assumptions.append(atom)
        metadata[atom.decl().name()] = ("pi", index)
    for index, allocation in enumerate(allocations):
        atom = z3.Bool(f"twohole_endpoint_{index}")
        solver.add(z3.Implies(
            atom,
            z3.Not(payment_hole_bounded_endpoint(
                value, allocation, 2, required_paid_owners,
            )),
        ))
        assumptions.append(atom)
        metadata[atom.decl().name()] = ("endpoint", index)

    started = time.monotonic()
    status = solver.check(*assumptions)
    if status != z3.unsat:
        raise RuntimeError(f"core source did not replay UNSAT: {status} {solver.reason_unknown()}")
    core = solver.unsat_core()
    pi_indices = []
    endpoint_indices = []
    for atom in core:
        kind, index = metadata[atom.decl().name()]
        (pi_indices if kind == "pi" else endpoint_indices).append(index)

    result = {
        "schema": "allocated-e-two-hole-unsat-core-v1",
        "status": "UNSAT_CORE_EXTRACTED",
        "solver": f"Z3 {z3.get_version_string()}",
        "pi_source": str(pi_source.relative_to(ROOT)),
        "pi_source_sha256": hashlib.sha256(pi_source.read_bytes()).hexdigest(),
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "input_pi_clause_count": len(signatures),
        "input_endpoint_count": len(allocations),
        "core_pi_clause_count": len(pi_indices),
        "core_endpoint_count": len(endpoint_indices),
        "required_paid_owners": list(required_paid_owners),
        "pi_signatures": [
            [[source, list(pieces)] for source, pieces in signatures[index]]
            for index in sorted(pi_indices)
        ],
        "endpoint_indices": [index + 1 for index in sorted(endpoint_indices)],
        "allocations": [allocations[index] for index in sorted(endpoint_indices)],
        "elapsed_seconds": time.monotonic() - started,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "core_minimize": True,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Solver-minimized assumption core for the exact twelve-atom "
            "two-payment-hole theorem; independent formula replay remains "
            "separate."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pi-source", type=Path, required=True)
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=999983)
    parser.add_argument("--required-paid-owners", nargs="*", default=())
    args = parser.parse_args()
    result = run(
        args.pi_source, args.core_source, args.output,
        args.timeout_seconds, args.random_seed,
        tuple(args.required_paid_owners),
    )
    print(json.dumps({
        "status": result["status"],
        "core_pi_clause_count": result["core_pi_clause_count"],
        "core_endpoint_count": result["core_endpoint_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
