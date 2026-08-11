#!/usr/bin/env python3
"""Decide the radius-three flower gate after excluding basic PI cycles."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path

import z3

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
    )
    from .decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from .decide_flexible_later_owner_topology_menu import (
        build_master,
        fractions,
        true_tail,
    )
    from .run_flexible_lex_allocation_cegar import (
        add_live_constraints,
        allocation_key,
        earliest_improved_owner,
        moved_good_count,
        sha256,
    )
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
    )
    from decide_flexible_later_owner_connected_transfer import (
        endpoint_formula,
        enumerate_connected,
    )
    from decide_flexible_later_owner_topology_menu import (
        build_master,
        fractions,
        true_tail,
    )
    from run_flexible_lex_allocation_cegar import (
        add_live_constraints,
        allocation_key,
        earliest_improved_owner,
        moved_good_count,
        sha256,
    )


def add_no_self_champions(solver, old, value, base):
    count = 0
    for owner in AGENTS:
        offer = tuple(old[owner]) + ("f",)
        for size in range(1, len(offer) + 1):
            for subset in itertools.combinations(offer, size):
                if "f" not in subset:
                    continue
                solver.add(z3.Not(z3.And(
                    z3.Sum(*(value[good, owner] for good in subset)) > base[owner],
                    *(
                        true_tail([value[good, observer] for good in subset])
                        <= base[observer]
                        for observer in AGENTS
                    ),
                )))
                count += 1
    return count


def add_no_single_genuine_cycles(solver, old, value, base):
    genuine_cache = {}

    def genuine(source, target):
        key = (source, target)
        if key not in genuine_cache:
            offer = tuple(old[target]) + ("f",)
            witnesses = []
            for size in range(1, len(offer) + 1):
                for subset in itertools.combinations(offer, size):
                    if "f" not in subset:
                        continue
                    witnesses.append(z3.And(
                        z3.Sum(*(value[good, source] for good in subset))
                        > base[source],
                        *(
                            true_tail([value[good, observer] for good in subset])
                            <= base[observer]
                            for observer in AGENTS
                        ),
                    ))
            genuine_cache[key] = z3.Or(*witnesses)
        return genuine_cache[key]

    count = 0
    for size in range(2, len(AGENTS) + 1):
        for cycle in itertools.permutations(AGENTS, size):
            if cycle[0] != min(cycle):
                continue
            edges = tuple(
                (cycle[index], cycle[(index + 1) % size])
                for index in range(size)
            )
            for genuine_index, (source, target) in enumerate(edges):
                ordinary = [
                    z3.Sum(*(value[good, edge_source] for good in old[edge_target]))
                    > base[edge_source]
                    for index, (edge_source, edge_target) in enumerate(edges)
                    if index != genuine_index
                ]
                solver.add(z3.Not(z3.And(genuine(source, target), *ordinary)))
                count += 1
    return count


def add_no_envy_cycles(solver, old, value, base):
    count = 0
    for size in range(2, len(AGENTS) + 1):
        for cycle in itertools.permutations(AGENTS, size):
            if cycle[0] != min(cycle):
                continue
            solver.add(z3.Not(z3.And(*(
                z3.Sum(*(
                    value[good, cycle[index]]
                    for good in old[cycle[(index + 1) % size]]
                )) > base[cycle[index]]
                for index in range(size)
            ))))
            count += 1
    return count


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(output_path, maximum_iterations, timeout_seconds, batch_size):
    solver, atoms, old, symbolic_value, base = build_master()
    symmetry_count = add_live_constraints(
        solver, atoms, symbolic_value, symmetry=True
    )
    self_champion_constraint_count = add_no_self_champions(
        solver, old, symbolic_value, base
    )
    single_genuine_cycle_constraint_count = add_no_single_genuine_cycles(
        solver, old, symbolic_value, base
    )
    envy_cycle_constraint_count = add_no_envy_cycles(
        solver, old, symbolic_value, base
    )
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
    iterations = []
    script = Path(__file__).resolve()
    root = script.parents[2]
    result = {
        "schema": "flexible-lex-basic-pi-free-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "objective": "lex",
        "live_polarity": True,
        "global_item_symmetry": True,
        "symmetry_constraint_count": symmetry_count,
        "genuine_self_champions_excluded": True,
        "self_champion_subset_constraint_count": self_champion_constraint_count,
        "single_genuine_pi_cycles_excluded": True,
        "single_genuine_cycle_constraint_count": (
            single_genuine_cycle_constraint_count
        ),
        "ordinary_envy_cycles_excluded": True,
        "envy_cycle_constraint_count": envy_cycle_constraint_count,
        "candidate_allocation_count": len(candidates),
        "selected_candidate_indices": selected_indices,
        "iterations": iterations,
        "claim_boundary": (
            "bounded two-atom representative live-polarity flower decision "
            "excluding every genuine self-champion subset and every simple "
            "cycle with exactly one genuine edge; UNSAT is a bounded hard-state "
            "theorem candidate, while SAT still requires an audit of PI edge sets "
            "with at least two genuine edges"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }
    assert len(candidates) == 41394
    assert self_champion_constraint_count == 290
    assert single_genuine_cycle_constraint_count == 60
    assert envy_cycle_constraint_count == 20
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
        record["added_candidate_indices"] = [
            candidate_index[allocation_key(allocation)] for allocation in chosen
        ]
        for allocation in chosen:
            key = allocation_key(allocation)
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
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    result = run(
        args.output.resolve(),
        args.maximum_iterations,
        args.timeout_seconds,
        args.batch_size,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
