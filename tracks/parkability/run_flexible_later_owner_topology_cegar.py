#!/usr/bin/env python3
"""Run topology-class CEGAR for connected three-good flower transfers."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import z3

try:
    from .analyze_flexible_later_owner_escape_topologies import (
        old_bundles,
        transfer_topology,
    )
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        endpoint_succeeds,
        lex_endpoint_succeeds,
    )
    from .decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from .decide_flexible_later_owner_topology_menu import (
        MINED_SIGNATURES,
        build_master,
        fractions,
    )
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import (
        old_bundles,
        transfer_topology,
    )
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        endpoint_succeeds,
        lex_endpoint_succeeds,
    )
    from decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from decide_flexible_later_owner_topology_menu import (
        MINED_SIGNATURES,
        build_master,
        fractions,
    )


def classify_candidates(old, objective):
    groups = defaultdict(list)
    for allocation in enumerate_connected(
        old,
        radius=3,
        rooted=False,
        structural_reductions=objective == "later",
    ):
        signature = transfer_topology(old, allocation)["signature"]
        groups[signature].append(allocation)
    return {signature: tuple(allocations) for signature, allocations in groups.items()}


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(
    output_path,
    maximum_iterations=30,
    timeout_seconds=120,
    seed_path=None,
    objective="later",
):
    solver, atoms, old, value, base = build_master()
    groups = classify_candidates(old, objective)
    selected = set(
        signature
        for signature in (MINED_SIGNATURES if objective == "later" else ())
        if signature in groups
    )
    if seed_path is not None:
        seed = json.loads(seed_path.read_text())
        selected.update(
            signature
            for signature in seed.get("selected_topology_classes", ())
            if signature in groups
        )
    blocked_allocations = 0

    def add_signature(signature):
        nonlocal blocked_allocations
        for allocation in groups[signature]:
            solver.add(z3.Not(endpoint_formula(
                allocation, old, value, base, objective
            )))
            blocked_allocations += 1

    for signature in sorted(selected):
        add_signature(signature)
    solver.set(timeout=timeout_seconds * 1000)
    records = []
    result = {
        "schema": "flexible-later-owner-topology-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "objective": objective,
        "candidate_allocation_count": sum(map(len, groups.values())),
        "topology_class_count": len(groups),
        "initial_topology_classes": sorted(selected),
        "seed": str(seed_path) if seed_path is not None else None,
        "iterations": records,
        "claim_boundary": (
            "bounded two-atom representative full-capture flower class-CEGAR; "
            "UNSAT covers this bounded cell only, while SAT with no connected "
            "repair refutes the bounded radius-three statement only"
        ),
    }
    checkpoint(output_path, result)
    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {
            "iteration": iteration,
            "status": str(checked),
            "selected_topology_class_count": len(selected),
            "blocked_allocation_count": blocked_allocations,
        }
        records.append(record)
        print(json.dumps(record, sort_keys=True), flush=True)
        if checked == z3.unsat:
            result["status"] = "unsat"
            result["selected_topology_classes"] = sorted(selected)
            checkpoint(output_path, result)
            return result
        if checked == z3.unknown:
            result["status"] = "unknown"
            result["reason_unknown"] = solver.reason_unknown()
            result["selected_topology_classes"] = sorted(selected)
            checkpoint(output_path, result)
            return result

        model = solver.model()
        values = fractions(model, atoms, value)
        succeeds = (
            endpoint_succeeds if objective == "later" else lex_endpoint_succeeds
        )
        successful = defaultdict(list)
        radius_counts = Counter()
        for signature, allocations in groups.items():
            if signature in selected:
                continue
            for allocation in allocations:
                if succeeds(values, old, allocation):
                    successful[signature].append(allocation)
                    radius_counts[len(transfer_topology(old, allocation)["moved_goods"])] += 1
        record["successful_unselected_allocation_count"] = sum(
            map(len, successful.values())
        )
        record["successful_unselected_topology_class_count"] = len(successful)
        record["successful_radius_counts"] = dict(sorted(radius_counts.items()))
        if not successful:
            result["values"] = {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            }
            result["status"] = "sat"
            result["countermodel_iteration"] = iteration
            result["selected_topology_classes"] = sorted(selected)
            checkpoint(output_path, result)
            return result

        added = sorted(successful)
        record["added_topology_classes"] = added
        record["added_allocation_count"] = sum(len(groups[item]) for item in added)
        for signature in added:
            add_signature(signature)
        selected.update(added)
        checkpoint(output_path, result)

    result["status"] = "iteration_limit"
    result["selected_topology_classes"] = sorted(selected)
    checkpoint(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=30)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--seed", type=Path)
    parser.add_argument("--objective", choices=("later", "lex"), default="later")
    args = parser.parse_args()
    result = run(
        args.output,
        args.maximum_iterations,
        args.timeout_seconds,
        args.seed,
        args.objective,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
        "selected_topology_class_count": len(result["selected_topology_classes"]),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
