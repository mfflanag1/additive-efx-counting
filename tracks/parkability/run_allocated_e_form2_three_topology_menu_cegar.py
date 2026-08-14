#!/usr/bin/env python3
"""Exact CEGAR for a three-topology form-2 completion menu."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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

# Smallest topology cover of the six existing adversarial PI-free profiles.
MENU = (
    (("charity", "r"), ("r", "d"), ("r", "s")),
    (("charity", "r"), ("q", "d"), ("r", "d"), ("r", "q")),
    (("charity", "q"), ("d", "q"), ("q", "d"), ("r", "s")),
)


def allocations_for_topology(topology):
    outgoing = {supplier: [] for supplier in CURRENT}
    charity_target = None
    for supplier, recipient in topology:
        if supplier == "charity":
            assert charity_target is None
            charity_target = recipient
        else:
            outgoing[supplier].append(recipient)
    assert charity_target is not None

    supplier_rows = []
    for supplier in ("r", "q", "d", "s"):
        recipients = outgoing[supplier]
        destinations = (supplier, *recipients)
        rows = []
        for assignment in itertools.product(destinations, repeat=len(CURRENT[supplier])):
            if any(recipient not in assignment for recipient in recipients):
                continue
            rows.append(dict(zip(CURRENT[supplier], assignment, strict=True)))
        supplier_rows.append(rows)

    allocations = []
    for selected in itertools.product(*supplier_rows):
        allocation = {owner: [] for owner in ("r", "q", "d", "s")}
        allocation[charity_target].append("p")
        for routing in selected:
            for good, owner in routing.items():
                allocation[owner].append(good)
        allocation["charity"] = []
        allocations.append(allocation)
    return allocations


def menu_allocations():
    rows = {}
    for topology in MENU:
        for allocation in allocations_for_topology(topology):
            key = tuple(
                (owner, tuple(sorted(goods)))
                for owner, goods in sorted(allocation.items())
            )
            rows.setdefault(key, allocation)
    return list(rows.values())


def run(output: Path, timeout_seconds: int, random_seed: int,
        maximum_iterations: int, maximum_families_per_round: int,
        resume: Path | None = None):
    solver, value = build_master(2)
    allocations = menu_allocations()
    for allocation in allocations:
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    signatures = set()
    resume_record = None
    if resume is not None:
        resume_payload = json.loads(resume.read_text())
        assert resume_payload["form_index"] == 2
        assert resume_payload["menu"] == [
            [list(edge) for edge in topology] for topology in MENU
        ]
        for iteration in resume_payload.get("iterations", ()):
            for witness in iteration.get("pi_witnesses", ()):
                signature = cycle_signature(witness)
                if signature in signatures:
                    continue
                signatures.add(signature)
                solver.add(generalized_pi_cut(value, witness))
        resume_record = {
            "source": str(resume),
            "source_sha256": hashlib.sha256(resume.read_bytes()).hexdigest(),
            "loaded_cut_count": len(signatures),
        }
    result = {
        "schema": "allocated-e-form2-three-topology-menu-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": 2,
        "menu": [[list(edge) for edge in topology] for topology in MENU],
        "topology_allocation_counts": [
            len(allocations_for_topology(topology)) for topology in MENU
        ],
        "allocation_count": len(allocations),
        "timeout_seconds_per_check": timeout_seconds,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "random_seed": random_seed,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "resume": resume_record,
        "iterations": [],
        "claim_boundary": (
            "Exact twelve-atom allocated-E form-2 decision for the declared "
            "three-topology menu. Any verdict is bounded-atom only."
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
    parser.add_argument("--maximum-iterations", type=int, default=40)
    parser.add_argument("--maximum-families-per-round", type=int, default=10000)
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    result = run(
        args.output, args.timeout_seconds, args.random_seed,
        args.maximum_iterations, args.maximum_families_per_round, args.resume,
    )
    print(json.dumps({
        "status": result["status"],
        "cuts": result["generalized_pi_cut_count"],
        "iterations": len(result["iterations"]),
        "allocations": result["allocation_count"],
        "topology_allocation_counts": result["topology_allocation_counts"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
