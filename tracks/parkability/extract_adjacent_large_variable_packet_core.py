#!/usr/bin/env python3
"""Shrink a fixed adjacent-large split-cell rival pool to an exact core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        load_pool,
        make_cell,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        AGENTS,
        load_pool,
        make_cell,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "adjacent-large-variable-packet-core-extraction-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def named_allocation(cell, owner):
    return {
        AGENTS[agent]: [
            cell["goods"][good]
            for good, assigned in enumerate(owner)
            if assigned == agent
        ]
        for agent in range(4)
    } | {
        "charity": [
            cell["goods"][good]
            for good, assigned in enumerate(owner)
            if assigned is None
        ]
    }


def extract(sizes, order, pool_path):
    cell = make_cell(sizes)
    rivals = load_pool(pool_path, cell, order)
    solver, values, own = structural_solver(cell)
    tags = []
    owner_by_name = {}
    for index, owner in enumerate(rivals):
        tag = z3.Bool(f"rival_{index}")
        solver.add(z3.Implies(tag, rival_blocker(values, own, owner, order)))
        tags.append(tag)
        owner_by_name[str(tag)] = owner
    if solver.check(*tags) != z3.unsat:
        raise AssertionError("pool is not UNSAT")
    original_core = list(solver.unsat_core())
    core = list(original_core)
    for tag in tuple(core):
        trial = [candidate for candidate in core if candidate is not tag]
        if solver.check(*trial) == z3.unsat:
            core = trial
    deletion_statuses = []
    for tag in core:
        status = str(solver.check(*(candidate for candidate in core if candidate is not tag)))
        deletion_statuses.append(status)
        if status != "sat":
            raise AssertionError("core is not deletion-minimal")
    core_owners = [owner_by_name[str(tag)] for tag in core]
    script = Path(__file__).resolve()
    search = script.with_name("run_adjacent_large_variable_packet_global_lex_cegar.py")
    return {
        "schema": SCHEMA,
        "status": "UNSAT_ADJACENT_SPLIT_CELL",
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "pool_size": len(rivals),
        "initial_core_size": len(original_core),
        "deletion_minimal_core_size": len(core_owners),
        "single_deletion_statuses": deletion_statuses,
        "core": [
            {
                "owner_by_good": list(owner),
                "allocation": named_allocation(cell, owner),
            }
            for owner in core_owners
        ],
        "claim_boundary": {
            "proved_exactly": "unrestricted global-lex escape in this fixed adjacent-large packet cell and priority order",
            "not_proved": "arbitrary packet sizes, other priority orders in this split cell, or complete four-agent EFX",
        },
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "search_script": str(search.relative_to(search.parents[2])),
            "search_script_sha256": sha256(search),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    order = tuple(int(part) for part in args.order.split(","))
    result = extract(sizes, order, args.pool)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
