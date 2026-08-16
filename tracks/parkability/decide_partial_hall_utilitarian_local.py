#!/usr/bin/env python3
"""Decide whether a radius-one Hall obstruction can be locally utilitarian-maximal."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import integerize
    from .run_partial_hall_pareto_cegar import build_master
    from .run_partial_hall_utilitarian_cegar import (
        add_good_symmetry_breaking,
        utilitarian_blocker,
    )
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import integerize
    from run_partial_hall_pareto_cegar import build_master
    from run_partial_hall_utilitarian_cegar import (
        add_good_symmetry_breaking,
        utilitarian_blocker,
    )


SCHEMA = "partial-hall-utilitarian-local-gate-v1"


def owner_vector(base, floater, m):
    owners = [-1] * m
    for owner, bundle in enumerate(base):
        for good in bundle:
            owners[good] = owner
    owners[floater] = -1
    return tuple(owners)


def rival_from_owners(owners):
    floater = owners.index(-1)
    masks = tuple(
        sum(1 << good for good, assigned in enumerate(owners) if assigned == owner)
        for owner in range(4)
    )
    if any(mask == 0 for mask in masks):
        return None
    return {"floater": floater, "masks": masks}


def transfer_component_count(original, candidate):
    adjacency = {}
    for source, destination in zip(original, candidate):
        if source == destination:
            continue
        adjacency.setdefault(source, set()).add(destination)
        adjacency.setdefault(destination, set()).add(source)
    unseen = set(adjacency)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return components


def local_rivals(base, floater, m, radius, connected_only=False):
    original = owner_vector(base, floater, m)
    rivals = {}
    for distance in range(1, radius + 1):
        for changed_goods in itertools.combinations(range(m), distance):
            choices = []
            for good in changed_goods:
                choices.append(
                    tuple(owner for owner in range(-1, 4) if owner != original[good])
                )
            for replacements in itertools.product(*choices):
                candidate = list(original)
                for good, replacement in zip(changed_goods, replacements):
                    candidate[good] = replacement
                if candidate.count(-1) != 1:
                    continue
                if connected_only and transfer_component_count(original, candidate) != 1:
                    continue
                rival = rival_from_owners(candidate)
                if rival is None:
                    continue
                key = (rival["floater"], rival["masks"])
                rivals[key] = rival
    return tuple(rivals[key] for key in sorted(rivals))


def run(output, smt2_output, radius, timeout_seconds, break_good_symmetry):
    solver, values, base, floater, partitions = build_master(
        int(timeout_seconds * 1000)
    )
    if break_good_symmetry:
        add_good_symmetry_breaking(solver, values, base)
    rivals = local_rivals(base, floater, len(values[0]), radius)
    for rival in rivals:
        solver.add(utilitarian_blocker(values, base, rival))
    verdict = solver.check()
    model_values = integerize(solver.model(), values) if verdict == z3.sat else None
    if verdict == z3.sat:
        status = "SAT_LOCAL_MAXIMAL_OBSTRUCTION"
    elif verdict == z3.unsat:
        status = "UNSAT"
    else:
        status = "UNKNOWN"
    smt2_output.write_text(solver.to_smt2())
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "SAT gives a radius-one Hall obstruction with no eligible "
            "normalized-utilitarian improver within the stated owner distance; "
            "UNSAT proves the fixed-base local-improvement lemma."
        ),
        "n": 4,
        "m": 9,
        "base_bundles": [list(bundle) for bundle in base],
        "floater": floater,
        "candidate_partition_count": len(partitions),
        "owner_distance_radius": radius,
        "local_rival_template_count": len(rivals),
        "break_good_symmetry": break_good_symmetry,
        "timeout_seconds": timeout_seconds,
        "values": model_values,
        "smt2_output": str(smt2_output),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "solver_statistics": str(solver.statistics()),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path, required=True)
    parser.add_argument("--radius", type=int, choices=range(1, 10), default=2)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--break-good-symmetry", action="store_true")
    args = parser.parse_args()
    result = run(
        args.output,
        args.smt2_output,
        args.radius,
        args.timeout_seconds,
        args.break_good_symmetry,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
