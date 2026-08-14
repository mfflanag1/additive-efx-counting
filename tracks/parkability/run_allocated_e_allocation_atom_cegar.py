#!/usr/bin/env python3
"""Exact all-allocation/generalized-PI CEGAR for the allocated-E R3 cell.

The master seeks a positive-rational profile satisfying the complete declared
R3 premises.  Two exact separation oracles are then applied to every model:

* every closed disjoint desired-core family is excluded (generalized PI); and
* every complete EFX allocation on at most four support-provenance edges is
  excluded.

Unlike the earlier selector runs, the allocation oracle scans the complete
93,480-member nonempty-owner menu.  Allocation formulae are introduced only
when they are genuine EFX witnesses for a master model, avoiding the large
eager conjunction that previously timed out.  SAT after both oracles are
empty is an exact bounded-atom counterprofile.  UNSAT is only a bounded-atom
theorem; neither outcome by itself settles the cap-free statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
)
from .find_generalized_pi_cycle import find_closed_core_families
from .flatten_allocated_e_cegar_resume import load_chain, witnesses
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_allocated_e_pi_payment_atom_cegar import CoreAtoms
from .run_fixed_u_full_packet_terminal_cegar import (
    OWNERS,
    SUPPORT_STATE,
    allocation_formula,
    fractions,
)
from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]


def canonical(allocation):
    return tuple((owner, tuple(sorted(allocation[owner]))) for owner in (*OWNERS, "charity"))


def serialize_values(values):
    return {
        owner: {good: str(amount) for good, amount in row.items()}
        for owner, row in values.items()
    }


def deserialize_values(payload):
    return {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload.items()
    }


def complete_menu():
    return tuple(
        allocation
        for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE)
        if all(allocation[owner] for owner in OWNERS)
    )


class AllocationAtoms:
    """Define each encountered complete-EFX allocation predicate once."""

    def __init__(self, solver, value):
        self.solver = solver
        self.value = value
        self.atoms = {}

    def forbid(self, allocation):
        key = canonical(allocation)
        atom = self.atoms.get(key)
        if atom is None:
            atom = z3.Bool(f"aec_efx_{len(self.atoms)}")
            self.solver.add(
                atom == allocation_formula(allocation, self.value, "complete_efx")
            )
            self.atoms[key] = atom
        return z3.Not(atom)


def _resume_records(resume):
    """Return prior generalized-PI witnesses and lazy allocation cuts."""
    pi = []
    allocation_cuts = []
    if resume is None:
        return pi, allocation_cuts, None
    chain = load_chain(resume)
    for _, payload in chain:
        for witness in witnesses(payload):
            pi.append(witness)
        for record in payload.get("iterations", []):
            allocation_cuts.extend(record.get("blocking_efx_allocations", []))
    record = {
        "source": str(resume.resolve().relative_to(ROOT)),
        "source_sha256": hashlib.sha256(resume.read_bytes()).hexdigest(),
        "recursive_chain_length": len(chain),
    }
    return pi, allocation_cuts, record


def run(output: Path, resume: Path | None, timeout_seconds: int,
        random_seed: int, maximum_iterations: int,
        maximum_families_per_round: int, maximum_allocations_per_round: int):
    solver, value = build_master(2)
    core_atoms = CoreAtoms(solver, value)
    allocation_atoms = AllocationAtoms(solver, value)
    signatures = set()
    allocation_keys = set()

    prior_pi, prior_allocations, resume_record = _resume_records(resume)
    for witness in prior_pi:
        signature = cycle_signature(witness)
        if signature not in signatures:
            signatures.add(signature)
            solver.add(core_atoms.cut(signature))
    for allocation in prior_allocations:
        key = canonical(allocation)
        if key not in allocation_keys:
            allocation_keys.add(key)
            solver.add(allocation_atoms.forbid(allocation))
    if resume_record is not None:
        resume_record["loaded_distinct_pi_cut_count"] = len(signatures)
        resume_record["loaded_distinct_allocation_cut_count"] = len(allocation_keys)

    menu = complete_menu()
    if len(menu) != 93_480:
        raise AssertionError(f"unexpected complete menu size: {len(menu)}")

    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    result = {
        "schema": "allocated-e-all-allocation-atom-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "form_index": 2,
        "base": {owner: list(goods) for owner, goods in ALLOCATED_E_BASE.items()},
        "support": {owner: list(goods) for owner, goods in SUPPORT_STATE.items()},
        "allocation_menu_count": len(menu),
        "edge_bound": 4,
        "edge_origin": "support",
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "maximum_families_per_round": maximum_families_per_round,
        "maximum_allocations_per_round": maximum_allocations_per_round,
        "resume": resume_record,
        "iterations": [],
        "source": str(Path(__file__).resolve().relative_to(ROOT)),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact two-oracle CEGAR over every nonempty-owner complete allocation "
            "with at most four support-provenance edges in the declared twelve-atom "
            "allocated-E R3 cell, plus complete generalized-PI separation. Terminal "
            "SAT is a bounded-atom counterprofile, not automatically a reachable "
            "saturated fixed-U state. UNSAT is a bounded-atom theorem, not a "
            "cap-free theorem."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["distinct_core_atom_count"] = len(core_atoms.atoms)
        result["allocation_cut_count"] = len(allocation_keys)
        result["distinct_allocation_atom_count"] = len(allocation_atoms.atoms)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        status = solver.check()
        record = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PI_OR_FOUR_EDGE_COMPLETE_EFX"
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
            exact_values, ALLOCATED_E_BASE,
            maximum=maximum_families_per_round,
        )
        record["minimal_common_safe_desired_counts"] = {
            owner: len(rows) for owner, rows in minimal.items()
        }
        fresh_pi = []
        for witness in found:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            fresh_pi.append(witness)
            solver.add(core_atoms.cut(signature))
        if fresh_pi:
            record["separation"] = "generalized_pi"
            record["pi_cycle_count"] = len(found)
            record["fresh_cut_count"] = len(fresh_pi)
            record["pi_witnesses"] = fresh_pi
            result["iterations"].append(record)
            checkpoint()
            continue

        efx_witnesses = [
            allocation for allocation in menu
            if complete_efx(exact_values, allocation)
        ]
        record["complete_efx_witness_count"] = len(efx_witnesses)
        if not efx_witnesses:
            result["status"] = "SAT_PI_FREE_NO_FOUR_EDGE_COMPLETE_EFX"
            result["values"] = serialize_values(exact_values)
            result["iterations"].append(record)
            checkpoint()
            break

        fresh_allocations = []
        for allocation in efx_witnesses:
            key = canonical(allocation)
            if key in allocation_keys:
                continue
            allocation_keys.add(key)
            fresh_allocations.append(allocation)
            solver.add(allocation_atoms.forbid(allocation))
            if len(fresh_allocations) >= maximum_allocations_per_round:
                break
        if not fresh_allocations:
            raise AssertionError("exact EFX oracle returned no fresh allocation")
        record["separation"] = "complete_efx"
        record["fresh_cut_count"] = len(fresh_allocations)
        record["blocking_efx_allocations"] = fresh_allocations
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
    parser.add_argument("--maximum-allocations-per-round", type=int, default=500)
    args = parser.parse_args()
    result = run(
        args.output, args.resume, args.timeout_seconds, args.random_seed,
        args.maximum_iterations, args.maximum_families_per_round,
        args.maximum_allocations_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
        "pi_cuts": result["generalized_pi_cut_count"],
        "allocation_cuts": result["allocation_cut_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
