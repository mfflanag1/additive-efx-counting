#!/usr/bin/env python3
"""Iteratively minimize the bounded R3 assumption core."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master, linear_base_response
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula


ROOT = Path(__file__).resolve().parents[2]


def run(source: Path, output: Path, timeout_seconds: int,
        random_seed: int, maximum_passes: int):
    source = source.resolve()
    payload = json.loads(source.read_text())
    signatures = [
        tuple((source_owner, tuple(core)) for source_owner, core in signature)
        for signature in payload["pi_signatures"]
    ]
    allocations = payload["allocations"]
    solver, value = build_master(2)
    solver.set(
        timeout=timeout_seconds * 1000,
        random_seed=random_seed,
        **{"core.minimize": True},
    )
    response_atoms = {}

    def response_atom(source_owner, core):
        key = source_owner, core
        atom = response_atoms.get(key)
        if atom is None:
            atom = z3.Bool(f"min_response_{source_owner}_{'_'.join(core)}")
            solver.add(atom == linear_base_response(value, source_owner, core))
            response_atoms[key] = atom
        return atom

    rows = {}
    for index, signature in enumerate(signatures):
        label = z3.Bool(f"min_pi_{index}")
        solver.add(z3.Implies(label, z3.Or(*(
            z3.Not(response_atom(source_owner, core))
            for source_owner, core in signature
        ))))
        rows[str(label)] = ("pi", index, label)
    for index, allocation in enumerate(allocations):
        label = z3.Bool(f"min_efx_{index}")
        solver.add(z3.Implies(
            label,
            z3.Not(allocation_formula(allocation, value, "complete_efx")),
        ))
        rows[str(label)] = ("efx", index, label)

    active = [row[2] for row in rows.values()]
    passes = []
    started = time.monotonic()
    final_status = None
    for pass_index in range(maximum_passes):
        status = solver.check(*active)
        final_status = status
        record = {
            "pass": pass_index,
            "input_assumption_count": len(active),
            "solver_status": str(status),
        }
        if status != z3.unsat:
            if status == z3.unknown:
                record["reason_unknown"] = solver.reason_unknown()
            passes.append(record)
            break
        core_names = {str(label) for label in solver.unsat_core()}
        reduced = [label for label in active if str(label) in core_names]
        record["output_core_count"] = len(reduced)
        passes.append(record)
        if len(reduced) == len(active):
            active = reduced
            break
        active = reduced

    active_names = {str(label) for label in active}
    pi_indices = sorted(
        index for kind, index, label in rows.values()
        if kind == "pi" and str(label) in active_names
    )
    efx_indices = sorted(
        index for kind, index, label in rows.values()
        if kind == "efx" and str(label) in active_names
    )
    result = {
        "schema": "allocated-e-all-allocation-minimized-unsat-core-v1",
        "status": "UNSAT_CORE_MINIMIZED" if final_status == z3.unsat else str(final_status),
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds_per_pass": timeout_seconds,
        "random_seed": random_seed,
        "core_minimize_option": True,
        "passes": passes,
        "pi_clause_count": len(pi_indices),
        "allocation_clause_count": len(efx_indices),
        "response_atom_count": len({
            (source_owner, core)
            for index in pi_indices
            for source_owner, core in signatures[index]
        }),
        "pi_signatures": [
            [[source_owner, list(core)] for source_owner, core in signatures[index]]
            for index in pi_indices
        ],
        "allocations": [allocations[index] for index in efx_indices],
        "elapsed_seconds": time.monotonic() - started,
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Solver-minimized assumption core for the bounded twelve-atom R3 "
            "dichotomy. Solver core minimization does not by itself produce a "
            "human proof or a cap-free theorem."
        ),
    }
    if final_status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=1618033)
    parser.add_argument("--maximum-passes", type=int, default=4)
    args = parser.parse_args()
    result = run(
        args.source, args.output, args.timeout_seconds,
        args.random_seed, args.maximum_passes,
    )
    print(json.dumps({
        "status": result["status"],
        "pi_core": result["pi_clause_count"],
        "allocation_core": result["allocation_clause_count"],
        "passes": result["passes"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
