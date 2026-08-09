#!/usr/bin/env python3
"""Decide selected-root EFX completion in one adjacent-large packet cell."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        N,
        atomic_json,
        make_cell,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        N,
        atomic_json,
        make_cell,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "adjacent-large-selected-root-completion-v1"


def selected_bundle(cell, root):
    if root == 0:
        return cell["packets"][0] + (cell["floater"],)
    if root == 1:
        return cell["packets"][2] + (cell["floater"],)
    raise ValueError("selected root must be p=0 or r=1")


def candidates(cell, root):
    selected = set(selected_bundle(cell, root))
    remaining = tuple(good for good in range(cell["m"]) if good not in selected)
    destinations = tuple(agent for agent in range(4) if agent != root) + (None,)
    for assignment in itertools.product(destinations, repeat=len(remaining)):
        owner = [None] * cell["m"]
        for good in selected:
            owner[good] = root
        for good, assigned in zip(remaining, assignment):
            owner[good] = assigned
        yield tuple(owner)


def decide(sizes, root, timeout_seconds):
    cell = make_cell(sizes)
    solver, values, own = structural_solver(cell)
    solver.set(timeout=timeout_seconds * 1000)
    menu = tuple(candidates(cell, root))
    # Any EFX completion of the selected desired root bundle improves p.
    # Use order (p,r,s,q), so rival_blocker reduces to EFX failure here.
    order = (root,) + tuple(agent for agent in range(4) if agent != root)
    for owner in menu:
        solver.add(rival_blocker(values, own, owner, order))
    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "status": (
            "UNSAT_SELECTED_ROOT_ALWAYS_COMPLETES"
            if checked == z3.unsat
            else "SAT_SELECTED_ROOT_COMPLETION_REFUTED"
            if checked == z3.sat
            else "UNKNOWN"
        ),
        "solver_status": str(checked),
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "selected_root": root,
        "selected_root_name": AGENTS[root],
        "selected_root_bundle": [
            cell["goods"][good]
            for good in selected_bundle(cell, root)
        ],
        "candidate_count": len(menu),
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "claim_boundary": {
            "unsat": "selected p-root completion theorem only in this fixed packet cell",
            "sat": "exact refutation only of selected-root completion; unrestricted adjacent escape may remain",
            "unknown": "no mathematical decision",
        },
    }
    if checked == z3.sat:
        from run_alternating_variable_packet_rooted_cegar import integerize

        result["values"] = [list(row) for row in integerize(solver.model(), values)]
    elif checked == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--root", type=int, choices=(0, 1), default=0)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    result = decide(sizes, args.root, args.timeout_seconds)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
