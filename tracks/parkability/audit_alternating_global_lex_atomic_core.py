#!/usr/bin/env python3
"""Replay deletion-minimal global-lex cores for the alternating atom."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import (
        AGENTS,
        BASE_OWNER,
        GOODS,
        rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_global_lex_cegar import (
        AGENTS,
        BASE_OWNER,
        GOODS,
        rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-global-lex-atomic-core-audit-v1"
CORE_MENUS = {
    "0123": ((None, None, 3, None, 0, 1, 2),),
    "0132": ((None, None, 3, None, 0, 1, 2),),
    "0213": (
        (1, 1, 3, 1, 0, 2, None),
        (0, 1, 3, 1, None, 2, 0),
        (3, None, 2, 3, 0, 1, 2),
        (1, 3, 2, 3, 0, None, 2),
        (1, None, 3, 1, 0, 2, 3),
    ),
    "0231": (
        (0, 1, None, 1, 3, 2, 0),
        (0, 1, 1, None, 3, 2, 0),
        (0, None, 1, 1, 3, 2, 0),
        (1, 3, 3, 3, 0, 2, None),
    ),
    "0312": (
        (None, None, 3, 3, 0, 1, 2),
        (0, 2, 2, None, 3, 1, 0),
    ),
    "0321": (
        (2, 3, 3, 3, 0, 1, 2),
        (0, None, 2, 2, 3, 1, 0),
        (0, 2, 2, None, 3, 1, 0),
    ),
    "1023": ((None, None, 3, None, 0, 1, 2),),
    "1032": ((None, None, 3, None, 0, 1, 2),),
    "1203": ((None, None, 3, None, 0, 1, 2),),
    "1230": ((0, None, None, None, 3, 1, 2),),
    "1302": ((None, None, 2, None, 3, 1, 0),),
    "1320": ((0, None, None, None, 3, 1, 2),),
    "2013": (
        (1, None, 3, 1, 0, 2, None),
        (3, None, 2, 3, 0, 1, 2),
        (1, 1, 3, 1, 0, 2, None),
        (None, 3, 2, 3, 0, 1, 2),
    ),
    "2031": (
        (0, 1, None, 1, 3, 2, 0),
        (0, 1, 1, None, 3, 2, 0),
        (1, 3, 3, 1, 0, 2, None),
        (1, 3, 3, 3, 0, 2, 1),
    ),
    "2103": (
        (1, 1, 0, 1, 3, 2, 0),
        (0, 0, 2, None, 3, 1, 2),
        (0, None, 2, 0, 3, 1, 2),
    ),
    "2130": (
        (1, 1, None, 0, 3, 2, 0),
        (0, 0, 2, None, 3, 1, 2),
    ),
    "2301": ((1, None, None, None, 3, 2, 0),),
    "2310": ((1, None, None, None, 3, 2, 0),),
    "3012": ((None, None, 2, None, 3, 1, 0),),
    "3021": ((1, None, None, None, 3, 2, 0),),
    "3102": ((None, None, 2, None, 3, 1, 0),),
    "3120": ((0, None, None, None, 3, 1, 2),),
    "3201": ((1, None, None, None, 3, 2, 0),),
    "3210": ((1, None, None, None, 3, 2, 0),),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def named_owner(owner: tuple[int | None, ...]) -> list[str | None]:
    return [None if assigned is None else AGENTS[assigned] for assigned in owner]


def audit() -> dict:
    expected_orders = {"".join(map(str, order)) for order in itertools.permutations(range(4))}
    if set(CORE_MENUS) != expected_orders:
        raise AssertionError("the frozen cores do not cover all 24 orders")

    base_solver, _, _ = structural_solver()
    if base_solver.check() != z3.sat:
        raise AssertionError("the structural cell itself is not satisfiable")

    records = []
    for tag in sorted(CORE_MENUS):
        order = tuple(int(character) for character in tag)
        menu = CORE_MENUS[tag]
        solver, values, own = structural_solver()
        blockers = tuple(rival_blocker(values, own, owner, order) for owner in menu)
        solver.add(*blockers)
        status = str(solver.check())
        if status != "unsat":
            raise AssertionError((tag, "full core", status))

        deletion_statuses = []
        for removed in range(len(menu)):
            reduced, reduced_values, reduced_own = structural_solver()
            reduced.add(
                *(
                    rival_blocker(reduced_values, reduced_own, owner, order)
                    for index, owner in enumerate(menu)
                    if index != removed
                )
            )
            reduced_status = str(reduced.check())
            deletion_statuses.append(reduced_status)
            if reduced_status != "sat":
                raise AssertionError((tag, "deletion", removed, reduced_status))

        records.append(
            {
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "core_size": len(menu),
                "core_status": status,
                "single_deletion_statuses": deletion_statuses,
                "rival_allocations": [
                    {
                        "owner_by_good": list(owner),
                        "owner_by_good_names": named_owner(owner),
                    }
                    for owner in menu
                ],
            }
        )

    script = Path(__file__).resolve()
    search_script = script.with_name("run_alternating_global_lex_cegar.py")
    return {
        "schema": SCHEMA,
        "status": "ALL_24_PRIORITY_ORDERS_UNSAT",
        "claim_boundary": {
            "proved_exactly": "no globally lexicographically maximal state exists in the strict seven-good alternating 2+2+1+1 structural cell",
            "not_proved": "the priority-sensitive escape for arbitrary bundle sizes or complete four-agent EFX",
        },
        "agents": list(AGENTS),
        "goods": list(GOODS),
        "base_owner_by_good": list(BASE_OWNER),
        "priority_order_count": len(records),
        "single_rival_order_count": sum(record["core_size"] == 1 for record in records),
        "maximum_core_size": max(record["core_size"] for record in records),
        "total_order_specific_rivals": sum(record["core_size"] for record in records),
        "orders": records,
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
        "provenance": {
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "search_script": str(search_script.relative_to(search_script.parents[2])),
            "search_script_sha256": sha256(search_script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload)


if __name__ == "__main__":
    main()
