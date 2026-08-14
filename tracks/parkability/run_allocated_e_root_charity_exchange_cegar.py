#!/usr/bin/env python3
"""Exact generalized-PI CEGAR for the two-edge root/charity exchange family."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .decide_two_survivor_named_topology_family import allocations_supported_by, canonical
from .find_generalized_pi_cycle import find_closed_core_families
from .flatten_allocated_e_cegar_resume import load_chain, witnesses
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_allocated_e_pi_payment_atom_cegar import CoreAtoms
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula, fractions
from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]
TOPOLOGIES = (
    (("r", "d"), ("charity", "r")),
    (("r", "d"), ("charity", "d")),
)


def selector_allocations():
    allocations = {}
    for topology in TOPOLOGIES:
        for allocation in allocations_supported_by(topology):
            allocations.setdefault(canonical(allocation), allocation)
    return allocations


def run(output: Path, resume: Path | None, timeout_seconds: int,
        random_seed: int, maximum_iterations: int,
        maximum_families_per_round: int):
    solver, value = build_master(2)
    allocations = selector_allocations()
    for allocation in allocations.values():
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))

    atoms = CoreAtoms(solver, value)
    signatures = set()
    resume_record = None
    if resume is not None:
        chain = load_chain(resume)
        for _, payload in chain:
            for witness in witnesses(payload):
                signature = cycle_signature(witness)
                if signature in signatures:
                    continue
                signatures.add(signature)
                solver.add(atoms.cut(signature))
        resume_record = {
            "source": str(resume.resolve().relative_to(ROOT)),
            "source_sha256": hashlib.sha256(resume.read_bytes()).hexdigest(),
            "recursive_chain_length": len(chain),
            "loaded_distinct_cut_count": len(signatures),
        }

    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "allocated-e-root-charity-exchange-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": 2,
        "base": {owner: list(goods) for owner, goods in ALLOCATED_E_BASE.items()},
        "topologies": [[list(edge) for edge in topology] for topology in TOPOLOGIES],
        "selector_allocation_count": len(allocations),
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "resume": resume_record,
        "iterations": [],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact twelve-good R3 decision for full generalized-PI-freeness "
            "versus complete EFX in either root-to-d plus charity-to-{r,d} "
            "two-edge family. UNSAT is bounded; SAT refutes only this selector."
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
        record = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PI_OR_ROOT_CHARITY_EFX"
            result["iterations"].append(record)
            checkpoint()
            break
        if status == z3.unknown:
            record["reason_unknown"] = solver.reason_unknown()
            result["status"] = "UNKNOWN"
            result["iterations"].append(record)
            checkpoint()
            break

        exact_values = fractions(solver.model(), value)
        found, minimal = find_closed_core_families(
            exact_values, ALLOCATED_E_BASE, maximum=maximum_families_per_round,
        )
        record["minimal_common_safe_desired_counts"] = {
            owner: len(rows) for owner, rows in minimal.items()
        }
        if not found:
            result["status"] = "SAT_PI_FREE_NO_ROOT_CHARITY_EFX"
            result["values"] = {
                owner: {good: str(amount) for good, amount in row.items()}
                for owner, row in exact_values.items()
            }
            result["iterations"].append(record)
            checkpoint()
            break

        fresh = []
        for witness in found:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            fresh.append(witness)
            solver.add(atoms.cut(signature))
        if not fresh:
            raise AssertionError("PI oracle returned no fresh family")
        record["pi_cycle_count"] = len(found)
        record["fresh_cut_count"] = len(fresh)
        record["pi_witnesses"] = fresh
        result["iterations"].append(record)
        checkpoint()
    else:
        result["status"] = "ITERATION_LIMIT"
        checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=200)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    args = parser.parse_args()
    result = run(
        args.output, args.resume, args.timeout_seconds, args.random_seed,
        args.maximum_iterations, args.maximum_families_per_round,
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
