#!/usr/bin/env python3
"""Exact generalized-PI CEGAR for seven-endpoint payment strengthenings."""

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
from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_allocated_e_pi_payment_atom_cegar import CoreAtoms
from .run_fixed_u_full_packet_terminal_cegar import fractions
from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]


def run(
    pi_source: Path,
    endpoint_source: Path,
    output: Path,
    maximum_payment_holes: int,
    required_paid_owners: tuple[str, ...],
    timeout_seconds: int,
    random_seed: int,
    maximum_iterations: int,
    maximum_families_per_round: int,
):
    pi_source = pi_source.resolve()
    endpoint_source = endpoint_source.resolve()
    _, collected, _ = collect(pi_source)
    endpoint_payload = json.loads(endpoint_source.read_text())
    allocations = tuple(endpoint_payload["allocations"])

    solver, value = build_master(2)
    atoms = CoreAtoms(solver, value)
    signatures = set()
    for signature in collected:
        signatures.add(signature)
        solver.add(atoms.cut(signature))
    for allocation in allocations:
        solver.add(z3.Not(payment_hole_bounded_endpoint(
            value,
            allocation,
            maximum_payment_holes,
            required_paid_owners,
        )))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    result = {
        "schema": "allocated-e-seven-endpoint-payment-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "pi_source": str(pi_source.relative_to(ROOT)),
        "pi_source_sha256": hashlib.sha256(pi_source.read_bytes()).hexdigest(),
        "endpoint_source": str(endpoint_source.relative_to(ROOT)),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "initial_pi_cut_count": len(signatures),
        "endpoint_count": len(allocations),
        "maximum_payment_holes": maximum_payment_holes,
        "required_paid_owners": list(required_paid_owners),
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "iterations": [],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact twelve-atom form-2 CEGAR. UNSAT proves the declared payment "
            "strengthening under full generalized-PI exclusion. A terminal SAT "
            "profile is a bounded countermodel to that strengthening only."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["distinct_core_atom_count"] = len(atoms.atoms)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        status = solver.check()
        row = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PI_OR_REQUIRED_ENDPOINT"
            result["iterations"].append(row)
            checkpoint()
            break
        if status == z3.unknown:
            row["reason_unknown"] = solver.reason_unknown()
            result["status"] = "UNKNOWN"
            result["iterations"].append(row)
            checkpoint()
            break

        exact_values = fractions(solver.model(), value)
        found, minimal = find_closed_core_families(
            exact_values,
            ALLOCATED_E_BASE,
            maximum=maximum_families_per_round,
        )
        row["minimal_common_safe_desired_counts"] = {
            owner: len(cores) for owner, cores in minimal.items()
        }
        if not found:
            result["status"] = "SAT_PI_FREE_NO_REQUIRED_ENDPOINT"
            result["values"] = {
                owner: {good: str(amount) for good, amount in values.items()}
                for owner, values in exact_values.items()
            }
            result["iterations"].append(row)
            checkpoint()
            break

        fresh = []
        for witness in found:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            solver.add(atoms.cut(signature))
            fresh.append(witness)
        if not fresh:
            raise AssertionError("PI oracle returned no fresh family")
        row["pi_cycle_count"] = len(found)
        row["fresh_cut_count"] = len(fresh)
        row["pi_witnesses"] = fresh
        result["iterations"].append(row)
        checkpoint()
    else:
        result["status"] = "ITERATION_LIMIT"
        checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pi-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-payment-holes", type=int, choices=range(5), required=True)
    parser.add_argument("--required-paid-owners", nargs="*", default=())
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=179424673)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--maximum-families-per-round", type=int, default=1000)
    args = parser.parse_args()
    result = run(
        args.pi_source,
        args.endpoint_source,
        args.output,
        args.maximum_payment_holes,
        tuple(args.required_paid_owners),
        args.timeout_seconds,
        args.random_seed,
        args.maximum_iterations,
        args.maximum_families_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
