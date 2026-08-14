#!/usr/bin/env python3
"""Generalized-PI CEGAR after negating the three paid matching families."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .decide_three_candidate_functional_payment_skeleton import TOPOLOGIES, paid_formula
from .decide_two_survivor_named_topology_family import allocations_supported_by, canonical
from .find_generalized_pi_cycle import find_closed_core_families
from .flatten_allocated_e_cegar_resume import load_chain, witnesses
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_fixed_u_full_packet_terminal_cegar import OWNERS, fractions
from .run_generalized_pi_named_selector_cegar import cycle_signature, generalized_pi_cut


ROOT = Path(__file__).resolve().parents[2]


def run(output: Path, form_index: int, resume: Path | None,
        timeout_seconds: int, random_seed: int, maximum_iterations: int,
        maximum_families_per_round: int):
    solver, value = build_master(form_index)
    allocations = {}
    for topology in TOPOLOGIES[form_index]:
        for allocation in allocations_supported_by(topology):
            allocations.setdefault(canonical(allocation), allocation)
    for allocation in allocations.values():
        solver.add(z3.Not(paid_formula(allocation, value)))

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
                solver.add(generalized_pi_cut(value, witness))
        resume_record = {
            "source": str(resume.resolve().relative_to(ROOT)),
            "source_sha256": hashlib.sha256(resume.read_bytes()).hexdigest(),
            "recursive_chain_length": len(chain),
            "loaded_distinct_cut_count": len(signatures),
        }
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "allocated-e-pi-payment-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": form_index,
        "form_name": "R2_TWO_CYCLE" if form_index == 0 else "R3_THREE_CYCLE",
        "base": {owner: list(goods) for owner, goods in ALLOCATED_E_BASE.items()},
        "paid_matching_allocation_count": len(allocations),
        "paid_matching_topologies": [
            [list(edge) for edge in topology] for topology in TOPOLOGIES[form_index]
        ],
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "resume": resume_record,
        "iterations": [],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact twelve-good decision for full generalized-PI-freeness "
            "together with failure of every allocation in the three canonical "
            "paid near-perfect matching topologies. UNSAT is a bounded payment/"
            "PI dichotomy, not a cap-free theorem or EFX result."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        status = solver.check()
        record = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PI_OR_PAID_MATCHING"
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
            result["status"] = "SAT_PI_FREE_NO_PAID_MATCHING"
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
            solver.add(generalized_pi_cut(value, witness))
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
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=20)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    args = parser.parse_args()
    result = run(
        args.output, args.form_index, args.resume, args.timeout_seconds,
        args.random_seed, args.maximum_iterations, args.maximum_families_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["paid_matching_allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
