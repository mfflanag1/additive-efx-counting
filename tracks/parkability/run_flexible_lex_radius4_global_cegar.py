#!/usr/bin/env python3
"""Add radius-four global-maximality cuts to the basic PI-free flower gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        transfer_topology,
    )
    from .decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from .decide_flexible_later_owner_topology_menu import build_master, fractions
    from .find_flexible_lex_connected_escape import solve as solve_escape
    from .run_flexible_lex_allocation_cegar import (
        add_live_constraints,
        allocation_key,
        sha256,
    )
    from .run_flexible_lex_self_pi_free_cegar import (
        add_no_envy_cycles,
        add_no_self_champions,
        add_no_single_genuine_cycles,
    )
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        transfer_topology,
    )
    from decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from decide_flexible_later_owner_topology_menu import build_master, fractions
    from find_flexible_lex_connected_escape import solve as solve_escape
    from run_flexible_lex_allocation_cegar import (
        add_live_constraints,
        allocation_key,
        sha256,
    )
    from run_flexible_lex_self_pi_free_cegar import (
        add_no_envy_cycles,
        add_no_self_champions,
        add_no_single_genuine_cycles,
    )


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(output_path, seed_path, maximum_iterations, timeout_seconds):
    seed = json.loads(seed_path.read_text())
    if seed.get("status") != "sat":
        raise ValueError("seed is not a SAT basic-PI-free gate")
    solver, atoms, old, symbolic_value, base = build_master()
    symmetry_count = add_live_constraints(
        solver, atoms, symbolic_value, symmetry=True
    )
    self_count = add_no_self_champions(solver, old, symbolic_value, base)
    envy_count = add_no_envy_cycles(solver, old, symbolic_value, base)
    one_genuine_count = add_no_single_genuine_cycles(
        solver, old, symbolic_value, base
    )
    radius3 = enumerate_connected(
        old, radius=3, rooted=False, structural_reductions=False
    )
    selected_keys = set()
    for index in seed["selected_candidate_indices"]:
        allocation = radius3[index]
        selected_keys.add(allocation_key(allocation))
        solver.add(z3.Not(endpoint_formula(
            allocation, old, symbolic_value, base, "lex"
        )))
    solver.set(timeout=timeout_seconds * 1000)
    iterations = []
    script = Path(__file__).resolve()
    root = script.parents[2]
    result = {
        "schema": "flexible-lex-radius4-global-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "objective": "lex",
        "maximum_connected_radius": 4,
        "live_polarity": True,
        "basic_pi_free_constraints": {
            "self_champion_subsets": self_count,
            "ordinary_envy_cycles": envy_count,
            "single_genuine_cycles": one_genuine_count,
        },
        "symmetry_constraint_count": symmetry_count,
        "seed_radius3_cut_count": len(selected_keys),
        "iterations": iterations,
        "claim_boundary": (
            "bounded two-atom representative hard-flower CEGAR excluding basic "
            "PI cycles and every discovered connected lex endpoint through "
            "radius four; UNSAT would prove only the bounded conditional that "
            "absence of radius-four endpoints forces an earlier contradiction"
        ),
        "provenance": {
            "seed": str(seed_path.relative_to(root)),
            "seed_sha256": sha256(seed_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }
    checkpoint(output_path, result)
    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {
            "iteration": iteration,
            "master_status": str(checked),
            "installed_endpoint_cut_count": len(selected_keys),
        }
        iterations.append(record)
        if checked == z3.unsat:
            result["status"] = "unsat"
            checkpoint(output_path, result)
            return result
        if checked == z3.unknown:
            result["status"] = "unknown_master"
            result["reason_unknown"] = solver.reason_unknown()
            checkpoint(output_path, result)
            return result

        model = solver.model()
        values = fractions(model, atoms, symbolic_value)
        oracle_status, allocation = solve_escape(
            values, old, radius=4, timeout_seconds=timeout_seconds, objective="lex"
        )
        record["oracle_status"] = str(oracle_status)
        if oracle_status == z3.unknown:
            result["status"] = "unknown_oracle"
            checkpoint(output_path, result)
            return result
        if oracle_status == z3.unsat:
            result["status"] = "sat_no_connected_radius4_lex_endpoint"
            result["countermodel_iteration"] = iteration
            result["values"] = {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            }
            checkpoint(output_path, result)
            return result

        assert allocation is not None
        assert lex_endpoint_succeeds(values, old, allocation)
        key = allocation_key(allocation)
        if key in selected_keys:
            raise AssertionError("oracle returned an installed endpoint")
        selected_keys.add(key)
        topology = transfer_topology(old, allocation)
        record["added_allocation"] = allocation
        record["added_topology"] = topology
        solver.add(z3.Not(endpoint_formula(
            allocation, old, symbolic_value, base, "lex"
        )))
        checkpoint(output_path, result)
        print(json.dumps({
            "iteration": iteration,
            "master_status": str(checked),
            "oracle_status": str(oracle_status),
            "installed_endpoint_cut_count": len(selected_keys),
            "added_radius": len(topology["moved_goods"]),
            "added_topology": topology["signature"],
        }, sort_keys=True), flush=True)

    result["status"] = "iteration_limit"
    checkpoint(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    result = run(
        args.output.resolve(),
        args.seed.resolve(),
        args.maximum_iterations,
        args.timeout_seconds,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
