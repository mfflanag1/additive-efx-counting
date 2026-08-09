#!/usr/bin/env python3
"""Audit the exact anchored-or-promoted dichotomy in the alternating atom."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .audit_alternating_global_lex_atomic_core import CORE_MENUS
    from .run_alternating_global_lex_cegar import (
        AGENTS,
        ALL_OWNERS,
        BASE_BUNDLES,
        BASE_OWNER,
        GOODS,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
    from .run_alternating_rooted_global_lex_cegar import rooted_owners
except ImportError:
    from audit_alternating_global_lex_atomic_core import CORE_MENUS
    from run_alternating_global_lex_cegar import (
        AGENTS,
        ALL_OWNERS,
        BASE_BUNDLES,
        BASE_OWNER,
        GOODS,
        numeric_efx,
        numeric_utilities,
        rival_blocker,
        structural_solver,
    )
    from run_alternating_rooted_global_lex_cegar import rooted_owners


SCHEMA = "alternating-anchored-or-promoted-atomic-audit-v1"
HARD_ORDERS = (
    (0, 2, 1, 3),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
    (0, 3, 2, 1),
    (2, 0, 1, 3),
    (2, 0, 3, 1),
    (2, 1, 0, 3),
    (2, 1, 3, 0),
)
ANCHORED_UNSAT_CORES = {
    (0, 2, 1, 3): (
        (1, 1, 3, 1, 0, 2, None),
        (3, 3, 2, 3, 0, 1, 2),
        (None, 3, 2, 3, 0, 1, 2),
        (1, None, 3, 1, 0, 2, None),
    ),
    (2, 0, 3, 1): (
        (1, 3, 3, 3, 0, 2, None),
        (0, 1, 1, 1, 3, 2, 0),
        (0, 1, None, 1, 3, 2, 0),
        (1, 3, 3, None, 0, 2, None),
    ),
}
ANCHORED_COUNTERMODELS = {
    (0, 2, 3, 1): (
        (201, 4, 12, 4, 209, 205, 197),
        (15, 182, 12, 9, 194, 209, 3),
        (14, 42, 202, 146, 411, 418, 223),
        (3, 5, 13, 4, 170, 12, 1),
    ),
    (0, 3, 1, 2): (
        (191, 8, 4, 4, 203, 199, 199),
        (7, 10, 1, 6, 16, 160, 2),
        (4, 4, 195, 12, 207, 211, 175),
        (9, 2, 12, 16, 130, 27, 6),
    ),
    (0, 3, 2, 1): (
        (103, 4, 12, 4, 111, 107, 99),
        (5, 11, 4, 1, 15, 72, 2),
        (15, 3, 97, 3, 100, 103, 9),
        (3, 1, 5, 7, 84, 9, 1),
    ),
    (2, 0, 1, 3): (
        (26, 1, 1, 1, 29, 28, 24),
        (12, 6, 2, 1, 11, 74, 4),
        (6, 4, 51, 2, 53, 55, 49),
        (10, 89, 99, 20, 213, 114, 5),
    ),
    (2, 1, 0, 3): (
        (123, 4, 103, 8, 135, 131, 16),
        (12, 7, 1, 3, 16, 85, 6),
        (6, 4, 61, 2, 63, 65, 59),
        (8, 131, 139, 123, 278, 254, 107),
    ),
    (2, 1, 3, 0): (
        (21, 1, 3, 1, 23, 22, 17),
        (5, 7, 3, 1, 9, 62, 1),
        (12, 4, 81, 4, 85, 89, 77),
        (9, 3, 12, 71, 86, 80, 3),
    ),
}
PROMOTED_COUNTERMODELS = {
    0: (
        (87, 6, 85, 8, 95, 93, 10),
        (187, 6, 166, 12, 3, 196, 6),
        (2, 1, 3, 29, 31, 64, 62),
        (188, 7, 188, 202, 397, 174, 188),
    ),
    2: (
        (9, 2, 8, 1, 54, 4, 46),
        (3, 9, 2, 1, 5, 101, 3),
        (12, 12, 16, 97, 121, 125, 113),
        (1, 2, 14, 7, 89, 4, 7),
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lex_dominates(values, owner, order) -> bool:
    rival = numeric_utilities(values, owner)
    base = numeric_utilities(values, BASE_OWNER)
    return tuple(rival[agent] for agent in order) > tuple(base[agent] for agent in order)


def pin_structural(values) -> None:
    solver, symbolic, _ = structural_solver()
    solver.add(
        *(symbolic[agent][good] * sum(values[agent]) == values[agent][good]
          for agent in range(4) for good in range(7))
    )
    if solver.check() != z3.sat:
        raise AssertionError("frozen profile is outside the structural cell")


def root_mode(owner, root: int) -> str | None:
    owned = tuple(good for good, assigned in enumerate(owner) if assigned == root)
    singleton = BASE_BUNDLES[root]
    desired = (0, 6) if root == 0 else (2, 6)
    if owned == singleton:
        return "anchored"
    if owned == desired:
        return "promoted"
    return None


def promoted_owners(root: int):
    desired = (0, 6) if root == 0 else (2, 6)
    remaining = tuple(good for good in range(7) if good not in desired)
    destinations = tuple(agent for agent in range(4) if agent != root) + (None,)
    for assignments in itertools.product(destinations, repeat=len(remaining)):
        owner = [None] * 7
        for good in desired:
            owner[good] = root
        for good, destination in zip(remaining, assignments):
            owner[good] = destination
        yield tuple(owner)


def audit() -> dict:
    dichotomy_records = []
    for order in HARD_ORDERS:
        menu = CORE_MENUS["".join(map(str, order))]
        modes = tuple(root_mode(owner, order[0]) for owner in menu)
        if None in modes:
            raise AssertionError((order, modes))
        solver, values, own = structural_solver()
        solver.add(*(rival_blocker(values, own, owner, order) for owner in menu))
        if solver.check() != z3.unsat:
            raise AssertionError((order, "dichotomy core"))
        dichotomy_records.append(
            {
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "core_size": len(menu),
                "anchored_rivals": modes.count("anchored"),
                "promoted_rivals": modes.count("promoted"),
            }
        )

    anchored_unsat = []
    for order, menu in ANCHORED_UNSAT_CORES.items():
        if not all(root_mode(owner, order[0]) == "anchored" for owner in menu):
            raise AssertionError((order, "non-anchored core rival"))
        solver, values, own = structural_solver()
        solver.add(*(rival_blocker(values, own, owner, order) for owner in menu))
        if solver.check() != z3.unsat:
            raise AssertionError((order, "anchored core"))
        deletion_statuses = []
        for removed in range(len(menu)):
            reduced, reduced_values, reduced_own = structural_solver()
            reduced.add(
                *(rival_blocker(reduced_values, reduced_own, owner, order)
                  for index, owner in enumerate(menu) if index != removed)
            )
            status = str(reduced.check())
            deletion_statuses.append(status)
            if status != "sat":
                raise AssertionError((order, "anchored deletion", removed, status))
        anchored_unsat.append(
            {
                "agent_order": list(order),
                "core_size": len(menu),
                "single_deletion_statuses": deletion_statuses,
            }
        )

    anchored_sat = []
    for order, values in ANCHORED_COUNTERMODELS.items():
        pin_structural(values)
        candidates = rooted_owners(order[0])
        efx = [owner for owner in candidates if numeric_efx(values, owner)]
        dominating = [owner for owner in efx if lex_dominates(values, owner, order)]
        if dominating:
            raise AssertionError((order, "anchored escape", dominating[0]))
        unrestricted = [
            owner for owner in ALL_OWNERS
            if numeric_efx(values, owner) and lex_dominates(values, owner, order)
        ]
        if not unrestricted:
            raise AssertionError((order, "missing unrestricted escape"))
        anchored_sat.append(
            {
                "agent_order": list(order),
                "candidate_count": len(candidates),
                "anchored_efx_count": len(efx),
                "anchored_dominating_count": 0,
                "unrestricted_dominating_count": len(unrestricted),
                "values": [list(row) for row in values],
            }
        )

    promoted_sat = []
    for root, values in PROMOTED_COUNTERMODELS.items():
        pin_structural(values)
        candidates = tuple(promoted_owners(root))
        efx = [owner for owner in candidates if numeric_efx(values, owner)]
        if efx:
            raise AssertionError((root, "promoted escape", efx[0]))
        promoted_sat.append(
            {
                "root": root,
                "root_name": AGENTS[root],
                "candidate_count": len(candidates),
                "promoted_efx_count": 0,
                "values": [list(row) for row in values],
            }
        )

    script = Path(__file__).resolve()
    search_script = script.with_name("run_alternating_rooted_global_lex_cegar.py")
    return {
        "schema": SCHEMA,
        "status": "ATOMIC_ANCHORED_OR_PROMOTED_DICHOTOMY_UNSAT",
        "claim_boundary": {
            "proved_exactly": "in every hard seven-good alternating order, an anchored or promoted EFX lexicographic escape exists",
            "refuted_exactly": "anchored-only in six hard orders and promoted-only for either singleton root",
            "not_proved": "the dichotomy for arbitrary packet sizes, alternating closure, or complete four-agent EFX",
        },
        "agents": list(AGENTS),
        "goods": list(GOODS),
        "dichotomy_orders": dichotomy_records,
        "anchored_unsat_orders": anchored_unsat,
        "anchored_countermodels": anchored_sat,
        "promoted_countermodels": promoted_sat,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "provenance": {
            "audit_script": str(script.relative_to(script.parents[2])),
            "audit_script_sha256": sha256(script),
            "rooted_search_script": str(search_script.relative_to(search_script.parents[2])),
            "rooted_search_script_sha256": sha256(search_script),
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
