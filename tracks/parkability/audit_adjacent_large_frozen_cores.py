#!/usr/bin/env python3
"""Replay frozen adjacent-large atomic and one-split UNSAT cores exactly."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_adjacent_large_global_lex_atomic_cegar import (
        rival_blocker as atomic_blocker,
        structural_solver as atomic_solver,
    )
    from .run_adjacent_large_variable_packet_global_lex_cegar import (
        make_cell,
        rival_blocker as split_blocker,
        structural_solver as split_solver,
    )
except ImportError:
    from run_adjacent_large_global_lex_atomic_cegar import (
        rival_blocker as atomic_blocker,
        structural_solver as atomic_solver,
    )
    from run_adjacent_large_variable_packet_global_lex_cegar import (
        make_cell,
        rival_blocker as split_blocker,
        structural_solver as split_solver,
    )


SCHEMA = "adjacent-large-frozen-cores-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_tuple(raw):
    return tuple(None if assigned is None else int(assigned) for assigned in raw)


def check_core(make_solver, blocker, order, owners):
    solver, values, own = make_solver()
    constraints = [blocker(values, own, owner, order) for owner in owners]
    solver.add(*constraints)
    full = str(solver.check())
    deletions = []
    for removed in range(len(constraints)):
        trial, trial_values, trial_own = make_solver()
        trial.add(
            *(
                blocker(trial_values, trial_own, owner, order)
                for index, owner in enumerate(owners)
                if index != removed
            )
        )
        deletions.append(str(trial.check()))
    if full != "unsat" or any(status != "sat" for status in deletions):
        raise AssertionError((order, full, deletions))
    return {"full_status": full, "single_deletion_statuses": deletions}


def audit(results: Path):
    atomic_path = results / "adjacent_large_global_lex_atomic_cores.json"
    atomic = json.loads(atomic_path.read_text())
    atomic_records = []
    for record in atomic["orders"]:
        order = tuple(record["agent_order"])
        owners = tuple(owner_tuple(raw) for raw in record["rival_allocations"])
        atomic_records.append(
            {
                "agent_order": list(order),
                "core_size": len(owners),
                **check_core(atomic_solver, atomic_blocker, order, owners),
            }
        )

    split_records = []
    split_paths = sorted(results.glob("adjacent_large_split_*_2103_core.json"))
    for path in split_paths:
        payload = json.loads(path.read_text())
        cell = make_cell(tuple(payload["packet_sizes"]))
        order = tuple(payload["agent_order"])
        owners = tuple(owner_tuple(record["owner_by_good"]) for record in payload["core"])

        def make_split_solver(cell=cell):
            return split_solver(cell)

        split_records.append(
            {
                "path": str(path.relative_to(results.parent)),
                "sha256": sha256(path),
                "packet_sizes": payload["packet_sizes"],
                "core_size": len(owners),
                **check_core(make_split_solver, split_blocker, order, owners),
            }
        )
    if len(split_records) != 4:
        raise AssertionError(("expected four split cores", len(split_records)))
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "ALL_ADJACENT_FROZEN_CORES_REPLAY_EXACTLY",
        "atomic": {
            "path": str(atomic_path.relative_to(results.parent)),
            "sha256": sha256(atomic_path),
            "records": atomic_records,
        },
        "splits": split_records,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA"},
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.results)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
