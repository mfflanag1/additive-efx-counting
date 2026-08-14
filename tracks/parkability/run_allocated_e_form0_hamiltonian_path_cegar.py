#!/usr/bin/env python3
"""Decide the common form-0 Hamiltonian-path EFX selector.

The decision is exact only for the declared twelve-atom allocated-E master.
Generalized PI cycles are removed lazily by exact rational separation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula, fractions
from .run_generalized_pi_named_selector_cegar import cycle_signature, generalized_pi_cut


CURRENT = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("m", "gq", "gr"),
    "s": ("l", "e"),
    "charity": ("p",),
}

PATH = {
    "r": "q",
    "q": "d",
    "d": "s",
}


def hamiltonian_path_allocations():
    """All complete allocations using exactly c->r->q->d->s."""
    choices = []
    for supplier in ("r", "q", "d"):
        goods = CURRENT[supplier]
        recipient = PATH[supplier]
        supplier_choices = []
        for mask in range(1, 1 << len(goods)):
            moved = {good for bit, good in enumerate(goods) if mask & (1 << bit)}
            supplier_choices.append((supplier, recipient, moved))
        choices.append(supplier_choices)

    allocations = []
    for r_choice in choices[0]:
        for q_choice in choices[1]:
            for d_choice in choices[2]:
                selected = {row[0]: row for row in (r_choice, q_choice, d_choice)}
                allocation = {owner: [] for owner in ("r", "q", "d", "s")}
                allocation["r"].append("p")
                allocation["s"].extend(CURRENT["s"])
                for supplier in ("r", "q", "d"):
                    _, recipient, moved = selected[supplier]
                    for good in CURRENT[supplier]:
                        allocation[recipient if good in moved else supplier].append(good)
                allocation["charity"] = []
                allocations.append(allocation)
    assert len(allocations) == 7 ** 3
    return allocations


def run(output: Path, timeout_seconds: int, random_seed: int,
        maximum_iterations: int, maximum_families_per_round: int):
    solver, value = build_master(0)
    allocations = hamiltonian_path_allocations()
    for allocation in allocations:
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    signatures = set()
    result = {
        "schema": "allocated-e-form0-hamiltonian-path-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": 0,
        "path_edges": [
            ["charity", "r"], ["r", "q"], ["q", "d"], ["d", "s"]
        ],
        "allocation_count": len(allocations),
        "timeout_seconds_per_check": timeout_seconds,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "iterations": [],
        "claim_boundary": (
            "Exact twelve-atom allocated-E form-0 theorem only. UNSAT proves "
            "the path selector after all discovered generalized-PI families; "
            "SAT_NO_GENERALIZED_PI is a bounded counterprofile. Neither is a "
            "cap-free fixed-U theorem."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {"iteration": iteration, "solver_status": str(checked)}
        if checked == z3.unsat:
            result["status"] = "UNSAT"
            result["iterations"].append(record)
            checkpoint()
            break
        if checked == z3.unknown:
            result["status"] = "UNKNOWN"
            record["reason_unknown"] = solver.reason_unknown()
            result["iterations"].append(record)
            checkpoint()
            break

        values = fractions(solver.model(), value)
        witnesses, minimal = find_closed_core_families(
            values, ALLOCATED_E_BASE, maximum=maximum_families_per_round,
        )
        record["minimal_common_safe_desired_counts"] = {
            owner: len(rows) for owner, rows in minimal.items()
        }
        if not witnesses:
            result["status"] = "SAT_NO_GENERALIZED_PI"
            result["values"] = {
                owner: {good: str(amount) for good, amount in row.items()}
                for owner, row in values.items()
            }
            result["iterations"].append(record)
            checkpoint()
            break

        fresh = []
        for witness in witnesses:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            fresh.append(witness)
            solver.add(generalized_pi_cut(value, witness))
        if not fresh:
            raise AssertionError("generalized PI separator returned no fresh cut")
        record["pi_cycle_count"] = len(witnesses)
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
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    args = parser.parse_args()
    result = run(
        args.output, args.timeout_seconds, args.random_seed,
        args.maximum_iterations, args.maximum_families_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
