#!/usr/bin/env python3
"""Independent literal-tail replay of the minimized seven-endpoint R3 core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .audit_allocated_e_all_allocation_unsat import structural_pi_signature
from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula
from .run_fixed_u_rank_three_relation_cegar import base_response


ROOT = Path(__file__).resolve().parents[2]


def audit(source: Path, output: Path, timeout_seconds: int, random_seed: int):
    source = source.resolve()
    payload = json.loads(source.read_text())
    signatures = [
        tuple((source_owner, tuple(core)) for source_owner, core in signature)
        for signature in payload["pi_signatures"]
    ]
    allocations = payload["allocations"]
    if not all(structural_pi_signature(signature) for signature in signatures):
        raise AssertionError("invalid closed-disjoint PI signature")

    solver, value = build_master(2)
    atoms = {}
    for signature in signatures:
        clause = []
        for source_owner, core in signature:
            key = source_owner, core
            atom = atoms.get(key)
            if atom is None:
                atom = z3.Bool(f"min_audit_{source_owner}_{'_'.join(core)}")
                solver.add(atom == base_response(value, source_owner, core))
                atoms[key] = atom
            clause.append(z3.Not(atom))
        solver.add(z3.Or(*clause))
    for allocation in allocations:
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    status = solver.check()
    result = {
        "schema": "allocated-e-minimized-unsat-core-independent-audit-v1",
        "status": "AUDIT_PASSED" if status == z3.unsat else "AUDIT_FAILED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "solver": f"Z3 {z3.get_version_string()}",
        "solver_status": str(status),
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else None,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "pi_clause_count": len(signatures),
        "allocation_clause_count": len(allocations),
        "independent_response_atom_count": len(atoms),
        "pi_predicate_encoding": "literal tail-minimum base_response",
        "allocation_encoding": "direct complete_efx formula",
        "all_pi_signatures_structurally_valid": True,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent exact replay of the minimized 425-PI/seven-allocation "
            "bounded core. This is a bounded-cell certificate and candidate "
            "analytic dichotomy, not a cap-free theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=57721)
    args = parser.parse_args()
    result = audit(source=args.source, output=args.output,
                   timeout_seconds=args.timeout_seconds,
                   random_seed=args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "solver_status": result["solver_status"],
        "pi_clauses": result["pi_clause_count"],
        "allocations": result["allocation_clause_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
