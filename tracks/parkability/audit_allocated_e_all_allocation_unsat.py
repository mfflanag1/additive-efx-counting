#!/usr/bin/env python3
"""Independent exact audit of the allocated-E all-allocation UNSAT result.

This replay deliberately does not import either atom class from the producer.
Generalized desired-core predicates are rebuilt with the independent
``base_response`` implementation (which uses the literal EFX-tail minimum),
whereas the producer uses the min-free additive expansion.  The 143 allocation
cuts are replayed directly, without allocation atoms.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
    provenance_holder,
)
from .flatten_allocated_e_cegar_resume import load_chain, witnesses
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_fixed_u_full_packet_terminal_cegar import (
    GOODS,
    OWNERS,
    SUPPORT_STATE,
    allocation_formula,
)
from .run_fixed_u_rank_three_relation_cegar import base_response
from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]


def canonical(allocation):
    return tuple((owner, tuple(sorted(allocation[owner]))) for owner in (*OWNERS, "charity"))


def structural_pi_signature(signature):
    sources = tuple(source for source, _ in signature)
    cores = tuple(set(core) for _, core in signature)
    if not sources or len(sources) != len(set(sources)):
        return False
    if any(not core or not core <= set(GOODS) for core in cores):
        return False
    if any(cores[i] & cores[j] for i in range(len(cores)) for j in range(i)):
        return False
    base_owner = {
        good: owner for owner, goods in ALLOCATED_E_BASE.items() for good in goods
    }
    permitted = set(sources) | {"charity"}
    return all(base_owner[good] in permitted for core in cores for good in core)


def collect(source):
    chain = load_chain(source)
    signatures = {}
    allocations = {}
    for _, payload in chain:
        for witness in witnesses(payload):
            signature = cycle_signature(witness)
            signatures.setdefault(signature, witness)
        for record in payload.get("iterations", []):
            for allocation in record.get("blocking_efx_allocations", []):
                allocations.setdefault(canonical(allocation), allocation)
    return chain, signatures, allocations


def audit(source: Path, output: Path, timeout_seconds: int, random_seed: int):
    source = source.resolve()
    payload = json.loads(source.read_text())
    chain, signatures, allocations = collect(source)
    menu_keys = {
        canonical(allocation)
        for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE)
        if all(allocation[owner] for owner in OWNERS)
    }
    supplier = provenance_holder(SUPPORT_STATE)
    allocation_checks = []
    for key, allocation in allocations.items():
        final = {good: owner for owner, goods in allocation.items() for good in goods}
        edges = {
            (supplier[good], final[good])
            for good in GOODS if supplier[good] != final[good]
        }
        allocation_checks.append(
            key in menu_keys
            and not allocation["charity"]
            and all(allocation[owner] for owner in OWNERS)
            and len(edges) <= 4
        )

    structural_checks = {
        "terminal_source_status_unsat": (
            payload.get("status") == "UNSAT_PI_OR_FOUR_EDGE_COMPLETE_EFX"
        ),
        "complete_menu_has_93480_allocations": len(menu_keys) == 93_480,
        "pi_count_matches_manifest": (
            len(signatures) == payload.get("generalized_pi_cut_count") == 46_683
        ),
        "allocation_count_matches_manifest": (
            len(allocations) == payload.get("allocation_cut_count") == 143
        ),
        "every_pi_signature_is_closed_disjoint_family": all(
            structural_pi_signature(signature) for signature in signatures
        ),
        "every_allocation_cut_is_in_complete_four_edge_menu": all(allocation_checks),
    }
    if not all(structural_checks.values()):
        raise AssertionError(structural_checks)

    solver, value = build_master(2)
    independent_atoms = {}
    for signature in signatures:
        clause = []
        for source_owner, core in signature:
            key = source_owner, tuple(core)
            atom = independent_atoms.get(key)
            if atom is None:
                atom = z3.Bool(f"audit_core_{source_owner}_{'_'.join(core)}")
                solver.add(atom == base_response(value, source_owner, core))
                independent_atoms[key] = atom
            clause.append(z3.Not(atom))
        solver.add(z3.Or(*clause))
    for allocation in allocations.values():
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    replay = solver.check()

    result = {
        "schema": "allocated-e-all-allocation-unsat-independent-audit-v1",
        "status": "AUDIT_PASSED" if replay == z3.unsat else "AUDIT_FAILED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_chain": [
            {
                "source": str(path.relative_to(ROOT)),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path, _ in chain
        ],
        "structural_checks": structural_checks,
        "independent_replay": {
            "solver": f"Z3 {z3.get_version_string()}",
            "status": str(replay),
            "reason_unknown": solver.reason_unknown() if replay == z3.unknown else None,
            "timeout_seconds": timeout_seconds,
            "random_seed": random_seed,
            "independent_core_atom_count": len(independent_atoms),
            "pi_clause_count": len(signatures),
            "direct_allocation_clause_count": len(allocations),
            "pi_predicate_encoding": "literal tail-minimum base_response",
            "allocation_encoding": "direct complete_efx formula without atoms",
        },
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent exact UNSAT replay of the complete declared 93,480-"
            "allocation, four-support-edge decision in the twelve-atom allocated-E "
            "R3 cell. This proves the bounded-cell disjunction only. Lifting from "
            "the declared atoms and necessary premises to every saturated cap-free "
            "fixed-U state remains open."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=104729)
    args = parser.parse_args()
    result = audit(
        args.source, args.output, args.timeout_seconds, args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "replay": result["independent_replay"]["status"],
        "pi_clauses": result["independent_replay"]["pi_clause_count"],
        "allocation_clauses": result["independent_replay"]["direct_allocation_clause_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
