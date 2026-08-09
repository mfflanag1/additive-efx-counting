#!/usr/bin/env python3
"""Shrink and replay a rooted variable-packet UNSAT rival core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        load_pool,
        make_cell,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        load_pool,
        make_cell,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-variable-packet-rooted-core-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(cell, order, rivals) -> str:
    solver, values, own = structural_solver(cell)
    solver.add(*(rival_blocker(values, own, rival, order) for rival in rivals))
    return str(solver.check())


def audit(sizes, order, pool_path) -> dict:
    cell = make_cell(sizes)
    rivals = load_pool(pool_path, cell, order)
    solver, values, own = structural_solver(cell)
    assumptions = [z3.Bool(f"rival_{index}") for index in range(len(rivals))]
    solver.add(
        *(z3.Implies(assumption, rival_blocker(values, own, rival, order))
          for assumption, rival in zip(assumptions, rivals))
    )
    if solver.check(*assumptions) != z3.unsat:
        raise AssertionError("full pool is not UNSAT")
    core_indices = {
        int(str(assumption).rsplit("_", 1)[1]) for assumption in solver.unsat_core()
    }
    core = [rivals[index] for index in sorted(core_indices)]

    changed = True
    while changed:
        changed = False
        for index in range(len(core)):
            reduced = core[:index] + core[index + 1 :]
            if check(cell, order, reduced) == "unsat":
                core = reduced
                changed = True
                break
    if check(cell, order, core) != "unsat":
        raise AssertionError("minimized core is not UNSAT")
    deletion_statuses = [
        check(cell, order, core[:index] + core[index + 1 :])
        for index in range(len(core))
    ]
    if deletion_statuses != ["sat"] * len(core):
        raise AssertionError(("core is not deletion-minimal", deletion_statuses))

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "DELETION_MINIMAL_ROOTED_CORE_UNSAT",
        "claim_boundary": {
            "proved_exactly": "the rooted external-observer escape in the recorded finite variable-packet cell",
            "not_proved": "the escape for arbitrary packet sizes or complete EFX",
        },
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "pool_size": len(rivals),
        "initial_assumption_core_size": len(core_indices),
        "minimal_core_size": len(core),
        "single_deletion_statuses": deletion_statuses,
        "rivals": [
            {
                "owner_by_good": list(rival),
                "owner_by_good_names": [
                    None if owner is None else AGENTS[owner] for owner in rival
                ],
            }
            for rival in core
        ],
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "provenance": {
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "pool": str(pool_path),
            "pool_sha256": sha256(pool_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-sizes", required=True)
    parser.add_argument("--agent-order", default="0,2,1,3")
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(field) for field in args.packet_sizes.split(","))
    order = tuple(int(field) for field in args.agent_order.split(","))
    result = audit(sizes, order, args.pool)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {key: result[key] for key in ("status", "pool_size", "initial_assumption_core_size", "minimal_core_size")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
