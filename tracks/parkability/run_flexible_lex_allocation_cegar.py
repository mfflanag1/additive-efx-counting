#!/usr/bin/env python3
"""Run lean allocation-level CEGAR for the radius-three flower gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import z3

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        value as exact_value,
    )
    from .decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from .decide_flexible_later_owner_topology_menu import build_master, fractions
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        value as exact_value,
    )
    from decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from decide_flexible_later_owner_topology_menu import build_master, fractions


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allocation_key(allocation):
    return tuple(tuple(allocation[recipient]) for recipient in (*AGENTS, "_"))


def earliest_improved_owner(values, old, allocation):
    for agent in AGENTS:
        if exact_value(values, agent, allocation[agent]) != exact_value(
            values, agent, old[agent]
        ):
            return agent
    raise AssertionError("successful lex endpoint has no changed owner utility")


def moved_good_count(old, allocation):
    base_owner = {
        good: recipient
        for recipient, goods in {**old, "_": ("f",)}.items()
        for good in goods
    }
    new_owner = {
        good: recipient for recipient, goods in allocation.items() for good in goods
    }
    return sum(new_owner[good] != base_owner[good] for good in base_owner)


def add_live_constraints(solver, atoms, value, symmetry):
    bottom_r = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
    bottom_q = ("ar_bq_0", "ar_bq_1")
    solver.add(z3.Sum(*(value[good, "r"] for good in bottom_r)) >= value["f", "r"])
    solver.add(
        value["f", "r"] > z3.Sum(*(value[good, "r"] for good in bottom_q))
    )
    solver.add(
        z3.Sum(*(value[good, "q"] for good in bottom_q))
        > z3.Sum(*(value[good, "q"] for good in bottom_r))
    )
    symmetry_count = 0
    if symmetry:
        atom_set = set(atoms)
        for atom in atoms:
            if not atom.endswith("_0"):
                continue
            partner = atom[:-1] + "1"
            if partner in atom_set:
                solver.add(value[atom, "r"] <= value[partner, "r"])
                symmetry_count += 1
    return symmetry_count


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(
    output_path,
    maximum_iterations,
    timeout_seconds,
    batch_size,
    symmetry,
    resume_path=None,
):
    solver, atoms, old, symbolic_value, base = build_master()
    symmetry_count = add_live_constraints(solver, atoms, symbolic_value, symmetry)
    candidates = enumerate_connected(
        old, radius=3, rooted=False, structural_reductions=False
    )
    candidate_index = {
        allocation_key(allocation): index
        for index, allocation in enumerate(candidates)
    }
    solver.set(timeout=timeout_seconds * 1000)
    selected = set()
    selected_indices = []
    if resume_path is not None:
        resume = json.loads(resume_path.read_text())
        resume_indices = list(resume.get("selected_candidate_indices", ()))
        if not resume_indices:
            resume_indices = [
                index
                for record in resume.get("iterations", ())
                for index in record.get("added_candidate_indices", ())
            ]
        for index in resume_indices:
            allocation = candidates[index]
            key = allocation_key(allocation)
            if key in selected:
                continue
            selected.add(key)
            selected_indices.append(index)
            solver.add(z3.Not(endpoint_formula(
                allocation, old, symbolic_value, base, "lex"
            )))
    iterations = []
    script = Path(__file__).resolve()
    root = script.parents[2]
    result = {
        "schema": "flexible-lex-allocation-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "objective": "lex",
        "live_polarity": True,
        "global_item_symmetry": symmetry,
        "symmetry_constraint_count": symmetry_count,
        "candidate_allocation_count": len(candidates),
        "selected_candidate_indices": selected_indices,
        "iterations": iterations,
        "claim_boundary": (
            "bounded two-atom representative live-polarity flower decision; "
            "UNSAT covers only this bounded cell, while SAT is a countermodel "
            "only if the exact complete radius-three scan finds no lex endpoint"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }
    assert len(candidates) == 41394
    checkpoint(output_path, result)
    for iteration in range(maximum_iterations):
        checked = solver.check()
        record = {
            "iteration": iteration,
            "status": str(checked),
            "selected_allocation_count": len(selected),
        }
        iterations.append(record)
        if checked == z3.unsat:
            result["status"] = "unsat"
            checkpoint(output_path, result)
            return result
        if checked == z3.unknown:
            result["status"] = "unknown"
            result["reason_unknown"] = solver.reason_unknown()
            checkpoint(output_path, result)
            return result

        model = solver.model()
        values = fractions(model, atoms, symbolic_value)
        successful = [
            allocation
            for allocation in candidates
            if lex_endpoint_succeeds(values, old, allocation)
            and allocation_key(allocation) not in selected
        ]
        record["successful_allocation_count"] = len(successful)
        if not successful:
            result["status"] = "sat"
            result["countermodel_iteration"] = iteration
            result["values"] = {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            }
            checkpoint(output_path, result)
            return result

        buckets = defaultdict(list)
        for allocation in successful:
            key = (
                earliest_improved_owner(values, old, allocation),
                moved_good_count(old, allocation),
            )
            buckets[key].append(allocation)
        chosen = []
        for key in sorted(buckets, key=lambda item: (AGENTS.index(item[0]), item[1])):
            chosen.append(buckets[key][0])
            if len(chosen) == batch_size:
                break
        if len(chosen) < batch_size:
            chosen_keys = {allocation_key(allocation) for allocation in chosen}
            for allocation in successful:
                if allocation_key(allocation) in chosen_keys:
                    continue
                chosen.append(allocation)
                if len(chosen) == batch_size:
                    break
        record["successful_bucket_counts"] = {
            f"{owner}:radius{radius}": len(allocations)
            for (owner, radius), allocations in sorted(
                buckets.items(), key=lambda item: (AGENTS.index(item[0][0]), item[0][1])
            )
        }
        record["added_allocation_count"] = len(chosen)
        record["added_candidate_indices"] = [
            candidate_index[allocation_key(allocation)] for allocation in chosen
        ]
        for allocation in chosen:
            key = allocation_key(allocation)
            assert key not in selected
            selected.add(key)
            selected_indices.append(candidate_index[key])
            solver.add(z3.Not(endpoint_formula(
                allocation, old, symbolic_value, base, "lex"
            )))
        checkpoint(output_path, result)
        print(json.dumps(record, sort_keys=True), flush=True)

    result["status"] = "iteration_limit"
    checkpoint(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=500)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--no-symmetry", action="store_true")
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    result = run(
        args.output.resolve(),
        args.maximum_iterations,
        args.timeout_seconds,
        args.batch_size,
        not args.no_symmetry,
        args.resume.resolve() if args.resume is not None else None,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
