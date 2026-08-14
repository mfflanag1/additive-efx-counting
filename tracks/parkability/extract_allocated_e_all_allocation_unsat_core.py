#!/usr/bin/env python3
"""Extract a compact assumption core from the all-allocation R3 decision."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .audit_allocated_e_all_allocation_unsat import collect
from .run_allocated_e_capture_rank_three_cegar import build_master, linear_base_response
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula


ROOT = Path(__file__).resolve().parents[2]


def run(source: Path, output: Path, timeout_seconds: int, random_seed: int):
    source = source.resolve()
    _, signatures, allocations = collect(source)
    solver, value = build_master(2)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    core_atoms = {}

    def response_atom(source_owner, core):
        key = source_owner, tuple(core)
        atom = core_atoms.get(key)
        if atom is None:
            atom = z3.Bool(f"core_extract_response_{source_owner}_{'_'.join(core)}")
            solver.add(atom == linear_base_response(value, source_owner, core))
            core_atoms[key] = atom
        return atom

    labels = {}
    signature_rows = list(signatures)
    allocation_rows = list(allocations.values())
    for index, signature in enumerate(signature_rows):
        label = z3.Bool(f"assume_pi_{index}")
        clause = z3.Or(*(
            z3.Not(response_atom(source_owner, core))
            for source_owner, core in signature
        ))
        solver.add(z3.Implies(label, clause))
        labels[str(label)] = ("pi", index, label)
    for index, allocation in enumerate(allocation_rows):
        label = z3.Bool(f"assume_efx_{index}")
        solver.add(z3.Implies(
            label,
            z3.Not(allocation_formula(allocation, value, "complete_efx")),
        ))
        labels[str(label)] = ("efx", index, label)

    assumptions = [row[2] for row in labels.values()]
    started = time.monotonic()
    status = solver.check(*assumptions)
    elapsed = time.monotonic() - started
    core_names = {str(label) for label in solver.unsat_core()} if status == z3.unsat else set()
    pi_indices = sorted(
        index for kind, index, label in labels.values()
        if kind == "pi" and str(label) in core_names
    )
    efx_indices = sorted(
        index for kind, index, label in labels.values()
        if kind == "efx" and str(label) in core_names
    )
    result = {
        "schema": "allocated-e-all-allocation-unsat-assumption-core-v1",
        "status": "UNSAT_CORE_EXTRACTED" if status == z3.unsat else str(status),
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "elapsed_seconds": elapsed,
        "full_pi_clause_count": len(signature_rows),
        "full_allocation_clause_count": len(allocation_rows),
        "core_pi_clause_count": len(pi_indices),
        "core_allocation_clause_count": len(efx_indices),
        "core_response_atom_count": len({
            (source_owner, tuple(core))
            for index in pi_indices
            for source_owner, core in signature_rows[index]
        }),
        "pi_signatures": [
            [[source_owner, list(core)] for source_owner, core in signature_rows[index]]
            for index in pi_indices
        ],
        "allocations": [allocation_rows[index] for index in efx_indices],
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Solver-produced assumption core for the bounded twelve-atom UNSAT "
            "decision. The core is not guaranteed inclusion-minimal and is not "
            "itself a cap-free analytic proof."
        ),
    }
    if status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=271828)
    args = parser.parse_args()
    result = run(args.source, args.output, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "pi_core": result["core_pi_clause_count"],
        "allocation_core": result["core_allocation_clause_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
