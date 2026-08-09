#!/usr/bin/env python3
"""Replay the two-rival split-packet core behind the root-flip lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import AGENTS
    from .run_alternating_split_packet_cegar import (
        GOODS,
        concrete_rival_blocker,
        structural_solver,
    )
except ImportError:
    from run_alternating_global_lex_cegar import AGENTS
    from run_alternating_split_packet_cegar import (
        GOODS,
        concrete_rival_blocker,
        structural_solver,
    )


SCHEMA = "alternating-root-flip-split-core-audit-v1"
ORDER = (0, 3, 1, 2)
RIVALS = (
    (2, 2, None, None, 3, 3, 3, 3, 0, 1, 2),
    (0, 0, None, None, 2, 2, 2, 2, 3, 1, 0),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def named_owner(owner):
    return [None if assigned is None else AGENTS[assigned] for assigned in owner]


def audit() -> dict:
    solver, values, own = structural_solver()
    solver.add(*(concrete_rival_blocker(values, own, rival, ORDER) for rival in RIVALS))
    full_status = str(solver.check())
    if full_status != "unsat":
        raise AssertionError(("full core", full_status))

    deletion_statuses = []
    for removed in range(len(RIVALS)):
        reduced, reduced_values, reduced_own = structural_solver()
        reduced.add(
            *(concrete_rival_blocker(reduced_values, reduced_own, rival, ORDER)
              for index, rival in enumerate(RIVALS) if index != removed)
        )
        status = str(reduced.check())
        deletion_statuses.append(status)
        if status != "sat":
            raise AssertionError(("deletion", removed, status))

    script = Path(__file__).resolve()
    search_script = script.with_name("run_alternating_anchored_or_promoted_split_cegar.py")
    return {
        "schema": SCHEMA,
        "status": "TWO_RIVAL_ROOT_FLIP_CORE_UNSAT",
        "claim_boundary": {
            "proved_exactly": "the two root-flip rivals suffice in the exact eleven-good alternating split-packet cell for order (p,q,r,s)",
            "analytic_lift": "the accompanying root-flip lemma proves the same conclusion for arbitrary packet sizes",
            "not_proved": "the other six hard priority orders, alternating closure, or complete four-agent EFX",
        },
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "goods": list(GOODS),
        "core_status": full_status,
        "core_size": len(RIVALS),
        "single_deletion_statuses": deletion_statuses,
        "rivals": [
            {"owner_by_good": list(rival), "owner_by_good_names": named_owner(rival)}
            for rival in RIVALS
        ],
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
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
