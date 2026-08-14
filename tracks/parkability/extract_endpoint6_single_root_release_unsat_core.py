#!/usr/bin/env python3
"""Extract an assumption core for the endpoint-6 single-root-release theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .audit_allocated_e_all_allocation_unsat import collect
from .run_allocated_e_capture_rank_three_cegar import build_master, linear_base_response
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula, total
from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]


def collected_constraints(producer):
    pi_source = ROOT / producer["pi_source"]
    _, initial, _ = collect(pi_source)
    signatures = set(initial)
    allocations = {}
    for row in producer["iterations"]:
        for witness in row.get("pi_witnesses", []):
            signatures.add(cycle_signature(witness))
        for record in row.get("efx_allocations", []):
            allocation = record["allocation"]
            key = tuple(tuple(allocation[owner]) for owner in ("r", "q", "d", "s"))
            allocations[key] = allocation
    assert len(signatures) == producer["generalized_pi_cut_count"]
    assert len(allocations) == producer["allocation_cut_count"]
    return tuple(sorted(signatures)), tuple(allocations.values())


def run(
    producer_source: Path,
    endpoint_source: Path,
    output: Path,
    timeout_seconds: int,
    random_seed: int,
):
    producer_source = producer_source.resolve()
    endpoint_source = endpoint_source.resolve()
    producer = json.loads(producer_source.read_text())
    assert producer["status"] == "UNSAT_PI_OR_SINGLE_ROOT_RELEASE_EFX"
    signatures, allocations = collected_constraints(producer)
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    retained = RETAINED[6]

    solver, value = build_master(2)
    solver.add(
        allocation_formula(endpoint6, value, "complete_efx"),
        total(value, "q", endpoint6["q"]) >= 1,
        total(value, "s", endpoint6["s"]) >= 1,
        total(value, "q", retained["q"]) < 1,
    )
    solver.set(
        timeout=timeout_seconds * 1000,
        random_seed=random_seed,
        **{"core.minimize": True},
    )
    assumptions = []
    metadata = {}
    for index, signature in enumerate(signatures):
        atom = z3.Bool(f"release_pi_{index}")
        solver.add(z3.Implies(atom, z3.Or(*(
            z3.Not(linear_base_response(value, source, tuple(pieces)))
            for source, pieces in signature
        ))))
        assumptions.append(atom)
        metadata[atom.decl().name()] = ("pi", index)
    for index, allocation in enumerate(allocations):
        atom = z3.Bool(f"release_endpoint_{index}")
        solver.add(z3.Implies(
            atom,
            z3.Not(allocation_formula(allocation, value, "complete_efx")),
        ))
        assumptions.append(atom)
        metadata[atom.decl().name()] = ("allocation", index)

    started = time.monotonic()
    status = solver.check(*assumptions)
    if status != z3.unsat:
        raise RuntimeError(f"producer did not replay UNSAT: {status} {solver.reason_unknown()}")
    core = solver.unsat_core()
    pi_indices = []
    allocation_indices = []
    for atom in core:
        kind, index = metadata[atom.decl().name()]
        (pi_indices if kind == "pi" else allocation_indices).append(index)

    result = {
        "schema": "endpoint6-single-root-release-unsat-core-v1",
        "status": "UNSAT_CORE_EXTRACTED",
        "solver": f"Z3 {z3.get_version_string()}",
        "producer": str(producer_source.relative_to(ROOT)),
        "producer_sha256": hashlib.sha256(producer_source.read_bytes()).hexdigest(),
        "endpoint_source": str(endpoint_source.relative_to(ROOT)),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "input_pi_clause_count": len(signatures),
        "input_allocation_count": len(allocations),
        "core_pi_clause_count": len(pi_indices),
        "core_allocation_count": len(allocation_indices),
        "pi_signatures": [
            [[source, list(pieces)] for source, pieces in signatures[index]]
            for index in sorted(pi_indices)
        ],
        "allocations": [allocations[index] for index in sorted(allocation_indices)],
        "elapsed_seconds": time.monotonic() - started,
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "core_minimize": True,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Assumption core for the exact twelve-atom single-root-release "
            "theorem. Independent formula replay remains separate."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=49979687)
    args = parser.parse_args()
    result = run(
        args.producer_source,
        args.endpoint_source,
        args.output,
        args.timeout_seconds,
        args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "core_pi_clause_count": result["core_pi_clause_count"],
        "core_allocation_count": result["core_allocation_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
