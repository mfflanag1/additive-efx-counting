#!/usr/bin/env python3
"""CEGAR over every four-edge completion retaining the current root bundle."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

from .audit_allocated_e_all_allocation_unsat import collect
from .audit_allocated_e_paid_strengthening_counterprofile import complete_efx
from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_allocated_e_pi_payment_atom_cegar import CoreAtoms
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_fixed_u_full_packet_terminal_cegar import (
    GOODS, SUPPORT_STATE, allocation_formula, fractions, total,
)
from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]


def support_edges(allocation):
    supplier = {
        good: source
        for source, goods in SUPPORT_STATE.items()
        for good in goods
    }
    return frozenset(
        (supplier[good], owner)
        for owner in ("r", "q", "d", "s")
        for good in allocation[owner]
        if supplier[good] != owner
    )


def root_fixed_menu():
    root = tuple(SUPPORT_STATE["r"])
    remaining = tuple(good for good in GOODS if good not in root)
    menu = []
    for recipients in itertools.product(("q", "d", "s"), repeat=len(remaining)):
        allocation = {"r": list(root), "q": [], "d": [], "s": [], "charity": []}
        for good, owner in zip(remaining, recipients):
            allocation[owner].append(good)
        edges = support_edges(allocation)
        if len(edges) <= 4:
            menu.append((allocation, edges))
    return menu


def run(
    pi_source: Path,
    endpoint_source: Path,
    output: Path,
    timeout_seconds: int,
    random_seed: int,
    maximum_iterations: int,
    maximum_pi_families_per_round: int,
    maximum_allocations_per_round: int,
):
    pi_source = pi_source.resolve()
    endpoint_source = endpoint_source.resolve()
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    retained = RETAINED[6]
    menu = root_fixed_menu()
    _, collected, _ = collect(pi_source)

    solver, value = build_master(2)
    atoms = CoreAtoms(solver, value)
    signatures = set()
    for signature in collected:
        signatures.add(signature)
        solver.add(atoms.cut(signature))
    solver.add(
        allocation_formula(endpoint6, value, "complete_efx"),
        total(value, "q", endpoint6["q"]) >= 1,
        total(value, "s", endpoint6["s"]) >= 1,
        total(value, "q", retained["q"]) < 1,
    )
    allocation_signatures = set()
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    result = {
        "schema": "allocated-e-endpoint6-root-fixed-completion-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "pi_source": str(pi_source.relative_to(ROOT)),
        "pi_source_sha256": hashlib.sha256(pi_source.read_bytes()).hexdigest(),
        "endpoint_source": str(endpoint_source.relative_to(ROOT)),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "initial_pi_cut_count": len(signatures),
        "root_fixed_allocation_count": len(menu),
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "maximum_pi_families_per_round": maximum_pi_families_per_round,
        "maximum_allocations_per_round": maximum_allocations_per_round,
        "iterations": [],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact twelve-atom CEGAR over every complete allocation retaining "
            "the current root and using at most four support edges. It is not cap-free."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["generalized_pi_cut_count"] = len(signatures)
        result["allocation_cut_count"] = len(allocation_signatures)
        result["distinct_core_atom_count"] = len(atoms.atoms)
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        status = solver.check()
        row = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PI_OR_ROOT_FIXED_FOUR_EDGE_EFX"
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
        found_pi, minimal = find_closed_core_families(
            exact_values,
            ALLOCATED_E_BASE,
            maximum=maximum_pi_families_per_round,
        )
        row["minimal_common_safe_desired_counts"] = {
            owner: len(cores) for owner, cores in minimal.items()
        }
        fresh_pi = []
        for witness in found_pi:
            signature = cycle_signature(witness)
            if signature in signatures:
                continue
            signatures.add(signature)
            solver.add(atoms.cut(signature))
            fresh_pi.append(witness)
        if fresh_pi:
            row["fresh_pi_cut_count"] = len(fresh_pi)
            row["pi_witnesses"] = fresh_pi
            result["iterations"].append(row)
            checkpoint()
            continue

        fresh_allocations = []
        for allocation, edges in menu:
            signature = tuple(tuple(allocation[owner]) for owner in ("r", "q", "d", "s"))
            if signature in allocation_signatures:
                continue
            if complete_efx(exact_values, allocation):
                allocation_signatures.add(signature)
                solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
                fresh_allocations.append({
                    "allocation": allocation,
                    "edges": [list(edge) for edge in sorted(edges)],
                })
                if len(fresh_allocations) >= maximum_allocations_per_round:
                    break
        if fresh_allocations:
            row["fresh_allocation_cut_count"] = len(fresh_allocations)
            row["efx_allocations"] = fresh_allocations
            result["iterations"].append(row)
            checkpoint()
            continue

        result["status"] = "SAT_PI_FREE_NO_ROOT_FIXED_FOUR_EDGE_EFX"
        result["values"] = {
            owner: {good: str(amount) for good, amount in values.items()}
            for owner, values in exact_values.items()
        }
        result["iterations"].append(row)
        checkpoint()
        break
    else:
        result["status"] = "ITERATION_LIMIT"
        checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pi-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=961748941)
    parser.add_argument("--maximum-iterations", type=int, default=500)
    parser.add_argument("--maximum-pi-families-per-round", type=int, default=1000)
    parser.add_argument("--maximum-allocations-per-round", type=int, default=100)
    args = parser.parse_args()
    result = run(
        args.pi_source,
        args.endpoint_source,
        args.output,
        args.timeout_seconds,
        args.random_seed,
        args.maximum_iterations,
        args.maximum_pi_families_per_round,
        args.maximum_allocations_per_round,
    )
    print(json.dumps({
        "status": result["status"],
        "pi_cuts": result["generalized_pi_cut_count"],
        "allocation_cuts": result["allocation_cut_count"],
        "menu": result["root_fixed_allocation_count"],
        "iterations": len(result["iterations"]),
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
